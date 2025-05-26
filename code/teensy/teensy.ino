#include <TMCStepper.h>
#include <SPI.h>

const int STEP1_PIN = 2, DIR1_PIN = 3;
const int STEP2_PIN = 4, DIR2_PIN = 5;
const int STEP3_PIN = 6, DIR3_PIN = 7;
const int EN_PIN = 8;

const int ADC_CS_PIN = 9;
const int ADC_SCLK_PIN = 10;
const int ADC_ECHO_PIN = 11;
const int ADC_SDOA_PIN = 12;
const int ADC_SDOB_PIN = 13;
const int ADC_CNV_PIN = 14;
const int ADC_BUSY_PIN = 15;

const int DAC_CS_PIN = 16;
const int DAC_LDAC_PIN = 17;
const int DAC_CLR_PIN = 18;

const uint8_t DRIVER1_ADDRESS = 0b00;
const uint8_t DRIVER2_ADDRESS = 0b01;
const uint8_t DRIVER3_ADDRESS = 0b10;

const float R_SENSE = 0.11f;
const int MICROSTEPS = 128;
const int STEPS_PER_REV = 200;
const int TOTAL_STEPS_PER_REV = STEPS_PER_REV * MICROSTEPS;

const uint8_t DAC_CMD_WRITE_INPUT_REG = 0x00;
const uint8_t DAC_CMD_UPDATE_DAC_REG = 0x01;
const uint8_t DAC_CMD_WRITE_UPDATE_ALL = 0x02;
const uint8_t DAC_CMD_WRITE_UPDATE_N = 0x03;
const uint8_t DAC_CMD_POWER_DOWN = 0x04;
const uint8_t DAC_CMD_CLEAR_CODE = 0x05;
const uint8_t DAC_CMD_LDAC_REG = 0x06;
const uint8_t DAC_CMD_RESET = 0x07;
const uint8_t DAC_CMD_INTERNAL_REF = 0x08;

TMC2209Stepper driver1(&Serial1, R_SENSE, DRIVER1_ADDRESS);
TMC2209Stepper driver2(&Serial1, R_SENSE, DRIVER2_ADDRESS);
TMC2209Stepper driver3(&Serial1, R_SENSE, DRIVER3_ADDRESS);

struct MotorState {
  long position;
  long targetPosition;
  bool moving;
  unsigned long lastStepTime;
  unsigned long stepInterval;
  int stepPin;
  int dirPin;
};

struct ADCData {
  uint16_t channelA;
  uint16_t channelB;
  bool dataReady;
  unsigned long lastConversion;
};

struct DACData {
  uint16_t channelA;
  uint16_t channelB;
  uint16_t channelC;
  uint16_t channelD;
  bool needsUpdate[4];
};

MotorState motor1 = {0, 0, false, 0, 1000, STEP1_PIN, DIR1_PIN};
MotorState motor2 = {0, 0, false, 0, 1000, STEP2_PIN, DIR2_PIN};
MotorState motor3 = {0, 0, false, 0, 1000, STEP3_PIN, DIR3_PIN};

ADCData adcData = {0, 0, false, 0};
DACData dacData = {0, 0, 0, 0, {false, false, false, false}};

volatile bool echoReceived = false;
volatile int echoBitCount = 0;
volatile uint32_t adcResultA = 0;
volatile uint32_t adcResultB = 0;

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  
  pinMode(STEP1_PIN, OUTPUT); pinMode(DIR1_PIN, OUTPUT);
  pinMode(STEP2_PIN, OUTPUT); pinMode(DIR2_PIN, OUTPUT);
  pinMode(STEP3_PIN, OUTPUT); pinMode(DIR3_PIN, OUTPUT);
  pinMode(EN_PIN, OUTPUT);
  
  pinMode(ADC_CS_PIN, OUTPUT);
  pinMode(ADC_SCLK_PIN, OUTPUT);
  pinMode(ADC_CNV_PIN, OUTPUT);
  pinMode(ADC_ECHO_PIN, INPUT);
  pinMode(ADC_SDOA_PIN, INPUT);
  pinMode(ADC_SDOB_PIN, INPUT);
  pinMode(ADC_BUSY_PIN, INPUT);
  
  pinMode(DAC_CS_PIN, OUTPUT);
  pinMode(DAC_LDAC_PIN, OUTPUT);
  pinMode(DAC_CLR_PIN, OUTPUT);
  
  digitalWrite(EN_PIN, LOW);
  digitalWrite(ADC_CS_PIN, HIGH);
  digitalWrite(ADC_SCLK_PIN, LOW);
  digitalWrite(ADC_CNV_PIN, LOW);
  
  digitalWrite(DAC_CS_PIN, HIGH);
  digitalWrite(DAC_LDAC_PIN, HIGH);
  digitalWrite(DAC_CLR_PIN, HIGH);
  
  SPI.begin();
  SPI.beginTransaction(SPISettings(20000000, MSBFIRST, SPI_MODE1));
  
  attachInterrupt(digitalPinToInterrupt(ADC_ECHO_PIN), echoISR, RISING);
  
  initializeDriver(driver1);
  initializeDriver(driver2);
  initializeDriver(driver3);
  
  initializeADC();
  initializeDAC();
}

