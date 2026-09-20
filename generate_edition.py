import sys
import os
import re
import urllib.request
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

base_url = 'https://raw.githubusercontent.com/DarkerStar/epub-turing-computing-machinery-and-intelligence/master/src/text/'

sections_info = [
    ('section-1.xhtml', 'sec-1', '1. The Imitation Game'),
    ('section-2.xhtml', 'sec-2', '2. Critique of the New Problem'),
    ('section-3.xhtml', 'sec-3', '3. The Machines Concerned in the Game'),
    ('section-4.xhtml', 'sec-4', '4. Digital Computers'),
    ('section-5.xhtml', 'sec-5', '5. Universality of Digital Computers'),
    ('section-6.xhtml', 'sec-6', '6. Contrary Views on the Main Question'),
    ('section-7.xhtml', 'sec-7', '7. Learning Machines'),
    ('bibliography.xhtml', 'sec-bib', 'Bibliography')
]

objections_meta = [
    ('the-theological-objection', '1', 'The Theological Objection'),
    ('the-heads-in-the-sand-objection', '2', 'The ‘Heads in the Sand’ Objection'),
    ('the-mathematical-objection', '3', 'The Mathematical Objection'),
    ('the-argument-from-consciousness', '4', 'The Argument from Consciousness'),
    ('arguments-from-various-disabilities', '5', 'Arguments from Various Disabilities'),
    ('lady-lovelaces-objection', '6', 'Lady Lovelace’s Objection'),
    ('argument-from-continuity-in-the-nervous-system', '7', 'Argument from Continuity in the Nervous System'),
    ('the-argument-from-informality-of-behaviour', '8', 'The Argument from Informality of Behaviour'),
    ('the-argument-from-extrasensory-perception', '9', 'The Argument from Extra-Sensory Perception')
]

objection_dict = {slug: (num, title) for slug, num, title in objections_meta}

def clean_text(html_str):
    html_str = html_str.replace('&#173;', '').replace('\xad', '')
    html_str = html_str.replace('apart front the other two', 'apart from the other two')
    html_str = html_str.replace('does calculations in his bead', 'does calculations in his head')
    return html_str

footnotes = {
    'fn1': {
        'num': '1',
        'html': 'Possibly this view is heretical. St. Thomas Aquinas (<em>Summa Theologica</em>, quoted by Bertrand Russell p. 480) states that God cannot make a man to have no soul. But this may not be a real restriction on His powers, but only a result of the fact that men’s souls are immortal, and therefore indestructible.',
        'sec': 'sec-6'
    },
    'fn2': {
        'num': '2',
        'html': 'Author’s names in italics refer to the <a href="#sec-bib">Bibliography</a>.',
        'sec': 'sec-6'
    },
    'fn3': {
        'num': '3',
        'html': 'Or rather ‘programmed in’ for our child-machine will be programmed in a digital computer. But the logical system will not have to be learnt.',
        'sec': 'sec-7'
    },
    'fn4': {
        'num': '4',
        'html': 'Compare Lady Lovelace’s statement (<a class="page-link" href="#p450">p. 450</a>), which does not contain the word ‘only’.',
        'sec': 'sec-7'
    }
}

def transform_links(soup):
    for a in soup.find_all('a'):
        href = a.get('href', '')
        href = re.sub(r'section-1\.xhtml', '#sec-1', href)
        href = re.sub(r'section-2\.xhtml', '#sec-2', href)
        href = re.sub(r'section-3\.xhtml', '#sec-3', href)
        href = re.sub(r'section-4\.xhtml#page-(\d+)', r'#p\1', href)
        href = re.sub(r'section-4\.xhtml', '#sec-4', href)
        href = re.sub(r'section-5\.xhtml', '#sec-5', href)
        href = re.sub(r'section-6\.xhtml#page-(\d+)', r'#p\1', href)
        href = re.sub(r'section-6\.xhtml', '#sec-6', href)
        href = re.sub(r'section-7\.xhtml#page-(\d+)', r'#p\1', href)
        href = re.sub(r'section-7\.xhtml', '#sec-7', href)
        href = re.sub(r'bibliography\.xhtml', '#sec-bib', href)
        a['href'] = href

