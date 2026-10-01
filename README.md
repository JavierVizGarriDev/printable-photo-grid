# Printable Photo Grid

Two Python scripts that generate print-ready PDFs from image grids. Built to automate a repetitive Photoshop workflow at a print shop.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

> 🇬🇧 English · 🇪🇸 [Versión en español](README.es.md)

---

## 📖 Overview

At the print shop where I work, customers often bring dozens of card images, screenshots, or photos to be printed on Letter-size sheets. The original process required opening each image in Photoshop, resizing it to the exact target size, arranging them manually on a grid, and printing sheet by sheet.

These two scripts automate the whole process: they read images from `input/`, compose them into a grid on Letter sheets at 300 DPI, and export a single multi-page PDF to `output/`.

The first script was built for a very specific use case (Yu-Gi-Oh cards, always 3×3). The second was added later to handle more flexible layouts when new customer needs appeared. Both are kept in the same repository because each has its own niche.

---

## 🛠️ The two tools

| Script | Use case | Configuration |
|---|---|---|
| `yugioh_cards.py` | Yu-Gi-Oh cards, always 3×3, exact card size | None — just run it |
| `image_grid.py` | Any layout: screenshots, legal evidence, framed photos | Prompts for columns, rows, and aspect ratio |

### `yugioh_cards.py` — Specialized tool

Lays out cards in a fixed 3×3 grid at the exact size of a real Yu-Gi-Oh card (5.9 × 8.6 cm at 300 DPI). Zero prompts: drop the images in `input/` and run it. Output: `output/Complete_Card_Print.pdf`.

### `image_grid.py` — Flexible tool

Asks for the number of columns and rows per page, and whether to preserve each image's aspect ratio. When preserving aspect ratio, images are fitted inside their cell and centered; otherwise they are stretched to fill it. Output: `output/Image_Grid_Print.pdf`.

---

## 🚀 How to run

### Setup

```bash
git clone https://github.com/JavierVizGarriDev/printable-photo-grid.git
cd printable-photo-grid
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### Yu-Gi-Oh cards

1. Put your card images in `input/` (the folder is created on first run if missing).
2. Run:
   ```bash
   python yugioh_cards.py
   ```
3. Get `output/Complete_Card_Print.pdf`.

### Custom grid

1. Put your images in `input/`.
2. Run:
   ```bash
   python image_grid.py
   ```
3. Answer the prompts (columns, rows, aspect ratio).
4. Get `output/Image_Grid_Print.pdf`.

---

## 📂 Project structure

```
printable-photo-grid/
├── yugioh_cards.py      # Specialized: fixed 3×3 grid for Yu-Gi-Oh cards
├── image_grid.py        # Flexible: configurable columns, rows, aspect ratio
├── requirements.txt     # Pillow
├── input/               # Source images (gitignored)
└── output/              # Generated PDFs (gitignored)
```

---

## 🧠 Design notes

Both scripts share the same core logic: read images, resize them, place them on a Letter sheet at 300 DPI, and export a multi-page PDF. They are kept separate on purpose:

- The **specialized script** is optimized for the most common case: no configuration, no decisions. Preferred when the output format stays the same.
- The **flexible script** covers the less frequent cases: custom grids, mixed aspect ratios, formats that came up over time.

Merging them into a single script with flags was considered, but the simplicity of the specialized one is part of its value.

---

## ⚙️ Requirements

- Python 3.10 or higher
- [Pillow](https://python-pillow.org/) (installed via `requirements.txt`)

No other dependencies. No GUI, no external services.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Javier A. Vizcaino Garriga**
- GitHub: [@JavierVizGarriDev](https://github.com/JavierVizGarriDev)
- Email: javieralejandrovizcainogarriga@gmail.com

---

<p align="center">
  <i>Automating the boring parts, one script at a time.</i>
</p>