import os
import re
from bs4 import BeautifulSoup

base_dir = os.path.dirname(__file__)

# Read index.html to extract the cleaned content
with open(os.path.join(base_dir, 'index.html'), 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

# --------------------------------------------------------------------------
# 1. Build llms.txt (The Curated Index & Summary)
# --------------------------------------------------------------------------
llms_txt_content = """# Computing Machinery and Intelligence

> By Alan M. Turing (1950). Originally published in *Mind: A Quarterly Review of Psychology and Philosophy*, Vol. LIX, No. 236, Oct. 1950, pp. 433–460.
> Digital Edition: https://spinchange.github.io/computing-machinery-and-intelligence/
> Full Unabridged Text: https://spinchange.github.io/computing-machinery-and-intelligence/llms-full.txt

A landmark philosophical and computational treatise that founded modern artificial intelligence, replacing the ambiguous question "Can machines think?" with an operational test: the **Imitation Game** (now known as the **Turing Test**).

## Structure & Section Directory

- [1. The Imitation Game](https://spinchange.github.io/computing-machinery-and-intelligence/#sec-1): Proposes replacing "Can machines think?" with a concrete test. Introduces the three-player game (man $A$, woman $B$, interrogator $C$) and analyzes what happens when an artificial machine takes the part of player $A$.
- [2. Critique of the New Problem](https://spinchange.github.io/computing-machinery-and-intelligence/#sec-2): Justifies the question-and-answer (teleprinter) format, isolating intellectual capacity from physical appearance or sensory performance. Includes the famous chess move and poetry examples.
- [3. The Machines Concerned in the Game](https://spinchange.github.io/computing-machinery-and-intelligence/#sec-3): Delimits the scope strictly to "digital computers", excluding biological engineering and cloning.
- [4. Digital Computers](https://spinchange.github.io/computing-machinery-and-intelligence/#sec-4): Explains the computational architecture: Store (memory), Executive Unit (ALU/processor), and Control (instruction execution); distinction between book of rules and table of instructions.
- [5. Universality of Digital Computers](https://spinchange.github.io/computing-machinery-and-intelligence/#sec-5): Formulates the Discrete-State Machine model and the Universal Turing Machine principle: a digital computer with sufficient storage and speed can mimic the behaviour of any discrete-state machine. Includes the transition state table ($q_1, q_2, q_3$ / $i_0, i_1$).
- [6. Contrary Views on the Main Question](https://spinchange.github.io/computing-machinery-and-intelligence/#sec-6): Foresees and methodically refutes nine primary counterarguments:
  - [(1) The Theological Objection](https://spinchange.github.io/computing-machinery-and-intelligence/#the-theological-objection): Thinking is a function of an immortal soul granted only to humans. (Refutation: Does not limit divine omnipotence to embody a soul in a machine).
  - [(2) The 'Heads in the Sand' Objection](https://spinchange.github.io/computing-machinery-and-intelligence/#the-heads-in-the-sand-objection): The consequences of machine thought are too dreadful to contemplate. (Refutation: Emotional fear rather than argument).
  - [(3) The Mathematical Objection](https://spinchange.github.io/computing-machinery-and-intelligence/#the-mathematical-objection): Gödel's Incompleteness Theorem and Turing's Halting Problem limit formal logical systems. (Refutation: Humans are also fallible and subject to limitations).
  - [(4) The Argument from Consciousness](https://spinchange.github.io/computing-machinery-and-intelligence/#the-argument-from-consciousness): Jefferson's Lister Oration arguing machines cannot feel emotions or pride. Includes the famous *viva voce* dialogue on Shakespeare's Sonnet 18 and Mr. Pickwick. (Refutation: Leads inevitably to solipsism; the Imitation Game is our only empirical criterion for other minds).
  - [(5) Arguments from Various Disabilities](https://spinchange.github.io/computing-machinery-and-intelligence/#arguments-from-various-disabilities): "A machine can never do $X$" (be kind, have a sense of humour, make mistakes, fall in love, enjoy strawberries and cream). (Refutation: Based on ungrounded induction from special-purpose calculating engines).
  - [(6) Lady Lovelace's Objection](https://spinchange.github.io/computing-machinery-and-intelligence/#lady-lovelaces-objection): Babbage's Analytical Engine had no pretensions to originate anything; it only does what we know how to order it to do. (Refutation: Machines frequently surprise their creators through unexpected deductive consequences).
  - [(7) Argument from Continuity in the Nervous System](https://spinchange.github.io/computing-machinery-and-intelligence/#argument-from-continuity-in-the-nervous-system): The physical nervous system is continuous, not discrete. (Refutation: A discrete-state machine can approximate a continuous differential system arbitrarily closely).
  - [(8) The Argument from Informality of Behaviour](https://spinchange.github.io/computing-machinery-and-intelligence/#the-argument-from-informality-of-behaviour): There is no complete set of rules covering every human contingency. (Refutation: Confuses 'rules of conduct' with deterministic 'laws of behaviour').
  - [(9) The Argument from Extra-Sensory Perception](https://spinchange.github.io/computing-machinery-and-intelligence/#the-argument-from-extrasensory-perception): Telepathy, clairvoyance, and precognition might distinguish humans. (Refutation: A random number generator inside a "telepathy-proof room" neutralizes the statistical difference).
- [7. Learning Machines](https://spinchange.github.io/computing-machinery-and-intelligence/#sec-7): Turing’s prophetic blueprint for artificial general intelligence:
  - Rather than programming an adult mind, programme a **child machine** and subject it to an education process.
  - Parallels with evolution: child programme (heredity), education (environment), mutations (experimenter changes).
  - Reinforcement learning: teaching through systematic punishment and reward signals coupled with symbolic language.
  - Imperatives, internal reasoning, and incorporating random elements for heuristic search.
  - Final prophecy: "We can only see a short distance ahead, but we can see plenty there that needs to be done."
- [Footnotes](https://spinchange.github.io/computing-machinery-and-intelligence/#sec-footnotes): Four author footnotes detailing Aquinas on souls, bibliography references, child-machine logic, and Lady Lovelace's phrasing.
- [Bibliography](https://spinchange.github.io/computing-machinery-and-intelligence/#sec-bib): Key references (Samuel Butler, Alonzo Church, Kurt Gödel, D. R. Hartree, S. C. Kleene, Geoffrey Jefferson, Ada Lovelace, Bertrand Russell, and A. M. Turing).

## Key Quotations & Passages

### The Core Inquiry
> "I propose to consider the question, 'Can machines think?' This should begin with definitions of the meaning of the terms 'machine' and 'think' ... Instead of attempting such a definition I shall replace the question by another, which is closely related to it and is expressed in relatively unambiguous words." (§1)

### Viva Voce on Sonnet 18
> **Interrogator:** In the first line of your sonnet which reads "Shall I compare thee to a summer's day", would not "a spring day" do as well or better?  
> **Witness:** It wouldn't scan.  
> **Interrogator:** How about "a winter's day"? That would scan all right.  
> **Witness:** Yes, but nobody wants to be compared to a winter's day.  
> **Interrogator:** Would you say Mr. Pickwick reminded you of Christmas?  
> **Witness:** In a way.  
> **Interrogator:** Yet Christmas is a winter's day, and I do not think Mr. Pickwick would mind the comparison.  
> **Witness:** I don't think you're serious. By a winter's day one means a typical winter's day, rather than a special one like Christmas. (§6)

### The Child Machine Strategy
> "Instead of trying to produce a programme to simulate the adult mind, why not rather try to produce one which simulates the child's? If this were then subjected to an appropriate course of education one would obtain the adult brain ... We can only see a short distance ahead, but we can see plenty there that needs to be done." (§7)
"""

with open(os.path.join(base_dir, 'llms.txt'), 'w', encoding='utf-8') as f:
    f.write(llms_txt_content.strip() + "\n")

print(f"Generated llms.txt successfully ({len(llms_txt_content)} bytes).")

# --------------------------------------------------------------------------
# 2. Build llms-full.txt (The Unabridged Paper in Pristine Markdown)
# --------------------------------------------------------------------------
md_lines = [
    "# Computing Machinery and Intelligence",
    "### By A. M. Turing",
    "*Victoria University of Manchester*",
    "",
    "Originally published in *Mind: A Quarterly Review of Psychology and Philosophy*, Vol. LIX, No. 236, October 1950, pp. 433–460.",
    "",
    "---",
    ""
]

# Remove page markers from markdown export
for pm in soup.find_all(class_='page-marker'):
    pm.decompose()

sections = soup.find_all('section', class_='paper-section')

for sec in sections:
    sec_id = sec.get('id', '')
    title_el = sec.find(['h2', 'h1'])
    sec_title = title_el.get_text().strip() if title_el else sec_id
    
    if sec_id == 'sec-footnotes':
        md_lines.append(f"## Footnotes\n")
        for fn in sec.find_all('li', class_='footnote-item'):
            num = fn.find('span', class_='fn-number').get_text().strip()
            content = fn.find('div', class_='fn-content').get_text().replace('↩ Return to text', '').strip()
            md_lines.append(f"[^{num.strip('[]')}]: {content}\n")
        continue
        
    if sec_id == 'sec-colophon':
        continue
        
    md_lines.append(f"## {sec_title}\n")
    
    # Process content nodes
    content_div = sec.find('div', class_='section-content')
    if not content_div:
        content_div = sec
        
    for child in content_div.children:
        if not hasattr(child, 'name') or not child.name:
            continue
            
        if child.name == 'header' and 'objection-header' in child.get('class', []):
            num = child.find('span', class_='objection-badge').get_text().strip()
            title = child.find('h3', class_='objection-title').get_text().strip()
            md_lines.append(f"\n### {num} {title}\n")
            
        elif child.name == 'p':
            ptxt = child.get_text().strip()
            if ptxt:
                # Replace footnote anchors with markdown footnotes
                ptxt = re.sub(r'\[(\d+)\]', r'[^\1]', ptxt)
                md_lines.append(f"{ptxt}\n")
                
        elif child.name == 'div' and 'dialogue-card' in child.get('class', []):
            md_lines.append("")
            for turn in child.find_all('div', class_='dialogue-turn'):
                speaker = turn.find('div', class_='speaker-label').get_text().strip()
                bubble = turn.find('div', class_='speech-bubble').get_text().strip()
                # Clean up multiple whitespaces
                bubble = ' '.join(bubble.split())
                md_lines.append(f"> **{speaker}:** {bubble}")
            md_lines.append("")
            
        elif child.name == 'div' and 'table-container' in child.get('class', []):
            tbl = child.find('table')
            if tbl:
                md_lines.append("\n| | Last State: $q_1$ | Last State: $q_2$ | Last State: $q_3$ |")
                md_lines.append("|:---|:---:|:---:|:---:|")
                md_lines.append("| **Input: $i_0$** | $q_2$ | $q_3$ | $q_1$ |")
                md_lines.append("| **Input: $i_1$** | $q_1$ | $q_2$ | $q_3$ |\n")
                
        elif child.name == 'ol':
            md_lines.append("")
            for i, li in enumerate(child.find_all('li'), 1):
                md_lines.append(f"{i}. {li.get_text().strip()}")
            md_lines.append("")

full_md_text = "\n".join(md_lines)

with open(os.path.join(base_dir, 'llms-full.txt'), 'w', encoding='utf-8') as f:
    f.write(full_md_text)

print(f"Generated llms-full.txt successfully ({len(full_md_text)} bytes).")
