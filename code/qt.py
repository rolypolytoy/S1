import sys
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QFrame, QGridLayout, QSpacerItem, QSizePolicy, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPainter, QPen, QBrush, QPixmap


class LogSlider(QWidget):
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


class HumeInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_styles()
    
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
        
        status_indicator = QLabel("●")
        status_indicator.setStyleSheet("color: #00ff88; font-size: 24px;")
        status_label = QLabel("ONLINE")
        status_label.setStyleSheet("color: #00ff88; font-size: 14px; font-weight: 600; letter-spacing: 1px;")
        
        status_layout = QVBoxLayout()
        status_layout.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(status_indicator)
        status_layout.addWidget(status_label)
        
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
        
        beam_controls_title = QLabel("ELECTRON BEAM ALIGNMENT")
        beam_controls_title.setStyleSheet("color: #888888; font-size: 12px; font-weight: 600; letter-spacing: 2px;")
        controls_layout.addWidget(beam_controls_title)
        
        beam_sliders_layout = QGridLayout()
        beam_sliders_layout.setHorizontalSpacing(40)
        beam_sliders_layout.setVerticalSpacing(30)
        
        self.stigmator_x = LogSlider("Stigmator X", 0.00, 100.00, is_linear=True)
        self.stigmator_y = LogSlider("Stigmator Y", 0.00, 100.00, is_linear=True)
        self.beam_align_x = LogSlider("Beam Alignment X", 0.00, 100.00, is_linear=True)
        self.beam_align_y = LogSlider("Beam Alignment Y", 0.00, 100.00, is_linear=True)
        
        beam_sliders_layout.addWidget(self.stigmator_x, 0, 0)
        beam_sliders_layout.addWidget(self.stigmator_y, 0, 1)
        beam_sliders_layout.addWidget(self.beam_align_x, 1, 0)
        beam_sliders_layout.addWidget(self.beam_align_y, 1, 1)
        
        controls_layout.addLayout(beam_sliders_layout)
        
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
        interface = HumeInterface()
        self.setCentralWidget(interface)


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