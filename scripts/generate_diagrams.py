"""Generate all 7 draw.io diagrams for the FDR presentation."""
from __future__ import annotations

import uuid
import xml.etree.ElementTree as ET


# ── draw.io XML helpers ──────────────────────────────────────────────────

def _uid() -> str:
    return uuid.uuid4().hex[:12]


class Diagram:
    """Container for a single draw.io diagram page."""

    def __init__(self, name: str, w: int = 800, h: int = 600):
        self.name = name
        self.w = w
        self.h = h
        self.cells: list[ET.Element] = []
        self._connectors: list[tuple[str, str, dict]] = []  # src, dst, style_overrides

    def vertex(self, x: float, y: float, w: float, h: float,
               label: str, style: str, **attrs) -> str:
        cid = _uid()
        el = ET.SubElement(self._root(), "mxCell", id=cid)
        el.set("value", label)
        el.set("style", style)
        el.set("vertex", "1")
        el.set("parent", "1")
        for k, v in attrs.items():
            el.set(k, v)
        geo = ET.SubElement(el, "mxGeometry")
        geo.set("x", str(x))
        geo.set("y", str(y))
        geo.set("width", str(w))
        geo.set("height", str(h))
        geo.set("as", "geometry")
        self.cells.append(el)
        return cid

    def _root(self) -> ET.Element:
        for c in self.cells:
            if c.tag == "root":
                return c
        r = ET.Element("root")
        ET.SubElement(r, "mxCell", id="0")
        ET.SubElement(r, "mxCell", id="1", parent="0")
        self.cells.insert(0, r)
        return r

    def __iadd__(self, other: ET.Element):
        self.cells.append(other)
        return self

    def arrow(self, src: str, dst: str, style: str | None = None,
              **geo_attrs):
        """Add an edge between two cell IDs."""
        eid = _uid()
        el = ET.SubElement(self._root(), "mxCell", id=eid)
        el.set("style", style or "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;")
        el.set("edge", "1")
        el.set("parent", "1")
        el.set("source", src)
        el.set("target", dst)
        geo = ET.SubElement(el, "mxGeometry")
        geo.set("relative", "1")
        geo.set("as", "geometry")
        for k, v in geo_attrs.items():
            geo.set(k, str(v))
        self.cells.append(el)
        return eid

    def label(self, x: float, y: float, w: float, h: float,
              text: str, style: str = "text;html=1;align=center;verticalAlign=middle;") -> str:
        return self.vertex(x, y, w, h, text, style)

    def save(self, path: str):
        """Write as uncompressed .drawio (plain XML)."""
        mxfile = ET.Element("mxfile")
        mxfile.set("host", "Electron")
        mxfile.set("agent", "TrayGuard")
        diag_el = ET.SubElement(mxfile, "diagram", id=_uid(), name=self.name)

        model = ET.SubElement(diag_el, "mxGraphModel")
        model.set("dx", "0")
        model.set("dy", "0")
        model.set("grid", "1")
        model.set("gridSize", "10")
        model.set("guides", "1")
        model.set("tooltips", "1")
        model.set("connect", "1")
        model.set("arrows", "1")
        model.set("fold", "1")
        model.set("page", "1")
        model.set("pageScale", "1")
        model.set("pageWidth", str(self.w))
        model.set("pageHeight", str(self.h))
        model.set("math", "0")
        model.set("shadow", "0")

        # root already has all cells as children (added via SubElement)
        model.append(self._root())

        tree = ET.ElementTree(mxfile)
        ET.indent(tree, space="  ")
        tree.write(path, xml_declaration=True, encoding="utf-8")


# ── Colour palette ──────────────────────────────────────────────────────
BLUE   = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
GREEN  = "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
ORANGE = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;"
RED_BG = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
PURPLE = "rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;"
GREY   = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;"
YELLOW = "rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
WHITE  = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;"

ARROW_STYLE = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"


