#include <TMCStepper.h>

const int STEP1_PIN = 2, DIR1_PIN = 3;
const int STEP2_PIN = 4, DIR2_PIN = 5;
const int STEP3_PIN = 6, DIR3_PIN = 7;
const int EN_PIN = 8;

const uint8_t DRIVER1_ADDRESS = 0b00;
const uint8_t DRIVER2_ADDRESS = 0b01;
const uint8_t DRIVER3_ADDRESS = 0b10;

const float R_SENSE = 0.11f;
const int MICROSTEPS = 128;
const int STEPS_PER_REV = 200;
const int TOTAL_STEPS_PER_REV = STEPS_PER_REV * MICROSTEPS;

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

MotorState motor1 = {0, 0, false, 0, 1000, STEP1_PIN, DIR1_PIN};
MotorState motor2 = {0, 0, false, 0, 1000, STEP2_PIN, DIR2_PIN};
MotorState motor3 = {0, 0, false, 0, 1000, STEP3_PIN, DIR3_PIN};

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  
  pinMode(STEP1_PIN, OUTPUT); pinMode(DIR1_PIN, OUTPUT);
  pinMode(STEP2_PIN, OUTPUT); pinMode(DIR2_PIN, OUTPUT);
  pinMode(STEP3_PIN, OUTPUT); pinMode(DIR3_PIN, OUTPUT);
  pinMode(EN_PIN, OUTPUT);
  
  digitalWrite(EN_PIN, LOW);
  
  initializeDriver(driver1);
  initializeDriver(driver2);
  initializeDriver(driver3);
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

void loop() {
  updateMotors();
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