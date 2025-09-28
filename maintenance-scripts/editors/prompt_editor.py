#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QListWidget, QTextEdit, QLineEdit, QPushButton,
    QLabel, QStatusBar, QMessageBox, QListWidgetItem, QTabWidget,
    QToolBar, QFontComboBox, QSpinBox, QComboBox, QCheckBox,
    QScrollArea, QFrame, QGridLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QAction, QTextCharFormat, QColor, QTextCursor
import markdown


ROOT = Path(__file__).resolve().parents[2]  # Go up to repo root from maintenance-scripts/editors/
PROMPTS_DIR = ROOT / "system-prompts" / "json"


class MarkdownEditor(QWidget):
    textChanged = Signal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Simple toolbar for common markdown formatting
        toolbar_layout = QHBoxLayout()
        
        bold_btn = QPushButton("**Bold**")
        bold_btn.clicked.connect(lambda: self.insert_markdown("**", "**"))
        toolbar_layout.addWidget(bold_btn)
        
        italic_btn = QPushButton("*Italic*")
        italic_btn.clicked.connect(lambda: self.insert_markdown("*", "*"))
        toolbar_layout.addWidget(italic_btn)
        
        code_btn = QPushButton("`Code`")
        code_btn.clicked.connect(lambda: self.insert_markdown("`", "`"))
        toolbar_layout.addWidget(code_btn)
        
        link_btn = QPushButton("Link")
        link_btn.clicked.connect(lambda: self.insert_markdown("[", "](url)"))
        toolbar_layout.addWidget(link_btn)
        
        header_btn = QPushButton("# Header")
        header_btn.clicked.connect(lambda: self.insert_markdown("## ", ""))
        toolbar_layout.addWidget(header_btn)
        
        list_btn = QPushButton("• List")
        list_btn.clicked.connect(lambda: self.insert_markdown("- ", ""))
        toolbar_layout.addWidget(list_btn)
        
        toolbar_layout.addStretch()
        layout.addLayout(toolbar_layout)
        
        # Rich text editor that can display markdown-like formatting
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        # Set minimum height for about 20 lines of text (roughly 400px)
        self.editor.setMinimumHeight(400)
        self.editor.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.editor)
    
    def insert_markdown(self, prefix, suffix):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            cursor.insertText(f"{prefix}{selected_text}{suffix}")
        else:
            cursor.insertText(f"{prefix}{suffix}")
            # Move cursor between the markers if there's a suffix
            if suffix:
                cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, len(suffix))
                self.editor.setTextCursor(cursor)
    
    def _on_text_changed(self):
        self.textChanged.emit()
    
    def setPlainText(self, text):
        self.editor.setPlainText(text)
    
    def toPlainText(self):
        return self.editor.toPlainText()
    
    def blockSignals(self, block):
        self.editor.blockSignals(block)


