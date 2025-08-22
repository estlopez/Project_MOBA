import requests
from bs4 import BeautifulSoup


def extract_and_print_grid(published_url: str):
    # 1. Fetch the HTML from the provided URL
    response = requests.get(published_url)
    if response.status_code != 200:
        print(f"Failed to fetch document. Status code: {response.status_code}")
        return

    html = response.text

    # 2. Parse the HTML and extract text content
    soup = BeautifulSoup(html, "html.parser")
    text_content = soup.get_text("\n")

    # 3. Extract entries of the form: x, char, y
    entries = []
    for line in text_content.splitlines():
        parts = line.strip().split()
        if len(parts) == 3:
            try:
                x = int(parts[0])
                ch = parts[1]
                y = int(parts[2])
                entries.append((x, y, ch))
            except ValueError:
                continue

    if not entries:
        print("No grid data found in document.")
        return

    # 4. Determine grid dimensions
    max_x = max(entry[0] for entry in entries)
    max_y = max(entry[1] for entry in entries)

    width = max_x + 1
    height = max_y + 1

    # 5. Initialize empty grid
    grid = [[" " for _ in range(width)] for _ in range(height)]

    # 6. Populate grid with characters
    for x, y, ch in entries:
        grid[y][x] = ch

    # 7. Print grid row by row
    for row in grid:
        print("".join(row))


# Example usage with your Google Doc URL
url = "https://docs.google.com/document/u/0/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub?pli=1"
extract_and_print_grid(url)
