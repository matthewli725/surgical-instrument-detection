"""Convert fdr_presentation_plan.md -> fdr_presentation.tex (Beamer).

Usage:
    python scripts/md_to_beamer.py

Reads:  final_paper/source/fdr_presentation_plan.md
Writes: final_paper/source/fdr_presentation.tex (generated -- do not hand-edit)
"""

import re
import sys
from pathlib import Path

SRC_DIR = Path("final_paper/source")
MD_FILE = SRC_DIR / "fdr_presentation_plan.md"
TEX_FILE = SRC_DIR / "fdr_presentation.tex"

# ── Inline markdown -> LaTeX ─────────────────────────────────────────────

def inline_md_to_tex(text: str) -> str:
    """Convert inline markdown formatting to LaTeX."""
    # Escape special LaTeX characters first (before other conversions)
    text = text.replace("\\", "\\textbackslash{}")
    text = text.replace("$", "\\$")
    text = text.replace("%", "\\%")
    text = text.replace("&", "\\&")
    text = text.replace("#", "\\#")
    text = text.replace("_", "\\_")
    # Unicode replacements
    text = text.replace("✗", "")  # handled by item label in itemize-block
    text = text.replace("✓", "\\checkmark")
    text = text.replace("≥", "$\\ge$")
    # Citation keys (cite: key) -- handles single and multi-key (; separated)
    def _replace_cite(m):
        keys = m.group(1)
        cleaned = ",".join(k.strip() for k in keys.split(";"))
        return f"\\cite{{{cleaned}}}"
    text = re.sub(r"\(cite:\s*([a-zA-Z0-9_-]+(?:\s*;\s*[a-zA-Z0-9_-]+)*)\)", _replace_cite, text)
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    # Italic
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\\textit{\1}", text)
    return text


def block_md_to_tex(text: str) -> str:
    """Convert a multi-line block of markdown text to LaTeX block content."""
    lines = text.split("\n")
    result = []
    for line in lines:
        if re.match(r"^\d+\.\s+", line):
            item = re.sub(r"^\d+\.\s+", "", line)
            item = inline_md_to_tex(item)
            result.append(f"  \\item {item}")
        elif re.match(r"^[-*+]\s+", line):
            item = re.sub(r"^[-*+]\s+", "", line)
            item = inline_md_to_tex(item)
            result.append(f"  \\item {item}")
        elif line.strip() == "":
            result.append("")
        else:
            result.append(inline_md_to_tex(line))
    return "\n".join(result)


# ── Element types ───────────────────────────────────────────────────────

class Elem:
    TEXT = "text"
    BLOCKQUOTE = "quote"
    IMAGE = "image"
    TABLE = "table"
    LIST = "list"
    CODE = "code"
    HR = "hr"


# ── Parsing ─────────────────────────────────────────────────────────────

