#  File Organizer

Automatically sorts files in a selected folder into organized subfolders:

- 🖼 **Images**
- 📄 **PDFs**
- 🎬 **Videos**
- 📑 **Documents**

Built with **Python + Tkinter** using only the built-in `os` and `shutil` libraries — no external dependencies.

## ▶ Run

```powershell
python file_organizer.py
```

## ✦ How to Use

1. Click **Browse…** and select the folder you want to organize.
2. Click **Organize Files**.
3. Files are moved into `Images/`, `PDFs/`, `Videos/`, and `Documents/` subfolders automatically.
4. A live activity log shows each file moved, plus a per-category count.

## 🗂 Supported Extensions

| Category | Extensions |
|---|---|
| 🖼 Images | jpg, jpeg, png, gif, bmp, webp, svg, ico, tiff, heic, raw |
| 📄 PDFs | pdf |
| 🎬 Videos | mp4, avi, mkv, mov, wmv, flv, webm, m4v, mpg, mpeg, 3gp |
| 📑 Documents | txt, doc, docx, xls, xlsx, ppt, pptx, odt, ods, odp, rtf, csv, md |

> Duplicate filenames are automatically renamed (e.g. `file_1.png`) to avoid overwriting.
> Unrecognized file types are left untouched.

## 📁 Files
- `file_organizer.py` — single-file Tkinter app