# ── Diagram 1: Fishbone RCA (Slide 4) ──────────────────────────────────
def fishbone() -> Diagram:
    d = Diagram("Fishbone RCA", w=900, h=550)

    # spine
    spine = d.vertex(100, 250, 700, 4, "", "line;strokeWidth=2;fillColor=none;")
    # effect head (right arrow)
    head = d.vertex(780, 230, 120, 50,
                    "Tray content errors\nduring reconstruction",
                    WHITE + "gradientDirection=none;")

    # — 6 branches —
    y_bases = [50, 110, 170, 330, 390, 460]
    labels = [
        "Product\nLookalike instruments,\nno markings, wear hides\ndifferences",
        "Knowledge\nNo recurring competency\ncheck, general names\n≠ local rules",
        "Process\nSingle-pass assembly,\nno backup check",
        "Information\nOutdated count sheets,\nmissing photos,\nlocal aliases",
        "Environment\nProduction pressure,\ninterruptions,\nergonomic friction",
        "Policy / Feedback\nNo standard owner,\nslow manual error\nreporting",
    ]
    for i, (y, lab) in enumerate(zip(y_bases, labels)):
        box = d.vertex(120 if i < 3 else 480, y, 110, 55 if i < 3 else 55,
                       lab, BLUE if i < 3 else PURPLE)
        # diagonal connector to spine
        mid_x = 170 if i < 3 else 530
        mid_y = y + 28
        spine_contact = (250, 252) if i < 3 else (600, 252)
        extra = {}
        conn_id = _uid()
        conn_el = ET.SubElement(d._root(), "mxCell", id=conn_id)
        conn_el.set("style", "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;")
        conn_el.set("edge", "1")
        conn_el.set("parent", "1")
        # We'll draw freeform lines using geometry points
        ET.SubElement(conn_el, "mxGeometry", relative="1", **{"as": "geometry"})
        pts = ET.SubElement(conn_el, "Array", **{"as": "points"})
        if i < 3:
            # downward diagonal
            ET.SubElement(pts, "mxPoint", x=str(mid_x), y=str(spine_contact[1]))
        else:
            # upward diagonal
            ET.SubElement(pts, "mxPoint", x=str(mid_x), y=str(spine_contact[1]))
        d.cells.append(conn_el)

    # —— structural drivers callout ——
    d.vertex(140, 15, 620, 30,
             "Three structural drivers: (1) SPD evolved from materials management → no licensure  |  "
             "(2) Cost-center accounting → error costs invisible  |  "
             "(3) No information loop → errors repeat",
             "text;html=1;align=center;verticalAlign=middle;fontSize=11;fontStyle=1;whiteSpace=wrap;")

    return d


# ── Diagram 2: Broken feedback loop (Slide 5) ──────────────────────────
def feedback_loop() -> Diagram:
    d = Diagram("Feedback Loop", w=800, h=300)

    # Step boxes
    labels = [
        "OR finds error\n(missing instrument)",
        "Paper incident\nreport (slow)",
        "Received by SPD\nweeks later",
        "No tie to specific\ntray/shift/training gap",
        "Same error\nrepeats",
    ]
    xs = [40, 200, 360, 520, 680]
    colors = [RED_BG, ORANGE, ORANGE, RED_BG, RED_BG]
    ids = []
    for x, lab, col in zip(xs, labels, colors):
        ids.append(d.vertex(x, 100, 120, 60, lab, col))

    # Arrows between boxes
    for i in range(len(ids)-1):
        d.arrow(ids[i], ids[i+1])

    # Quote below
    d.label(100, 230, 600, 30,
            "\"Error reporting is cumbersome, human-dependent, delayed, and incomplete.\" — Nichol et al.",
            "text;html=1;align=center;verticalAlign=middle;fontSize=11;fontStyle=2;")

    return d


# ── Diagram 3: CV + training complementary (Slide 13) ──────────────────
def complementary() -> Diagram:
    d = Diagram("CV and Training Complementary", w=700, h=350)

    # Center: module
    module = d.vertex(280, 120, 140, 60, "Local Tray\nModule", ORANGE + "fontStyle=1;")

    # Left path: training
    train_boxes = ["Pre-test", "Study cards", "Quiz", "Practice sort", "Post-test", "Export"]
    train_ids = []
    lx = 20
    for b in train_boxes:
        train_ids.append(d.vertex(lx, 40, 90, 36, b, BLUE, fontSize="10"))
        lx += 100

    # Right path: future CV
    cv_ids = []
    cv_items = ["Needs same data", "Names, aliases,", "lookalike pairs,", "counts, variants..."]
    cy = 202
    cv_ids.append(d.vertex(470, cy, 120, 40, cv_items[0], GREEN, fontSize="10"))
    cv_ids.append(d.vertex(470, cy+46, 120, 36, cv_items[1]+"\n"+cv_items[2]+"\n"+cv_items[3], GREEN, fontSize="9"))

    # Curved arrows from module to left and right
    a1 = d.arrow(module, train_ids[0], entryX="1", entryY="0.5")
    a2 = d.arrow(module, cv_ids[0], entryX="0", entryY="0.5")

    # Label above
    d.label(200, 5, 300, 25,
            "The module is the durable artifact. Training proves it. CV consumes it.",
            "text;html=1;align=center;verticalAlign=middle;fontSize=12;fontStyle=1;")

    return d


# ── Diagram 4: 7-step learning loop (Slide 18) ─────────────────────────
def learning_loop() -> Diagram:
    d = Diagram("Learning Loop", w=780, h=220)

    steps = [
        ("Pre-test\n(no hints)", BLUE),
        ("Study cards\n(prompt-before-reveal)", GREEN),
        ("Quiz\n(with confidence)", GREEN),
        ("Practice sort\n(with feedback)", GREEN),
        ("Weak-item\nreview", YELLOW),
        ("Post-test\n(parallel variant)", BLUE),
        ("Export\n(CSV/JSON)", GREY),
    ]
    ids = []
    xs = 15
    for label, color in steps:
        ids.append(d.vertex(xs, 60, 96, 50, label, color, fontSize="9"))
        xs += 104

    for i in range(len(ids)-1):
        d.arrow(ids[i], ids[i+1])

    d.label(100, 160, 580, 25,
            "Pre / post use parallel variants. Study cards are retrieval practice. Practice gives error-specific feedback.",
            "text;html=1;align=center;verticalAlign=middle;fontSize=10;fontStyle=2;")

    return d


