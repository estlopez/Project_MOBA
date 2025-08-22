import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ---------- Parsing helpers ----------

def fetch_doc_text(url: str) -> str:
    """Fetch and return visible text from the published Google Doc."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.get_text("\n")

def parse_entries(text: str):
    """
    Parse lines of the form:
      x-coordinate
      Character    (Unicode, e.g., '█' or '░')
      y-coordinate
    Returns list of (x, y, ch).
    """
    toks = [line.strip() for line in text.splitlines() if line.strip()]
    out = []
    i = 0
    while i + 2 < len(toks):
        try:
            x = int(toks[i])
            ch = toks[i + 1]
            y = int(toks[i + 2])
            out.append((x, y, ch))
            i += 3
        except ValueError:
            # Skip any non-triple noise defensively
            i += 1
    return out

def build_grid(entries):
    """Build a 2D list (rows of strings) from (x, y, ch); fill blanks with spaces."""
    if not entries:
        return []

    max_x = max(x for x, _, _ in entries)
    max_y = max(y for _, y, _ in entries)

    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y, ch in entries:
        grid[y][x] = ch
    return grid

def grid_to_string(grid):
    """Join grid rows into a single string."""
    return "\n".join("".join(row) for row in grid)

def foreground_only(grid):
    """
    Convert a grid that may contain '█' and '░' into a display that emphasizes the letters.
    By default we treat '█' as foreground and drop '░' to space.
    """
    return "\n".join("".join(" " if c == "░" else c for c in row) for row in grid)

def split_letter_blocks(grid_str):
    """
    Heuristic: split the banner into letter blocks using fully-blank columns as separators.
    Returns a list of strings, each a multi-line ASCII block for one letter.
    """
    rows = grid_str.splitlines()
    if not rows:
        return []

    H = len(rows)
    W = max(len(r) for r in rows)
    # Pad rows to identical width
    rows = [r + " " * (W - len(r)) for r in rows]

    # Identify blank columns
    blank = []
    for x in range(W):
        col = [rows[y][x] for y in range(H)]
        blank.append(all(ch == " " for ch in col))

    # Group consecutive non-blank columns into segments
    segments = []
    start = None
    for x in range(W):
        if not blank[x] and start is None:
            start = x
        if (blank[x] or x == W - 1) and start is not None:
            end = x if not blank[x] and x == W - 1 else x - 1
            segments.append((start, end))
            start = None

    blocks = []
    for a, b in segments:
        block_lines = [rows[y][a : b + 1] for y in range(H)]
        blocks.append("\n".join(block_lines))
    return blocks

# ---------- GUI ----------

def display_doc_grid(url: str):
    """
    Main function:
      1) Takes a published Google Doc URL,
      2) Fetches & parses (x, ch, y) entries,
      3) Builds and displays the grid with Tkinter,
      4) Prints the grid and a foreground-only version to stdout,
      5) Lets you save the grid to a .txt file,
      6) Shows letter blocks split by blank columns (for easier reading).
    """
    # Fetch & parse
    text = fetch_doc_text(url)
    entries = parse_entries(text)
    grid = build_grid(entries)
    if not grid:
        raise RuntimeError("No entries found in the document.")

    full_grid_str = grid_to_string(grid)
    letters_only_str = foreground_only(grid)

    # Console outputs (so you can copy/paste if you like)
    print("=== FULL GRID (includes ░ if present) ===\n")
    print(full_grid_str)
    print("\n=== LETTERS ONLY (░ -> space) ===\n")
    print(letters_only_str)

    # Prepare letter blocks
    blocks = split_letter_blocks(letters_only_str)

    # Tkinter UI
    root = tk.Tk()
    root.title("Secret Message Grid")

    # Main panes
    paned = ttk.Panedwindow(root, orient=tk.HORIZONTAL)
    paned.pack(fill="both", expand=True)

    # Left: grid text
    left = ttk.Frame(paned); paned.add(left, weight=3)
    lbl1 = ttk.Label(left, text="Grid (fixed-width):")
    lbl1.pack(anchor="w", padx=8, pady=(8, 2))
    text_box = tk.Text(left, font=("Courier New", 12), wrap="none")
    text_box.insert("1.0", letters_only_str)
    text_box.config(state="disabled")
    text_box.pack(fill="both", expand=True, padx=8, pady=8)

    # Right: letter blocks
    right = ttk.Frame(paned); paned.add(right, weight=2)
    lbl2 = ttk.Label(right, text="Detected letter blocks:")
    lbl2.pack(anchor="w", padx=8, pady=(8, 2))
    blocks_box = tk.Text(right, font=("Courier New", 12), wrap="none")
    for i, b in enumerate(blocks, 1):
        blocks_box.insert("end", f"--- Letter {i} ---\n{b}\n\n")
    blocks_box.config(state="disabled")
    blocks_box.pack(fill="both", expand=True, padx=8, pady=8)

    # Buttons
    btns = ttk.Frame(root); btns.pack(fill="x", padx=8, pady=8)

    def save_file():
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save decoded grid"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(letters_only_str + "\n")
            messagebox.showinfo("Saved", f"Grid saved to:\n{path}")

    ttk.Button(btns, text="Save Grid as .txt", command=save_file).pack(side="left")

    root.mainloop()


# ----------- Run with your URL -----------
if __name__ == "__main__":
    url = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"
    display_doc_grid(url)
