"""
📁 File Organizer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
No external dependencies — pure Python (os, shutil) + Tkinter
Run:  python file_organizer.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ── Palette (matches other DAA apps) ────────────────────────────
BG      = "#0f0f1a"
SIDEBAR = "#12121f"
CARD    = "#1a1a2e"
CARD2   = "#16213e"
BORDER  = "#2a3045"
TEXT    = "#f1f5f9"
SUBTEXT = "#64748b"
ACCENT  = "#a855f7"   # purple accent
BLUE    = "#3b82f6"
GREEN   = "#22c55e"
AMBER   = "#f59e0b"
RED     = "#ef4444"
WHITE   = "#ffffff"

FONT      = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE= ("Segoe UI", 16, "bold")
FONT_SMALL= ("Segoe UI", 8)

# ── Category definitions ────────────────────────────────────────
CATEGORIES = {
    "Images": {
        "exts": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
                 ".svg", ".ico", ".tiff", ".tif", ".heic", ".raw"},
        "color": GREEN,
        "icon": "🖼",
    },
    "PDFs": {
        "exts": {".pdf"},
        "color": RED,
        "icon": "📄",
    },
    "Videos": {
        "exts": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv",
                 ".webm", ".m4v", ".mpg", ".mpeg", ".3gp"},
        "color": BLUE,
        "icon": "🎬",
    },
    "Documents": {
        "exts": {".txt", ".doc", ".docx", ".xls", ".xlsx", ".ppt",
                 ".pptx", ".odt", ".ods", ".odp", ".rtf", ".csv",
                 ".md", ".pdf"},
        "color": AMBER,
        "icon": "📑",
    },
}
DOC_EXTS = {".pdf"}  # special: route .pdf into "PDFs" not "Documents"


def classify(filename):
    """Return the category name for a file, or None if not recognized."""
    ext = os.path.splitext(filename)[1].lower()
    if not ext:
        return None
    if ext in CATEGORIES["PDFs"]["exts"]:
        return "PDFs"
    for name, info in CATEGORIES.items():
        if name != "PDFs" and ext in info["exts"]:
            return name
    return None


# ─────────────────────────────────────────────────────────────────
class FileOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("📁 File Organizer")
        self.root.geometry("820x640")
        self.root.configure(bg=BG)
        self.root.minsize(680, 540)

        self.folder = tk.StringVar(value="")
        self.log    = []
        self._build_ui()

    # ── UI construction ──────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=SIDEBAR, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Frame(hdr, bg=ACCENT, width=5).pack(side="left", fill="y")
        tk.Label(hdr, text="  📁  FILE ORGANIZER",
                 bg=SIDEBAR, fg=TEXT, font=FONT_TITLE).pack(side="left", padx=(10, 0))
        tk.Label(hdr, text="os + shutil",
                 bg=SIDEBAR, fg=SUBTEXT, font=FONT_SMALL).pack(side="left", padx=12)

        # Folder selection
        sel = tk.Frame(self.root, bg=CARD, pady=16)
        sel.pack(fill="x", padx=16, pady=(16, 0))
        tk.Label(sel, text="Choose a folder to organize:",
                 bg=CARD, fg=SUBTEXT, font=FONT_BOLD).pack(anchor="w", padx=16, pady=(0, 8))

        row = tk.Frame(sel, bg=CARD)
        row.pack(fill="x", padx=16)
        self.folder_entry = tk.Entry(row, textvariable=self.folder, bg=CARD2, fg=TEXT,
                                     insertbackground=TEXT, relief="flat",
                                     font=FONT, state="readonly")
        self.folder_entry.pack(side="left", fill="x", expand=True, ipady=6)
        tk.Button(row, text="📂 Browse…", command=self._browse,
                  bg=ACCENT, fg=WHITE, relief="flat", font=FONT_BOLD,
                  activebackground=BLUE, cursor="hand2", padx=16, pady=6).pack(side="left", padx=(8, 0))

        # Category cards
        cards = tk.Frame(self.root, bg=BG)
        cards.pack(fill="x", padx=16, pady=14)
        self.count_labels = {}
        for i, (name, info) in enumerate(CATEGORIES.items()):
            card = tk.Frame(cards, bg=CARD, highlightbackground=BORDER,
                            highlightthickness=1)
            card.pack(side="left", expand=True, fill="x", padx=4)
            tk.Label(card, text=info["icon"], bg=CARD, fg=info["color"],
                     font=("Segoe UI", 22)).pack(pady=(14, 0))
            tk.Label(card, text=name, bg=CARD, fg=info["color"],
                     font=FONT_BOLD).pack(pady=(2, 0))
            count = tk.Label(card, text="0 files", bg=CARD, fg=TEXT,
                             font=("Segoe UI", 12, "bold"))
            count.pack(pady=(2, 2))
            self.count_labels[name] = count
            tk.Label(card, text="—", bg=CARD, fg=SUBTEXT,
                     font=FONT_SMALL).pack(pady=(0, 14))

        # Action buttons
        actions = tk.Frame(self.root, bg=BG)
        actions.pack(fill="x", padx=16)
        tk.Button(actions, text="🧹 Organize Files", command=self._organize,
                  bg=ACCENT, fg=WHITE, relief="flat", font=("Segoe UI", 12, "bold"),
                  activebackground=BLUE, cursor="hand2", pady=10).pack(fill="x")
        tk.Button(actions, text="↺  Reset Counts", command=self._reset_counts,
                  bg=CARD2, fg=TEXT, relief="flat", font=FONT_BOLD,
                  activebackground=BORDER, cursor="hand2", pady=6).pack(fill="x", pady=(8, 0))

        # Log area
        log_lbl = tk.Label(self.root, text="📋 Activity Log", bg=BG, fg=SUBTEXT,
                           font=FONT_BOLD).pack(anchor="w", padx=20, pady=(12, 4))
        log_wrap = tk.Frame(self.root, bg=CARD, highlightbackground=BORDER,
                            highlightthickness=1)
        log_wrap.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.log_text = tk.Text(log_wrap, bg=CARD2, fg=TEXT, font=("Consolas", 9),
                                wrap="word", relief="flat", padx=12, pady=10,
                                state="disabled", height=8)
        self.log_text.pack(fill="both", expand=True)

        self._log("Ready. Select a folder and click 'Organize Files'.")

    # ── Helpers ──────────────────────────────────────────────────
    def _log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _browse(self):
        path = filedialog.askdirectory(title="Select Folder to Organize")
        if path:
            self.folder.set(os.path.normpath(path))

    def _reset_counts(self):
        for name, lbl in self.count_labels.items():
            lbl.config(text="0 files")
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")
        self._log("Counts reset.")

    # ── Organize logic ───────────────────────────────────────────
    def _organize(self):
        folder = self.folder.get().strip()
        if not folder or not os.path.isdir(folder):
            return messagebox.showwarning("No Folder", "Please select a folder first.")

        self._reset_counts()
        self._log(f"Scanning: {folder}")

        # Create category folders
        for name in CATEGORIES:
            path = os.path.join(folder, name)
            if not os.path.exists(path):
                os.makedirs(path)

        moved = {name: 0 for name in CATEGORIES}
        skipped = 0

        for item in sorted(os.listdir(folder)):
            src = os.path.join(folder, item)
            if not os.path.isfile(src):
                continue  # skip existing category folders / subdirs

            cat = classify(item)
            if cat is None:
                skipped += 1
                continue

            dest_dir = os.path.join(folder, cat)
            dest = os.path.join(dest_dir, item)

            # avoid clobbering an existing file
            if os.path.exists(dest):
                base, ext = os.path.splitext(item)
                i = 1
                while os.path.exists(dest):
                    dest = os.path.join(dest_dir, f"{base}_{i}{ext}")
                    i += 1

            shutil.move(src, dest)
            moved[cat] += 1
            self._log(f"  {CATEGORIES[cat]['icon']} {item}  →  {cat}/")

        # Update counts
        for name, count in moved.items():
            self.count_labels[name].config(text=f"{count} files")

        self._log("")
        self._log(f"--- Done! Moved {sum(moved.values())} file(s), "
                  f"skipped {skipped} unrecognized file(s). ---")
        messagebox.showinfo("Complete",
                            f"Organized {sum(moved.values())} files!\n\n"
                            + "\n".join(f"{n}: {c}" for n, c in moved.items()))


# ── Entry point ──────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    FileOrganizer(root)
    root.mainloop()