def parse_md(filepath: Path) -> dict:
    """Parse the markdown file into structured data."""
    text = filepath.read_text()
    lines = text.split("\n")

    data = {
        "title": "",
        "subtitle": "EC ENGR 180DW --- Final Design Review",
        "author": "Owen Fan, Matthew Li, Andy Ma, Jacob Moore, Qiyu Xin",
        "sections": [],
    }

    current_section = None
    current_slide = None
    in_visual = False
    in_script = False
    in_code_fence = False
    code_fence_lang = ""
    code_lines = []
    visual_lines = []
    script_lines = []

    def flush_slide():
        nonlocal visual_lines, script_lines, in_visual, in_script
        if current_slide is None:
            return
        # Only parse and store if we have accumulated content
        if visual_lines or script_lines:
            elements = parse_visual(visual_lines, current_slide.get("type"))
            current_slide["elements"] = elements
            notes = parse_script(script_lines)
            current_slide["notes"] = notes
        visual_lines = []
        script_lines = []
        in_visual = False
        in_script = False

    for line in lines:
        stripped = line.rstrip()

        # Code fence
        if stripped.startswith("```"):
            if not in_code_fence:
                in_code_fence = True
                code_fence_lang = stripped[3:].strip()
                code_lines = []
            else:
                in_code_fence = False
                if current_slide and in_visual:
                    visual_lines.append(f"__CODE_FENCE__ {code_fence_lang}")
                    for cl in code_lines:
                        visual_lines.append(cl)
                    visual_lines.append("__END_CODE_FENCE__")
                code_lines = []
            continue
        if in_code_fence:
            code_lines.append(stripped)
            continue

        # Skip appendix
        if stripped.startswith("## Appendix"):
            flush_slide()
            break

        # Title (H1)
        if stripped.startswith("# ") and not stripped.startswith("## ") and not stripped.startswith("### "):
            data["title"] = stripped[2:].strip()
            continue

        # Section header (H2) -- only "## Section N:" marks a real section
        if re.match(r"^## Section\s+\d+:", stripped):
            flush_slide()
            m = re.match(r"^## Section \d+: (.+?)(?: \((\d+ slides?.*?)\))?\s*(?:[—–-]+\s*(.+))?$", stripped)
            section_name = m.group(1).strip() if m else stripped[3:].strip()
            current_section = {"name": section_name, "speaker": "", "timing": "", "slides": []}
            data["sections"].append(current_section)
            continue

        # Slide header (H3)
        if stripped.startswith("### "):
            flush_slide()
            m = re.match(r"^### Slide (\d+)\s*[—–\-]\s*(.+)$", stripped)
            if m:
                slide_num = int(m.group(1))
                slide_title = m.group(2).strip()
            else:
                slide_num = 0
                slide_title = stripped[4:].strip()
            current_slide = {
                "num": slide_num,
                "title": slide_title,
                "type": None,
                "elements": [],
                "notes": "",
            }
            if current_section is not None:
                current_section["slides"].append(current_slide)
            in_visual = False
            in_script = False
            continue

        # Visual / Script markers
        if stripped.startswith("**Visual**"):
            flush_slide()
            type_m = re.search(r"\(type:\s*(\S+)\)", stripped)
            if type_m:
                current_slide["type"] = type_m.group(1)
            in_visual = True
            in_script = False
            rest = re.sub(r"\*\*Visual\*\*\s*:\s*", "", stripped)
            rest = re.sub(r"\s*\(type:\s*\S+\)", "", rest).strip()
            if rest:
                visual_lines.append(rest)
            continue

        if stripped.startswith("**Script**"):
            in_visual = False
            in_script = True
            if current_slide and not current_slide["type"]:
                type_m = re.search(r"\(type:\s*(\S+)\)", line)
                if type_m:
                    current_slide["type"] = type_m.group(1)
            continue

        # Collect visual / script content
        if in_visual:
            if current_slide and not current_slide["type"]:
                type_m = re.search(r"\(type:\s*(\S+)\)", stripped)
                if type_m:
                    current_slide["type"] = type_m.group(1)
                    line = re.sub(r"\s*\(type:\s*\S+\)", "", line).strip()
                    if not line:
                        continue
            visual_lines.append(line)

        if in_script:
            script_lines.append(line)

    flush_slide()
    return data


