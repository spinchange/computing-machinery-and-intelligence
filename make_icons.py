import os
from PIL import Image, ImageDraw, ImageFont

img_dir = os.path.dirname(__file__)

# 1. Generate icon.svg
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2c2417"/>
      <stop offset="100%" stop-color="#141416"/>
    </linearGradient>
    <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f97316"/>
      <stop offset="100%" stop-color="#ea580c"/>
    </linearGradient>
  </defs>
  <!-- Background with subtle border -->
  <rect width="512" height="512" rx="108" fill="url(#bg)"/>
  <rect x="16" y="16" width="480" height="480" rx="94" fill="none" stroke="#40404a" stroke-width="4"/>
  
  <!-- Outer decorative ring -->
  <circle cx="256" cy="256" r="190" fill="none" stroke="#2d2d34" stroke-width="3" stroke-dasharray="6,6"/>
  
  <!-- Classic Monogram "T" -->
  <text x="256" y="325" font-family="'Cinzel', Georgia, serif" font-size="280" font-weight="700" fill="url(#gold)" text-anchor="middle">T</text>
  
  <!-- Year 1950 sub-badge -->
  <rect x="186" y="375" width="140" height="38" rx="8" fill="#1e1e24" stroke="#40404a" stroke-width="2"/>
  <text x="256" y="401" font-family="'JetBrains Mono', monospace" font-size="20" font-weight="600" fill="#e6e6ea" text-anchor="middle" letter-spacing="3">1950</text>
</svg>
'''

with open(os.path.join(img_dir, 'icon.svg'), 'w', encoding='utf-8') as f:
    f.write(svg_content)

# 2. Generate PNG icons (192 and 512)
for size in [192, 512]:
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # Rounded rectangle background
    corner_radius = int(size * 0.21)
    draw.rounded_rectangle([0, 0, size, size], radius=corner_radius, fill='#1f1c18')
    
    # Subtle inner border
    border_inset = int(size * 0.04)
    draw.rounded_rectangle(
        [border_inset, border_inset, size - border_inset, size - border_inset],
        radius=int(corner_radius * 0.85),
        outline='#383228',
        width=max(1, int(size * 0.01))
    )
    
    # Try loading font or draw clean glyph
    fonts_dir = os.path.join(img_dir, 'fonts')
    cinzel_path = os.path.join(fonts_dir, 'cinzel-normal-700.woff2')
    mono_path = os.path.join(fonts_dir, 'jetbrains-mono-normal-500.woff2')
    
    try:
        font_t = ImageFont.truetype(cinzel_path, int(size * 0.55))
        font_yr = ImageFont.truetype(mono_path, int(size * 0.08))
    except Exception:
        font_t = ImageFont.load_default()
        font_yr = ImageFont.load_default()
        
    # Draw 'T'
    draw.text((size / 2, size * 0.44), "T", fill='#ea580c', font=font_t, anchor='mm')
    
    # Draw '1950' pill
    pill_w = int(size * 0.35)
    pill_h = int(size * 0.1)
    pill_x0 = (size - pill_w) / 2
    pill_y0 = int(size * 0.76)
    draw.rounded_rectangle([pill_x0, pill_y0, pill_x0 + pill_w, pill_y0 + pill_h], radius=int(pill_h * 0.3), fill='#2d2720', outline='#4a4034')
    draw.text((size / 2, pill_y0 + pill_h / 2), "1950", fill='#e6e6ea', font=font_yr, anchor='mm')
    
    png_path = os.path.join(img_dir, f'icon-{size}.png')
    im.save(png_path, 'PNG')
    print(f"Generated icon-{size}.png ({os.path.getsize(png_path)} bytes)")

print("Generated icon.svg, icon-192.png, icon-512.png successfully.")
