# Computing Machinery and Intelligence
### Alan M. Turing (1950) — Modern Reading Edition

> *"I propose to consider the question, 'Can machines think?'"*

A distraction-free, beautifully formatted digital reading edition of Alan Turing’s seminal 1950 paper, originally published in the journal *Mind* (Vol. LIX, No. 236, Oct. 1950, pp. 433–460). Designed as a standalone static publication optimized for GitHub Pages.

---

## ✨ Features

- **📖 Three Typographic Themes**:
  - **Paper (Light)**: Clean academic editorial typography with warm off-white tones.
  - **Sepia (Warm Library)**: Parchment-inspired palette designed for extended reading comfort.
  - **Dark (Obsidian)**: Deep charcoal background with calibrated contrast to reduce eye fatigue.
- **🧭 Sticky, Collapsible Table of Contents**:
  - Full section navigation (Sections 1 through 7, Footnotes, Bibliography, Colophon).
  - Dynamic scrollspy: Active section highlighting, including individual tracking for all **9 Objections** in Section 6.
- **💬 Dialogue Transcript Styling**:
  - The famous **Imitation Game** and **viva voce** dialogues (e.g. *Sonnet 18*, *Pickwick*, *chess moves*) are styled as clean conversational script exchanges with speaker badges (`Interrogator`, `Witness`, `Q`, `A`).
- **📐 Scientific State Machine Tables**:
  - Discrete-state machine tables (Section 5) rendered with crisp borders, subscript variables ($q_1, q_2, q_3$, $i_0, i_1$), and responsive horizontal scrolling.
- **🔖 Original Mind Journal Page Anchors**:
  - Every page transition from the original 1950 *Mind* journal (pp. 433–460) is preserved as a margin anchor (`#p433` – `#p460`) for academic reference.
- **💡 Interactive Footnotes**:
  - Inline references with hover tooltips for previewing notes without losing reading position, plus bottom anchor links with return jump (`↩`).
- **🔍 Quick Citations**:
  - One-click copy for **Chicago/APA** and **BibTeX** citations.
- **📱 Responsive & Print-Ready**:
  - Mobile drawer navigation and clean print styles (`@media print`) suitable for saving to PDF or physical printing.

---

## 🚀 Local Preview

To view the edition locally in your default web browser:

```powershell
Start-Process "C:\Users\executor\computing-machinery-and-intelligence\index.html"
```

---

## 🌐 Publishing to GitHub Pages

This project is self-contained (zero build dependencies, pure HTML5/CSS3/vanilla JS):

1. **Initialize Git & Push**:
   ```bash
   git init -b main
   git add .
   git commit -m "Initial commit: Turing 1950 reading edition"
   gh repo create computing-machinery-and-intelligence --public --source=. --remote=origin --push
   ```
2. **Enable GitHub Pages**:
   ```bash
   gh repo edit --enable-pages --pages-branch main
   ```
   The site will be live at:
   `https://<username>.github.io/computing-machinery-and-intelligence/`

---

## ⚖️ Legal & License

Alan Turing passed away on June 7, 1954. In the United Kingdom and other life-plus-70 copyright jurisdictions, Alan Turing's original writings entered the **Public Domain** on January 1, 2025. (Copyright status in other jurisdictions, such as the United States where protection for foreign works published in 1950 may run for 95 years from publication through 2046, may differ).

The typography, digital formatting, responsive layout, and accompanying code of this edition are dedicated to the public domain under the [Creative Commons Zero (CC0 1.0 Universal) Deed](https://creativecommons.org/publicdomain/zero/1.0/).
