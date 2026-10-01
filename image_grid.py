"""Generate a print-ready PDF with images arranged in a configurable grid.

Prompts the user for the number of columns and rows per page and whether
to preserve each image's aspect ratio. Reads images from ``input/`` and
writes a single multi-page PDF to ``output/``.
"""

from pathlib import Path
from PIL import Image, ImageOps

# --- BASE CONFIGURATION (300 DPI) ---
SHEET_W = 2550  # 8.5 in (Letter, width)
SHEET_H = 3300  # 11 in (Letter, height)
MARGIN = 100    # ~2 cm at 300 DPI

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
OUTPUT_PDF = OUTPUT_DIR / "Image_Grid_Print.pdf"

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp")


def ask_positive_int(prompt: str) -> int:
    """Ask the user for a positive integer, retrying on invalid input."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Please enter a number greater than 0.")
        except ValueError:
            print("That doesn't look like a number. Please enter an integer.")


def ask_yes_no(prompt: str) -> bool:
    """Ask the user a yes/no question, retrying on invalid input."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "n", "yes", "no"):
            return answer.startswith("y")
        print("Please answer 'y' for Yes, or 'n' for No.")


def find_images(input_dir: Path) -> list[Path]:
    """Return image paths in ``input_dir`` matching supported extensions."""
    return [
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    ]


def load_image(image_path: Path) -> Image.Image | None:
    """Open an image as RGB, returning ``None`` if it cannot be read.

    Any unreadable file is skipped by the caller instead of aborting the
    whole run.
    """
    try:
        with Image.open(image_path) as img:
            return img.convert("RGB")
    except Exception as exc:
        print(f"Warning: could not open '{image_path.name}': {exc}")
        return None


def build_page(
    image_paths: list[Path],
    columns: int,
    rows: int,
    cell_w: int,
    cell_h: int,
    keep_aspect: bool,
) -> Image.Image:
    """Compose one Letter sheet with the given images in a grid."""
    sheet = Image.new("RGB", (SHEET_W, SHEET_H), "white")

    for index, path in enumerate(image_paths):
        img = load_image(path)
        if img is None:
            continue

        column = index % columns
        row = index // columns
        x = MARGIN + column * cell_w
        y = MARGIN + row * cell_h

        if keep_aspect:
            # Fit inside the cell without distortion, then center it.
            fitted = ImageOps.contain(img, (cell_w, cell_h), Image.LANCZOS)
            center_x = x + (cell_w - fitted.width) // 2
            center_y = y + (cell_h - fitted.height) // 2
            sheet.paste(fitted, (center_x, center_y))
        else:
            # Stretch to fill the cell exactly.
            stretched = img.resize((cell_w, cell_h), Image.LANCZOS)
            sheet.paste(stretched, (x, y))

    return sheet


def build_pdf(
    image_paths: list[Path],
    columns: int,
    rows: int,
    keep_aspect: bool,
    output_path: Path,
) -> tuple[int, int, int]:
    """Build a multi-page PDF from the images.

    Returns ``(page_count, cell_w, cell_h)`` so callers can report the
    grid dimensions that were used.
    """
    available_w = SHEET_W - MARGIN * 2
    available_h = SHEET_H - MARGIN * 2
    cell_w = available_w // columns
    cell_h = available_h // rows

    images_per_page = columns * rows
    chunks = [
        image_paths[i:i + images_per_page]
        for i in range(0, len(image_paths), images_per_page)
    ]

    pages: list[Image.Image] = []
    for index, chunk in enumerate(chunks):
        print(f"Processing page {index + 1} of {len(chunks)}...")
        pages.append(build_page(chunk, columns, rows, cell_w, cell_h, keep_aspect))

    if not pages:
        return 0, cell_w, cell_h

    first_page, *remaining = pages
    first_page.save(
        output_path,
        "PDF",
        resolution=300.0,
        save_all=True,
        append_images=remaining,
    )
    return len(pages), cell_w, cell_h


def main() -> None:
    """Interactive entry point: prepare folders, prompt the user, build PDF."""
    print("=== IMAGE GRID CREATOR ===")

    if not INPUT_DIR.exists():
        INPUT_DIR.mkdir(parents=True)
        print(f"Created '{INPUT_DIR}/'. Put your photos there and run again.")
        input("Press Enter to exit...")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image_paths = find_images(INPUT_DIR)
    if not image_paths:
        print(f"No images found in '{INPUT_DIR}/'.")
        input("Press Enter to exit...")
        return

    columns = ask_positive_int("How many columns of images per page? (e.g. 3): ")
    rows = ask_positive_int("How many rows of images per page? (e.g. 4): ")
    keep_aspect = ask_yes_no("Keep the original aspect ratio (no stretching)? (y/n): ")

    page_count, cell_w, cell_h = build_pdf(
        image_paths, columns, rows, keep_aspect, OUTPUT_PDF
    )
    print(f"\nSuccess! Created a PDF with {page_count} page(s) in '{OUTPUT_DIR}/'.")
    print(f"Maximum space per image: {cell_w}x{cell_h} pixels.")
    input("Press Enter to finish...")


if __name__ == "__main__":
    main()