def transform_footnotes_in_text(soup):
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if href in ['#fn1', '#fn2', '#fn3', '#fn4']:
            fn_id = href.lstrip('#')
            fn_info = footnotes[fn_id]
            sup = soup.new_tag('sup', **{'class': 'fn-ref'})
            new_a = soup.new_tag('a', href=f"#{fn_id}", id=f"ref-{fn_id}", **{
                'data-footnote-id': fn_id,
                'class': 'fn-link',
                'title': f"Footnote {fn_info['num']}"
            })
            new_a.string = f"[{fn_info['num']}]"
            sup.append(new_a)
            a.replace_with(sup)
    for aside in soup.find_all('aside'):
        aside.decompose()

def transform_pagebreaks(soup):
    for sp in soup.find_all('span', attrs={'epub:type': 'pagebreak'}):
        pg = sp.get('title') or sp.get('id', '').replace('page-', '')
        marker = soup.new_tag('span', **{
            'class': 'page-marker',
            'id': f'p{pg}',
            'data-page': pg,
            'title': f'Original Mind journal page {pg}'
        })
        badge = soup.new_tag('span', **{'class': 'page-marker-badge'})
        badge.string = f'p. {pg}'
        marker.append(badge)
        sp.replace_with(marker)

def transform_dialogues(soup, fname):
    if fname == 'section-1.xhtml':
        ps = soup.find_all('p')
        for i, p in enumerate(ps):
            t = p.get_text().strip()
            if 'Will' in t and 'please tell me the length of his or her hair?' in t:
                if i + 1 < len(ps):
                    next_p = ps[i+1]
                    card = soup.new_tag('div', **{'class': 'dialogue-card imitation-intro'})
                    
                    turn1 = soup.new_tag('div', **{'class': 'dialogue-turn speaker-interrogator'})
                    badge1 = soup.new_tag('div', **{'class': 'speaker-label'})
                    badge1.string = 'Interrogator (C)'
                    bubble1 = soup.new_tag('div', **{'class': 'speech-bubble'})
                    bubble1.append(BeautifulSoup('Will <var>X</var> please tell me the length of his or her hair?', 'html.parser'))
                    turn1.append(badge1)
                    turn1.append(bubble1)
                    
                    turn2 = soup.new_tag('div', **{'class': 'dialogue-turn speaker-candidate'})
                    badge2 = soup.new_tag('div', **{'class': 'speaker-label'})
                    badge2.string = 'Candidate (A)'
                    bubble2 = soup.new_tag('div', **{'class': 'speech-bubble'})
                    bubble2.append(BeautifulSoup('“My hair is shingled, and the longest strands are about nine inches long.”', 'html.parser'))
                    turn2.append(badge2)
                    turn2.append(bubble2)
                    
                    card.append(turn1)
                    card.append(turn2)
                    p.replace_with(card)
                    next_p.decompose()
                break

    for dl in soup.find_all('dl', class_=re.compile(r'conversation')):
        card = soup.new_tag('div', **{'class': 'dialogue-card script-format'})
        dts = dl.find_all('dt')
        dds = dl.find_all('dd')
        for dt, dd in zip(dts, dds):
            raw_spk = dt.get_text().strip().rstrip(':').strip()
            cls = 'speaker-interrogator' if raw_spk in ['Q', 'Interrogator'] else 'speaker-candidate'
            
            turn = soup.new_tag('div', **{'class': f'dialogue-turn {cls}'})
            label = soup.new_tag('div', **{'class': 'speaker-label'})
            label.string = raw_spk
            bubble = soup.new_tag('div', **{'class': 'speech-bubble'})
            for c in dd.contents:
                bubble.append(c)
            turn.append(label)
            turn.append(bubble)
            card.append(turn)
        dl.replace_with(card)

def transform_section_6(soup):
    h1s = soup.find_all('h1')
    for h in h1s:
        hid = h.get('id', '')
        if hid in objection_dict:
            num, title = objection_dict[hid]
            header_div = soup.new_tag('header', **{'class': 'objection-header', 'id': hid})
            badge = soup.new_tag('span', **{'class': 'objection-badge'})
            badge.string = f"({num})"
            title_tag = soup.new_tag('h3', **{'class': 'objection-title'})
            title_tag.string = title.replace(f"({num})", "").strip()
            header_div.append(badge)
            header_div.append(title_tag)
            h.replace_with(header_div)

def transform_tables(soup):
    for tbl in soup.find_all('table'):
        tbl['class'] = tbl.get('class', []) + ['turing-table']
        wrap = soup.new_tag('div', **{'class': 'table-container'})
        tbl.wrap(wrap)

