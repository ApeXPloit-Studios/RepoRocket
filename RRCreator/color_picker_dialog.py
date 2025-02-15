from PyQt6.QtWidgets import QDialog, QVBoxLayout, QColorDialog, QLineEdit, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QColor

class ColorPickerDialog(QDialog):
    def __init__(self, initial_color="#ffffff", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Color")
        self.selected_color = QColor(initial_color)
        layout = QVBoxLayout(self)
        
        # Color wheel widget
        self.color_dialog = QColorDialog(self.selected_color, self)
        self.color_dialog.setOptions(QColorDialog.ColorDialogOption.DontUseNativeDialog)
        layout.addWidget(self.color_dialog)
        
        # Hex code input
        hex_layout = QHBoxLayout()
        hex_layout.addWidget(QLabel("Hex Code:"))
        self.hex_input = QLineEdit(self.selected_color.name())
        hex_layout.addWidget(self.hex_input)
        layout.addLayout(hex_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Connect signals
        self.color_dialog.currentColorChanged.connect(self._color_changed)
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        self.hex_input.textChanged.connect(self._hex_changed)
    
    def _color_changed(self, color):
        # Update hex input when color wheel changes
        self.hex_input.setText(color.name())
        self.selected_color = color
    
    def _hex_changed(self, text):
        # Update color wheel when hex input changes
        color = QColor(text)
        if color.isValid():
            self.color_dialog.setCurrentColor(color)
            self.selected_color = color

    def getColor(self):
        return self.selected_color.name()