def parse_visual(lines: list[str], slide_type: str | None) -> list[dict]:
    """Parse raw visual block lines into structured elements."""
    elements = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        # Strip HTML comment markers (<!-- -->) for Google Docs compatibility
        stripped = re.sub(r"^\s*<!--\s*", "", stripped)
        stripped = re.sub(r"\s*-->\s*$", "", stripped)

        if not stripped.strip():
            i += 1
            continue

        # Code fence block
        if stripped.startswith("__CODE_FENCE__"):
            lang = stripped[len("__CODE_FENCE__"):].strip()
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("__END_CODE_FENCE__"):
                code.append(lines[i])
                i += 1
            i += 1  # skip end marker
            elements.append({"kind": Elem.CODE, "content": "\n".join(code), "language": lang})
            continue

        if stripped.startswith("__END_CODE_FENCE__"):
            i += 1
            continue

        # Horizontal rule
        if stripped.startswith("---") and len(stripped) >= 3:
            i += 1
            continue

        # Image ![alt](path) -- extract all from line
        img_matches = list(re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", stripped))
        if img_matches:
            remaining = stripped
            for m in img_matches:
                alt, path = m.group(1), m.group(2)
                width = None
                if "|" in alt:
                #   parts = alt.split("|", 1)
                #   alt = parts[0].strip()
                #   w = parts[1].strip()
                #   if w == "full":
                #       width = "full"
                #   else:
                #       width = float(w)
                    pass
                elements.append({"kind": Elem.IMAGE, "alt": alt, "path": path, "width": width})
                remaining = remaining.replace(m.group(0), "", 1)
            stripped = remaining.strip()
            if not stripped:
                i += 1
                continue

        # Blockquote
        if stripped.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                qline = re.sub(r"^>\s?", "", lines[i])
                quote_lines.append(qline)
                i += 1
            content = "\n".join(quote_lines).strip()
            if content:
                elements.append({"kind": Elem.BLOCKQUOTE, "content": content})
            continue

        # Table row
        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].rstrip())
                i += 1
            elements.append({"kind": Elem.TABLE, "rows": table_lines})
            continue

        # Markdown separator row (|---|) -- already skipped by table above, but catch leftovers
        if re.match(r"^[-| :+]+\s*$", stripped) and "|" in stripped:
            i += 1
            continue

        # Bullet / numbered list
        if re.match(r"^[-*+]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
            list_lines = []
            is_numbered = bool(re.match(r"^\d+\.\s+", stripped))
            while i < len(lines):
                ls = lines[i].rstrip()
                if not ls.strip():
                    i += 1
                    continue
                if ls.startswith("---"):
                    break
                if ls.startswith("|"):
                    break
                if ls.startswith("**") and ":" in ls:
                    break
                if re.match(r"^[-*+]\s+", ls) or re.match(r"^\d+\.\s+", ls):
                    list_lines.append(ls)
                    i += 1
                else:
                    break
            if list_lines:
                elements.append({"kind": Elem.LIST, "items": list_lines, "numbered": is_numbered})
            continue

        # Plain text -- skip (descriptive prose)
        i += 1

    return elements


def parse_script(lines: list[str]) -> str:
    """Parse script block into LaTeX note text."""
    parts = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Skip markers and separators
        if stripped.startswith("---"):
            continue
        if stripped.startswith("**"):
            continue
        if stripped.startswith(">"):
            q = re.sub(r"^>\s?", "", stripped)
            parts.append(q)
        elif stripped.startswith("_"):
            # Duration suffix like _(45 sec)_
            continue
        else:
            parts.append(stripped)
    return "\n".join(parts).strip()


# ── Beamer generation ──────────────────────────────────────────────────

BEAMER_PREAMBLE = r"""% !TEX program = pdflatex
% This file is GENERATED from fdr_presentation_plan.md -- do not hand-edit.
\documentclass[10pt,aspectratio=169]{beamer}

% -- Theme ---------------------------------------------------------------
\usetheme{Madrid}
\usecolortheme{default}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}[frame number]

% Second-screen speaker notes (uncomment for presenting):
% \setbeameroption{show notes on second screen}

% -- Packages ------------------------------------------------------------
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{listings}
\lstset{basicstyle=\footnotesize\ttfamily,breaklines=true}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes}
\usepackage{hyperref}
\usepackage[numbers]{natbib}
\bibliographystyle{IEEEtran}
\usepackage{pifont}
\usepackage{amssymb}

% -- Convenience macros --------------------------------------------------
\newcommand{\sectiondivider}[1]{%
  \begin{frame}[plain]
    \centering\vfill
    {\Huge\color{blue!60!black}#1}\par
    \vfill
  \end{frame}
}
\newcommand{\greencheck}{\textcolor{green!60!black}{\checkmark}}
\newcommand{\redcross}{\textcolor{red}{\ding{55}}}

\newcommand{\incfig}[2][0.8\textwidth]{%
  \IfFileExists{#2}{%
    \includegraphics[width=#1]{#2}%
  }{%
    \fbox{\makebox[#1][c]{\shortstack{\small FIGURE TBD\\\tiny\detokenize{#2}}}}%
  }%
}
\newcommand{\incfigw}[2][\textwidth]{\incfig[#1]{#2}}
"""


def generate_beamer(data: dict) -> str:
    """Generate full .tex content from parsed data."""
    out = []
    out.append(BEAMER_PREAMBLE)
    out.append("")

    title = inline_md_to_tex(data["title"])
    out.append(f"\\title{{{title}}}")
    out.append(f"\\subtitle{{{data['subtitle']}}}")
    out.append(f"\\author{{{data['author']}}}")
    out.append("\\date{\\today}")
    out.append("")
    out.append("\\begin{document}")
    out.append("")

    # Title slide
    first_notes = _get_first_slide_notes(data)
    out.append("% -- Title slide -------------------------------------------------")
    out.append("\\begin{frame}")
    out.append("  \\titlepage")
    if first_notes:
        note_text = inline_md_to_tex(first_notes)
        out.append(f"  \\note{{{note_text}}}")
    out.append("\\end{frame}")
    out.append("")

    # Outline
    out.append("% -- Outline ----------------------------------------------------")
    out.append("\\begin{frame}{Roadmap}")
    out.append("  \\tableofcontents")
    out.append("\\end{frame}")
    out.append("")

    # Sections
    for sec_idx, section in enumerate(data["sections"]):
        section_name = section["name"]
        # Use clean name for \section{} (no timing/speaker suffix)
        clean_name = re.sub(r"\s*\(.*?\)\s*", "", section_name).strip()
        # Remove speaker attribution after em-dash or long dash
        clean_name = re.sub(r"\s*[—–-]+\s*[^—–-]*$", "", clean_name).strip()
        if not clean_name:
            clean_name = section_name

        out.append(f"% {'=' * 70}")
        out.append(f"%  SECTION {sec_idx + 1}: {clean_name}")
        out.append(f"% {'=' * 70}")
        out.append(f"\\section{{{clean_name}}}")
        out.append(f"\\sectiondivider{{{section_name}}}")
        out.append("")

        for slide in section["slides"]:
            out.extend(generate_slide(slide))

    # References
    out.append("% -- References -------------------------------------------------")
    out.append("\\begin{frame}[allowframebreaks]{References}")
    out.append("  \\bibliography{trayguard_refs}")
    out.append("\\end{frame}")
    out.append("")

    out.append("\\end{document}")
    out.append("")
    return "\n".join(out)


def _get_first_slide_notes(data: dict) -> str:
    for sec in data.get("sections", []):
        for slide in sec.get("slides", []):
            if slide["notes"]:
                return slide["notes"]
    return ""


# ── Slide generation ───────────────────────────────────────────────────

def generate_slide(slide: dict) -> list[str]:
    """Generate Beamer code for a single content slide."""
    out = []
    slide_type = slide.get("type", "")
    title = inline_md_to_tex(slide["title"])
    elements = slide.get("elements", [])
    notes = slide.get("notes", "")

    # Slide 1 is the title slide -- already handled
    if slide["num"] == 1:
        return out

    out.append(f"% {'─' * 55}")
    out.append(f"% Slide {slide['num']}: {slide['title']}")
    out.append(f"% {'─' * 55}")
    frame_opts = ""
    if slide_type == "code-bullets":
        frame_opts = "[fragile]"
    out.append(f"\\begin{{frame}}{frame_opts}{{{title}}}")

    if slide_type:
        safe = slide_type.replace("-", "_").replace("+", "_")
        handler_name = f"_type_{safe}"
        handler = globals().get(handler_name)
        if handler:
            content = handler(elements)
            out.append(content)
        else:
            out.append(f"  % Unknown type: {slide_type}, rendering generically")
            out.append(_render_generic(elements))
    else:
        out.append(_render_generic(elements))

    if notes:
        note_text = inline_md_to_tex(notes)
        out.append(f"  \\note{{{note_text}}}")

    out.append("\\end{frame}")
    out.append("")
    return out


def _render_generic(elements: list[dict]) -> str:
    """Fallback renderer for unknown slide types."""
    out = []
    for el in elements:
        kind = el["kind"]
        if kind == Elem.BLOCKQUOTE:
            content = block_md_to_tex(el["content"])
            out.append(f"  \\begin{{block}}{{\\centering}}")
            for line in content.split("\n"):
                out.append(f"    {line}")
            out.append(f"  \\end{{block}}")
        elif kind == Elem.IMAGE:
            out.append(f"  \\centering")
            out.append(f"  \\incfigw{{{el['path']}}}")
        elif kind == Elem.TABLE:
            out.append(f"  \\centering")
            out.append(f"  \\small")
            out.append(f"  {_markdown_table_to_latex(el['rows'])}")
        elif kind == Elem.LIST:
            env = "enumerate" if el.get("numbered") else "itemize"
            out.append(f"  \\begin{{{env}}}")
            for item in el["items"]:
                text = re.sub(r"^[-*+]\s+|^\d+\.\s+", "", item)
                text = inline_md_to_tex(text)
                out.append(f"    \\item {text}")
            out.append(f"  \\end{{{env}}}")
        elif kind == Elem.CODE:
            out.append(f"  \\begin{{lstlisting}}")
            out.append(f"    {el['content']}")
            out.append(f"  \\end{{lstlisting}}")
    return "\n".join(out)


# ── Type handlers -------------------------------------------------------

def _type_three_callout(elements: list[dict]) -> str:
    """Three callout blocks side by side, last block becomes alert below."""
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    out.append("  \\begin{columns}[T]")
    for q in quotes[:3]:
        content = block_md_to_tex(q["content"])
        out.append("    \\column{0.32\\textwidth}")
        out.append("    \\begin{block}{\\centering\\small}")
        for line in content.split("\n"):
            out.append(f"      {line}")
        out.append("    \\end{block}")
    out.append("  \\end{columns}")
    if len(quotes) > 3:
        out.append("  \\vspace{0.5cm}")
        alert_text = block_md_to_tex(quotes[-1]["content"])
        out.append("  \\begin{alertblock}{}")
        out.append("    \\centering")
        out.append(f"    {alert_text}")
        out.append("  \\end{alertblock}")
    return "\n".join(out)


def _type_image_bullets(elements: list[dict]) -> str:
    """Image left, bullet list right."""
    images = [el for el in elements if el["kind"] == Elem.IMAGE]
    lists = [el for el in elements if el["kind"] == Elem.LIST]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    out.append("  \\begin{columns}[T]")
    if images:
        out.append("    \\column{0.48\\textwidth}")
        out.append("    \\centering")
        out.append(f"    \\incfig[0.7\\textheight]{{{images[0]['path']}}}")
    if lists:
        out.append("    \\column{0.48\\textwidth}")
        out.append("    \\begin{itemize}")
        for item in lists[0]["items"]:
            text = re.sub(r"^[-*+]\s+", "", item)
            text = inline_md_to_tex(text)
            out.append(f"      \\item {text}")
        out.append("    \\end{itemize}")
    out.append("  \\end{columns}")
    for q in quotes:
        content = block_md_to_tex(q["content"])
        out.append("  \\begin{block}{}")
        out.append("    \\centering")
        out.append(f"    {content}")
        out.append("  \\end{block}")
    return "\n".join(out)


def _type_image_and_columns(elements: list[dict]) -> str:
    """Image full width, then columns below."""
    images = [el for el in elements if el["kind"] == Elem.IMAGE]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    if images:
        out.append("  \\centering")
        out.append(f"  \\incfigw{{{images[0]['path']}}}")
    if quotes:
        out.append("  \\vspace{0.3cm}")
        content = quotes[0]["content"]
        lines = content.split("\n")
        header = None
        items = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Detect bold header like **Three structural drivers:**
            if re.match(r"^\*\*.+\*\*:?", line):
                header = re.sub(r"^\*\*(.+)\*\*:?", r"\1", line)
            elif re.match(r"^\d+\.\s+", line):
                items.append(line)
        if header and items:
            n = len(items)
            cw = "0.32" if n >= 3 else ("0.48" if n == 2 else "0.8")
            out.append("  \\begin{columns}[T]")
            for i, item in enumerate(items):
                item_text = re.sub(r"^\d+\.\s+", "", item)
                item_text = inline_md_to_tex(item_text)
                out.append(f"    \\column{{{cw}\\textwidth}}")
                if i == 0:
                    out.append(f"    \\textbf{{{header}}}")
                out.append("    \\begin{enumerate}")
                if i > 0:
                    out.append(f"      \\setcounter{{enumi}}{{{i}}}")
                out.append(f"      \\item {item_text}")
                out.append("    \\end{enumerate}")
            out.append("  \\end{columns}")
        else:
            out.append("  \\begin{block}{}")
            out.append(f"    {inline_md_to_tex(content)}")
            out.append("  \\end{block}")
    return "\n".join(out)


def _type_image_and_quote(elements: list[dict]) -> str:
    """Image full width, then a quote block below."""
    images = [el for el in elements if el["kind"] == Elem.IMAGE]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    if images:
        out.append("  \\centering")
        out.append(f"  \\incfigw{{{images[0]['path']}}}")
    if quotes:
        out.append("  \\vspace{0.3cm}")
        out.append("  \\begin{quote}")
        out.append("    \\small")
        for line in quotes[0]["content"].split("\n"):
            line = inline_md_to_tex(line)
            if line.strip():
                out.append(f"    {line}")
        out.append("  \\end{quote}")
    return "\n".join(out)


def _type_table(elements: list[dict]) -> str:
    """Full-width table, optional trailing blockquote."""
    tables = [el for el in elements if el["kind"] == Elem.TABLE]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    if tables:
        out.append("  \\centering")
        out.append("  \\small")
        out.append(f"  {_markdown_table_to_latex(tables[0]['rows'])}")
    if quotes:
        out.append("  \\vspace{0.3cm}")
        content = block_md_to_tex(quotes[0]["content"])
        out.append("  \\begin{block}{}")
        out.append("    \\centering")
        out.append(f"    {content}")
        out.append("  \\end{block}")
    return "\n".join(out)


_type_table_block = _type_table


def _type_two_column_block(elements: list[dict]) -> str:
    """Two side-by-side blocks (exampleblock / alertblock)."""
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    out.append("  \\begin{columns}[T]")

    for idx, q in enumerate(quotes[:2]):
        content = q["content"]
        lines = content.split("\n")
        title = lines[0].strip() if lines else ""
        items = [l for l in lines[1:] if re.match(r"^[-*+]\s+", l.strip())]
        blocktype = "exampleblock" if idx == 0 else "alertblock"
        out.append(f"    \\column{{0.48\\textwidth}}")
        out.append(f"    \\begin{{{blocktype}}}{{\\centering {inline_md_to_tex(title)}}}")
        if items:
            out.append("      \\begin{itemize}")
            for item in items:
                text = re.sub(r"^[-*+]\s+", "", item.strip())
                text = inline_md_to_tex(text)
                out.append(f"        \\item {text}")
            out.append("      \\end{itemize}")
        out.append(f"    \\end{{{blocktype}}}")

    out.append("  \\end{columns}")

    if len(quotes) > 2:
        for q in quotes[2:]:
            content = block_md_to_tex(q["content"])
            out.append("  \\begin{block}{}")
            out.append("    \\centering")
            out.append(f"    {content}")
            out.append("  \\end{block}")
    return "\n".join(out)


def _type_image_only(elements: list[dict]) -> str:
    """Full-width image."""
    images = [el for el in elements if el["kind"] == Elem.IMAGE]
    out = []
    if images:
        out.append("  \\centering")
        out.append(f"  \\includegraphics[width=0.8\\textwidth]{{{images[0]['path']}}}")
    return "\n".join(out)


def _type_two_image(elements: list[dict]) -> str:
    """Two images side by side, optional third image + table below."""
    imgs = [el for el in elements if el["kind"] == Elem.IMAGE]
    tables = [el for el in elements if el["kind"] == Elem.TABLE]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    if len(imgs) >= 2:
        out.append("  \\begin{columns}[T]")
        for i in range(2):
            out.append("    \\column{0.48\\textwidth}")
            out.append("    \\centering")
            if imgs[i].get("alt"):
                out.append(f"    \\textbf{{{imgs[i]['alt']}}}\\\\")
            out.append(f"    \\incfig[\\textwidth]{{{imgs[i]['path']}}}")
        out.append("  \\end{columns}")
    if len(imgs) >= 3:
        out.append("  \\vspace{0.2cm}")
        out.append("  \\centering")
        if imgs[2].get("alt"):
            out.append(f"  \\tiny {imgs[2]['alt']}\\\\")
        out.append(f"  \\incfig[0.6\\textwidth]{{{imgs[2]['path']}}}")
    if tables:
        out.append("  \\vspace{0.2cm}")
        out.append("  \\centering")
        out.append("  \\small")
        out.append(f"  {_markdown_table_to_latex(tables[0]['rows'])}")
    if quotes:
        out.append("  \\vspace{0.3cm}")
        out.append("  \\begin{block}{}")
        out.append("    \\centering")
        out.append(f"    {inline_md_to_tex(quotes[0]['content'])}")
        out.append("  \\end{block}")
    return "\n".join(out)


_type_two_image_table = _type_two_image


def _type_itemize_block(elements: list[dict]) -> str:
    """Itemize list inside block + optional exampleblock below."""
    lists = [el for el in elements if el["kind"] == Elem.LIST]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    if lists:
        out.append("  \\begin{block}{\\centering What a deployment-grade CV system still needs}")
        out.append("    \\begin{itemize}")
        for item in lists[0]["items"]:
            text = re.sub(r"^[-*+]\s+", "", item)
            text = inline_md_to_tex(text)
            out.append(f"      \\item[\\textcolor{{red}}{{\\ding{{55}}}}] {text}")
        out.append("    \\end{itemize}")
        out.append("  \\end{block}")
    if quotes:
        out.append("  \\vspace{0.3cm}")
        content = block_md_to_tex(quotes[0]["content"])
        out.append("  \\begin{exampleblock}{}")
        out.append("    \\centering")
        out.append(f"    {content}")
        out.append("  \\end{exampleblock}")
    return "\n".join(out)


def _type_image_block(elements: list[dict]) -> str:
    """Image + block below."""
    imgs = [el for el in elements if el["kind"] == Elem.IMAGE]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    if imgs:
        out.append("  \\centering")
        out.append(f"  \\incfigw{{{imgs[0]['path']}}}")
    if quotes:
        out.append("  \\vspace{0.3cm}")
        content = block_md_to_tex(quotes[0]["content"])
        out.append("  \\begin{block}{}")
        out.append("    \\centering")
        out.append(f"    {content}")
        out.append("  \\end{block}")
    return "\n".join(out)


_type_image_and_block = _type_image_block
_type_image_plus_block = _type_image_block


def _type_code_bullets(elements: list[dict]) -> str:
    """Code listing left, bullet list right."""
    code = [el for el in elements if el["kind"] == Elem.CODE]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    lists = [el for el in elements if el["kind"] == Elem.LIST]
    out = []
    out.append("  \\begin{columns}[T]")
    out.append("    \\column{0.55\\textwidth}")
    out.append("    \\begin{lstlisting}")
    if code:
        out.append(code[0]["content"])
    elif quotes:
        out.append(quotes[0]["content"])
    out.append("    \\end{lstlisting}")
    out.append("    \\column{0.42\\textwidth}")
    if lists:
        out.append("    \\begin{itemize}")
        for item in lists[0]["items"]:
            text = re.sub(r"^[-*+]\s+", "", item)
            text = inline_md_to_tex(text)
            out.append(f"      \\item {text}")
        out.append("    \\end{itemize}")
    else:
        out.append("    \\begin{itemize}")
        for q in quotes[1:]:
            content = block_md_to_tex(q["content"])
            for line in content.split("\n"):
                line = line.strip()
                if line:
                    out.append(f"      \\item {line}")
        out.append("    \\end{itemize}")
    out.append("  \\end{columns}")
    return "\n".join(out)


def _type_centered_text(elements: list[dict]) -> str:
    """Centered large text with optional block below."""
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    out.append("  \\begin{center}")
    out.append("    \\vfill")
    out.append("    \\Large")
    if quotes:
        content = block_md_to_tex(quotes[0]["content"])
        for line in content.split("\n"):
            l = line.strip()
            if l:
                out.append(f"    {l}\\\\")
    out.append("    \\vfill")
    out.append("  \\end{center}")
    if len(quotes) > 1:
        out.append("  \\begin{exampleblock}{}")
        out.append("    \\centering")
        content = block_md_to_tex(quotes[1]["content"])
        out.append(f"    {content}")
        out.append("  \\end{exampleblock}")
    return "\n".join(out)


def _type_image_plus_columns_block(elements: list[dict]) -> str:
    """Image + columns + alertblock (for retention slide)."""
    imgs = [el for el in elements if el["kind"] == Elem.IMAGE]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    lists = [el for el in elements if el["kind"] == Elem.LIST]
    out = []
    if imgs:
        out.append("  \\centering")
        out.append(f"  \\incfigw{{{imgs[0]['path']}}}")
    if lists:
        out.append("  \\vspace{0.3cm}")
        out.append("  \\begin{columns}[T]")
        n = len(lists[0]["items"])
        cw = "0.32" if n >= 3 else "0.48"
        for item in lists[0]["items"]:
            text = re.sub(r"^[-*+]\s+", "", item)
            text = inline_md_to_tex(text)
            out.append(f"    \\column{{{cw}\\textwidth}}")
            out.append(f"    {text}")
        out.append("  \\end{columns}")
    if quotes:
        out.append("  \\vspace{0.2cm}")
        content = block_md_to_tex(quotes[-1]["content"])
        out.append("  \\begin{alertblock}{}")
        out.append(f"    {content}")
        out.append("  \\end{alertblock}")
    return "\n".join(out)


def _type_table_itemize(elements: list[dict]) -> str:
    """Table + itemize below."""
    tables = [el for el in elements if el["kind"] == Elem.TABLE]
    lists = [el for el in elements if el["kind"] == Elem.LIST]
    out = []
    if tables:
        out.append("  \\centering")
        out.append("  \\small")
        out.append(f"  {_markdown_table_to_latex(tables[0]['rows'])}")
    if lists:
        out.append("  \\vspace{0.3cm}")
        out.append("  \\begin{itemize}")
        for item in lists[0]["items"]:
            text = re.sub(r"^[-*+]\s+", "", item)
            text = inline_md_to_tex(text)
            out.append(f"    \\item {text}")
        out.append("  \\end{itemize}")
    return "\n".join(out)


def _type_image_blocks(elements: list[dict]) -> str:
    """Image + two side-by-side blocks (for confidence slide)."""
    imgs = [el for el in elements if el["kind"] == Elem.IMAGE]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    if imgs:
        out.append("  \\centering")
        out.append(f"  \\incfigw{{{imgs[0]['path']}}}")
    if len(quotes) >= 2:
        out.append("  \\vspace{0.3cm}")
        out.append("  \\begin{columns}[T]")
        out.append("    \\column{0.48\\textwidth}")
        content = block_md_to_tex(quotes[0]["content"])
        out.append("    \\begin{alertblock}{\\centering High-confidence error}")
        for line in content.split("\n"):
            l = line.strip()
            if l:
                out.append(f"      {l}")
        out.append("    \\end{alertblock}")
        out.append("    \\column{0.48\\textwidth}")
        content = block_md_to_tex(quotes[1]["content"])
        out.append("    \\begin{exampleblock}{\\centering Low-confidence correct}")
        for line in content.split("\n"):
            l = line.strip()
            if l:
                out.append(f"      {l}")
        out.append("    \\end{exampleblock}")
        out.append("  \\end{columns}")
    return "\n".join(out)


def _type_itemize_plus_block(elements: list[dict]) -> str:
    """Itemize + block below (for expert review slide)."""
    lists = [el for el in elements if el["kind"] == Elem.LIST]
    quotes = [el for el in elements if el["kind"] == Elem.BLOCKQUOTE]
    out = []
    if lists:
        out.append("  \\begin{itemize}")
        for item in lists[0]["items"]:
            text = re.sub(r"^[-*+]\s+", "", item)
            text = inline_md_to_tex(text)
            out.append(f"    \\item[\\textbf{{Q}}] {text}")
        out.append("  \\end{itemize}")
    if quotes:
        out.append("  \\vspace{0.3cm}")
        content = block_md_to_tex(quotes[0]["content"])
        out.append("  \\begin{block}{}")
        out.append("    \\centering")
        out.append(f"    {content}")
        out.append("  \\end{block}")
    return "\n".join(out)


# ── Markdown table -> LaTeX ────────────────────────────────────────────

def _markdown_table_to_latex(rows: list[str]) -> str:
    if not rows:
        return ""
    header = _parse_table_row(rows[0])
    if len(rows) < 2:
        return ""
    alignment = _parse_alignment(rows[1], len(header))
    n_cols = len(header)
    col_spec = "".join(alignment)
    out = []
    out.append(f"\\begin{{tabular}}{{{col_spec}}}")
    out.append("    \\toprule")
    out.append("    " + " & ".join(inline_md_to_tex(h) for h in header) + " \\\\")
    out.append("    \\midrule")
    for row in rows[2:]:
        cells = _parse_table_row(row)
        if len(cells) != n_cols:
            continue
        tex_cells = [inline_md_to_tex(c) for c in cells]
        out.append("    " + " & ".join(tex_cells) + " \\\\")
    out.append("    \\bottomrule")
    out.append("\\end{tabular}")
    return "\n".join(out)


def _parse_table_row(row: str) -> list[str]:
    row = row.strip()
    if not row.startswith("|"):
        return [row]
    row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    cells = []
    current = ""
    for ch in row:
        if ch == "|":
            cells.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        cells.append(current.strip())
    return cells


def _parse_alignment(row: str, n_cols: int) -> list[str]:
    cells = _parse_table_row(row)
    alignments = []
    for i in range(n_cols):
        if i < len(cells):
            cell = cells[i].strip()
            has_left = cell.startswith(":")
            has_right = cell.endswith(":")
            if has_left and has_right:
                alignments.append("c")
            elif has_right:
                alignments.append("r")
            elif has_left:
                alignments.append("l")
            else:
                alignments.append("c")
        else:
            alignments.append("c")
    return alignments


# ── Main ────────────────────────────────────────────────────────────────

def main():
    print(f"Reading: {MD_FILE}")
    data = parse_md(MD_FILE)
    print(f"  Title: {data['title']}")
    print(f"  Sections: {len(data['sections'])}")
    total = sum(len(s["slides"]) for s in data["sections"])
    print(f"  Slides: {total}")

    for sec in data["sections"]:
        for sl in sec["slides"]:
            els = ", ".join(f"{e['kind']}" for e in sl.get("elements", []))
            print(f"    Slide {sl['num']}: type={sl['type']}, elements=[{els}]")

    tex = generate_beamer(data)
    TEX_FILE.write_text(tex)
    print(f"Written: {TEX_FILE} ({len(tex)} chars)")


if __name__ == "__main__":
    main()