# Process all sections
sections_html = []
for fname, sec_id, title in sections_info:
    url = base_url + fname
    raw = urllib.request.urlopen(url).read().decode('utf-8')
    raw = clean_text(raw)
    soup = BeautifulSoup(raw, 'html.parser')
    
    transform_links(soup)
    transform_footnotes_in_text(soup)
    transform_pagebreaks(soup)
    transform_dialogues(soup, fname)
    transform_tables(soup)
    if fname == 'section-6.xhtml':
        transform_section_6(soup)
        
    first_h1 = soup.find('h1')
    if first_h1:
        first_h1.decompose()
        
    body_content = soup.find('section') or soup.find('body')
    inner_html = ''.join(str(c) for c in body_content.children if str(c).strip())
    
    sections_html.append({
        'id': sec_id,
        'title': title,
        'fname': fname,
        'html': inner_html
    })

# Build Table of Contents HTML
toc_items = []
for sec in sections_html:
    if sec['id'] == 'sec-6':
        sub_items = "".join([
            f'<li class="toc-subitem"><a href="#{slug}" class="toc-sublink"><span class="toc-num">({num})</span> {title.split(f"({num}) ")[-1]}</a></li>'
            for slug, num, title in objections_meta
        ])
        toc_items.append(f'''
        <li class="toc-item has-subitems" id="toc-item-sec-6">
            <a href="#{sec['id']}" class="toc-link"><span class="toc-bullet">6</span> Contrary Views</a>
            <ul class="toc-sublist">
                {sub_items}
            </ul>
        </li>
        ''')
    elif sec['id'] == 'sec-bib':
        continue
    else:
        num = sec['title'].split('.')[0]
        label = sec['title'].split('. ', 1)[-1]
        toc_items.append(f'''
        <li class="toc-item" id="toc-item-{sec['id']}">
            <a href="#{sec['id']}" class="toc-link"><span class="toc-bullet">{num}</span> {label}</a>
        </li>
        ''')

toc_items.append('''
<li class="toc-item" id="toc-item-sec-footnotes">
    <a href="#sec-footnotes" class="toc-link"><span class="toc-bullet">※</span> Footnotes</a>
</li>
<li class="toc-item" id="toc-item-sec-bib">
    <a href="#sec-bib" class="toc-link"><span class="toc-bullet">¶</span> Bibliography</a>
</li>
<li class="toc-item" id="toc-item-sec-colophon">
    <a href="#sec-colophon" class="toc-link"><span class="toc-bullet">ℹ</span> Colophon</a>
</li>
''')

toc_html = f'''
<nav id="toc-nav" aria-label="Table of Contents">
    <div class="toc-header">
        <span class="toc-title">Table of Contents</span>
        <button id="toc-close-btn" class="icon-btn close-btn" aria-label="Close Table of Contents">✕</button>
    </div>
    <ul class="toc-list">
        {"".join(toc_items)}
    </ul>
</nav>
'''

# Build Footnotes Section HTML
fn_list_items = []
for fn_id in ['fn1', 'fn2', 'fn3', 'fn4']:
    info = footnotes[fn_id]
    fn_list_items.append(f'''
    <li class="footnote-item" id="{fn_id}">
        <span class="fn-number">[{info['num']}]</span>
        <div class="fn-content">
            <p>{info['html']} <a href="#ref-{fn_id}" class="fn-backlink" title="Return to reference in text">↩ Return to text</a></p>
        </div>
    </li>
    ''')

footnotes_section_html = f'''
<section id="sec-footnotes" class="paper-section footnotes-section">
    <header class="section-header">
        <h2 class="section-title">Footnotes</h2>
    </header>
    <ol class="footnotes-list">
        {"".join(fn_list_items)}
    </ol>
</section>
'''

# Build Articles Body HTML
body_sections_html = []
for sec in sections_html:
    if sec['id'] == 'sec-bib':
        body_sections_html.append(f'''
        <section id="{sec['id']}" class="paper-section bibliography-section">
            <header class="section-header">
                <h2 class="section-title">Bibliography</h2>
            </header>
            <div class="section-content">
                {sec['html']}
            </div>
        </section>
        ''')
    else:
        body_sections_html.append(f'''
        <section id="{sec['id']}" class="paper-section">
            <header class="section-header">
                <h2 class="section-title">{sec['title']}</h2>
            </header>
            <div class="section-content">
                {sec['html']}
            </div>
        </section>
        ''')

