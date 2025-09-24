#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / "system-prompts" / "json"


class PromptEditor(tk.Tk):
    def __init__(self, prompts_dir: Path):
        super().__init__()
        self.title("System Prompt Editor")
        self.geometry("1100x700")
        self.minsize(900, 600)

        self.prompts_dir = prompts_dir
        self.files = []  # list[Path]
        self.current_path: Optional[Path] = None
        self.current_data: Optional[dict] = None
        self.dirty = False

        self._build_ui()
        self._load_file_list()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # UI setup
    def _build_ui(self):
        # Top frame with filter and actions
        top = ttk.Frame(self)
        top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        ttk.Label(top, text="Filter:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *_: self._refresh_file_list())
        self.filter_entry = ttk.Entry(top, textvariable=self.filter_var, width=40)
        self.filter_entry.pack(side=tk.LEFT, padx=(6, 12))

        self.reload_btn = ttk.Button(top, text="Reload", command=self._load_file_list)
        self.reload_btn.pack(side=tk.LEFT)

        # Main Paned layout
        paned = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Left panel: file list
        left = ttk.Frame(paned)
        paned.add(left, weight=1)

        self.file_list = tk.Listbox(left, activestyle="dotbox")
        self.file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_list.bind("<<ListboxSelect>>", self.on_select)

        left_scroll = ttk.Scrollbar(left, orient=tk.VERTICAL, command=self.file_list.yview)
        left_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_list.config(yscrollcommand=left_scroll.set)

        # Right panel: editors
        right = ttk.Frame(paned)
        paned.add(right, weight=3)

        # Description
        desc_label = ttk.Label(right, text="description")
        desc_label.pack(anchor="w", padx=6, pady=(6, 0))
        self.desc_text = tk.Text(right, height=5, wrap=tk.WORD, undo=True)
        self.desc_text.pack(fill=tk.X, padx=6)
        self.desc_text.bind("<<Modified>>", self._on_text_modified)

        # System prompt
        sp_label = ttk.Label(right, text="systemprompt")
        sp_label.pack(anchor="w", padx=6, pady=(10, 0))

        sp_frame = ttk.Frame(right)
        sp_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))
        self.sp_text = tk.Text(sp_frame, wrap=tk.WORD, undo=True)
        self.sp_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sp_text.bind("<<Modified>>", self._on_text_modified)
        sp_scroll = ttk.Scrollbar(sp_frame, orient=tk.VERTICAL, command=self.sp_text.yview)
        sp_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.sp_text.config(yscrollcommand=sp_scroll.set)

        # Action buttons and status
        bottom = ttk.Frame(self)
        bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=8, pady=6)

        self.save_btn = ttk.Button(bottom, text="Save", command=self.save)
        self.save_btn.pack(side=tk.RIGHT)

        self.revert_btn = ttk.Button(bottom, text="Revert", command=self.revert)
        self.revert_btn.pack(side=tk.RIGHT, padx=(0, 8))

        self.status_var = tk.StringVar(value=f"Editing folder: {self.prompts_dir}")
        self.status = ttk.Label(bottom, textvariable=self.status_var, anchor="w")
        self.status.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Data loading
    def _load_file_list(self):
        try:
            self.files = sorted([p for p in self.prompts_dir.glob("*.json") if p.is_file()], key=lambda p: p.name.lower())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list files in {self.prompts_dir}:\n{e}")
            self.files = []
        self._refresh_file_list()

    def _refresh_file_list(self):
        sel = self.get_selected_filename()
        self.file_list.delete(0, tk.END)
        needle = self.filter_var.get().strip().lower()
        for p in self.files:
            if needle and needle not in p.name.lower():
                continue
            self.file_list.insert(tk.END, p.name)
        # restore selection if possible
        if sel:
            for i in range(self.file_list.size()):
                if self.file_list.get(i) == sel:
                    self.file_list.selection_set(i)
                    self.file_list.see(i)
                    break

    def get_selected_filename(self):
        try:
            idxs = self.file_list.curselection()
            if not idxs:
                return None
            return self.file_list.get(idxs[0])
        except Exception:
            return None

    def on_select(self, _event=None):
        name = self.get_selected_filename()
        if not name:
            return
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
            self.file_list.selection_clear(0, tk.END)
            return
        target = self.current_path.name
        for i in range(self.file_list.size()):
            if self.file_list.get(i) == target:
                self.file_list.selection_clear(0, tk.END)
                self.file_list.selection_set(i)
                self.file_list.see(i)
                break

    def load_file(self, path: Path):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON:\n{path}\n\n{e}")
            return

        self.current_path = path
        self.current_data = data
        self._set_text(self.desc_text, data.get("description", ""))
        self._set_text(self.sp_text, data.get("systemprompt", ""))
        self.dirty = False
        self._update_title()
        self.status_var.set(f"Loaded: {path.relative_to(ROOT)}")
        self._restore_selection()

    def _set_text(self, widget: tk.Text, value: str):
        widget.edit_reset()
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
        widget.edit_modified(False)

    def _on_text_modified(self, event):
        widget: tk.Text = event.widget  # type: ignore
        if widget.edit_modified():
            widget.edit_modified(False)
            self.dirty = True
            self._update_title()

    # Actions
    def save(self):
        if not self.current_path or self.current_data is None:
            messagebox.showinfo("No file", "Select a JSON file to save.")
            return
        desc = self.desc_text.get("1.0", tk.END).rstrip("\n")
        sp = self.sp_text.get("1.0", tk.END).rstrip("\n")
        data = dict(self.current_data)
        data["description"] = desc
        data["systemprompt"] = sp
        try:
            # Write atomically
            tmp = self.current_path.with_suffix(self.current_path.suffix + ".tmp")
            with tmp.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            os.replace(tmp, self.current_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{self.current_path}\n\n{e}")
            return
        self.current_data = data
        self.dirty = False
        self._update_title()
        self.status_var.set(f"Saved: {self.current_path.relative_to(ROOT)}")

    def revert(self):
        if not self.current_path:
            return
        self.load_file(self.current_path)

    def _update_title(self):
        mark = "*" if self.dirty else ""
        name = self.current_path.name if self.current_path else "(no file)"
        self.title(f"System Prompt Editor - {mark}{name}")

    def _maybe_discard_changes(self) -> bool:
        if not self.dirty:
            return True
        res = messagebox.askyesnocancel(
            "Unsaved changes",
            "You have unsaved changes. Save them before switching?",
            default=messagebox.YES,
        )
        if res is None:
            return False  # cancel
        if res:
            self.save()
            return not self.dirty
        return True  # discard

    def on_close(self):
        if not self._maybe_discard_changes():
            return
        self.destroy()


def main():
    if not PROMPTS_DIR.exists():
        messagebox.showerror("Missing folder", f"Folder not found: {PROMPTS_DIR}")
        return 1
    app = PromptEditor(PROMPTS_DIR)
    # Auto-select first file for convenience
    if app.file_list.size() > 0:
        app.file_list.selection_set(0)
        app.on_select()
    app.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
