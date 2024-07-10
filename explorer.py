#pip install PyQt5 un
#pip install PyQt5-stubs un

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileSystemModel, 
                             QTreeView, QVBoxLayout, QWidget, QPushButton, 
                             QDialog, QColorDialog, QLabel, QSlider)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle("Settings")

        self.layout = QVBoxLayout()
        
        self.default_btn = QPushButton("Default Dark Mode")
        self.default_btn.clicked.connect(self.set_default_mode)
        
        self.color_btn = QPushButton("Change Background Color")
        self.color_btn.clicked.connect(self.set_color_mode)
        
        self.matte_btn = QPushButton("Matte Background")
        self.matte_btn.clicked.connect(self.set_matte_mode)
        
        self.transparent_btn = QPushButton("Transparent Background")
        self.transparent_btn.clicked.connect(self.set_transparent_mode)
        
        self.light_btn = QPushButton("Light Mode")
        self.light_btn.clicked.connect(self.set_light_mode)

        self.layout.addWidget(self.default_btn)
        self.layout.addWidget(self.color_btn)
        self.layout.addWidget(self.matte_btn)
        self.layout.addWidget(self.transparent_btn)
        self.layout.addWidget(self.light_btn)
        
        self.setLayout(self.layout)

    def set_default_mode(self):
        self.parent().set_dark_mode()
        self.close()

    def set_color_mode(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.parent().set_background_color(color)
        self.close()

    def set_matte_mode(self):
        color = QColor(33, 33, 33)
        self.parent().set_background_color(color)
        self.close()

    def set_transparent_mode(self):
        self.parent().show_transparency_slider()
        self.close()
        
    def set_light_mode(self):
        self.parent().set_light_mode()
        self.close()

class FileExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom File Explorer")

        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")

        self.model = QFileSystemModel()
        self.model.setRootPath('')
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(''))
        self.tree.setSortingEnabled(True)
        self.tree.setStyleSheet("""
            QTreeView {
                background-color: #2E2E2E;
                color: #FFFFFF;
                alternate-background-color: #353535;
                selection-background-color: #444444;
            }
            QHeaderView::section {
                background-color: #2E2E2E;
                color: #FFFFFF;
                padding: 4px;
                border: 1px solid #444444;
            }
        """)

        self.settings_action = QPushButton("Settings", self)
        self.settings_action.clicked.connect(self.open_settings)
        self.settings_action.setStyleSheet("padding: 10px;")

        layout = QVBoxLayout()
        layout.addWidget(self.settings_action)
        layout.addWidget(self.tree)

        self.transparency_slider_label = QLabel("Transparency")
        self.transparency_slider_label.setStyleSheet("color: #FFFFFF;")
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(0, 100)
        self.transparency_slider.setValue(100)
        self.transparency_slider.valueChanged.connect(self.change_transparency)
        self.transparency_slider.setVisible(False)
        self.transparency_slider_label.setVisible(False)

        layout.addWidget(self.transparency_slider_label)
        layout.addWidget(self.transparency_slider)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.set_dark_mode()

    def open_settings(self):
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.exec_()

    def set_dark_mode(self):
        dark_palette = QPalette()

        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(42, 42, 42))
        dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

        self.setPalette(dark_palette)

    def set_background_color(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Window, color)
        palette.setColor(QPalette.Base, color)
        self.setPalette(palette)

        self.tree.setStyleSheet(f"""
            QTreeView {{
                background-color: {color.name()};
                color: #FFFFFF;
                alternate-background-color: {color.darker().name()};
                selection-background-color: {color.darker().name()};
            }}
            QHeaderView::section {{
                background-color: {color.name()};
                color: #FFFFFF;
                padding: 4px;
                border: 1px solid #444444;
            }}
        """)

    def show_transparency_slider(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.transparency_slider.setVisible(True)
        self.transparency_slider_label.setVisible(True)

    def change_transparency(self, value):
        self.setWindowOpacity(value / 100.0)

    def set_light_mode(self):
        light_palette = QPalette()

        light_palette.setColor(QPalette.Window, QColor(255, 255, 255))
        light_palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Base, QColor(242, 242, 242))
        light_palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Text, QColor(0, 0, 0))
        light_palette.setColor(QPalette.Button, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        light_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        light_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        light_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

        self.setPalette(light_palette)

        self.tree.setStyleSheet(f"""
            QTreeView {{
                background-color: #FFFFFF;
                color: #000000;
                alternate-background-color: #F0F0F0;
                selection-background-color: #D0D0D0;
            }}
            QHeaderView::section {{
                background-color: #FFFFFF;
                color: #000000;
                padding: 4px;
                border: 1px solid #D0D0D0;
            }}
        """)
        self.transparency_slider_label.setStyleSheet("color: #000000;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = FileExplorer()
    window.show()
    sys.exit(app.exec_())
