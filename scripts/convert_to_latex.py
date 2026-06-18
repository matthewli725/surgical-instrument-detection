"""
Convert TrayGuard final paper from Markdown to LaTeX (.tex) and bibliography
from Markdown to BibTeX (.bib).

Usage:
  python3 scripts/convert_to_latex.py
"""

import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(SCRIPT_DIR, "..", "docs")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "latex_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── helpers ──────────────────────────────────────────────────────────────

def esc(text):
    """Escape LaTeX special characters."""
    replacements = [
        ('\\', '\\textbackslash{}'),
        ('{', '\\{'),
        ('}', '\\}'),
        ('$', '\\$'),
        ('%', '\\%'),
        ('&', '\\&'),
        ('#', '\\#'),
        ('_', '\\_'),
        ('^', '\\^{}'),
        ('~', '\\textasciitilde{}'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def convert_inline(text, cite_map):
    """Convert inline markdown in a line of text.
    
    cite_map: dict mapping placeholder -> \cite{key} string (restored last)
    """

    # 1. Replace citations with placeholders (protected from escaping)
    def _cite_repl(m):
        key = m.group(2)
        placeholder = f'\x00CT{len(cite_map)}\x00'
        cite_map[placeholder] = f'\\cite{{{key}}}'
        return placeholder

    text = re.sub(
        r'\(?\[([^\]]+)\]\(bibliography\.md#([^\)]+)\)\)?',
        _cite_repl,
        text,
    )

    # 2. Inline code `code` -> \texttt{code} (escape special chars within)
    parts = re.split(r'(`[^`]+`)', text)
    for i, part in enumerate(parts):
        if part.startswith('`') and part.endswith('`'):
            code = part[1:-1]
            parts[i] = f'\\texttt{{{esc(code)}}}'
        else:
            parts[i] = esc(part)
    text = ''.join(parts)

    # 3. Bold **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    # 4. Italic *text* (not adjacent to word characters)
    text = re.sub(r'(?<!\w)\*(?!\*)([^*]+?)(?<!\*)\*(?!\w)', r'\\textit{\1}', text)

    # 5. Restore cite placeholders
    for placeholder, cmd in cite_map.items():
        text = text.replace(placeholder, cmd)

    return text


_label_counts = {}

def convert_heading(line, cite_map):
    """Convert a markdown heading line to LaTeX."""
    m = re.match(r'^(#{1,4})\s+(.+)$', line)
    if not m:
        return line
    level = len(m.group(1))
    title = m.group(2).strip()

    # Include section number (if any) in label for uniqueness
    numbering = re.match(r'^([\d.]+)', title)
    num_prefix = numbering.group(1).replace('.', '-') if numbering else ''
    label_title = re.sub(r'^[\d.]+ ', '', title)
    base = label_title.lower()
    base = re.sub(r'[^a-z0-9]+', '-', base).strip('-')
    label = f'{num_prefix}-{base}' if num_prefix else base
    label = label.strip('-')

    # Deduplicate if needed
    global _label_counts
    if label in _label_counts:
        _label_counts[label] += 1
        label = f'{label}-{_label_counts[label]}'
    else:
        _label_counts[label] = 0

    title_tex = convert_inline(title, cite_map)

    if level == 2:
        cmd = 'section'
    elif level == 3:
        cmd = 'subsection'
    elif level == 4:
        cmd = 'subsubsection'
    else:
        return line

    return f'\\{cmd}{{{title_tex}}}\n\\label{{sec:{label}}}'


def process_table(table_lines, cite_map):
    """Convert a markdown table to LaTeX tabular."""
    if len(table_lines) < 2:
        return table_lines

    header = [c.strip() for c in table_lines[0].split('|')[1:-1]]
    sep = table_lines[1]
    aligns = []
    for cell in sep.split('|')[1:-1]:
        c = cell.strip()
        if c.startswith(':') and c.endswith(':'):
            aligns.append('c')
        elif c.endswith(':'):
            aligns.append('r')
        else:
            aligns.append('l')
    data = table_lines[2:]

    num_cols = len(header)
    col_spec = '|' + '|'.join(aligns[:num_cols]) + '|'

    out = []
    out.append('\\begin{table}[ht]')
    out.append('\\centering')
    out.append('\\resizebox{\\textwidth}{!}{%')
    out.append(f'\\begin{{tabular}}{{{col_spec}}}')
    out.append('\\hline')
    out.append(' & '.join(convert_inline(h, cite_map) for h in header) + ' \\\\')
    out.append('\\hline')
    for row in data:
        cells = [c.strip() for c in row.split('|')[1:-1]]
        out.append(' & '.join(convert_inline(c, cite_map) for c in cells) + ' \\\\')
    out.append('\\hline')
    out.append('\\end{tabular}')
    out.append('}')
    out.append('\\end{table}')
    return out


def process_list_block(lines, list_type, cite_map):
    """Convert a list block to LaTeX itemize/enumerate."""
    env = 'itemize' if list_type == 'ul' else 'enumerate'
    out = [f'\\begin{{{env}}}']
    for line in lines:
        stripped = line.strip()
        if list_type == 'ul':
            content = re.sub(r'^[-*+]\s+', '', stripped)
        else:
            content = re.sub(r'^\d+\.\s+', '', stripped)
        out.append(f'  \\item {convert_inline(content, cite_map)}')
    out.append(f'\\end{{{env}}}')
    return out


def convert_document(text):
    """Full markdown-to-LaTeX conversion."""
    lines = text.split('\n')
    result = []
    cite_map = {}  # shared across all inline processing in this doc

    i = 0
    in_table = False
    table_lines = []
    in_list = False
    list_type = None
    list_lines = []
    in_code = False
    code_lines = []
    code_lang = ''
    in_quote = False
    quote_lines = []

    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        # ── code fence ──
        if stripped.startswith('```'):
            if not in_code:
                in_code = True
                code_lang = stripped[3:].strip()
                code_lines = []
                i += 1
                continue
            else:
                in_code = False
                content = '\n'.join(code_lines)
                if code_lang == 'mermaid':
                    result.append('\\begin{lstlisting}')
                    result.append('[Mermaid diagram]')
                    result.append(content)
                    result.append('\\end{lstlisting}')
                else:
                    result.append('\\begin{lstlisting}')
                    result.append(content)
                    result.append('\\end{lstlisting}')
                i += 1
                continue

        if in_code:
            code_lines.append(stripped)
            i += 1
            continue

        # ── blockquote ──
        if stripped.startswith('> '):
            quote_lines.append(convert_inline(stripped[2:], cite_map))
            i += 1
            continue
        elif quote_lines:
            result.append('\\begin{quote}')
            result.extend(quote_lines)
            result.append('\\end{quote}')
            quote_lines = []

        # ── table ──
        if '|' in stripped and stripped.startswith('|') and stripped.endswith('|'):
            table_lines.append(stripped)
            i += 1
            continue
        elif table_lines:
            result.extend(process_table(table_lines, cite_map))
            table_lines = []

        # ── blank line ──
        if stripped == '':
            if in_list:
                result.extend(process_list_block(list_lines, list_type, cite_map))
                list_lines = []
                in_list = False
            i += 1
            continue

        # ── heading ──
        if stripped.startswith('#'):
            if in_list:
                result.extend(process_list_block(list_lines, list_type, cite_map))
                list_lines = []
                in_list = False
            result.append(convert_heading(stripped, cite_map))
            i += 1
            continue

        # ── horizontal rule ──
        if re.match(r'^[-*_]{3,}\s*$', stripped):
            i += 1
            continue

        # ── list item ──
        ul_match = re.match(r'^(\s*)[-*+]\s+', stripped)
        ol_match = re.match(r'^(\s*)\d+\.\s+', stripped)
        if ul_match or ol_match:
            typ = 'ul' if ul_match else 'ol'
            if not in_list:
                in_list = True
                list_type = typ
                list_lines = [stripped]
            elif typ == list_type:
                list_lines.append(stripped)
            else:
                result.extend(process_list_block(list_lines, list_type, cite_map))
                list_type = typ
                list_lines = [stripped]
            i += 1
            continue
        elif in_list:
            # Continuation line (indented)
            if stripped.startswith('  ') and list_lines:
                list_lines[-1] = list_lines[-1] + ' ' + stripped.strip()
                i += 1
                continue
            else:
                result.extend(process_list_block(list_lines, list_type, cite_map))
                list_lines = []
                in_list = False

        # ── regular paragraph ──
        result.append(convert_inline(stripped, cite_map))
        i += 1

    # Close any open blocks
    if quote_lines:
        result.append('\\begin{quote}')
        result.extend(quote_lines)
        result.append('\\end{quote}')
    if table_lines:
        result.extend(process_table(table_lines, cite_map))
    if in_list:
        result.extend(process_list_block(list_lines, list_type, cite_map))
    if in_code:
        result.append('\\begin{lstlisting}')
        result.extend(code_lines)
        result.append('\\end{lstlisting}')

    return '\n'.join(result)


def build_preamble():
    return r"""% !TEX root = trayguard_paper.tex
\documentclass[11pt,a4paper]{article}

% ── Packages ───────────────────────────────────────────────────────────
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{setspace}
\setstretch{1.15}
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue,
}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{verbatim}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{listings}
\lstset{basicstyle=\footnotesize\ttfamily,breaklines=true,columns=fullflexible}

\setcounter{tocdepth}{3}
\setcounter{secnumdepth}{3}

\title{TrayGuard\\A Local Tray Training And Assessment System}
\author{}
\date{}

\begin{document}

\maketitle
\tableofcontents
\newpage

"""


def build_postamble():
    return r"""

\bibliographystyle{plain}
\bibliography{trayguard_refs}

\end{document}
"""


# ── Bibliography conversion ────────────────────────────────────────────

def convert_bib(md_text):
    """Convert bibliography.md to BibTeX .bib format."""
    entries = []
    lines = md_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.search(r'<a\s+id="([^"]+)"', line)
        if m:
            key = m.group(1)
            title = ''
            j = i + 1
            while j < len(lines) and not title:
                t = lines[j].strip()
                if t.startswith('### '):
                    title = t[4:].strip()
                j += 1

            cite_lines = []
            while j < len(lines):
                l = lines[j].strip()
                if l.startswith('<a id=') or l.startswith('### '):
                    break
                if l:
                    cite_lines.append(l)
                j += 1

            cite_text = ' '.join(cite_lines)
            entry = _make_bib_entry(key, title, cite_text)
            if entry:
                entries.append(entry)
            i = j
            continue
        i += 1

    return '\n\n'.join(entries)


def _make_bib_entry(key, short_title, cite_text):
    """Build a BibTeX entry string from parsed components."""

    title = ''
    title_m = re.search(r'"([^"]+)"', cite_text)
    if title_m:
        title = title_m.group(1)

    journal = ''
    journal_m = re.search(r'\*([^*]+)\*', cite_text)
    if journal_m:
        journal = journal_m.group(1)

    url = ''
    url_m = re.search(r'(https?://[^\s,)\]]+)', cite_text)
    if url_m:
        url = url_m.group(1)

    typ = 'article' if journal else 'misc'

    # Author from short_title
    author_part = short_title.split(',')[0].strip() if ',' in short_title else short_title

    # Year: try short_title first, then cite_text
    year = ''
    ym = re.search(r'(\d{4})', short_title)
    if ym:
        year = ym.group(1)
    else:
        ym = re.search(r'(\d{4})', cite_text)
        if ym:
            year = ym.group(1)

    fields = [f'  author = {{{author_part}}},']
    if title:
        fields.append(f'  title = {{{title}}},')
    if journal:
        fields.append(f'  journal = {{{journal}}},')
    if year:
        fields.append(f'  year = {{{year}}},')
    if url:
        url = re.sub(r'[\)\]]+$', '', url)
        fields.append(f'  url = {{{url}}},')
    if not title:
        note = cite_text.replace('"', "'").replace('{', '(').replace('}', ')')
        fields.append(f'  note = {{{note}}},')

    return f'@{typ}{{{key},\n' + '\n'.join(fields) + '\n}'


# ── Main ────────────────────────────────────────────────────────────────

def main():
    md_path = os.path.join(DOCS_DIR, 'fdr_fdr.md')
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    bib_md_path = os.path.join(DOCS_DIR, 'bibliography.md')
    with open(bib_md_path, 'r', encoding='utf-8') as f:
        bib_text = f.read()

    # Remove the "# TrayGuard:" title line from markdown (we have it in preamble)
    md_text = re.sub(r'^# TrayGuard.*\n', '', md_text)

    print("Converting main document...")
    body = convert_document(md_text)
    tex_content = build_preamble() + body + build_postamble()

    tex_path = os.path.join(OUTPUT_DIR, 'trayguard_paper.tex')
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(tex_content)
    print(f"Written: {tex_path} ({os.path.getsize(tex_path)} bytes)")

    print("Converting bibliography...")
    bib_entries = convert_bib(bib_text)

    bib_path = os.path.join(OUTPUT_DIR, 'trayguard_refs.bib')
    with open(bib_path, 'w', encoding='utf-8') as f:
        f.write(bib_entries)
    print(f"Written: {bib_path} ({os.path.getsize(bib_path)} bytes)")

    print("\nDone. Compile with:")
    print("  cd latex_output && pdflatex trayguard_paper")
    print("  bibtex trayguard_paper")
    print("  pdflatex trayguard_paper")
    print("  pdflatex trayguard_paper")


if __name__ == '__main__':
    main()
