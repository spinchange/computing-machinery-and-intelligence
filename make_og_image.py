import os
from PIL import Image, ImageDraw, ImageFont

img_width = 1200
img_height = 630

# Create canvas with warm editorial cream background
img = Image.new('RGB', (img_width, img_height), color='#f7f4ed')
draw = ImageDraw.Draw(img)

# Outer decorative border
draw.rectangle([24, 24, img_width - 25, img_height - 25], outline='#dcd4c3', width=2)
draw.rectangle([30, 30, img_width - 31, img_height - 31], outline='#8a2800', width=1)

# Try loading local fonts or fall back
fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
try:
    font_journal = ImageFont.truetype(os.path.join(fonts_dir, 'cinzel-normal-700.woff2'), 22)
    font_title = ImageFont.truetype(os.path.join(fonts_dir, 'cinzel-normal-700.woff2'), 44)
    font_author = ImageFont.truetype(os.path.join(fonts_dir, 'cinzel-normal-500.woff2'), 28)
    font_quote = ImageFont.truetype(os.path.join(fonts_dir, 'newsreader-italic-400700.woff2'), 25)
    font_footer = ImageFont.truetype(os.path.join(fonts_dir, 'inter-normal-600.woff2'), 18)
except Exception:
    font_journal = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_author = ImageFont.load_default()
    font_quote = ImageFont.load_default()
    font_footer = ImageFont.load_default()

# Header: Journal
journal_text = "M I N D  ·  O C T O B E R   1 9 5 0  ·  V O L .  L I X  ·  N O .  2 3 6"
draw.text((img_width / 2, 80), journal_text, fill='#7a7263', font=font_journal, anchor='mm')

# Title
title_line1 = "COMPUTING MACHINERY"
title_line2 = "AND INTELLIGENCE"
draw.text((img_width / 2, 160), title_line1, fill='#1f1c18', font=font_title, anchor='mm')
draw.text((img_width / 2, 215), title_line2, fill='#1f1c18', font=font_title, anchor='mm')

# Author
draw.text((img_width / 2, 280), "BY  A. M. TURING", fill='#9a3412', font=font_author, anchor='mm')

# Divider line
draw.line([(img_width / 2 - 120, 315), (img_width / 2 + 120, 315)], fill='#c8bfaf', width=1)

# Quote Box
quote_lines = [
    "“I propose to consider the question, ‘Can machines think?’",
    "The new form of the problem can be described in terms of a game",
    "which we call the ‘imitation game’.”"
]
y_start = 365
for line in quote_lines:
    draw.text((img_width / 2, y_start), line, fill='#4a4338', font=font_quote, anchor='mm')
    y_start += 38

# Footer badge
footer_bg = [img_width / 2 - 280, 520, img_width / 2 + 280, 565]
draw.rectangle(footer_bg, fill='#efe9db', outline='#d0c6b2', width=1)
draw.text((img_width / 2, 542), "DISTRACTION-FREE DIGITAL READING EDITION", fill='#8a2800', font=font_footer, anchor='mm')

out_path = os.path.join(os.path.dirname(__file__), 'og-preview.png')
img.save(out_path, 'PNG')
print(f"Generated og-preview.png ({os.path.getsize(out_path)} bytes)")
