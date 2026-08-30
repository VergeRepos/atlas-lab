"""
Generate SVG placeholder images for Atlas Lab documentation.
No dependencies required (uses standard library).
"""

import os

IMAGES = [
    ("banner.svg", 1200, 630, "Atlas Lab", "AI-Powered Research & Learning Workstation"),
    ("dashboard-overview.svg", 1280, 800, "Dashboard Overview", "Research Projects • Quick Actions • System Stats"),
    ("dashboard-full.svg", 1280, 800, "Dashboard", "Full view with all widgets"),
    ("research-workspace.svg", 1280, 800, "Research Workspace", "Experiments • Hypotheses • Notes"),
    ("documents-view.svg", 1280, 800, "Documents", "PDF • TXT • MD • CSV • DOCX"),
    ("rag-assistant.svg", 1280, 800, "RAG Assistant", "AI Answers with Source Attribution"),
    ("knowledge-graph.svg", 1280, 800, "Knowledge Graph", "Interactive Force-Directed Graph"),
    ("data-analysis.svg", 1280, 800, "Data Analysis", "Statistics • Correlations • Distributions"),
    ("learning-mode.svg", 1280, 800, "Learning Mode", "Structured Paths • Mastery Tracking"),
    ("paper-workspace.svg", 1280, 800, "Paper Workspace", "Technical Writing • Citations"),
    ("command-palette.svg", 800, 600, "Command Palette", "Ctrl+K Quick Navigation"),
    ("system-monitor.svg", 1280, 800, "System Monitor", "CPU • RAM • GPU • Diagnostics"),
    ("settings-view.svg", 1280, 800, "Settings", "AI Providers • Themes • Preferences"),
    ("experiments-tracking.svg", 1280, 800, "Experiments", "Lifecycle • Metrics • Reproducibility"),
    ("datasets-management.svg", 1280, 800, "Datasets", "Import • Preview • Analyze"),
    ("timeline-view.svg", 1280, 800, "Timeline", "Chronological Research Evolution"),
    ("benchmarks-view.svg", 1280, 800, "Benchmarks", "Performance Metrics & Timing"),
]


def create_svg(width, height, title, subtitle="", bg_color="#1c1917", accent_color="#10b981"):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" fill="{bg_color}"/>
  <rect width="{width}" height="8" fill="{accent_color}"/>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="none" stroke="#44403c" stroke-width="2"/>

  <text x="{width/2}" y="{height/2 - 20}" font-family="system-ui, -apple-system, sans-serif" font-size="32" font-weight="bold" fill="#ffffff" text-anchor="middle">{title}</text>

  {f'<text x="{width/2}" y="{height/2 + 25}" font-family="system-ui, -apple-system, sans-serif" font-size="16" fill="#a8a29e" text-anchor="middle">{subtitle}</text>' if subtitle else ''}

  <rect x="{width/2 - 60}" y="{height/2 + 50}" width="120" height="24" rx="4" fill="{accent_color}" opacity="0.2"/>
  <text x="{width/2}" y="{height/2 + 66}" font-family="monospace" font-size="11" font-weight="bold" fill="{accent_color}" text-anchor="middle">PLACEHOLDER</text>

  <text x="{width - 20}" y="{height - 20}" font-family="monospace" font-size="12" fill="#78716c" text-anchor="end">{width}x{height}</text>
</svg>"""


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "..", "docs", "images")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Generating SVG placeholder images in {output_dir}...")

    for filename, width, height, title, subtitle in IMAGES:
        svg_content = create_svg(width, height, title, subtitle)
        path = os.path.join(output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"  [OK] Created {filename}")

    print(f"\n[Done] Generated {len(IMAGES)} SVG placeholder images!")


if __name__ == "__main__":
    main()
