import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

BREAKPOINTS = [360, 768, 1024, 1280, 1920, 2560]

def take_screenshot(url, width, height, output, full, theme):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=2.0,
            color_scheme=theme
        )
        page.goto(url, wait_until="networkidle")
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=output, full_page=full)
        browser.close()
        print(f"✅ Screenshot saved: {output}")

def capture_all_breakpoints(url, height, basename, full, theme):
    for width in BREAKPOINTS:
        filename = f"{basename}_{width}px.png"
        take_screenshot(url, width, height, filename, full, theme)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="📸 Capture high-res screenshots of a website.")
    
    parser.add_argument("url", help="URL of the site (e.g., http://localhost:3000)")
    parser.add_argument("-w", "--width", type=int, default=1920, help="Viewport width (default: 1920)")
    parser.add_argument("-t", "--height", type=int, default=1080, help="Viewport height (default: 1080)")
    parser.add_argument("-o", "--output", type=str, default="output/screenshot.png", help="Output file name")
    parser.add_argument("-f", "--full", action="store_true", help="Capture full scrollable page")
    parser.add_argument("-m", "--multi", action="store_true", help="Capture screenshots at multiple breakpoints")
    parser.add_argument("-b", "--basename", type=str, default="output/screenshot", help="Base name for multi-output files")
    parser.add_argument("-T", "--theme", choices=["light", "dark", "no-preference"], default="dark", help="Preferred color scheme (default: dark)")

    args = parser.parse_args()

    if args.multi:
        capture_all_breakpoints(args.url, args.height, args.basename, args.full, args.theme)
    else:
        take_screenshot(args.url, args.width, args.height, args.output, args.full, args.theme)