# ── Diagram 5: Study ladder staircase (Slide 20) ───────────────────────
def study_ladder() -> Diagram:
    d = Diagram("Study Ladder", w=700, h=450)

    levels = [
        ("5 — SPD pilot", "SPD trainees\nor technicians", "Behavioral transfer", RED_BG),
        ("4 — Expert review", "1 SPD educator", "Content validity", ORANGE),
        ("3 — Delayed retention", "Same novices\n7 days later", "Temporal persistence", YELLOW),
        ("2 — Novice study", "8–12 novices", "Learning mechanism", GREEN),
        ("1 — Marker reliability", "Project members", "Measurement tool", BLUE),
    ]

    bases = [340, 270, 200, 130, 60]
    ids = []
    for i, (title, who, what, color) in enumerate(levels):
        x = 40 + i * 25
        ww = 600 - i * 30
        cid = d.vertex(x, bases[i], ww, 50,
                       f"<b>{title}</b>\n{who}  |  Validates: {what}",
                       color, fontSize="9", html="1")
        ids.append(cid)

    # Vertical arrows between levels
    for i in range(len(ids)-1):
        d.arrow(ids[i], ids[i+1])

    # Kirkpatrick callout
    d.label(200, 20, 300, 25,
            "Target: Kirkpatrick Level 2 (Learning). Levels 3–4 require future validation.",
            "text;html=1;align=center;verticalAlign=middle;fontSize=11;fontStyle=1;")

    return d


# ── Diagram 6: Retention 3-outcome (Slide 22) ──────────────────────────
def retention() -> Diagram:
    d = Diagram("Retention Outcomes", w=650, h=400)

    # Pre → Post arrow
    pre  = d.vertex(20, 40, 100, 40, "Pre-test\n(30%)", BLUE)
    post = d.vertex(250, 40, 100, 40, "Post-test\n(85%)", GREEN)
    d.arrow(pre, post)

    # 7-day label
    d.label(375, 40, 120, 40, "7 days later →", "text;html=1;align=center;verticalAlign=middle;fontSize=12;fontStyle=1;")

    # Three outcome branches
    a = d.vertex(20, 160, 280, 55,
                 "≥ 50% of gain retained\n→ learning persists",
                 GREEN)
    b = d.vertex(20, 260, 280, 55,
                 "≤ 5pp above baseline\n→ practice effect only",
                 ORANGE)
    c = d.vertex(20, 360, 280, 55,
                 "< 50% of gain retained\n→ partial decay",
                 RED_BG)

    # Connectors from post to the three (orthogonal routing)
    d.arrow(post, a)
    d.arrow(post, b)
    d.arrow(post, c)

    d.label(350, 180, 260, 30,
            "All three must be met for a retention claim.",
            "text;html=1;align=left;verticalAlign=middle;fontSize=10;fontStyle=2;")

    return d


# ── Diagram 7: Go/no-go flowchart (Slide 24) ───────────────────────────
def gonogo() -> Diagram:
    d = Diagram("Go No-Go", w=600, h=350)

    study = d.vertex(180, 10, 220, 50, "Study 1 + 2 pass?\n(learning + retention)", YELLOW, fontSize="10")

    yes = d.vertex(40, 130, 200, 50, "Yes → Study 3\n(expert review)", GREEN, fontSize="10")
    pos = d.vertex(40, 230, 200, 50, "Expert positive?\n→ SPD pilot warranted", GREEN, fontSize="10")
    neg = d.vertex(320, 230, 240, 50, "Expert negative?\n→ Fix content before pilot", ORANGE, fontSize="9")

    no = d.vertex(320, 130, 240, 50, "No → Report limitations\nLearning mechanism works\nbut retention fails", RED_BG, fontSize="9")

    d.arrow(study, yes)
    d.arrow(study, no)
    d.arrow(yes, pos)
    d.arrow(yes, neg)

    return d


# ── Generate all ────────────────────────────────────────────────────────
OUT = "/Users/matthewli/Projects/trayguard/final_paper/figures"
FUNCS = [
    ("fishbone_placeholder.drawio", fishbone),
    ("feedback_loop_placeholder.drawio", feedback_loop),
    ("complementary_placeholder.drawio", complementary),
    ("learning_loop_placeholder.drawio", learning_loop),
    ("study_ladder_placeholder.drawio", study_ladder),
    ("retention_placeholder.drawio", retention),
    ("gonogo_placeholder.drawio", gonogo),
]

if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    for fname, fn in FUNCS:
        path = os.path.join(OUT, fname)
        diag = fn()
        diag.save(path)
        print(f"  {path}")
    print("Done — open each .drawio in draw.io (diagrams.net), then File → Export As → PDF.")