void initializeDriver(TMC2209Stepper &driver) {
  driver.begin();
  driver.toff(5);
  driver.rms_current(800);
  driver.microsteps(MICROSTEPS);
  driver.pwm_autoscale(true);
  driver.en_spreadCycle(false);
  driver.interpolation(true);
}

void initializeADC() {
  digitalWrite(ADC_CS_PIN, LOW);
  delayMicroseconds(1);
  digitalWrite(ADC_CS_PIN, HIGH);
  delayMicroseconds(10);
}

void initializeDAC() {
  dacWriteCommand(DAC_CMD_RESET, 0, 0);
  delay(1);
  dacWriteCommand(DAC_CMD_INTERNAL_REF, 0, 0x0001);
  dacWriteCommand(DAC_CMD_POWER_DOWN, 0, 0x0000);
  dacWriteCommand(DAC_CMD_CLEAR_CODE, 0, 0x8000);
  dacWriteAll(0x8000);
}

void loop() {
  updateMotors();
  updateADC();
  updateDAC();
}

void updateMotors() {
  updateMotor(motor1);
  updateMotor(motor2);
  updateMotor(motor3);
}

void updateMotor(MotorState &motor) {
  if (!motor.moving) return;
  
  if (micros() - motor.lastStepTime >= motor.stepInterval) {
    digitalWrite(motor.stepPin, HIGH);
    delayMicroseconds(2);
    digitalWrite(motor.stepPin, LOW);
    
    if (motor.targetPosition > motor.position) {
      motor.position++;
    } else {
      motor.position--;
    }
    
    if (motor.position == motor.targetPosition) {
      motor.moving = false;
    }
    
    motor.lastStepTime = micros();
  }
}

void updateADC() {
  if (micros() - adcData.lastConversion >= 0.1) {
    startADCConversion();
    adcData.lastConversion = micros();
  }
  
  if (echoReceived && echoBitCount >= 16) {
    adcData.channelA = (adcResultA >> 2) & 0x3FFF;
    adcData.channelB = (adcResultB >> 2) & 0x3FFF;
    adcData.dataReady = true;
    echoReceived = false;
    echoBitCount = 0;
    adcResultA = 0;
    adcResultB = 0;
  }
}

void updateDAC() {
  for (int i = 0; i < 4; i++) {
    if (dacData.needsUpdate[i]) {
      uint16_t value;
      switch (i) {
        case 0: value = dacData.channelA; break;
        case 1: value = dacData.channelB; break;
        case 2: value = dacData.channelC; break;
        case 3: value = dacData.channelD; break;
      }
      dacWriteChannel(i, value);
      dacData.needsUpdate[i] = false;
    }
  }
}

void startADCConversion() {
  digitalWrite(ADC_CNV_PIN, HIGH);
  delayMicroseconds(1);
  digitalWrite(ADC_CNV_PIN, LOW);
  
  digitalWrite(ADC_CS_PIN, LOW);
  echoBitCount = 0;
  adcResultA = 0;
  adcResultB = 0;
}

void echoISR() {
  if (echoBitCount < 16) {
    adcResultA = (adcResultA << 1) | digitalReadFast(ADC_SDOA_PIN);
    adcResultB = (adcResultB << 1) | digitalReadFast(ADC_SDOB_PIN);
    echoBitCount++;
    
    if (echoBitCount >= 16) {
      digitalWrite(ADC_CS_PIN, HIGH);
      echoReceived = true;
    }
  }
}

void moveMotor(int motorNum, long steps) {
  MotorState* motor = getMotor(motorNum);
  if (!motor) return;
  
  motor->targetPosition = motor->position + steps;
  digitalWrite(motor->dirPin, steps > 0 ? HIGH : LOW);
  delayMicroseconds(10);
  motor->moving = true;
}

