import sys
import os
import json
import zipfile
import shutil
import importlib.util
import traceback
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QStackedWidget, QPushButton, QLabel, QLineEdit, QComboBox,
    QFileDialog, QFormLayout
)
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from color_picker_dialog import ColorPickerDialog

class RepoRocket(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RepoRocket Creator")
        self.resize(800, 600)
        self.app_directory = os.path.dirname(os.path.abspath(__file__))
        self.projects_path = os.path.join(self.app_directory, "projects")
        os.makedirs(self.projects_path, exist_ok=True)
        self.main_content = QStackedWidget()
        self.setCentralWidget(self.main_content)
        self.create_main_page()
        self.load_projects()
        self.load_plugins()

    def create_main_page(self):
        # Main projects page with list and "New Project" button.
        self.projects_page = QWidget()
        layout = QVBoxLayout()
        header = QLabel("Projects")
        layout.addWidget(header)
        self.projects_grid = QGridLayout()
        layout.addLayout(self.projects_grid)
        new_project_button = QPushButton("New Project")
        new_project_button.clicked.connect(self.show_create_project_dialog)
        layout.addWidget(new_project_button)
        self.projects_page.setLayout(layout)
        self.main_content.addWidget(self.projects_page)
        self.main_content.setCurrentWidget(self.projects_page)

    def load_projects(self):
        # Clears button grid and adds one button per project.
        for i in reversed(range(self.projects_grid.count())):
            widget = self.projects_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        row, col = 0, 0
        for proj in os.listdir(self.projects_path):
            proj_path = os.path.join(self.projects_path, proj)
            if os.path.isdir(proj_path):
                btn = QPushButton(proj)
                btn.clicked.connect(lambda _, p=proj: self.open_project(p))
                self.projects_grid.addWidget(btn, row, col)
                col += 1
                if col >= 3:
                    row += 1
                    col = 0

    def show_create_project_dialog(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Create New Project")
        form = QFormLayout(dlg)
        name_input = QLineEdit()
        desc_input = QLineEdit()
        image_input = QLineEdit()
        browse_btn = QPushButton("Browse...")
        type_selector = QComboBox()
        type_selector.addItems(["Theme", "Plugin"])
        form.addRow("Project Name:", name_input)
        form.addRow("Description:", desc_input)
        h_layout = QHBoxLayout()
        h_layout.addWidget(image_input)
        h_layout.addWidget(browse_btn)
        form.addRow("Tile Image (optional):", h_layout)
        form.addRow("Type:", type_selector)
        create_btn = QPushButton("Create")
        form.addRow(create_btn)
        browse_btn.clicked.connect(lambda: image_input.setText(
            QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg)")[0]
        ))
        create_btn.clicked.connect(lambda: self.create_project(
            name_input.text(), desc_input.text(), image_input.text(), type_selector.currentText(), dlg
        ))
        dlg.exec()

    def create_project(self, name, desc, image, proj_type, dialog):
        if not name:
            return
        proj_folder = os.path.join(self.projects_path, name)
        os.makedirs(proj_folder, exist_ok=True)
        metadata = {
            "name": name,
            "description": desc,
            "image": image,
            "type": proj_type
        }
        with open(os.path.join(proj_folder, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=4)
        dialog.accept()
        self.load_projects()
        if proj_type == "Theme":
            self.open_theme_editor(proj_folder)
        else:
            self.open_plugin_editor(proj_folder)

    def open_project(self, proj_name):
        proj_folder = os.path.join(self.projects_path, proj_name)
        with open(os.path.join(proj_folder, "metadata.json"), "r") as f:
            metadata = json.load(f)
        if metadata.get("type") == "Theme":
            self.open_theme_editor(proj_folder)
        else:
            self.open_plugin_editor(proj_folder)

    def open_theme_editor(self, proj_folder):
        # Create a theme editor with a button and a display for each UI element.
        self.theme_editor = QWidget()
        form = QFormLayout(self.theme_editor)
        form.addRow(QLabel("Theme Editor - Set colors for UI elements"))
        # Dictionary to store chosen colors
        self.theme_fields = {}
        elements = ["panel-background", "main-background", "button-color", "button-hover-color", "text-color"]
        for element in elements:
            # Create a horizontal layout with display and button.
            h_layout = QHBoxLayout()
            color_display = QLineEdit()
            color_display.setReadOnly(True)
            color_display.setPlaceholderText("No color selected")
            select_btn = QPushButton("Select Color")
            # On click, open our custom color picker dialog.
            select_btn.clicked.connect(lambda _, d=color_display: self.select_color(d))
            h_layout.addWidget(color_display)
            h_layout.addWidget(select_btn)
            form.addRow(f"{element}:", h_layout)
            self.theme_fields[element] = color_display
        save_btn = QPushButton("Save Theme")
        form.addRow(save_btn)
        save_btn.clicked.connect(lambda: self.save_theme(proj_folder))
        self.main_content.addWidget(self.theme_editor)
        self.main_content.setCurrentWidget(self.theme_editor)

    def select_color(self, display_field):
        # Open the custom color picker dialog.
        dialog = ColorPickerDialog(initial_color=display_field.text() or "#ffffff", parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            chosen_hex = dialog.getColor()
            display_field.setText(chosen_hex)

    def save_theme(self, proj_folder):
        # Save chosen colors into project's metadata
        theme_settings = { key: field.text() for key, field in self.theme_fields.items() }
        with open(os.path.join(proj_folder, "metadata.json"), "r+") as f:
            data = json.load(f)
            data["theme"] = theme_settings
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        print("Theme settings saved.")

    def open_plugin_editor(self, proj_folder):
        # Create a plugin editor with buttons to open directory, create base file, or export.
        self.plugin_editor = QWidget()
        layout = QVBoxLayout(self.plugin_editor)
        open_dir_button = QPushButton("Open Project Directory")
        base_file_button = QPushButton("Create base.py")
        export_button = QPushButton("Export Plugin")
        layout.addWidget(open_dir_button)
        layout.addWidget(base_file_button)
        layout.addWidget(export_button)
        open_dir_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(proj_folder)))
        base_file_button.clicked.connect(lambda: self.create_base_file(proj_folder))
        export_button.clicked.connect(lambda: self.export_plugin(proj_folder))
        self.main_content.addWidget(self.plugin_editor)
        self.main_content.setCurrentWidget(self.plugin_editor)

    def create_base_file(self, proj_folder):
        base_path = os.path.join(proj_folder, "base.py")
        if not os.path.exists(base_path):
            with open(base_path, "w") as f:
                f.write("# Base plugin file\n")
        print("Base plugin file created.")

    def export_plugin(self, proj_folder):
        save_dir = QFileDialog.getExistingDirectory(self, "Select Export Folder")
        if save_dir:
            proj_name = os.path.basename(proj_folder)
            zip_path = os.path.join(save_dir, f"{proj_name}.rrpp")
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for root, dirs, files in os.walk(proj_folder):
                    for file in files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, proj_folder)
                        zipf.write(full_path, rel_path)
            print("Plugin exported.")

    def load_plugins(self):
        plugins_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")
        os.makedirs(plugins_path, exist_ok=True)
        for folder in os.listdir(plugins_path):
            plugin_folder = os.path.join(plugins_path, folder)
            if os.path.isdir(plugin_folder):
                base_file = os.path.join(plugin_folder, "base.py")
                if os.path.exists(base_file):
                    try:
                        spec = importlib.util.spec_from_file_location(f"{folder}.base", base_file)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        if hasattr(module, "init_plugin"):
                            module.init_plugin(self)
                    except Exception as e:
                        print(f"Failed loading plugin {folder}: {e}\n{traceback.format_exc()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RepoRocket()
    window.show()
    sys.exit(app.exec())
