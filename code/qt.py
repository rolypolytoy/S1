import sys
import math
import serial
import serial.tools.list_ports
import threading
import time
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QFrame, QGridLayout, QSpacerItem, QSizePolicy, QLineEdit
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QPainter, QPen, QBrush, QPixmap


class LogSlider(QWidget):
    valueChanged = Signal(float)
    
    def __init__(self, label_text, min_val=0, max_val=10000, is_linear=False):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.is_linear = is_linear
        if not is_linear:
            self.log_min = math.log10(max(min_val, 1))
            self.log_max = math.log10(max_val)
        self.setup_ui(label_text)
    
    def setup_ui(self, label_text):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        header_layout = QHBoxLayout()
        self.label = QLabel(label_text)
        self.label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 500;")
        
        self.value_label = QLineEdit("100" if not self.is_linear else "0.00")
        self.value_label.setStyleSheet("""
            QLineEdit {
                color: #00d4ff; 
                font-size: 14px; 
                font-weight: 600;
                background-color: transparent;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 2px 8px;
                min-width: 60px;
                max-width: 80px;
            }
            QLineEdit:focus {
                border: 1px solid #00d4ff;
            }
        """)
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.returnPressed.connect(self.manual_input)
        
        header_layout.addWidget(self.label)
        header_layout.addWidget(self.value_label)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1000)
        self.slider.setValue(0)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #333333;
                height: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1a1a, stop:1 #2d2d2d);
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00d4ff, stop:1 #0099cc);
                border: 2px solid #ffffff;
                width: 18px;
                margin: -7px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #33ddff, stop:1 #00aadd);
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #0099cc);
                border: 1px solid #333333;
                height: 6px;
                border-radius: 3px;
            }
        """)
        
        self.slider.valueChanged.connect(self.update_value)
        
        layout.addLayout(header_layout)
        layout.addWidget(self.slider)
        self.setLayout(layout)
    
    def manual_input(self):
        try:
            input_value = float(self.value_label.text())
            if self.min_val <= input_value <= self.max_val:
                if self.is_linear:
                    slider_pos = int((input_value - self.min_val) / (self.max_val - self.min_val) * 1000)
                    self.value_label.setText(f"{input_value:.2f}")
                else:
                    if input_value <= 0:
                        return
                    log_pos = (math.log10(input_value) - self.log_min) / (self.log_max - self.log_min) * 1000
                    slider_pos = max(0, min(1000, int(log_pos)))
                    if input_value >= 1000:
                        self.value_label.setText(f"{input_value/1000:.1f}k")
                    else:
                        self.value_label.setText(str(int(input_value)))
                
                self.slider.blockSignals(True)
                self.slider.setValue(slider_pos)
                self.slider.blockSignals(False)
                self.valueChanged.emit(input_value)
        except ValueError:
            pass
    
    def update_value(self, slider_value):
        if self.is_linear:
            actual_value = self.min_val + (slider_value / 1000.0) * (self.max_val - self.min_val)
            self.value_label.setText(f"{actual_value:.2f}")
        else:
            if slider_value == 0:
                actual_value = self.min_val
            else:
                log_value = self.log_min + (slider_value / 1000.0) * (self.log_max - self.log_min)
                actual_value = int(10 ** log_value)
            
            if actual_value >= 1000:
                self.value_label.setText(f"{actual_value/1000:.1f}k")
            else:
                self.value_label.setText(str(actual_value))
        
        self.valueChanged.emit(actual_value)
    
    def get_value(self):
        if self.is_linear:
            return float(self.value_label.text())
        else:
            text = self.value_label.text()
            if 'k' in text:
                return float(text.replace('k', '')) * 1000
            else:
                return float(text)


class TeensyComm:
    def __init__(self):
        self.serial_conn = None
        self.is_connected = False
        self.adc_data = {'chA': 0, 'chB': 0, 'voltA': 0.0, 'voltB': 0.0}
        self.positions = {'motor1': 0, 'motor2': 0, 'motor3': 0}
        self.read_thread = None
        self.running = False
    
    def find_teensy(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "teensy" in port.description.lower() or "usb serial" in port.description.lower():
                return port.device
        return None
    
    def connect(self):
        port = self.find_teensy()
        if port:
            try:
                self.serial_conn = serial.Serial(port, 115200, timeout=1)
                time.sleep(2)
                self.is_connected = True
                self.running = True
                self.read_thread = threading.Thread(target=self.read_data)
                self.read_thread.daemon = True
                self.read_thread.start()
                self.send_command("STREAM 1 10000")
                return True
            except:
                self.is_connected = False
                return False
        return False
    
    def disconnect(self):
        self.running = False
        self.is_connected = False
        if self.serial_conn:
            self.serial_conn.close()
    
    def send_command(self, command):
        if self.is_connected and self.serial_conn:
            try:
                self.serial_conn.write((command + '\n').encode())
                return True
            except:
                self.is_connected = False
                return False
        return False
    
    def read_data(self):
        while self.running and self.is_connected:
            try:
                if self.serial_conn and self.serial_conn.in_waiting:
                    line = self.serial_conn.readline().decode().strip()
                    if line.startswith("DATA"):
                        parts = line.split()
                        if len(parts) >= 6:
                            self.adc_data['chA'] = int(parts[2])
                            self.adc_data['chB'] = int(parts[3])
                            self.adc_data['voltA'] = float(parts[4])
                            self.adc_data['voltB'] = float(parts[5])
            except:
                self.is_connected = False
                break
    
    def move_motor(self, motor, position):
        steps = int(position * 1000)
        return self.send_command(f"MOVE {motor} {steps}")
    
    def get_position(self, motor):
        if self.send_command(f"POS {motor}"):
            return True
        return False


class HumeInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.teensy = TeensyComm()
        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.check_connection)
        self.connection_timer.start(1000)
        
        self.setup_ui()
        self.setup_styles()
        self.connect_signals()
    
    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        header_layout = QHBoxLayout()
        
        title = QLabel("Hume S1")
        title_font = QFont("Segoe UI", 48, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #ffffff; letter-spacing: 2px;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("color: #ff4444; font-size: 24px;")
        self.status_label = QLabel("OFFLINE")
        self.status_label.setStyleSheet("color: #ff4444; font-size: 14px; font-weight: 600; letter-spacing: 1px;")
        
        status_layout = QVBoxLayout()
        status_layout.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.status_indicator)
        status_layout.addWidget(self.status_label)
        
        header_layout.addLayout(status_layout)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #333333; border: none; height: 2px;")
        
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(25)
        
        controls_title = QLabel("DESKTOP SEM CONTROLS")
        controls_title.setStyleSheet("color: #888888; font-size: 12px; font-weight: 600; letter-spacing: 2px;")
        controls_layout.addWidget(controls_title)
        
        sliders_layout = QGridLayout()
        sliders_layout.setHorizontalSpacing(40)
        sliders_layout.setVerticalSpacing(30)
        
        self.magnification = LogSlider("Magnification", 100, 10000)
        self.stage_x = LogSlider("Stage X (mm)", 0.00, 50.00, is_linear=True)
        self.stage_y = LogSlider("Stage Y (mm)", 0.00, 50.00, is_linear=True)
        self.stage_z = LogSlider("Stage Z (mm)", 0.00, 50.00, is_linear=True)
        
        sliders_layout.addWidget(self.magnification, 0, 0)
        sliders_layout.addWidget(self.stage_x, 0, 1)
        sliders_layout.addWidget(self.stage_y, 1, 0)
        sliders_layout.addWidget(self.stage_z, 1, 1)
        
        controls_layout.addLayout(sliders_layout)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        footer = QLabel("HUME NANOTECH © 2025")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #555555; font-size: 11px; letter-spacing: 1px;")
        
        main_layout.addLayout(header_layout)
        main_layout.addWidget(separator)
        main_layout.addLayout(controls_layout)
        main_layout.addItem(spacer)
        main_layout.addWidget(footer)
        
        self.setLayout(main_layout)
        
        self.set_controls_enabled(False)
    
    def connect_signals(self):
        self.stage_x.valueChanged.connect(lambda val: self.move_stage(1, val))
        self.stage_y.valueChanged.connect(lambda val: self.move_stage(2, val))
        self.stage_z.valueChanged.connect(lambda val: self.move_stage(3, val))
    
    def move_stage(self, motor, position):
        if self.teensy.is_connected:
            self.teensy.move_motor(motor, position)
    
    def check_connection(self):
        if not self.teensy.is_connected:
            if self.teensy.connect():
                self.status_indicator.setStyleSheet("color: #00ff88; font-size: 24px;")
                self.status_label.setStyleSheet("color: #00ff88; font-size: 14px; font-weight: 600; letter-spacing: 1px;")
                self.status_label.setText("ONLINE")
                self.set_controls_enabled(True)
        else:
            if not self.teensy.find_teensy():
                self.teensy.disconnect()
                self.status_indicator.setStyleSheet("color: #ff4444; font-size: 24px;")
                self.status_label.setStyleSheet("color: #ff4444; font-size: 14px; font-weight: 600; letter-spacing: 1px;")
                self.status_label.setText("OFFLINE")
                self.set_controls_enabled(False)
    
    def set_controls_enabled(self, enabled):
        self.stage_x.setEnabled(enabled)
        self.stage_y.setEnabled(enabled)
        self.stage_z.setEnabled(enabled)
        self.magnification.setEnabled(enabled)
    
    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0f0f0f;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
        """)


class HumeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_interface()
    
    def setup_window(self):
        self.setWindowTitle("Hume S1")
        self.showMaximized()
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f0f0f;
            }
        """)
    
    def setup_interface(self):
        self.interface = HumeInterface()
        self.setCentralWidget(self.interface)
    
    def closeEvent(self, event):
        if hasattr(self.interface, 'teensy'):
            self.interface.teensy.disconnect()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Hume S1")
    app.setApplicationVersion("1.0")
    
    app.setStyleSheet("""
        QApplication {
            background-color: #0f0f0f;
        }
    """)
    
    window = HumeWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()