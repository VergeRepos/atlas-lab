# Screenshot and GIF Capture Guide

This guide explains how to capture screenshots and create GIFs for the Atlas Lab documentation.

## Required Tools

### For Screenshots
- **Windows**: Built-in Snipping Tool or Win+Shift+S
- **macOS**: Cmd+Shift+4 for selection, Cmd+Shift+5 for recording
- **Linux**: gnome-screenshot, Flameshot, or Spectacle

### For GIFs
- [LICEcap](https://www.cockos.com/licecap/) (Windows/macOS, free)
- [ScreenToGif](https://www.screentogif.com/) (Windows, free)
- [Kap](https://getkap.co/) (macOS, free)
- [Peek](https://github.com/phw/peek) (Linux, free)

## Image Requirements

- **Format**: PNG for screenshots, GIF for animations
- **Size**: Max 1920px width, optimize for web
- **Naming**: Use kebab-case (e.g., `dashboard-overview.png`)
- **Location**: Save to `docs/images/`

## Screenshots to Capture

Create the `docs/images/` directory and capture these:

### 1. Banner Image (`banner.png`)
- Full application window
- Dashboard view with sample data
- Clean, professional look
- **Dimensions**: 1200x630px (social media optimized)

### 2. Dashboard Overview (`dashboard-overview.png`)
- Main dashboard showing:
  - Research projects card
  - Recent documents
  - Quick actions
  - System stats
- **Size**: 1280x800px

### 3. Research Workspace (`research-workspace.png`)
- Research tab open
- List of experiments
- Status badges visible
- **Size**: 1280x800px

### 4. Documents View (`documents-view.png`)
- Documents tab with several imported files
- Show file types (PDF, TXT, MD, CSV)
- Processing status visible
- **Size**: 1280x800px

### 5. RAG Assistant (`rag-assistant.png`)
- Chat interface with a question
- AI response with source citations
- Relevance scores visible
- **Size**: 1280x800px

### 6. Knowledge Graph (`knowledge-graph.png`)
- Knowledge tab showing force-directed graph
- Multiple nodes and edges
- Legend visible
- **Size**: 1280x800px

### 7. Data Analysis (`data-analysis.png`)
- Datasets tab with CSV loaded
- Statistics and correlations displayed
- Preview table visible
- **Size**: 1280x800px

### 8. Learning Mode (`learning-mode.png`)
- Learning tab open
- Topic list with progress bars
- Mastery percentages
- **Size**: 1280x800px

### 9. Paper Workspace (`paper-workspace.png`)
- Papers tab showing paper sections
- Citations list
- Word count stats
- **Size**: 1280x800px

### 10. Command Palette (`command-palette.png`)
- Command palette open (Ctrl+K)
- Search results visible
- Categories shown
- **Size**: 800x600px (centered)

### 11. System Monitor (`system-monitor.png`)
- System tab with CPU/RAM charts
- Performance bars
- Diagnostics visible
- **Size**: 1280x800px

### 12. Settings (`settings-view.png`)
- Settings tab open
- AI provider options
- Theme selection
- **Size**: 1280x800px

### 13. Experiments Tracking (`experiments-tracking.png`)
- Experiments tab with list
- Metrics visible
- Status indicators
- **Size**: 1280x800px

### 14. Datasets Management (`datasets-management.png`)
- Datasets tab
- Multiple datasets listed
- Preview columns
- **Size**: 1280x800px

### 15. Timeline View (`timeline-view.png`)
- Timeline tab showing events
- Chronological order
- Event type badges
- **Size**: 1280x800px

### 16. Benchmarks View (`benchmarks-view.png`)
- Benchmarks tab
- Performance metrics
- Timing results
- **Size**: 1280x800px

## GIFs to Create

### 1. Research Workspace Demo (`research-workspace.gif`)
**Steps** (15-20 seconds):
1. Click "New Experiment" button
2. Fill in experiment name
3. Select task type (classification)
4. Save experiment
5. Show it appearing in the list

**Settings**: 15fps, 800x600px max, optimize for web

### 2. Document Import Demo (`document-import.gif`)
**Steps** (15-20 seconds):
1. Click "Import Document"
2. Select a PDF file
3. Show upload progress
4. Document appears in list
5. Processing status updates

**Settings**: 15fps, 800x600px max

### 3. RAG Assistant Demo (`demo-rag.gif`)
**Steps** (20-25 seconds):
1. Type a question: "What is machine learning?"
2. Click "Ask"
3. Show loading state
4. Response appears with sources
5. Hover over a source citation

**Settings**: 15fps, 800x600px max

### 4. ML Experiment Demo (`demo-ml.gif`)
**Steps** (20-30 seconds):
1. Go to ML Lab
2. Create new experiment
3. Select dataset
4. Choose algorithm
5. Click "Run"
6. Show metrics appearing

**Settings**: 15fps, 800x600px max

### 5. Flashcards Demo (`flashcards.gif`)
**Steps** (15-20 seconds):
1. Show flashcard front
2. Click to flip
3. Show back
4. Click quality rating (3)
5. Next card appears

**Settings**: 15fps, 600x500px max

### 6. Knowledge Graph Demo (`demo-graph.gif`)
**Steps** (15-20 seconds):
1. Show static graph
2. Zoom in slightly
3. Click a node
4. Show details
5. Zoom out

**Settings**: 15fps, 800x600px max

### 7. Full Walkthrough (`demo-full.gif`)
**Steps** (45-60 seconds):
1. Dashboard overview (5s)
2. Import document (8s)
3. Ask RAG question (10s)
4. View knowledge graph (8s)
5. Check experiments (8s)
6. Review flashcard (8s)
7. Check system stats (8s)

**Settings**: 10fps, 1024x768px max, optimize heavily

## Capture Workflow

### Before Recording
1. **Clean the UI**: Remove any personal data or test content
2. **Prepare sample data**: Use the example project
3. **Set theme**: Use dark theme for consistency
4. **Window size**: 1280x800 or 1920x1080
5. **Clear notifications**: Close any system notifications

### During Capture
1. **Move slowly**: Give viewers time to see what you're doing
2. **Pause between actions**: 1-2 second pause after each click
3. **Highlight important UI**: Briefly hover over key elements
4. **Keep mouse visible**: Show where you're clicking

### After Capture
1. **Optimize GIFs**: Use [ezgif.com](https://ezgif.com/optimize) or similar
2. **Target size**: < 5MB for GIFs, < 500KB for PNGs
3. **Crop carefully**: Remove unnecessary borders
4. **Test loading**: Verify images load quickly

## Post-Processing

### Image Optimization
```bash
# Install ImageMagick (if not installed)
# brew install imagemagick  # macOS
# apt install imagemagick   # Linux

# Optimize PNGs
mogrify -strip -resize 1280x800\> -quality 85 docs/images/*.png

# Optimize GIFs
gifsicle -O3 --colors 256 -i input.gif -o output.gif
```

### Annotation (Optional)
Use tools like:
- **Snagit** (paid): Professional annotations
- **GIMP** (free): Open source image editor
- **Figma** (free): Add arrows and callouts

## Checklist

Before committing images:

- [ ] All images saved to `docs/images/`
- [ ] Filenames match README.md references
- [ ] PNGs optimized (< 500KB each)
- [ ] GIFs optimized (< 5MB each)
- [ ] No personal/sensitive data visible
- [ ] Consistent theme (dark mode)
- [ ] High quality and clear
- [ ] README.md image links work locally

## Creating Placeholder Images

Until you capture real screenshots, create placeholders:

```bash
mkdir -p docs/images

# Create simple placeholder PNGs (requires ImageMagick)
convert -size 1280x800 xc:#1c1917 -pointsize 48 -fill white \
  -gravity center -annotate +0+0 "Dashboard Overview" \
  docs/images/dashboard-overview.png

convert -size 1280x800 xc:#1c1917 -pointsize 48 -fill white \
  -gravity center -annotate +0+0 "Research Workspace" \
  docs/images/research-workspace.png

# Repeat for all images...
```

Or use online tools:
- [Placeholder.com](https://placeholder.com/)
- [PlaceKitten](https://placekitten.com/) (fun alternative)

## Tips for Great Documentation Images

1. **Tell a story**: Each image should show meaningful content
2. **Use realistic data**: Not "test1", "test2" but real-looking examples
3. **Show success states**: Features working, not error messages
4. **Maintain consistency**: Same theme, window size, data across images
5. **Update regularly**: Re-capture when UI changes significantly

## Questions?

If you need help with image capture:
- Check the project Discord
- Open a GitHub discussion
- Review other open-source projects' docs for inspiration
