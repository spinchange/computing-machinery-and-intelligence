import os
import urllib.request
import re

fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
os.makedirs(fonts_dir, exist_ok=True)

url = "https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=swap"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
css = urllib.request.urlopen(req).read().decode('utf-8')

# Extract only /* latin */ blocks
blocks = re.findall(r'(\/\* latin \*\/[^{]+\{[^}]+\})', css)
print(f"Total latin blocks found: {len(blocks)}")

local_css_blocks = []
for idx, block in enumerate(blocks):
    font_family = re.search(r'font-family:\s*\'([^\']+)\'', block).group(1)
    font_weight = re.search(r'font-weight:\s*([^;]+);', block).group(1).strip()
    font_style = re.search(r'font-style:\s*([^;]+);', block).group(1).strip()
    remote_url = re.search(r'url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)', block).group(1)
    
    clean_fam = font_family.lower().replace(' ', '-')
    clean_wt = font_weight.replace(' ', '')
    filename = f"{clean_fam}-{font_style}-{clean_wt}.woff2"
    filepath = os.path.join(fonts_dir, filename)
    
    # Download font file
    if not os.path.exists(filepath):
        print(f"Downloading {filename} from {remote_url}...")
        urllib.request.urlretrieve(remote_url, filepath)
    else:
        print(f"Already have {filename}")
        
    # Replace remote URL with local path in block
    local_block = block.replace(remote_url, f"fonts/{filename}")
    local_css_blocks.append(local_block)

fonts_css_path = os.path.join(os.path.dirname(__file__), 'fonts.css')
with open(fonts_css_path, 'w', encoding='utf-8') as f:
    f.write("/* Local Self-Hosted Fonts (Latin Subsets) */\n\n" + "\n\n".join(local_css_blocks) + "\n")

print(f"Created fonts.css successfully with {len(local_css_blocks)} @font-face rules.")
