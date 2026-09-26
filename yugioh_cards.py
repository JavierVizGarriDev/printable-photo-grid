"""Generate a print-ready PDF with Yu-Gi-Oh cards in a fixed 3x3 grid.

Reads images from ``input/``, arranges them in a 3x3 grid at the exact
Yu-Gi-Oh card size (5.9 x 8.6 cm at 300 DPI) on Letter sheets, and writes
a single multi-page PDF to ``output/``.
"""

from pathlib import Path
from PIL import Image

# --- CONFIGURATION (300 DPI) ---
CARD_W = 703   # 5.9 cm. Card width
CARD_H = 1020  # 8.6 cm. Card height
SHEET_W = 2550  # 8.5 in (Letter)
SHEET_H = 3300  # 11 in (Letter)
MARGIN_X = 130  # Side margin
MARGIN_Y = 120  # Top margin

COLUMNS = 3
ROWS = 3
CARDS_PER_PAGE = COLUMNS * ROWS

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_PDF = OUTPUT_DIR / "Complete_Card_Print.pdf"

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")


def find_images(input_dir: Path) -> list[Path]:
    """Return image paths in ``input_dir`` matching supported extensions."""
    return [
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def load_card(image_path: Path) -> Image.Image | None:
    """Open an image and resize it to the exact card size.

    Returns ``None`` if the file cannot be opened or processed, so the
    caller can skip it without aborting the whole run.
    """
    try:
        with Image.open(image_path) as img:
            return img.resize((CARD_W, CARD_H), Image.LANCZOS)
    except Exception as exc:
        print(f"Warning: could not process '{image_path.name}': {exc}")
        return None


def build_page(image_paths: list[Path]) -> Image.Image:
    """Compose one Letter sheet with up to 9 card images in a 3x3 grid."""
    sheet = Image.new("RGB", (SHEET_W, SHEET_H), "white")

    for index, path in enumerate(image_paths):
        card = load_card(path)
        if card is None:
            continue

        column = index % COLUMNS
        row = index // COLUMNS
        x = MARGIN_X + column * CARD_W
        y = MARGIN_Y + row * CARD_H
        sheet.paste(card, (x, y))

    return sheet


def build_pdf(image_paths: list[Path], output_path: Path) -> int:
    """Build a multi-page PDF from ``image_paths`` and save it.

    Returns the number of pages written (0 if there was nothing to write).
    """
    pages: list[Image.Image] = []
    for start in range(0, len(image_paths), CARDS_PER_PAGE):
        print(f"Processing page {len(pages) + 1}...")
        chunk = image_paths[start:start + CARDS_PER_PAGE]
        pages.append(build_page(chunk))

    if not pages:
        return 0

    first_page, *remaining_pages = pages
    first_page.save(
        output_path,
        "PDF",
        resolution=300.0,
        save_all=True,
        append_images=remaining_pages,
    )
    return len(pages)


def main() -> None:
    """Interactive entry point: prepare folders, gather images, build PDF."""
    if not INPUT_DIR.exists():
        INPUT_DIR.mkdir(parents=True)
        print(f"Created '{INPUT_DIR}/'. Put your photos there and run again.")
        input()
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image_paths = find_images(INPUT_DIR)
    if not image_paths:
        print(f"No images found in '{INPUT_DIR}/'.")
        input()
        return

    page_count = build_pdf(image_paths, OUTPUT_PDF)
    print(
        f"\nSuccess! Created a single PDF with {page_count} page(s) "
        f"in '{OUTPUT_DIR}/'."
    )
    input()


if __name__ == "__main__":
    main()