void moveMotorTo(int motorNum, long position) {
  MotorState* motor = getMotor(motorNum);
  if (!motor) return;
  
  long steps = position - motor->position;
  moveMotor(motorNum, steps);
}

void setMotorSpeed(int motorNum, float rpm) {
  MotorState* motor = getMotor(motorNum);
  if (!motor) return;
  
  motor->stepInterval = (60L * 1000000L) / (rpm * TOTAL_STEPS_PER_REV);
}

void stopMotor(int motorNum) {
  MotorState* motor = getMotor(motorNum);
  if (!motor) return;
  
  motor->moving = false;
  motor->targetPosition = motor->position;
}

void stopAllMotors() {
  stopMotor(1);
  stopMotor(2);
  stopMotor(3);
}

void homeMotor(int motorNum) {
  MotorState* motor = getMotor(motorNum);
  if (!motor) return;
  
  motor->position = 0;
  motor->targetPosition = 0;
  motor->moving = false;
}

void homeAllMotors() {
  homeMotor(1);
  homeMotor(2);
  homeMotor(3);
}

bool isMotorMoving(int motorNum) {
  MotorState* motor = getMotor(motorNum);
  return motor ? motor->moving : false;
}

bool anyMotorMoving() {
  return motor1.moving || motor2.moving || motor3.moving;
}

long getMotorPosition(int motorNum) {
  MotorState* motor = getMotor(motorNum);
  return motor ? motor->position : 0;
}

MotorState* getMotor(int motorNum) {
  switch(motorNum) {
    case 1: return &motor1;
    case 2: return &motor2;
    case 3: return &motor3;
    default: return nullptr;
  }
}

void setMotorCurrent(int motorNum, uint16_t current) {
  switch(motorNum) {
    case 1: driver1.rms_current(current); break;
    case 2: driver2.rms_current(current); break;
    case 3: driver3.rms_current(current); break;
  }
}

void enableMotors() {
  digitalWrite(EN_PIN, LOW);
}

void disableMotors() {
  digitalWrite(EN_PIN, HIGH);
}

uint16_t getADCChannelA() {
  if (adcData.dataReady) {
    adcData.dataReady = false;
    return adcData.channelA;
  }
  return 0;
}

uint16_t getADCChannelB() {
  if (adcData.dataReady) {
    return adcData.channelB;
  }
  return 0;
}

bool isADCDataReady() {
  return adcData.dataReady;
}

float adcToVoltage(uint16_t adcValue) {
  return (adcValue * 5.0) / 16383.0;
}

void dacWriteCommand(uint8_t cmd, uint8_t address, uint16_t data) {
  uint32_t packet = ((uint32_t)cmd << 19) | ((uint32_t)address << 16) | data;
  
  digitalWrite(DAC_CS_PIN, LOW);
  SPI.transfer((packet >> 16) & 0xFF);
  SPI.transfer((packet >> 8) & 0xFF);
  SPI.transfer(packet & 0xFF);
  digitalWrite(DAC_CS_PIN, HIGH);
}

void dacWriteChannel(uint8_t channel, uint16_t value) {
  dacWriteCommand(DAC_CMD_WRITE_UPDATE_N, channel, value);
}

void dacWriteAll(uint16_t value) {
  dacWriteCommand(DAC_CMD_WRITE_UPDATE_ALL, 0, value);
}

void setDACChannel(uint8_t channel, uint16_t value) {
  if (channel > 3) return;
  
  switch (channel) {
    case 0: dacData.channelA = value; break;
    case 1: dacData.channelB = value; break;
    case 2: dacData.channelC = value; break;
    case 3: dacData.channelD = value; break;
  }
  dacData.needsUpdate[channel] = true;
}

void setDACVoltage(uint8_t channel, float voltage) {
  if (voltage < -10.0) voltage = -10.0;
  if (voltage > 10.0) voltage = 10.0;
  
  uint16_t dacValue = (uint16_t)((voltage + 10.0) * 65535.0 / 20.0);
  setDACChannel(channel, dacValue);
}

uint16_t getDACChannel(uint8_t channel) {
  switch (channel) {
    case 0: return dacData.channelA;
    case 1: return dacData.channelB;
    case 2: return dacData.channelC;
    case 3: return dacData.channelD;
    default: return 0;
  }
}

float dacToVoltage(uint16_t dacValue) {
  return (dacValue * 20.0 / 65535.0) - 10.0;
}