class PromptEditor(QMainWindow):
    def __init__(self, prompts_dir: Path):
        super().__init__()
        self.setWindowTitle("System Prompt Editor")
        self.resize(1100, 700)
        self.setMinimumSize(900, 600)

        self.prompts_dir = prompts_dir
        self.files = []  # list[Path]
        self.current_path: Optional[Path] = None
        self.current_data: Optional[dict] = None
        self.dirty = False

        self._build_ui()
        self._load_file_list()

    # UI setup
    def _build_ui(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Top frame with filter and actions
        top_layout = QHBoxLayout()
        
        filter_label = QLabel("Filter:")
        top_layout.addWidget(filter_label)
        
        self.filter_entry = QLineEdit()
        self.filter_entry.setMaximumWidth(400)
        self.filter_entry.textChanged.connect(self._refresh_file_list)
        top_layout.addWidget(self.filter_entry)
        
        self.reload_btn = QPushButton("Reload")
        self.reload_btn.clicked.connect(self._load_file_list)
        top_layout.addWidget(self.reload_btn)
        
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        
        # Main splitter layout
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel: file list
        self.file_list = QListWidget()
        self.file_list.currentItemChanged.connect(self.on_select)
        splitter.addWidget(self.file_list)
        
        # Right panel: editors with scroll area
        right_widget = QScrollArea()
        right_content = QWidget()
        right_layout = QVBoxLayout(right_content)
        
        # Agent Name / Title
        title_label = QLabel("Agent Name")
        title_label.setFont(QFont("", 10, QFont.Bold))
        right_layout.addWidget(title_label)
        
        self.title_text = QLineEdit()
        self.title_text.textChanged.connect(self._on_text_modified)
        right_layout.addWidget(self.title_text)
        
        # Description
        desc_label = QLabel("Description")
        desc_label.setFont(QFont("", 10, QFont.Bold))
        right_layout.addWidget(desc_label)
        
        self.desc_text = QTextEdit()
        self.desc_text.setMaximumHeight(120)
        self.desc_text.textChanged.connect(self._on_text_modified)
        right_layout.addWidget(self.desc_text)
        
        # System prompt (moved to be right after description)
        sp_label = QLabel("System Prompt")
        sp_label.setFont(QFont("", 10, QFont.Bold))
        right_layout.addWidget(sp_label)
        
        self.sp_text = MarkdownEditor()
        self.sp_text.textChanged.connect(self._on_text_modified)
        right_layout.addWidget(self.sp_text)
        
        # ChatGPT Link
        chatgpt_label = QLabel("ChatGPT Link")
        chatgpt_label.setFont(QFont("", 10, QFont.Bold))
        right_layout.addWidget(chatgpt_label)
        
        self.chatgpt_text = QLineEdit()
        self.chatgpt_text.textChanged.connect(self._on_text_modified)
        right_layout.addWidget(self.chatgpt_text)
        
        # Boolean flags section
        flags_label = QLabel("Capabilities")
        flags_label.setFont(QFont("", 10, QFont.Bold))
        right_layout.addWidget(flags_label)
        
        flags_frame = QFrame()
        flags_layout = QGridLayout(flags_frame)
        
        self.is_agent_cb = QCheckBox("Is Agent")
        self.is_agent_cb.stateChanged.connect(self._on_text_modified)
        flags_layout.addWidget(self.is_agent_cb, 0, 0)
        
        self.is_single_turn_cb = QCheckBox("Single Turn")
        self.is_single_turn_cb.stateChanged.connect(self._on_text_modified)
        flags_layout.addWidget(self.is_single_turn_cb, 0, 1)
        
        self.structured_output_cb = QCheckBox("Structured Output")
        self.structured_output_cb.stateChanged.connect(self._on_text_modified)
        flags_layout.addWidget(self.structured_output_cb, 1, 0)
        
        self.image_generation_cb = QCheckBox("Image Generation")
        self.image_generation_cb.stateChanged.connect(self._on_text_modified)
        flags_layout.addWidget(self.image_generation_cb, 1, 1)
        
        self.data_utility_cb = QCheckBox("Data Utility")
        self.data_utility_cb.stateChanged.connect(self._on_text_modified)
        flags_layout.addWidget(self.data_utility_cb, 2, 0)
        
        self.personalised_cb = QCheckBox("Personalised")
        self.personalised_cb.stateChanged.connect(self._on_text_modified)
        flags_layout.addWidget(self.personalised_cb, 2, 1)
        
        right_layout.addWidget(flags_frame)
        
        # JSON Schema
        schema_label = QLabel("JSON Schema")
        schema_label.setFont(QFont("", 10, QFont.Bold))
        right_layout.addWidget(schema_label)
        
        self.schema_text = QTextEdit()
        self.schema_text.setMaximumHeight(100)
        self.schema_text.setFont(QFont("Consolas", 9))
        self.schema_text.textChanged.connect(self._on_text_modified)
        right_layout.addWidget(self.schema_text)
        
        # JSON Example
        example_label = QLabel("JSON Example")
        example_label.setFont(QFont("", 10, QFont.Bold))
        right_layout.addWidget(example_label)
        
        self.example_text = QTextEdit()
        self.example_text.setMaximumHeight(100)
        self.example_text.setFont(QFont("Consolas", 9))
        self.example_text.textChanged.connect(self._on_text_modified)
        right_layout.addWidget(self.example_text)
        
        # Set up scroll area
        right_widget.setWidget(right_content)
        right_widget.setWidgetResizable(True)
        
        splitter.addWidget(right_widget)
        
        # Set splitter proportions
        splitter.setSizes([300, 800])
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.revert_btn = QPushButton("Revert")
        self.revert_btn.clicked.connect(self.revert)
        button_layout.addWidget(self.revert_btn)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save)
        button_layout.addWidget(self.save_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Editing folder: {self.prompts_dir}")

    # Data loading
    def _load_file_list(self):
        try:
            self.files = sorted([p for p in self.prompts_dir.glob("*.json") if p.is_file()], key=lambda p: p.name.lower())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to list files in {self.prompts_dir}:\n{e}")
            self.files = []
        self._refresh_file_list()

    def _refresh_file_list(self):
        sel = self.get_selected_filename()
        self.file_list.clear()
        needle = self.filter_entry.text().strip().lower()
        for p in self.files:
            if needle and needle not in p.name.lower():
                continue
            item = QListWidgetItem(p.name)
            self.file_list.addItem(item)
        # restore selection if possible
        if sel:
            for i in range(self.file_list.count()):
                if self.file_list.item(i).text() == sel:
                    self.file_list.setCurrentRow(i)
                    break

    def get_selected_filename(self):
        try:
            current_item = self.file_list.currentItem()
            if not current_item:
                return None
            return current_item.text()
        except Exception:
            return None

    def on_select(self, current, previous):
        if not current:
            return
        name = current.text()
        path = self.prompts_dir / name
        if self.current_path == path:
            return
        if not self._maybe_discard_changes():
            # revert selection change
            self._restore_selection()
            return
        self.load_file(path)

    def _restore_selection(self):
        # ensure listbox shows current selection
        if not self.current_path:
            self.file_list.setCurrentRow(-1)
            return
        target = self.current_path.name
        for i in range(self.file_list.count()):
            if self.file_list.item(i).text() == target:
                self.file_list.setCurrentRow(i)
                break

    def load_file(self, path: Path):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load JSON:\n{path}\n\n{e}")
            return

        self.current_path = path
        self.current_data = data
        
        # Load all fields (using new standardized field names)
        self._set_text(self.title_text, data.get("agent_name", ""))
        self._set_text(self.desc_text, data.get("Description", ""))
        self._set_text(self.chatgpt_text, data.get("ChatGPT Access URL", ""))
        self._set_text(self.sp_text, data.get("System Prompt", ""))
        self._set_text(self.schema_text, data.get("JSON Schema (Full)", ""))
        self._set_text(self.example_text, data.get("JSON Schema (Example Value)", ""))
        
        # Load boolean flags (using new standardized field names)
        self._set_checkbox(self.is_agent_cb, data.get("Is Agent", False))
        self._set_checkbox(self.is_single_turn_cb, data.get("Single Turn (Workflow Type)", False))
        self._set_checkbox(self.structured_output_cb, data.get("Structured Output (Workflow Type)", False))
        self._set_checkbox(self.image_generation_cb, data.get("Image Generation (Workflow Type)", False))
        self._set_checkbox(self.data_utility_cb, data.get("Data Utility (Category)", False))
        self._set_checkbox(self.personalised_cb, data.get("Personalised", False))
        
        self.dirty = False
        self._update_title()
        self.status_bar.showMessage(f"Loaded: {path.relative_to(ROOT)}")
        self._restore_selection()

    def _set_text(self, widget, value: str):
        # Temporarily disconnect signal to avoid triggering dirty flag
        widget.blockSignals(True)
        if hasattr(widget, 'setPlainText'):
            widget.setPlainText(value or "")
        elif hasattr(widget, 'setText'):
            widget.setText(value or "")
        widget.blockSignals(False)
    
    def _set_checkbox(self, checkbox: QCheckBox, value):
        # Handle different boolean representations
        checkbox.blockSignals(True)
        if isinstance(value, bool):
            checkbox.setChecked(value)
        elif isinstance(value, str):
            checkbox.setChecked(value.lower() in ('true', '1', 'yes'))
        else:
            checkbox.setChecked(bool(value))
        checkbox.blockSignals(False)

    def _on_text_modified(self):
        self.dirty = True
        self._update_title()

    # Actions
    def save(self):
        if not self.current_path or self.current_data is None:
            QMessageBox.information(self, "No file", "Select a JSON file to save.")
            return
        
        # Get all field values (using new standardized field names)
        data = dict(self.current_data)
        data["agent_name"] = self.title_text.text()
        data["Description"] = self.desc_text.toPlainText()
        data["ChatGPT Access URL"] = self.chatgpt_text.text() or None
        data["System Prompt"] = self.sp_text.toPlainText()
        data["JSON Schema (Full)"] = self.schema_text.toPlainText() or None
        data["JSON Schema (Example Value)"] = self.example_text.toPlainText() or None
        
        # Save boolean flags as actual booleans (matching new standardized format)
        data["Is Agent"] = self.is_agent_cb.isChecked()
        data["Single Turn (Workflow Type)"] = self.is_single_turn_cb.isChecked()
        data["Structured Output (Workflow Type)"] = self.structured_output_cb.isChecked()
        data["Image Generation (Workflow Type)"] = self.image_generation_cb.isChecked()
        data["Data Utility (Category)"] = self.data_utility_cb.isChecked()
        data["Personalised"] = self.personalised_cb.isChecked()
        try:
            # Write atomically
            tmp = self.current_path.with_suffix(self.current_path.suffix + ".tmp")
            with tmp.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            os.replace(tmp, self.current_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{self.current_path}\n\n{e}")
            return
        self.current_data = data
        self.dirty = False
        self._update_title()
        self.status_bar.showMessage(f"Saved: {self.current_path.relative_to(ROOT)}")

    def revert(self):
        if not self.current_path:
            return
        self.load_file(self.current_path)

    def _update_title(self):
        mark = "*" if self.dirty else ""
        name = self.current_path.name if self.current_path else "(no file)"
        self.setWindowTitle(f"System Prompt Editor - {mark}{name}")

    def _maybe_discard_changes(self) -> bool:
        if not self.dirty:
            return True
        res = QMessageBox.question(
            self,
            "Unsaved changes",
            "You have unsaved changes. Save them before switching?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes
        )
        if res == QMessageBox.Cancel:
            return False  # cancel
        if res == QMessageBox.Yes:
            self.save()
            return not self.dirty
        return True  # discard

    def closeEvent(self, event):
        if not self._maybe_discard_changes():
            event.ignore()
            return
        event.accept()


def main():
    if not PROMPTS_DIR.exists():
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Missing folder", f"Folder not found: {PROMPTS_DIR}")
        return 1
    
    app = QApplication(sys.argv)
    editor = PromptEditor(PROMPTS_DIR)
    
    # Auto-select first file for convenience
    if editor.file_list.count() > 0:
        editor.file_list.setCurrentRow(0)
    
    editor.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
