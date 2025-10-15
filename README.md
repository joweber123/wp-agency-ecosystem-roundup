# Automattic RSS Aggregator

Weekly digest builder for Automattic family blogs.

## Quick Start - Styling Preview

To experiment with the digest styling locally:

### 1. Install dependencies

```bash
pip install jinja2
```

### 2. Generate the preview

```bash
python generate_preview.py
```

### 3. Open in browser

Open `preview.html` in your web browser to see the styled digest with sample posts.

### 4. Customize styling

Edit `template.html` to adjust colors, fonts, spacing, etc. Then re-run `python generate_preview.py` to see your changes.

## Files

- **template.html** - Jinja2 HTML template with embedded CSS styling
- **sample_data.json** - Sample RSS post data for preview generation
- **generate_preview.py** - Script to generate preview.html from template and sample data
- **preview.html** - Generated HTML file (open this in your browser)

## Next Steps

Once you're happy with the styling:
1. Implement the full RSS fetching logic (`digest_builder.py`)
2. Set up GitHub Actions workflow for automation
3. Configure email sending
4. Deploy to GitHub Pages

## Customization Tips

### Colors
The current color scheme uses WordPress blue (#2271b1). You can customize:
- Header gradient background
- Link colors
- Source badge colors (consider unique colors per blog)

### Layout
- Adjust `.container max-width` for wider/narrower digest
- Modify `.post` spacing and borders
- Change image sizing with `.post-image`

### Typography
- Font family is set in `body` selector
- Heading sizes: `.header h1`, `.post-title`
- Body text: `.post-summary`