# Build Colophon Section HTML
colophon_html = '''
<section id="sec-colophon" class="paper-section colophon-section">
    <header class="section-header">
        <h2 class="section-title">Colophon & Historical Notes</h2>
    </header>
    <div class="section-content colophon-box">
        <div class="colophon-item">
            <h4>Original Source</h4>
            <p><strong>Computing Machinery and Intelligence</strong> was originally published in the philosophical journal <em>Mind</em>, Vol. LIX, No. 236, October 1950, pp. 433–460 by Thomas Nelson &amp; Sons on behalf of the Mind Association.</p>
        </div>
        <div class="colophon-item">
            <h4>Textual Fidelity</h4>
            <p>This digital edition is faithfully transcribed from the original print pages. Soft hyphens and historical typesetting artifacts have been cleaned for modern continuous reading. Original journal page transitions are preserved as margin anchors (<em>p. 433</em> through <em>p. 460</em>). Cross-references and the four original author footnotes are linked interactively.</p>
        </div>
        <div class="colophon-item">
            <h4>Copyright &amp; License</h4>
            <p>Alan Turing passed away on June 7, 1954. Under United Kingdom and international copyright law (life of author plus 70 years), Alan Turing’s original writings entered the <strong>Public Domain</strong> on January 1, 2025. This reader edition and its formatting are released into the public domain under Creative Commons Zero (CC0).</p>
        </div>
    </div>
</section>
'''

