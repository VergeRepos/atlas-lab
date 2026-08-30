"""
Generate placeholder images for Atlas Lab documentation.
Requires Pillow: pip install Pillow
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Images to generate
IMAGES = [
    # Main images
    ("banner.png", 1200, 630, "Atlas Lab", "AI-Powered Research & Learning Workstation"),
    ("dashboard-overview.png", 1280, 800, "Dashboard Overview", "Research Projects • Quick Actions • System Stats"),
    ("dashboard-full.png", 1280, 800, "Dashboard", "Full view with all widgets"),

    # Feature screenshots
    ("research-workspace.png", 1280, 800, "Research Workspace", "Experiments • Hypotheses • Notes"),
    ("documents-view.png", 1280, 800, "Documents", "PDF • TXT • MD • CSV • DOCX"),
    ("rag-assistant.png", 1280, 800, "RAG Assistant", "AI Answers with Source Attribution"),
    ("knowledge-graph.png", 1280, 800, "Knowledge Graph", "Interactive Force-Directed Graph"),
    ("data-analysis.png", 1280, 800, "Data Analysis", "Statistics • Correlations • Distributions"),
    ("learning-mode.png", 1280, 800, "Learning Mode", "Structured Paths • Mastery Tracking"),
    ("paper-workspace.png", 1280, 800, "Paper Workspace", "Technical Writing • Citations"),
    ("command-palette.png", 800, 600, "Command Palette", "Ctrl+K Quick Navigation"),
    ("system-monitor.png", 1280, 800, "System Monitor", "CPU • RAM • GPU • Diagnostics"),
    ("settings-view.png", 1280, 800, "Settings", "AI Providers • Themes • Preferences"),
    ("experiments-tracking.png", 1280, 800, "Experiments", "Lifecycle • Metrics • Reproducibility"),
    ("datasets-management.png", 1280, 800, "Datasets", "Import • Preview • Analyze"),
    ("timeline-view.png", 1280, 800, "Timeline", "Chronological Research Evolution"),
    ("benchmarks-view.png", 1280, 800, "Benchmarks", "Performance Metrics & Timing"),
]

# GIF placeholders (static images that represent where GIFs will go)
GIF_PLACEHOLDERS = [
    ("research-workspace.gif", 800, 600, "Research Demo", "Creating experiments"),
    ("document-import.gif", 800, 600, "Document Import Demo", "Importing & processing files"),
    ("flashcards.gif", 600, 500, "Flashcards Demo", "Reviewing with SM-2 algorithm"),
    ("ml-lab.gif", 800, 600, "ML Lab Demo", "Running ML experiments"),
    ("demo-rag.gif", 800, 600, "RAG Demo", "Asking questions with citations"),
    ("demo-graph.gif", 800, 600, "Graph Demo", "Interactive graph navigation"),
    ("demo-full.gif", 1024, 768, "Full Demo", "End-to-end walkthrough"),
    ("demo-documents.gif", 800, 600, "Documents Demo", "Batch document processing"),
    ("demo-ml.gif", 800, 600, "ML Demo", "Model training & evaluation"),
]


def create_placeholder(filename, width, height, title, subtitle="", bg_color="#1c1917", text_color="#ffffff", accent_color="#10b981"):
    """Create a single placeholder image."""
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw border
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline="#44403c", width=2)

    # Draw accent header bar
    draw.rectangle([(0, 0), (width, 8)], fill=accent_color)

    # Try to load a font, fall back to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        subtitle_font = ImageFont.truetype("arial.ttf", 18)
        small_font = ImageFont.truetype("arial.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Draw title
    draw.text((width // 2, height // 2 - 30), title, fill=text_color, font=title_font, anchor="mm")

    # Draw subtitle if provided
    if subtitle:
        draw.text((width // 2, height // 2 + 20), subtitle, fill="#a8a29e", font=subtitle_font, anchor="mm")

    # Draw dimensions in corner
    draw.text((width - 15, height - 15), f"{width}x{height}", fill="#78716c", font=small_font, anchor="rb")

    # Draw "PLACEHOLDER" badge
    badge_text = "PLACEHOLDER"
    draw.text((width // 2, height // 2 + 70), badge_text, fill=accent_color, font=small_font, anchor="mm")

    return img


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "docs", "images")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Generating placeholder images in {output_dir}...")

    # Generate screenshots
    for filename, width, height, title, subtitle in IMAGES:
        img = create_placeholder(filename, width, height, title, subtitle)
        path = os.path.join(output_dir, filename)
        img.save(path)
        print(f"  ✓ Created {filename}")

    # Generate GIF placeholders (as PNGs with .gif extension for now)
    for filename, width, height, title, subtitle in GIF_PLACEHOLDERS:
        img = create_placeholder(filename, width, height, f"🎬 {title}", subtitle, bg_color="#0c0a09", accent_color="#3b82f6")
        path = os.path.join(output_dir, filename)
        img.save(path)
        print(f"  ✓ Created {filename} (placeholder)")

    print(f"\n✨ Generated {len(IMAGES) + len(GIF_PLACEHOLDERS)} placeholder images!")
    print("Replace these with real screenshots using the guide in docs/SCREENSHOTS.md")


if __name__ == "__main__":
    main()