full_html = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Computing Machinery and Intelligence — Alan M. Turing (1950)</title>
    <meta name="description" content="A distraction-free, beautifully formatted reading edition of Alan Turing's landmark 1950 paper 'Computing Machinery and Intelligence' introducing the Turing Test and Imitation Game.">
    <meta name="author" content="Alan M. Turing">
    
    <!-- OpenGraph / Social -->
    <meta property="og:title" content="Computing Machinery and Intelligence — Alan M. Turing (1950)">
    <meta property="og:description" content="Distraction-free, beautifully formatted digital edition of Alan Turing's seminal 1950 paper.">
    <meta property="og:type" content="article">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,300..700;1,6..72,300..700&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Top Progress Bar -->
    <div id="progress-container" aria-hidden="true">
        <div id="progress-bar"></div>
    </div>

    <!-- Top Navigation Deck -->
    <header id="top-bar">
        <div class="topbar-inner">
            <div class="topbar-left">
                <button id="toc-toggle" class="icon-btn" aria-label="Toggle Table of Contents" title="Table of Contents">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="3" y1="6" x2="21" y2="6"></line>
                        <line x1="3" y1="12" x2="21" y2="12"></line>
                        <line x1="3" y1="18" x2="21" y2="18"></line>
                    </svg>
                    <span class="btn-text">Contents</span>
                </button>
                <div class="topbar-branding">
                    <span class="topbar-paper-title">Computing Machinery and Intelligence</span>
                    <span class="topbar-author">A. M. Turing · 1950</span>
                </div>
            </div>

            <div class="topbar-right">
                <div class="read-stats" title="Estimated reading length">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                    <span>~35 min</span>
                </div>

                <div class="divider"></div>

                <!-- Font Size Controls -->
                <div class="font-controls" role="group" aria-label="Font size adjustment">
                    <button id="font-dec" class="control-btn" title="Decrease font size">A−</button>
                    <button id="font-inc" class="control-btn" title="Increase font size">A+</button>
                </div>

                <div class="divider"></div>

                <!-- Theme Switcher -->
                <div class="theme-controls" role="group" aria-label="Theme selector">
                    <button class="theme-btn" data-theme="light" title="Light (Clean Paper)">Paper</button>
                    <button class="theme-btn" data-theme="parchment" title="Parchment (Warm Library)">Sepia</button>
                    <button class="theme-btn" data-theme="dark" title="Dark (Obsidian)">Dark</button>
                </div>

                <!-- Citation Modal Trigger -->
                <button id="cite-btn" class="icon-btn cite-btn" title="Cite this work" aria-label="Cite this work">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path>
                        <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path>
                        <path d="M4 22h16"></path>
                        <path d="M10 14.66V17c0 .55-.45 1-1 1s-1-.45-1-1v-2.34c0-2.22 1.78-4.02 4-4.02v2a2.01 2.01 0 0 0-2 2.36z"></path>
                    </svg>
                    <span class="btn-text">Cite</span>
                </button>
            </div>
        </div>
    </header>

    <!-- App Layout Container -->
    <div class="app-layout">
        <!-- Sidebar Backdrop (Mobile) -->
        <div id="sidebar-backdrop" class="sidebar-backdrop"></div>

        <!-- Sticky Table of Contents Sidebar -->
        <aside id="sidebar" class="sidebar" aria-label="Navigation sidebar">
            <div class="sidebar-sticky">
                {toc_html}
            </div>
        </aside>

        <!-- Main Document Area -->
        <main id="main-content" class="reader-main">
            <article class="paper-article">
                <!-- Academic Title Header -->
                <header class="paper-header">
                    <div class="journal-stamp">
                        <span class="journal-name">Mind</span>
                        <span class="journal-volume">A Quarterly Review of Psychology and Philosophy</span>
                        <span class="journal-issue">Vol. LIX · No. 236 · October, 1950 · pp. 433–460</span>
                    </div>

                    <h1 class="paper-title">Computing Machinery and Intelligence</h1>

                    <div class="author-block">
                        <span class="author-by">By</span>
                        <span class="author-name">A. M. Turing</span>
                        <span class="author-affiliation">Victoria University of Manchester</span>
                    </div>

                    <div class="header-abstract-banner">
                        <p class="abstract-quote">“I propose to consider the question, <em>‘Can machines think?’</em> This should begin with definitions of the meaning of the terms ‘machine’ and ‘think’ … Instead of attempting such a definition I shall replace the question by another, which is closely related to it and is expressed in relatively unambiguous words.”</p>
                    </div>

                    <div class="quick-jump-bar">
                        <span class="jump-label">Jump to:</span>
                        <a href="#sec-1" class="jump-chip">1. The Imitation Game</a>
                        <a href="#sec-4" class="jump-chip">4. Digital Computers</a>
                        <a href="#sec-6" class="jump-chip">6. The 9 Objections</a>
                        <a href="#sec-7" class="jump-chip">7. Learning Machines</a>
                    </div>
                </header>

                <!-- Article Sections -->
                {"".join(body_sections_html)}

                <!-- Footnotes Section -->
                {footnotes_section_html}

                <!-- Colophon Section -->
                {colophon_html}
            </article>
        </main>
    </div>

    <!-- Floating Footnote Preview Tooltip / Popover -->
    <div id="fn-popover" class="fn-popover" role="tooltip" aria-hidden="true">
        <div class="popover-header">
            <span class="popover-title">Footnote</span>
            <button id="popover-close" class="popover-close-btn" aria-label="Close footnote popup">✕</button>
        </div>
        <div id="popover-body" class="popover-body"></div>
        <div class="popover-footer">
            <a id="popover-jump-btn" href="#" class="popover-jump-link">Go to footnote section ↓</a>
        </div>
    </div>

    <!-- Citation Modal -->
    <div id="cite-modal" class="modal" aria-hidden="true" role="dialog">
        <div class="modal-backdrop"></div>
        <div class="modal-card">
            <div class="modal-header">
                <h3>Cite This Paper</h3>
                <button id="modal-close" class="modal-close-btn" aria-label="Close dialog">✕</button>
            </div>
            <div class="modal-body">
                <div class="cite-tabs">
                    <button class="cite-tab-btn active" data-tab="chicago">Chicago / APA</button>
                    <button class="cite-tab-btn" data-tab="bibtex">BibTeX</button>
                </div>
                <div class="cite-panels">
                    <div class="cite-panel active" id="cite-chicago">
                        <pre class="cite-code" id="chicago-text">Turing, Alan M. "Computing Machinery and Intelligence." Mind 59, no. 236 (1950): 433–460.</pre>
                        <button class="copy-cite-btn" data-target="chicago-text">Copy Citation</button>
                    </div>
                    <div class="cite-panel" id="cite-bibtex">
                        <pre class="cite-code" id="bibtex-text">@article{{turing1950computing,
  title={{Computing Machinery and Intelligence}},
  author={{Turing, Alan M.}},
  journal={{Mind}},
  volume={{59}},
  number={{236}},
  pages={{433--460}},
  year={{1950}},
  publisher={{Oxford University Press}}
}}</pre>
                        <button class="copy-cite-btn" data-target="bibtex-text">Copy BibTeX</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="app.js"></script>
</body>
</html>
'''

output_path = os.path.join(os.path.dirname(__file__), 'index.html')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Generated index.html successfully ({len(full_html)} bytes).")
