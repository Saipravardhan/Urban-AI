"""
UrbanAI - Smart City Infrastructure Optimization Platform
Presentation Generator
Creates a professional PowerPoint with flow charts for each DSA module
(Updated: Removed sorting, Bellman-Ford, Topo Sort, MST; CO6 preserved as M6)
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import math

# ─── Color Palette (Light Cool Theme) ───
BG_PRIMARY = RGBColor(0xF0, 0xF4, 0xFC)      # Light blue-gray
BG_SECONDARY = RGBColor(0xE8, 0xEE, 0xF6)     # Slightly darker
ACCENT_BLUE = RGBColor(0x2C, 0x6F, 0xBB)      # Deep blue
ACCENT_TEAL = RGBColor(0x1A, 0xAB, 0x8E)      # Teal
ACCENT_GREEN = RGBColor(0x27, 0xAE, 0x60)     # Green
ACCENT_ORANGE = RGBColor(0xE6, 0x7E, 0x22)    # Orange
ACCENT_RED = RGBColor(0xC0, 0x39, 0x2B)       # Red
ACCENT_PURPLE = RGBColor(0x8E, 0x44, 0xAD)    # Purple
TEXT_DARK = RGBColor(0x1A, 0x1A, 0x2E)        # Near-black
TEXT_GRAY = RGBColor(0x55, 0x55, 0x6E)        # Gray
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_BOX = RGBColor(0xDD, 0xE8, 0xF5)        # Light blue fill

# Slide dimensions (widescreen 16:9)
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H


# ─── Helper Functions ───

def add_background(slide, color=BG_PRIMARY):
    """Set slide background color."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, left, top, width, height, fill_color, border_color=None, border_width=Pt(1.5)):
    """Add a rounded rectangle shape."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = border_width
    else:
        shape.line.fill.background()
    # Reduce corner rounding
    shape.adjustments[0] = 0.1
    return shape


def add_arrow(slide, left, top, width, height, color=ACCENT_BLUE):
    """Add a right arrow."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_down_arrow(slide, left, top, width, height, color=ACCENT_BLUE):
    """Add a down arrow."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.DOWN_ARROW, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_textbox(slide, left, top, width, height, text, font_size=16, color=TEXT_DARK, bold=False, alignment=PP_ALIGN.CENTER, font_name='Calibri'):
    """Add a text box."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_multiline_textbox(slide, left, top, width, height, lines, font_size=14, color=TEXT_DARK, bold=False, alignment=PP_ALIGN.LEFT, line_spacing=1.2, font_name='Calibri'):
    """Add a text box with multiple paragraphs."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.bold = bold
        p.font.name = font_name
        p.alignment = alignment
        p.space_after = Pt(font_size * (line_spacing - 1) * 2)
    return txBox




def add_flow_box(slide, left, top, width, height, text, fill_color, text_color=TEXT_DARK, font_size=11, bold=False):
    """Add a flow chart box with centered text."""
    shape = add_shape(slide, left, top, width, height, fill_color, ACCENT_BLUE)
    shape.text_frame.word_wrap = True
    p = shape.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = text_color
    p.font.bold = bold
    p.font.name = 'Calibri'
    p.alignment = PP_ALIGN.CENTER
    shape.text_frame.paragraphs[0].space_before = Pt(0)
    shape.text_frame.paragraphs[0].space_after = Pt(0)
    # Vertical center
    shape.text_frame.auto_size = None
    return shape


def add_section_header(slide, title_text, subtitle_text=""):
    """Add a section header bar at top."""
    # Top accent bar
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), SLIDE_W, Inches(0.08)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_BLUE
    bar.line.fill.background()

    # Title
    add_textbox(slide, Inches(0.6), Inches(0.3), Inches(12), Inches(0.7),
                title_text, font_size=30, color=ACCENT_BLUE, bold=True, alignment=PP_ALIGN.LEFT)
    if subtitle_text:
        add_textbox(slide, Inches(0.6), Inches(0.85), Inches(12), Inches(0.4),
                    subtitle_text, font_size=16, color=TEXT_GRAY, alignment=PP_ALIGN.LEFT)

    # Divider line
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.2), Inches(12), Inches(0.03)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_BLUE
    line.line.fill.background()
    line.fill.fore_color.brightness = 0.0


def add_footer(slide, text="UrbanAI | Smart City Infrastructure Optimization Platform"):
    """Add footer text."""
    add_textbox(slide, Inches(0.5), Inches(7.0), Inches(12), Inches(0.4),
                text, font_size=9, color=TEXT_GRAY, alignment=PP_ALIGN.CENTER)


def add_decorative_circle(slide, left, top, size, color, opacity=15):
    """Add a decorative semi-transparent circle."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, left, top, size, size
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    # Set transparency via XML
    from pptx.oxml.ns import qn, nsmap
    try:
        spPr = shape._element.find(qn('p:spPr'))
        if spPr is None:
            spPr = shape._element.find(qn('a:spPr'))
        if spPr is None:
            return shape
        solidFill = spPr.find(qn('a:solidFill'))
        if solidFill is not None:
            srgbClr = solidFill.find(qn('a:srgbClr'))
            if srgbClr is not None:
                alpha = srgbClr.makeelement(qn('a:alpha'), {'val': str(int(opacity * 2.55))})
                srgbClr.append(alpha)
    except Exception:
        pass  # transparency is non-critical
    return shape


# ════════════════════════════════════════════════════════════════
# SLIDE 1: TITLE SLIDE
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
add_background(slide, RGBColor(0x1A, 0x1A, 0x2E))

# Decorative circles
add_decorative_circle(slide, Inches(-1), Inches(-1), Inches(3), ACCENT_BLUE, 15)
add_decorative_circle(slide, Inches(10), Inches(-2), Inches(5), ACCENT_TEAL, 10)
add_decorative_circle(slide, Inches(9), Inches(4), Inches(3), ACCENT_PURPLE, 12)
add_decorative_circle(slide, Inches(-0.5), Inches(4), Inches(3), ACCENT_ORANGE, 8)

# Top accent line
line = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(2.0), Inches(10.333), Inches(0.04)
)
line.fill.solid()
line.fill.fore_color.rgb = ACCENT_TEAL
line.line.fill.background()

# Main Title
add_textbox(slide, Inches(1.5), Inches(2.3), Inches(10.333), Inches(1.0),
            "UrbanAI", font_size=54, color=WHITE, bold=True)

add_textbox(slide, Inches(1.5), Inches(3.2), Inches(10.333), Inches(0.6),
            "Intelligent Smart City Infrastructure Optimization Platform", font_size=24, color=RGBColor(0xA0, 0xC4, 0xFF))

# Subtitle
add_textbox(slide, Inches(1.5), Inches(4.2), Inches(10.333), Inches(0.5),
            "A Comprehensive DSA-Driven Solution for Urban Management", font_size=16, color=RGBColor(0x88, 0x99, 0xBB))

# Bottom accent line
line2 = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(5.0), Inches(10.333), Inches(0.04)
)
line2.fill.solid()
line2.fill.fore_color.rgb = ACCENT_TEAL
line2.line.fill.background()

# Team Details Header
add_textbox(slide, Inches(1.5), Inches(5.15), Inches(10.333), Inches(0.35),
            "Team Members", font_size=13, color=ACCENT_TEAL, bold=True, alignment=PP_ALIGN.LEFT)

# Team members in two rows
team_row1 = "2500030104 - PeddiReddy Chaitanya Raj        2500030107 - Perla Jyothika"
team_row2 = "2500030135 - Gurrala Srishanth        2500030138 - Raja Hithesh"
add_textbox(slide, Inches(1.5), Inches(5.5), Inches(10.333), Inches(0.35),
            team_row1, font_size=13, color=RGBColor(0xB0, 0xC4, 0xDE), alignment=PP_ALIGN.LEFT)
add_textbox(slide, Inches(1.5), Inches(5.85), Inches(10.333), Inches(0.35),
            team_row2, font_size=13, color=RGBColor(0xB0, 0xC4, 0xDE), alignment=PP_ALIGN.LEFT)

# Mentor
add_textbox(slide, Inches(1.5), Inches(6.25), Inches(10.333), Inches(0.35),
            "Mentor: DR. Razia", font_size=13, color=RGBColor(0x88, 0x99, 0xBB), bold=True, alignment=PP_ALIGN.LEFT)

# Module badges (M5 = Greedy & DP, sorting removed)
modules_text = "M1: Trees & Asset Mgmt  |  M2: Traffic Analytics (Fenwick)  |  M3: Graph Algorithms (BFS, DFS)\nM4: Shortest Path (Dijkstra, Floyd-Warshall)  |  M6: Greedy & DP (Activity Sel, Knapsack, Edit Dist)"
add_textbox(slide, Inches(1.5), Inches(6.6), Inches(10.333), Inches(0.5),
            modules_text, font_size=10, color=RGBColor(0x55, 0x66, 0x88), alignment=PP_ALIGN.LEFT)


# ════════════════════════════════════════════════════════════════
# SLIDE 2: PROBLEM STATEMENT
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Problem Statement")

problems = [
    "🌆 Managing large-scale urban infrastructure assets efficiently — roads, traffic signals, utility networks, and public facilities.",
    "🚦 Real-time traffic data analysis for congestion detection, density calculation, and urban mobility optimization.",
    "🗺️ Complex road network connectivity analysis to identify disconnected regions, optimize routes, and reduce emergency response times.",
    "📊 Handling massive city datasets with fast search and priority-based resource allocation.",
    "📋 Scheduling city maintenance projects and allocating limited budget/resources across competing infrastructure needs."
]

add_multiline_textbox(slide, Inches(0.8), Inches(1.5), Inches(11.5), Inches(5.5),
                      problems, font_size=15, color=TEXT_DARK, line_spacing=1.6, alignment=PP_ALIGN.LEFT)

# Bottom emphasis box
emphasis = add_shape(slide, Inches(0.8), Inches(5.8), Inches(11.5), Inches(0.7), RGBColor(0xE3, 0xF2, 0xFD), ACCENT_BLUE)
add_textbox(slide, Inches(1.0), Inches(5.85), Inches(11.0), Inches(0.6),
            "Challenge: How can Data Structures & Algorithms optimize every layer of smart city operations at scale?",
            font_size=15, color=ACCENT_BLUE, bold=True)

add_footer(slide)


# ════════════════════════════════════════════════════════════════
# SLIDE 3: ABSTRACT
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Abstract")

abstract_text = (
    "UrbanAI is a comprehensive smart city infrastructure optimization platform built using Java, "
    "leveraging advanced Data Structures and Algorithms to address real-world urban management challenges. "
    "The platform integrates five core DSA modules covering balanced search trees (AVL Trees), multiway indexing "
    "(Fenwick Tree), graph algorithms (BFS, DFS), shortest path optimization (Dijkstra, "
    "Floyd-Warshall), and greedy/DP optimization techniques "
    "(Activity Selection, Fractional Knapsack, 0/1 Knapsack, Edit Distance). "
    "Each module is applied to a specific urban scenario—infrastructure asset management, traffic analytics, road "
    "network analysis, emergency routing, maintenance scheduling, and citizen service prioritization. "
    "UrbanAI demonstrates how theoretical DSA concepts translate into practical, scalable solutions for smart city operations."
)
add_textbox(slide, Inches(0.8), Inches(1.6), Inches(11.5), Inches(2.0),
            abstract_text, font_size=15, color=TEXT_DARK, alignment=PP_ALIGN.LEFT)

# Key Highlights
add_textbox(slide, Inches(0.8), Inches(3.6), Inches(11.5), Inches(0.5),
            "Key Highlights", font_size=20, color=ACCENT_BLUE, bold=True, alignment=PP_ALIGN.LEFT)

highlights = [
    "✓ PostgreSQL integration for persistent data storage across all modules",
    "✓ Console-based interactive menu system for real-time demo of each algorithm",
    "✓ 15+ distinct DSA implementations, each mapped to a smart city use case",
    "✓ Modular architecture (5 modules) following object-oriented design principles",
    "✓ End-to-end flow from data input → algorithm processing → output visualization"
]
add_multiline_textbox(slide, Inches(0.8), Inches(4.2), Inches(11.5), Inches(2.8),
                      highlights, font_size=13, color=TEXT_GRAY, line_spacing=1.5, alignment=PP_ALIGN.LEFT)

add_footer(slide)


# ════════════════════════════════════════════════════════════════
# SLIDE 4: SOFTWARE & HARDWARE USED
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Software & Hardware Requirements")

# Left - Software
sw_box = add_shape(slide, Inches(0.6), Inches(1.5), Inches(5.8), Inches(5.2), RGBColor(0xE3, 0xF2, 0xFD), ACCENT_BLUE)
add_textbox(slide, Inches(0.8), Inches(1.6), Inches(5.4), Inches(0.5),
            "💻 Software Stack", font_size=20, color=ACCENT_BLUE, bold=True, alignment=PP_ALIGN.LEFT)
sw_items = [
    "• Java JDK 11+ (Primary Development)",
    "• PostgreSQL 15+ (Database Server)",
    "• PostgreSQL JDBC Driver (v42.7.11)",
    "• Visual Studio Code / IntelliJ IDEA (IDE)",
    "• Windows 10/11 (Development Platform)",
    "• pgAdmin 4 (Database Management)",
    "• Git (Version Control)",
    "",
    "Programming Language: Java",
    "Database: PostgreSQL (Port 7000)",
    "JDBC for database connectivity",
    "",
    "Libraries: java.util.*, java.sql.*",
    "Build: Manual compilation (javac)",
]
add_multiline_textbox(slide, Inches(0.8), Inches(2.2), Inches(5.4), Inches(4.3),
                      sw_items, font_size=13, color=TEXT_DARK, line_spacing=1.2, alignment=PP_ALIGN.LEFT)

# Right - Hardware
hw_box = add_shape(slide, Inches(6.8), Inches(1.5), Inches(5.8), Inches(5.2), RGBColor(0xFD, 0xF2, 0xE3), ACCENT_ORANGE)
add_textbox(slide, Inches(7.0), Inches(1.6), Inches(5.4), Inches(0.5),
            "🖥️ Hardware Requirements", font_size=20, color=ACCENT_ORANGE, bold=True, alignment=PP_ALIGN.LEFT)
hw_items = [
    "• Processor: Intel Core i5 / AMD Ryzen 5+",
    "• RAM: 8 GB minimum (16 GB recommended)",
    "• Storage: 256 GB SSD (for database & code)",
    "• OS: Windows 10 / 11 (64-bit)",
    "• Network: Localhost (127.0.0.1)",
    "• Display: 1920x1080 resolution",
    "",
    "",
    "Tested Configuration:",
    "• CPU: Intel Core i5-12th Gen",
    "• RAM: 16 GB DDR4",
    "• OS: Windows 11 Pro",
    "• PostgreSQL: Running locally on port 7000",
]
add_multiline_textbox(slide, Inches(7.0), Inches(2.2), Inches(5.4), Inches(4.3),
                      hw_items, font_size=13, color=TEXT_DARK, line_spacing=1.2, alignment=PP_ALIGN.LEFT)

add_footer(slide)


# ════════════════════════════════════════════════════════════════
# SLIDE 5: SYSTEM ARCHITECTURE (REDESIGNED - DETAILED LAYERS)
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "System Architecture", "Multi-layer architecture: UI → Controller → Modules → DAO → Database → Output")

# ── LAYER 1: USER INTERFACE ──
add_flow_box(slide, Inches(4.8), Inches(1.4), Inches(3.6), Inches(0.45), "LAYER 1: USER INTERFACE (Console Menu + Scanner Input)", RGBColor(0x2C, 0x6F, 0xBB), WHITE, 11, True)
add_down_arrow(slide, Inches(6.6), Inches(1.88), Inches(0.3), Inches(0.2), ACCENT_BLUE)

# ── LAYER 2: CONTROLLER ──
add_flow_box(slide, Inches(4.8), Inches(2.15), Inches(3.6), Inches(0.45), "LAYER 2: APPLICATION CONTROLLER (Main.java - Switch-Case Dispatcher)", RGBColor(0x2C, 0x6F, 0xBB), WHITE, 11, True)

# Arrows from controller to 5 modules
mod_start_x = Inches(1.0)
mod_w = Inches(2.3)
mod_gap = Inches(0.3)
mod_y = Inches(2.9)

for i in range(5):
    x = mod_start_x + i * (mod_w + mod_gap)
    # Arrow from controller to module
    arrow_center = x + mod_w / 2
    add_down_arrow(slide, arrow_center - Inches(0.12), Inches(2.63), Inches(0.25), Inches(0.2), ACCENT_BLUE)

# ── LAYER 3: MODULES (5 modules - sorting removed) ──
mod_names = [
    ("M1: Asset Management\n(AVL Tree, BST)", RGBColor(0xBB, 0xDE, 0xFB), ACCENT_BLUE),
    ("M2: Traffic Analytics\n(Fenwick Tree)", RGBColor(0xD4, 0xED, 0xDA), ACCENT_TEAL),
    ("M3: Graph Analysis\n(BFS, DFS)", RGBColor(0xC8, 0xE6, 0xC9), ACCENT_GREEN),
    ("M4: Shortest Path\n(Dijkstra, Floyd)", RGBColor(0xFD, 0xE8, 0xD0), ACCENT_ORANGE),
    ("M6: Greedy & DP\n(ActSel, FracKnap,\n01Knap, EditDist)", RGBColor(0xFF, 0xD9, 0xCC), ACCENT_RED),
]
for i, (name, fill, border) in enumerate(mod_names):
    x = mod_start_x + i * (mod_w + mod_gap)
    add_flow_box(slide, x, mod_y, mod_w, Inches(0.65), name, fill, TEXT_DARK, 9, True)

# ── LAYER 4: DATA ACCESS + DATABASE ──
add_down_arrow(slide, Inches(6.6), Inches(3.6), Inches(0.3), Inches(0.18), ACCENT_BLUE)
add_flow_box(slide, Inches(0.3), Inches(3.85), Inches(12.7), Inches(0.45),
             "LAYER 4: DATA ACCESS (AssetDAO, TrafficDAO - JDBC Prepared Statements)", RGBColor(0x2C, 0x6F, 0xBB), WHITE, 11, True)
add_down_arrow(slide, Inches(6.6), Inches(4.33), Inches(0.3), Inches(0.18), ACCENT_BLUE)

add_flow_box(slide, Inches(0.3), Inches(4.6), Inches(12.7), Inches(0.45),
             "LAYER 5: PERSISTENCE (PostgreSQL - urbanai_db → UrbanAI_Assets, UrbanAI_Traffic Tables)", RGBColor(0x2C, 0x6F, 0xBB), WHITE, 11, True)

# ── LAYER 6: MODELS ──
add_down_arrow(slide, Inches(6.6), Inches(5.08), Inches(0.3), Inches(0.18), ACCENT_BLUE)
model_names = ["Asset.java\n(ID, Name, Loc, Type)", "TrafficRecord.java\n(RoadID, VehicleCount)"]
model_start = Inches(3.5)
for i, m_name in enumerate(model_names):
    x = model_start + i * Inches(3.6)
    c = [RGBColor(0xE3, 0xF2, 0xFD), RGBColor(0xE0, 0xF2, 0xF1)][i]
    add_flow_box(slide, x, Inches(5.35), Inches(3.0), Inches(0.65), m_name, c, TEXT_DARK, 10, True)

# ── LAYER 7: OUTPUT ──
add_down_arrow(slide, Inches(6.6), Inches(6.05), Inches(0.3), Inches(0.18), ACCENT_BLUE)
add_flow_box(slide, Inches(0.3), Inches(6.3), Inches(12.7), Inches(0.45),
             "LAYER 7: OUTPUT (Console Display - Route Maps, Traffic Analytics, Maintenance Schedule, Priority Rankings)",
             RGBColor(0x2C, 0x6F, 0xBB), WHITE, 11, True)

# Data flow annotation on right side
add_textbox(slide, Inches(0.5), Inches(7.0), Inches(12.0), Inches(0.3),
            "Data Flow: User Input → Main Controller → Module Selection → Algorithm Execution → DAO Layer → PostgreSQL → Model Mapping → Console Output",
            font_size=10, color=TEXT_GRAY, alignment=PP_ALIGN.CENTER)

add_footer(slide)


# ════════════════════════════════════════════════════════════════
# MODULE SLIDES GENERATOR (unused - all slides now use direct step-by-step flow)
# ════════════════════════════════════════════════════════════════


# ════════════════════════════════════════════════════════════════
# SLIDE 6: MODULE 1 - TREES & ASSET MANAGEMENT (CO1)
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Module 1: Trees & Balanced Search Structures (CO1)",
                   "Infrastructure Asset Management using AVL Tree")

# ── Left Panel: DSA Techniques ──
add_shape(slide, Inches(0.4), Inches(1.25), Inches(5.0), Inches(1.9), RGBColor(0xE3, 0xF2, 0xFD), ACCENT_BLUE)
add_textbox(slide, Inches(0.6), Inches(1.28), Inches(4.6), Inches(0.3),
            "📋 DSA Techniques Used", font_size=13, color=ACCENT_BLUE, bold=True, alignment=PP_ALIGN.LEFT)
add_multiline_textbox(slide, Inches(0.6), Inches(1.58), Inches(4.6), Inches(1.5),
    [
        "1. BST — Index assets by AssetID for O(log n) search",
        "2. AVL Tree — Self-balancing BST (balance factor: -1,0,1)",
        "3. In-order Traversal — Sorted asset reports",
        "4. Rotations (LL/RR/LR/RL) — Auto-rebalancing"
    ], font_size=10, color=TEXT_DARK, line_spacing=1.3, alignment=PP_ALIGN.LEFT)

# ── Right Panel: Why ──
add_shape(slide, Inches(5.7), Inches(1.25), Inches(7.2), Inches(1.9), RGBColor(0xFD, 0xF2, 0xE3), ACCENT_ORANGE)
add_textbox(slide, Inches(5.9), Inches(1.28), Inches(6.8), Inches(0.3),
            "❓ Why These Data Structures?", font_size=13, color=ACCENT_ORANGE, bold=True, alignment=PP_ALIGN.LEFT)
add_multiline_textbox(slide, Inches(5.9), Inches(1.58), Inches(6.8), Inches(1.5),
    [
        "• Asset IDs are numeric → ideal for BST indexing",
        "• AVL prevents O(n) degradation → guaranteed O(log n)",
        "• In-order traversal → sorted output with zero extra cost",
        "• Real-time lookups for emergency asset dispatch"
    ], font_size=10, color=TEXT_DARK, line_spacing=1.3, alignment=PP_ALIGN.LEFT)

# ── Flow Chart Area ──
add_textbox(slide, Inches(0.4), Inches(3.3), Inches(4.0), Inches(0.25),
            "📊 Algorithm Flow Diagram — AVL Tree Insertion & Search", font_size=12, color=ACCENT_BLUE, bold=True, alignment=PP_ALIGN.LEFT)

# ─── MAIN INSERT FLOW (Vertical - Left Column) ───
bx = Inches(3.6)   # Insert flow left edge
bw = Inches(2.8)   # Insert flow box width
bh = Inches(0.35)  # Box height
cx = Inches(5.0)   # Center X for arrows

y_start = Inches(3.6)
y_step = Inches(0.55)  # step + gap

add_flow_box(slide, bx, y_start, bw, bh,
    "STEP 1: User enters Asset details\n(AssetID, Name, Location, Type)", LIGHT_BOX, TEXT_DARK, 9, False)
add_down_arrow(slide, cx - Inches(0.1), y_start + bh + Inches(0.02), Inches(0.2), Inches(0.15), ACCENT_BLUE)

add_flow_box(slide, bx, y_start + y_step, bw, bh,
    "STEP 2: Asset object created\nnew Asset(id, name, loc, type)", LIGHT_BOX, TEXT_DARK, 9, False)
add_down_arrow(slide, cx - Inches(0.1), y_start + y_step + bh + Inches(0.02), Inches(0.2), Inches(0.15), ACCENT_BLUE)

add_flow_box(slide, bx, y_start + 2*y_step, bw, bh,
    "STEP 3: avlTree.insert(asset) called\nCompares assetId with current node", LIGHT_BOX, TEXT_DARK, 9, False)
add_down_arrow(slide, cx - Inches(0.1), y_start + 2*y_step + bh + Inches(0.02), Inches(0.2), Inches(0.15), ACCENT_BLUE)

# Decision diamond
diamond_y = y_start + 3*y_step
diamond = slide.shapes.add_shape(
    MSO_SHAPE.DIAMOND, Inches(4.2), diamond_y, Inches(1.6), Inches(0.45)
)
diamond.fill.solid()
diamond.fill.fore_color.rgb = RGBColor(0xFF, 0xF3, 0xCD)
diamond.line.color.rgb = ACCENT_ORANGE
diamond.line.width = Pt(1.5)
diamond.text_frame.word_wrap = True
p = diamond.text_frame.paragraphs[0]
p.text = "Balance\n|BF| > 1?"
p.font.size = Pt(8)
p.font.color.rgb = TEXT_DARK
p.font.bold = True
p.font.name = 'Calibri'
p.alignment = PP_ALIGN.CENTER

# YES branch (right from diamond)
add_arrow(slide, Inches(5.85), diamond_y + Inches(0.12), Inches(0.25), Inches(0.15), ACCENT_RED)
add_flow_box(slide, Inches(6.2), diamond_y + Inches(0.02), Inches(2.5), Inches(0.35),
    "YES → Rotations\n(LL / RR / LR / RL)", RGBColor(0xFF, 0xCD, 0xD2), TEXT_DARK, 9, True)

# NO branch (down from diamond) + combine with bottom box
add_down_arrow(slide, cx - Inches(0.1), diamond_y + Inches(0.45), Inches(0.2), Inches(0.12), ACCENT_GREEN)
no_y = diamond_y + Inches(0.6)
add_flow_box(slide, bx, no_y, bw, bh,
    "NO → Tree balanced → Node height updated", RGBColor(0xC8, 0xE6, 0xC9), TEXT_DARK, 9, True)

# Bottom: combined DB + Display
db_y = no_y + bh + Inches(0.08)
add_flow_box(slide, bx, db_y, Inches(5.0), bh,
    "AssetDAO → PostgreSQL INSERT | Display Assets (In-order Traversal)", RGBColor(0xD5, 0xDB, 0xDB), TEXT_DARK, 9, True)

# ─── RIGHT COLUMN: Search Path ───
sx = Inches(6.5)
sw = Inches(2.5)
sh = Inches(0.32)
add_textbox(slide, sx, Inches(3.3), Inches(2.5), Inches(0.25),
            "🔍 Search Path", font_size=10, color=ACCENT_TEAL, bold=True)

add_flow_box(slide, sx, Inches(3.6), sw, sh,
    "searchAsset(id)\nBST while-loop compare node", RGBColor(0xE0, 0xF2, 0xF1), TEXT_DARK, 8, False)
add_down_arrow(slide, sx + sw/2 - Inches(0.08), Inches(3.95), Inches(0.16), Inches(0.12), ACCENT_TEAL)

add_flow_box(slide, sx, Inches(4.15), sw, sh,
    "Found in AVL Tree?\nReturn Asset object", RGBColor(0xE0, 0xF2, 0xF1), TEXT_DARK, 8, False)
add_down_arrow(slide, sx + sw/2 - Inches(0.08), Inches(4.5), Inches(0.16), Inches(0.12), ACCENT_TEAL)

add_flow_box(slide, sx, Inches(4.7), sw, sh,
    "Not found?\nFallback → PostgreSQL search", RGBColor(0xE0, 0xF2, 0xF1), TEXT_DARK, 8, False)
add_down_arrow(slide, sx + sw/2 - Inches(0.08), Inches(5.05), Inches(0.16), Inches(0.12), ACCENT_TEAL)

add_flow_box(slide, sx, Inches(5.25), sw, sh,
    "Display: Asset Details\nOR 'Asset Not Found'", RGBColor(0xE0, 0xF2, 0xF1), TEXT_DARK, 8, False)

# ─── RIGHTMOST: Code snippet panel ───
add_shape(slide, Inches(9.3), Inches(3.6), Inches(3.7), Inches(3.0), RGBColor(0x26, 0x26, 0x26), ACCENT_BLUE)
add_textbox(slide, Inches(9.5), Inches(3.65), Inches(3.4), Inches(0.2),
            "🔑 AVL Rotations Code", font_size=9, color=RGBColor(0x66, 0xBB, 0x66), bold=True, alignment=PP_ALIGN.LEFT)
code_lines = [
    "// Right Rotate (LL Case)",
    "rightRotate(Node y) {",
    "  Node x = y.left;",
    "  Node t2 = x.right;",
    "  x.right = y;",
    "  y.left = t2;",
    "  updateHeight(y);",
    "  updateHeight(x);",
    "  return x;",
    "}",
    "",
    "// getBalance(node)",
    "// = height(left) - height(right)",
    "// if |BF| > 1 → rotate"
]
add_multiline_textbox(slide, Inches(9.5), Inches(3.9), Inches(3.4), Inches(2.5),
    code_lines, font_size=7, color=RGBColor(0xCC, 0xDD, 0xCC), line_spacing=1.05, alignment=PP_ALIGN.LEFT)

# ─── Bottom note ───
add_textbox(slide, Inches(0.4), Inches(6.85), Inches(12.0), Inches(0.25),
    "Time: O(log n) insert/search  |  Space: O(n)  |  Key: Self-Balancing via Height Tracking (balance factor) + 4 Rotation Types",
    font_size=9, color=TEXT_GRAY, alignment=PP_ALIGN.CENTER)
add_footer(slide)

# ════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════
# SLIDE 7: MODULE 2 - RANGE QUERY STRUCTURES (CO2)
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Module 2: Range Query Structures (CO2)",
                   "Traffic Density Analytics using Fenwick Tree")

# ── Left Panel: DSA Techniques ──
add_shape(slide, Inches(0.4), Inches(1.25), Inches(5.0), Inches(1.5), RGBColor(0xE3, 0xF2, 0xFD), ACCENT_BLUE)
add_textbox(slide, Inches(0.6), Inches(1.28), Inches(4.6), Inches(0.3),
            "📋 DSA Techniques Used", font_size=12, color=ACCENT_BLUE, bold=True)
add_multiline_textbox(slide, Inches(0.6), Inches(1.55), Inches(4.6), Inches(1.1),
    ["1. Fenwick Tree (BIT) — Cumulative traffic stats O(log n)",
     "2. Bit Ops — i += i & (-i) for prefix sum updates",
     "3. Fenwick range query = prefix(R) - prefix(L-1)"],
    font_size=10, color=TEXT_DARK, line_spacing=1.3)

# ── Right Panel: Why ──
add_shape(slide, Inches(5.7), Inches(1.25), Inches(7.2), Inches(1.5), RGBColor(0xFD, 0xF2, 0xE3), ACCENT_ORANGE)
add_textbox(slide, Inches(5.9), Inches(1.28), Inches(6.8), Inches(0.3),
            "❓ Why These Data Structures?", font_size=12, color=ACCENT_ORANGE, bold=True)
add_multiline_textbox(slide, Inches(5.9), Inches(1.55), Inches(6.8), Inches(1.1),
    ["• RoadID ordering → natural for range queries",
     "• Real-time aggregation needs O(log n), not O(n)",
     "• Avoids full table scans on 1000+ road segments"],
    font_size=10, color=TEXT_DARK, line_spacing=1.3)

# ── Flow Chart ──
add_textbox(slide, Inches(0.4), Inches(3.2), Inches(4.0), Inches(0.25),
            "📊 Algorithm Flow Diagram — Traffic Data Insert & Query", font_size=12, color=ACCENT_TEAL, bold=True)

# ─── LEFT COLUMN: Insert Flow ───
lx = Inches(0.6)
lw = Inches(3.5)
lh = Inches(0.38)
add_flow_box(slide, lx, Inches(3.5), lw, lh, "STEP 1: User enters\nRoadID + VehicleCount", LIGHT_BOX, TEXT_DARK, 9, False)
add_down_arrow(slide, Inches(2.35), Inches(3.9), Inches(0.18), Inches(0.08), ACCENT_TEAL)

add_flow_box(slide, lx, Inches(4.05), lw, lh, "STEP 2: TrafficRecord object\nnew TrafficRecord(roadId, count)", LIGHT_BOX, TEXT_DARK, 9, False)
add_down_arrow(slide, Inches(2.35), Inches(4.45), Inches(0.18), Inches(0.08), ACCENT_TEAL)

add_flow_box(slide, lx, Inches(4.6), lw, lh, "STEP 3: fenwick.update(id, count)\nBIT[index] += value\n(index += index & -index)", LIGHT_BOX, TEXT_DARK, 9, False)
add_down_arrow(slide, Inches(2.35), Inches(5.0), Inches(0.18), Inches(0.08), ACCENT_TEAL)

add_flow_box(slide, lx, Inches(5.15), lw, lh, "STEP 4: trafficDAO.insertRecord()\nINSERT INTO UrbanAI_Traffic", LIGHT_BOX, TEXT_DARK, 9, False)
add_down_arrow(slide, Inches(2.35), Inches(5.55), Inches(0.18), Inches(0.08), ACCENT_TEAL)

add_flow_box(slide, lx, Inches(5.7), lw, lh, "STEP 5: records.add(record)\nIn-memory ArrayList backup", LIGHT_BOX, TEXT_DARK, 9, False)

# ─── RIGHT COLUMN: Query Flows ───
rx = Inches(5.2)
rw = Inches(3.5)
ry = Inches(3.5)
rh = Inches(0.38)

# Density Query
add_textbox(slide, rx, Inches(3.2), Inches(3.5), Inches(0.25),
            "▶ Density Query", font_size=10, color=ACCENT_ORANGE, bold=True)
add_flow_box(slide, rx, ry, rw, rh, "calculateTrafficDensity(id)\nLoop records ArrayList", RGBColor(0xFD, 0xF2, 0xE3), TEXT_DARK, 9)
add_down_arrow(slide, Inches(6.95), Inches(3.9), Inches(0.18), Inches(0.08), ACCENT_ORANGE)
add_flow_box(slide, rx, Inches(4.05), rw, rh, "If count > 1000 → HIGH\nIf count > 500 → MEDIUM\nElse → LOW", RGBColor(0xFD, 0xF2, 0xE3), TEXT_DARK, 9)
add_down_arrow(slide, Inches(6.95), Inches(4.45), Inches(0.18), Inches(0.08), ACCENT_ORANGE)
add_flow_box(slide, rx, Inches(4.6), rw, rh, "Output: 'Traffic Density: HIGH'", RGBColor(0xFD, 0xF2, 0xE3), TEXT_DARK, 9)

# Cumulative Query
add_textbox(slide, Inches(9.4), Inches(3.2), Inches(3.5), Inches(0.25),
            "▶ Cumulative Statistics", font_size=10, color=ACCENT_GREEN, bold=True)
add_flow_box(slide, Inches(9.4), ry, Inches(3.2), rh, "rangeQuery(start, end)\nfenwick.rangeQuery(L,R)", RGBColor(0xE8, 0xF5, 0xE9), TEXT_DARK, 9)
add_down_arrow(slide, Inches(11.0), Inches(3.9), Inches(0.18), Inches(0.08), ACCENT_GREEN)
add_flow_box(slide, Inches(9.4), Inches(4.05), Inches(3.2), rh, "= query(R) - query(L-1)\nPrefix Sum: SUM(1..R) - SUM(1..L-1)", RGBColor(0xE8, 0xF5, 0xE9), TEXT_DARK, 9)
add_down_arrow(slide, Inches(11.0), Inches(4.45), Inches(0.18), Inches(0.08), ACCENT_GREEN)
add_flow_box(slide, Inches(9.4), Inches(4.6), Inches(3.2), rh, "Output: 'Total Traffic = X'", RGBColor(0xE8, 0xF5, 0xE9), TEXT_DARK, 9)

# Fenwick BIT Visual
add_textbox(slide, Inches(0.4), Inches(6.2), Inches(12.0), Inches(0.2),
            "Fenwick Tree BIT[1..N]: update O(log n) | prefixSum O(log n) | rangeQuery = prefix(R) - prefix(L-1)",
            font_size=9, color=TEXT_GRAY)
add_footer(slide)

# ════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════
# SLIDE 8: MODULE 3 - GRAPH ALGORITHMS (CO3) — 2 STEP-BY-STEP FLOWS
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Module 3: Graph Algorithms for City Networks (CO3)",
                   "Road Network Analysis: BFS & DFS for Route Planning")

# ── Info Panels (compact) ──
add_shape(slide, Inches(0.4), Inches(1.2), Inches(4.5), Inches(1.35), RGBColor(0xE3, 0xF2, 0xFD), ACCENT_BLUE)
add_textbox(slide, Inches(0.6), Inches(1.22), Inches(4.2), Inches(0.25),
            "📋 DSA Techniques Used", font_size=11, color=ACCENT_BLUE, bold=True)
add_multiline_textbox(slide, Inches(0.6), Inches(1.5), Inches(4.2), Inches(0.95),
    ["1. Graph (Adj List) — roads=edges, nodes=intersections",
     "2. BFS — Shortest path routing (Queue-based)",
     "3. DFS — Region detection (Stack/Recursion)"],
    font_size=9, color=TEXT_DARK, line_spacing=1.2)

add_shape(slide, Inches(5.2), Inches(1.2), Inches(7.7), Inches(1.35), RGBColor(0xFD, 0xF2, 0xE3), ACCENT_ORANGE)
add_textbox(slide, Inches(5.4), Inches(1.22), Inches(7.3), Inches(0.25),
            "❓ Why These Algorithms?", font_size=11, color=ACCENT_ORANGE, bold=True)
add_multiline_textbox(slide, Inches(5.4), Inches(1.5), Inches(7.3), Inches(0.95),
    ["• Roads = edges, Intersections = vertices → City is a Graph!",
     "• BFS → fastest emergency vehicle route (shortest path)",
     "• DFS → detect disconnected neighborhoods (cycle detection)"],
    font_size=9, color=TEXT_DARK, line_spacing=1.2)

# ── Section subtitle ──
add_textbox(slide, Inches(0.3), Inches(2.7), Inches(12.5), Inches(0.25),
    "📊 Step-by-Step Algorithm Flows — How Each Algorithm Processes the City Road Network",
    font_size=11, color=ACCENT_RED, bold=True)

# ── Column widths & shared settings (2 columns instead of 3) ──
col_w = Inches(6.0)
col_gap = Inches(0.4)
col_starts = [Inches(0.3), Inches(6.7)]
step_h = Inches(0.48)
arrow_h = Inches(0.12)
base_y = Inches(3.0)

# ── COLUMN 1: BFS ──
add_shape(slide, col_starts[0], Inches(2.95), col_w, Inches(0.28), ACCENT_GREEN, ACCENT_GREEN)
add_textbox(slide, col_starts[0], Inches(2.95), col_w, Inches(0.28),
            "🌊 BFS — Emergency Route Planning", font_size=10, color=WHITE, bold=True)

bfs_steps = [
    ["STEP 1: Build adjacency list of road network\nIntersections (nodes) connected by roads (edges) — 6 nodes, 5 edges", RGBColor(0xE8, 0xF5, 0xE9)],
    ["STEP 2: Initialize Queue with start intersection\nMark visited → enqueue node 0 (Emergency HQ), dequeue → visit neighbors", RGBColor(0xC8, 0xE6, 0xC9)],
    ["STEP 3: Dequeue each node → visit all unvisited neighbors\nEnqueue them → repeat until queue is empty → shortest path found!", RGBColor(0xA5, 0xD6, 0xA7)],
    ["STEP 4: Output traversal + shortest path to every node\nRoute: 0→1→3→5 = fastest emergency response route ✅", RGBColor(0x81, 0xC7, 0x84)],
]
for i, (text, bg) in enumerate(bfs_steps):
    sy = base_y + i * (step_h + arrow_h + Inches(0.04))
    add_flow_box(slide, col_starts[0], sy, col_w, step_h, text, bg, TEXT_DARK, 9, False)
    if i < len(bfs_steps) - 1:
        add_down_arrow(slide, col_starts[0] + col_w/2 - Inches(0.1), sy + step_h + Inches(0.01), Inches(0.2), arrow_h, ACCENT_GREEN)

# ── COLUMN 2: DFS ──
add_shape(slide, col_starts[1], Inches(2.95), col_w, Inches(0.28), ACCENT_BLUE, ACCENT_BLUE)
add_textbox(slide, col_starts[1], Inches(2.95), col_w, Inches(0.28),
            "🌀 DFS — Infrastructure Region Detection", font_size=10, color=WHITE, bold=True)

dfs_steps = [
    ["STEP 1: Use same graph (adjacency list)\n6 intersections, 5 roads — model city zones as connected graph", RGBColor(0xE3, 0xF2, 0xFD)],
    ["STEP 2: Initialize Stack with start node\nPush 0 → mark visited → explore deep along each branch before backtracking", RGBColor(0xBB, 0xDE, 0xFB)],
    ["STEP 3: Recursively visit first unvisited neighbor\nGo deep 0→1→3→5, backtrack, then explore 2→4 → covers all nodes", RGBColor(0x90, 0xCA, 0xF9)],
    ["STEP 4: Output traversal order + connected regions\nDetect disconnected zones → plan new roads to connect them 🛣️", RGBColor(0x64, 0xB5, 0xF6)],
]
for i, (text, bg) in enumerate(dfs_steps):
    sy = base_y + i * (step_h + arrow_h + Inches(0.04))
    add_flow_box(slide, col_starts[1], sy, col_w, step_h, text, bg, TEXT_DARK, 9, False)
    if i < len(dfs_steps) - 1:
        add_down_arrow(slide, col_starts[1] + col_w/2 - Inches(0.1), sy + step_h + Inches(0.01), Inches(0.2), arrow_h, ACCENT_BLUE)

# ── Bottom summary bar ──
add_shape(slide, Inches(0.3), Inches(6.55), Inches(12.7), Inches(0.35), RGBColor(0x26, 0x26, 0x26), ACCENT_GREEN)
add_textbox(slide, Inches(0.5), Inches(6.56), Inches(12.0), Inches(0.32),
    "BFS: O(V+E) Queue-based  |  DFS: O(V+E) Stack-based  |  Graph: 6 nodes, 5 edges  |  Both find connected regions in city road network",
    font_size=9, color=RGBColor(0xBB, 0xCC, 0xBB))
add_footer(slide)

# ════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════
# SLIDE 9a: MODULE 4 - SHORTEST PATH (CO4) PART 1 — Dijkstra
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Module 4a: Shortest Path Optimization — Dijkstra (CO4)",
                   "Emergency Routes & Fastest Path Analysis")

# ── Left Panel: DSA Techniques ──
add_shape(slide, Inches(0.4), Inches(1.2), Inches(5.0), Inches(1.7), RGBColor(0xE3, 0xF2, 0xFD), ACCENT_BLUE)
add_textbox(slide, Inches(0.6), Inches(1.22), Inches(4.6), Inches(0.25),
            "📋 Techniques", font_size=12, color=ACCENT_BLUE, bold=True)
add_multiline_textbox(slide, Inches(0.6), Inches(1.5), Inches(4.6), Inches(1.3),
    ["1. Dijkstra — Single-source shortest path (positive weights)",
     "2. Floyd-Warshall → next slide for all-pairs analysis"],
    font_size=10, color=TEXT_DARK, line_spacing=1.3)

# ── Right Panel: Why ──
add_shape(slide, Inches(5.7), Inches(1.2), Inches(7.2), Inches(1.7), RGBColor(0xFD, 0xF2, 0xE3), ACCENT_ORANGE)
add_textbox(slide, Inches(5.9), Inches(1.22), Inches(6.8), Inches(0.25),
            "❓ Why?", font_size=12, color=ACCENT_ORANGE, bold=True)
add_multiline_textbox(slide, Inches(5.9), Inches(1.5), Inches(6.8), Inches(1.3),
    ["• Dijkstra: fastest emergency route with positive edge weights",
     "• Efficient O((V+E) log V) with priority queue"],
    font_size=10, color=TEXT_DARK, line_spacing=1.3)

add_textbox(slide, Inches(0.4), Inches(3.05), Inches(6.0), Inches(0.25),
            "📊 Step-by-Step Flow — Dijkstra Single-Source Shortest Path", font_size=12, color=ACCENT_ORANGE, bold=True)

# ── SINGLE COLUMN: Dijkstra (centered, wider) ──
dx = Inches(1.5); dw = Inches(10.0)
bh = Inches(0.55)
add_shape(slide, dx, Inches(3.35), dw, Inches(0.32), ACCENT_BLUE, ACCENT_BLUE)
add_textbox(slide, dx, Inches(3.35), dw, Inches(0.32),
            "▶ DIJKSTRA: Find Emergency Route (Single-Source Shortest Path)", font_size=13, color=WHITE, bold=True)

d_steps = [
    ("STEP 1: Initialize graph[5][5] with adjacency matrix of 5 city locations\nSet dist[0]=0 (starting location), all other distances = INFINITY, visited[] = false", RGBColor(0xE3, 0xF2, 0xFD)),
    ("STEP 2: Find unvisited node with smallest distance\nminDistance() scans for minimum dist[] value among unvisited nodes", RGBColor(0xE0, 0xF2, 0xF1)),
    ("STEP 3: Relax all neighboring edges of selected node\nif(dist[u] + edge_weight < dist[v]) → update dist[v] with shorter path", RGBColor(0xFD, 0xF2, 0xE3)),
    ("STEP 4: Repeat until all nodes visited\nOutput — Emergency distances: Location 0:0, 1:3, 2:2, 3:8, 4:10 (shortest routes from HQ)", RGBColor(0xC8, 0xE6, 0xC9)),
]
for i, (text, bg) in enumerate(d_steps):
    sy = Inches(3.75) + i * Inches(0.8)
    add_flow_box(slide, dx, sy, dw, bh, text, bg, TEXT_DARK, 11, False)
    if i < len(d_steps) - 1:
        add_down_arrow(slide, dx + dw/2 - Inches(0.1), sy + bh + Inches(0.02), Inches(0.2), Inches(0.15), ACCENT_BLUE)

add_textbox(slide, Inches(0.4), Inches(6.85), Inches(12.0), Inches(0.25),
            "Dijkstra: O((V+E) log V) using priority queue  |  V=5 locations, E=8 roads",
            font_size=10, color=TEXT_GRAY)
add_textbox(slide, Inches(0.5), Inches(7.1), Inches(12), Inches(0.2),
            "UrbanAI | Smart City Infrastructure Optimization Platform  —  Part 1 of 2",
            font_size=8, color=TEXT_GRAY, alignment=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════════
# SLIDE 9b: MODULE 4 - SHORTEST PATH (CO4) PART 2 — Floyd-Warshall
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Module 4b: Shortest Path Optimization — Floyd-Warshall (CO4)",
                   "City Distance Matrix for All-Pairs Urban Planning")

# ── Left Panel: DSA Techniques ──
add_shape(slide, Inches(0.4), Inches(1.2), Inches(5.0), Inches(1.7), RGBColor(0xE3, 0xF2, 0xFD), ACCENT_BLUE)
add_textbox(slide, Inches(0.6), Inches(1.22), Inches(4.6), Inches(0.25),
            "📋 Techniques", font_size=12, color=ACCENT_BLUE, bold=True)
add_multiline_textbox(slide, Inches(0.6), Inches(1.5), Inches(4.6), Inches(1.3),
    ["3. Floyd-Warshall — All-pairs shortest path (V³ dynamic prog)"],
    font_size=10, color=TEXT_DARK, line_spacing=1.3)

# ── Right Panel: Why ──
add_shape(slide, Inches(5.7), Inches(1.2), Inches(7.2), Inches(1.7), RGBColor(0xFD, 0xF2, 0xE3), ACCENT_ORANGE)
add_textbox(slide, Inches(5.9), Inches(1.22), Inches(6.8), Inches(0.25),
            "❓ Why?", font_size=12, color=ACCENT_ORANGE, bold=True)
add_multiline_textbox(slide, Inches(5.9), Inches(1.5), Inches(6.8), Inches(1.3),
    ["• Floyd-Warshall: complete city distance reference table",
     "• One matrix shows shortest path between EVERY pair of locations"],
    font_size=10, color=TEXT_DARK, line_spacing=1.3)

add_textbox(slide, Inches(0.4), Inches(3.05), Inches(6.0), Inches(0.25),
            "📊 Step-by-Step Flow — Floyd-Warshall All-Pairs Shortest Path", font_size=12, color=ACCENT_GREEN, bold=True)

# ── SINGLE COLUMN: Floyd-Warshall (centered, wider) ──
fx = Inches(1.5); fw = Inches(10.0); fh = Inches(0.55)
add_shape(slide, fx, Inches(3.35), fw, Inches(0.32), ACCENT_GREEN, ACCENT_GREEN)
add_textbox(slide, fx, Inches(3.35), fw, Inches(0.32),
            "▶ FLOYD-WARSHALL: Generate City Distance Matrix (All-Pairs)", font_size=13, color=WHITE, bold=True)

fw_steps = [
    ("STEP 1: Create 4×4 adjacency matrix graph[4][4] for 4 city zones\nSet INF where no direct edge exists, 0 on diagonal (distance to self)", RGBColor(0xE3, 0xF2, 0xFD)),
    ("STEP 2: Copy graph → dist[][] matrix\nInitialize dist[i][j] = graph[i][j] for all i,j — this is our starting distance table", RGBColor(0xE0, 0xF2, 0xF1)),
    ("STEP 3: Triple nested loop — for k in 0..3: for i in 0..3: for j in 0..3:\n    if(dist[i][k]+dist[k][j] < dist[i][j]) → update with shorter path via k", RGBColor(0xFD, 0xF2, 0xE3)),
    ("STEP 4: Output all-pairs shortest distance matrix\n0  5  8  9  |  INF 0  3  4  |  INF INF 0  1  |  INF INF INF 0", RGBColor(0xC8, 0xE6, 0xC9)),
]
for i, (text, bg) in enumerate(fw_steps):
    sy = Inches(3.75) + i * Inches(0.8)
    add_flow_box(slide, fx, sy, fw, fh, text, bg, TEXT_DARK, 11, False)
    if i < len(fw_steps) - 1:
        add_down_arrow(slide, fx + fw/2 - Inches(0.1), sy + fh + Inches(0.02), Inches(0.2), Inches(0.15), ACCENT_GREEN)

add_textbox(slide, Inches(0.4), Inches(6.85), Inches(12.0), Inches(0.25),
            "Floyd-Warshall: O(V³)  |  V=4 city zones  |  Dist matrix serves as master route reference table for urban planning",
            font_size=10, color=TEXT_GRAY)
add_textbox(slide, Inches(0.5), Inches(7.1), Inches(12), Inches(0.2),
            "UrbanAI | Smart City Infrastructure Optimization Platform  —  Part 2 of 2",
            font_size=8, color=TEXT_GRAY, alignment=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════
# SLIDE 10a: MODULE 6 - GREEDY & DP (CO6) PART 1 — Activity Sel + Fractional Knapsack
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Module 6a: Greedy Algorithms — Activity Selection & Fractional Knapsack (CO6)",
                   "Maximizing Daily Maintenance Tasks & Resource Allocation")

# ── Left Panel: DSA Techniques ──
add_shape(slide, Inches(0.4), Inches(1.2), Inches(5.0), Inches(1.7), RGBColor(0xE3, 0xF2, 0xFD), ACCENT_BLUE)
add_textbox(slide, Inches(0.6), Inches(1.22), Inches(4.6), Inches(0.25),
            "📋 Techniques", font_size=12, color=ACCENT_BLUE, bold=True)
add_multiline_textbox(slide, Inches(0.6), Inches(1.5), Inches(4.6), Inches(1.3),
    ["1. Activity Selection (Greedy) — Max maintenance tasks",
     "2. Fractional Knapsack (Greedy) — Partial resource allocation",
     "3. 0/1 Knapsack + Edit Distance → next slide"],
    font_size=10, color=TEXT_DARK, line_spacing=1.3)

# ── Right Panel: Why ──
add_shape(slide, Inches(5.7), Inches(1.2), Inches(7.2), Inches(1.7), RGBColor(0xFD, 0xF2, 0xE3), ACCENT_ORANGE)
add_textbox(slide, Inches(5.9), Inches(1.22), Inches(6.8), Inches(0.25),
            "❓ Why Greedy?", font_size=12, color=ACCENT_ORANGE, bold=True)
add_multiline_textbox(slide, Inches(5.9), Inches(1.5), Inches(6.8), Inches(1.3),
    ["• Activity Selection: earliest finish → max tasks scheduled",
     "• Fractional Knapsack: divisible resources → optimal greedy"],
    font_size=10, color=TEXT_DARK, line_spacing=1.3)

add_textbox(slide, Inches(0.4), Inches(3.05), Inches(6.0), Inches(0.25),
            "📊 Step-by-Step — Activity Selection (Left) + Fractional Knapsack (Right)", font_size=12, color=ACCENT_RED, bold=True)

# ── COLUMN 1: Activity Selection ──
ax = Inches(0.3); aw = Inches(5.8); ah = Inches(0.45)
add_shape(slide, ax, Inches(3.35), aw, Inches(0.32), ACCENT_BLUE, ACCENT_BLUE)
add_textbox(slide, ax, Inches(3.35), aw, Inches(0.32),
            "▶ ACTIVITY SELECTION: Schedule Max Maintenance Tasks (Greedy)", font_size=11, color=WHITE, bold=True)

ac_steps = [
    ["STEP 1: Input 4 maintenance tasks (start, finish)\nRoadRepair(8,10), PaintBridge(9,11), CleanPark(10,12), InspectDrain(11,13)", RGBColor(0xE3, 0xF2, 0xFD)],
    ["STEP 2: Create 3 parallel arrays (name, start, finish)\nBubble sort by finish time (ascending) — earliest finish first", RGBColor(0xE0, 0xF2, 0xF1)],
    ["STEP 3: Select first task (earliest finish)\nFor each next task: if start ≥ last_finish → select it (greedy pick)", RGBColor(0xFD, 0xF2, 0xE3)],
    ["STEP 4: Output: Max non-overlapping tasks scheduled\nRoadRepair(8-10) + CleanPark(10-12) = 2 / 4 tasks done ✅", RGBColor(0xC8, 0xE6, 0xC9)],
]
for i, (text, bg) in enumerate(ac_steps):
    sy = Inches(3.75) + i * Inches(0.72)
    add_flow_box(slide, ax, sy, aw, ah, text, bg, TEXT_DARK, 10, False)
    if i < len(ac_steps) - 1:
        add_down_arrow(slide, ax + aw/2 - Inches(0.1), sy + ah + Inches(0.02), Inches(0.2), Inches(0.15), ACCENT_BLUE)

# ── COLUMN 2: Fractional Knapsack ──
kx = Inches(6.5); kw = Inches(6.3)
add_shape(slide, kx, Inches(3.35), kw, Inches(0.32), ACCENT_TEAL, ACCENT_TEAL)
add_textbox(slide, kx, Inches(3.35), kw, Inches(0.32),
            "▶ FRACTIONAL KNAPSACK: Allocate Resources Optimally (Greedy)", font_size=11, color=WHITE, bold=True)

fk_steps = [
    ["STEP 1: Input resources (value, weight, capacity=20)\nAsphalt(50,10), Paint(30,5), Concrete(40,8), Steel(20,4)", RGBColor(0xE3, 0xF2, 0xFD)],
    ["STEP 2: Calculate value/weight ratio — sort descending\nPaint(6.0), Asphalt(5.0), Concrete(5.0), Steel(5.0)", RGBColor(0xE0, 0xF2, 0xF1)],
    ["STEP 3: Take full items while capacity remains\nThen take fraction of next item (partial weight × value)", RGBColor(0xFD, 0xF2, 0xE3)],
    ["STEP 4: Output: Max utility = 105.0\nPaint 5 full + Asphalt 10 full + Concrete 5 partial (62.5%)", RGBColor(0xC8, 0xE6, 0xC9)],
]
for i, (text, bg) in enumerate(fk_steps):
    sy = Inches(3.75) + i * Inches(0.72)
    add_flow_box(slide, kx, sy, kw, ah, text, bg, TEXT_DARK, 10, False)
    if i < len(fk_steps) - 1:
        add_down_arrow(slide, kx + kw/2 - Inches(0.1), sy + ah + Inches(0.02), Inches(0.2), Inches(0.15), ACCENT_TEAL)

add_textbox(slide, Inches(0.4), Inches(6.85), Inches(12.0), Inches(0.25),
            "Activity Selection: O(n log n)  |  Fractional Knapsack: O(n log n)",
            font_size=10, color=TEXT_GRAY)
add_textbox(slide, Inches(0.5), Inches(7.1), Inches(12), Inches(0.2),
            "UrbanAI | Smart City Infrastructure Optimization Platform  —  Part 1 of 2",
            font_size=8, color=TEXT_GRAY, alignment=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════════
# SLIDE 10b: MODULE 6 - GREEDY & DP (CO6) PART 2 — 0/1 Knapsack + Edit Distance
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Module 6b: Dynamic Programming — 0/1 Knapsack & Edit Distance (CO6)",
                   "Project Budgeting & Service Request Auto-Correction")

# ── Left Panel: DSA Techniques ──
add_shape(slide, Inches(0.4), Inches(1.2), Inches(5.0), Inches(1.7), RGBColor(0xE3, 0xF2, 0xFD), ACCENT_BLUE)
add_textbox(slide, Inches(0.6), Inches(1.22), Inches(4.6), Inches(0.25),
            "📋 Techniques", font_size=12, color=ACCENT_BLUE, bold=True)
add_multiline_textbox(slide, Inches(0.6), Inches(1.5), Inches(4.6), Inches(1.3),
    ["3. 0/1 Knapsack (DP) — Discrete project budgeting",
     "4. Edit Distance (DP) — Service request text correction"],
    font_size=10, color=TEXT_DARK, line_spacing=1.3)

# ── Right Panel: Why DP? ──
add_shape(slide, Inches(5.7), Inches(1.2), Inches(7.2), Inches(1.7), RGBColor(0xFD, 0xF2, 0xE3), ACCENT_ORANGE)
add_textbox(slide, Inches(5.9), Inches(1.22), Inches(6.8), Inches(0.25),
            "❓ Why Dynamic Programming?", font_size=12, color=ACCENT_ORANGE, bold=True)
add_multiline_textbox(slide, Inches(5.9), Inches(1.5), Inches(6.8), Inches(1.3),
    ["• 0/1 Knapsack: each project is select/skip → optimal substructure",
     "• Edit Distance: minimum operations needed → overlapping subproblems"],
    font_size=10, color=TEXT_DARK, line_spacing=1.3)

add_textbox(slide, Inches(0.4), Inches(3.05), Inches(6.0), Inches(0.25),
            "📊 Step-by-Step — 0/1 Knapsack DP (Left) + Edit Distance (Right)", font_size=12, color=ACCENT_RED, bold=True)

# ── COLUMN 1: 0/1 Knapsack ──
nx = Inches(0.3); nw = Inches(5.8); nh = Inches(0.45)
add_shape(slide, nx, Inches(3.35), nw, Inches(0.32), ACCENT_ORANGE, ACCENT_ORANGE)
add_textbox(slide, nx, Inches(3.35), nw, Inches(0.32),
            "▶ 0/1 KNAPSACK (DP): Select Best Projects Within Budget", font_size=11, color=WHITE, bold=True)

kp_steps = [
    ["STEP 1: Define 4 projects (cost, value), budget=5\nRoadExpansion(5,10), BridgeRepair(3,6), ParkUpgrade(2,4), DrainageFix(4,8)", RGBColor(0xE3, 0xF2, 0xFD)],
    ["STEP 2: Build DP[n+1][budget+1] table\nInitialize row 0 & col 0 = 0  —  dp[i][w] = max value for i projects, w budget", RGBColor(0xE0, 0xF2, 0xF1)],
    ["STEP 3: For each project i and budget w:\nif cost ≤ w: dp[i][w]=max(dp[i-1][w], value[i]+dp[i-1][w-cost[i]])\nelse: dp[i][w] = dp[i-1][w]", RGBColor(0xFD, 0xF2, 0xE3)],
    ["STEP 4: Backtrack DP table → optimal set\nSelected: RoadExpansion(cost=5,val=10)  →  Total Value = 10 ✅", RGBColor(0xC8, 0xE6, 0xC9)],
]
for i, (text, bg) in enumerate(kp_steps):
    sy = Inches(3.75) + i * Inches(0.72)
    add_flow_box(slide, nx, sy, nw, nh, text, bg, TEXT_DARK, 10, False)
    if i < len(kp_steps) - 1:
        add_down_arrow(slide, nx + nw/2 - Inches(0.1), sy + nh + Inches(0.02), Inches(0.2), Inches(0.15), ACCENT_ORANGE)

# ── COLUMN 2: Edit Distance ──
ex = Inches(6.5); ew = Inches(6.3)
add_shape(slide, ex, Inches(3.35), ew, Inches(0.32), ACCENT_PURPLE, ACCENT_PURPLE)
add_textbox(slide, ex, Inches(3.35), ew, Inches(0.32),
            "▶ EDIT DISTANCE (DP): Auto-Correct Service Request Text", font_size=11, color=WHITE, bold=True)

ed_steps = [
    ["STEP 1: User typed: 'Fix strt lite' (with typos)\nCompare against 5 valid categories in UrbanAI database", RGBColor(0xE3, 0xF2, 0xFD)],
    ["STEP 2: Build DP[m+1][n+1] cost matrix for each pair\nInitialize: dp[i][0]=i (delete all), dp[0][j]=j (insert all)", RGBColor(0xE0, 0xF2, 0xF1)],
    ["STEP 3: For each cell: min of 3 operations\nInsert = dp[i][j-1]+1, Delete = dp[i-1][j]+1, Replace = dp[i-1][j-1]+1(0 if match)", RGBColor(0xFD, 0xF2, 0xE3)],
    ["STEP 4: Find minimum distance across all categories\n'Fix strt lite' → 'Fix Street Light' (Dist=5) ← closest match ✅", RGBColor(0xC8, 0xE6, 0xC9)],
]
for i, (text, bg) in enumerate(ed_steps):
    sy = Inches(3.75) + i * Inches(0.72)
    add_flow_box(slide, ex, sy, ew, nh, text, bg, TEXT_DARK, 10, False)
    if i < len(ed_steps) - 1:
        add_down_arrow(slide, ex + ew/2 - Inches(0.1), sy + nh + Inches(0.02), Inches(0.2), Inches(0.15), ACCENT_PURPLE)

add_textbox(slide, Inches(0.4), Inches(6.85), Inches(12.0), Inches(0.25),
            "0/1 Knapsack: O(n×W)  |  Edit Distance: O(m×n)",
            font_size=10, color=TEXT_GRAY)
add_textbox(slide, Inches(0.5), Inches(7.1), Inches(12), Inches(0.2),
            "UrbanAI | Smart City Infrastructure Optimization Platform  —  Part 2 of 2",
            font_size=8, color=TEXT_GRAY, alignment=PP_ALIGN.CENTER)

# ════════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════════
# SLIDE 11: MAIN METHOD FLOW CHART
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Complete Program Flow — Main.java",
                   "End-to-end execution flow from startup to exit")

# Top: Start
add_flow_box(slide, Inches(5.6), Inches(1.4), Inches(2.0), Inches(0.5), "START\nmain()", RGBColor(0x2C, 0x6F, 0xBB), WHITE, 13, True)
add_down_arrow(slide, Inches(6.6), Inches(1.95), Inches(0.3), Inches(0.2), ACCENT_BLUE)

# Row 1: Initialization
add_flow_box(slide, Inches(0.5), Inches(2.2), Inches(2.8), Inches(0.55), "Initialize AssetManager\n(AVL Tree + PostgreSQL)", RGBColor(0xBB, 0xDE, 0xFB), TEXT_DARK, 11, True)
add_flow_box(slide, Inches(3.7), Inches(2.2), Inches(2.8), Inches(0.55), "Initialize TrafficManager\n(FenwickTree + PostgreSQL)", RGBColor(0xBB, 0xDE, 0xFB), TEXT_DARK, 11, True)
add_flow_box(slide, Inches(6.9), Inches(2.2), Inches(2.8), Inches(0.55), "Initialize Graph\n(6 vertices, + BFS/DFS)", RGBColor(0xBB, 0xDE, 0xFB), TEXT_DARK, 11, True)
add_flow_box(slide, Inches(10.1), Inches(2.2), Inches(2.8), Inches(0.55), "Init Dijkstra &\nFloyd-Warshall objects", RGBColor(0xBB, 0xDE, 0xFB), TEXT_DARK, 11, True)

# Row 2: More init - Greedy/DP only
add_flow_box(slide, Inches(3.7), Inches(3.2), Inches(5.5), Inches(0.45), "Init Greedy/DP Objects\n(ActivitySelection, FractionalKnapsack, Knapsack01, EditDistance)", RGBColor(0xD1, 0xC4, 0xE9), TEXT_DARK, 10, True)

# Arrow to infinite loop
add_down_arrow(slide, Inches(6.6), Inches(2.75), Inches(0.3), Inches(0.2), ACCENT_BLUE)
add_down_arrow(slide, Inches(6.6), Inches(3.65), Inches(0.3), Inches(0.25), ACCENT_BLUE)

# Row 3: Infinite loop
add_flow_box(slide, Inches(0.5), Inches(4.1), Inches(12.3), Inches(0.55), "INFINITE LOOP → Display Menu → Read User Choice (Scanner)", RGBColor(0xE8, 0xF5, 0xE9), ACCENT_GREEN, 13, True)

add_down_arrow(slide, Inches(6.6), Inches(4.7), Inches(0.3), Inches(0.25), ACCENT_BLUE)

# Row 4: Switch cases - 5 groups (sorting removed)
groups = [
    (Inches(0.3), "Cases 1-3\nTrees & Assets", ACCENT_BLUE),
    (Inches(2.3), "Cases 4-7\nTraffic Analytics", ACCENT_TEAL),
    (Inches(4.3), "Cases 8-9\nGraph Algorithms", ACCENT_GREEN),
    (Inches(6.3), "Cases 10-11\nShortest Path", ACCENT_ORANGE),
    (Inches(8.7), "Cases 12-15\nGreedy & DP", ACCENT_RED),
    (Inches(11.3), "Case 0\nExit", RGBColor(0x66, 0x66, 0x66)),
]
for (x, text, color) in groups:
    add_flow_box(slide, x, Inches(5.1), Inches(1.8), Inches(0.55), text, color, WHITE, 9, True)

# Loop back arrow
add_textbox(slide, Inches(5.0), Inches(5.8), Inches(3.0), Inches(0.4),
            "↩ Loop back to Menu Display", font_size=11, color=TEXT_GRAY, bold=True)

for gx in [Inches(1.2), Inches(3.2), Inches(5.2), Inches(7.2), Inches(9.6), Inches(12.2)]:
    add_down_arrow(slide, gx, Inches(5.7), Inches(0.2), Inches(0.2), ACCENT_GREEN)

# Row 5: Output
add_flow_box(slide, Inches(0.5), Inches(6.0), Inches(12.3), Inches(0.5), "Execute Algorithm → Console Output (Results, Reports, Routes, Analytics) → Return to Menu", RGBColor(0xE3, 0xF2, 0xFD), ACCENT_BLUE, 12, True)

# Exit path
add_textbox(slide, Inches(4.5), Inches(6.65), Inches(4.0), Inches(0.4),
            "Case 0: → System.exit(0) → Program Terminates", font_size=13, color=ACCENT_RED, bold=True, alignment=PP_ALIGN.CENTER)

add_footer(slide)


# ════════════════════════════════════════════════════════════════
# SLIDE 12: TOPICS & SCENARIO MAPPING TABLE
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)
add_section_header(slide, "Topics Used & Scenario Mapping",
                   "Every DSA technique mapped to its specific urban management scenario")

# Create a table
from pptx.util import Inches, Pt
rows = 14  # 13 data + 1 header
cols = 3
table_shape = slide.shapes.add_table(rows, cols, Inches(0.5), Inches(1.5), Inches(12.3), Inches(5.0))
table = table_shape.table

# Set column widths
table.columns[0].width = Inches(2.3)
table.columns[1].width = Inches(4.5)
table.columns[2].width = Inches(5.5)

# Header row
headers = ["Module", "DSA Technique", "UrbanAI Scenario Application"]
for i, h in enumerate(headers):
    cell = table.cell(0, i)
    cell.text = h
    for paragraph in cell.text_frame.paragraphs:
        paragraph.font.size = Pt(13)
        paragraph.font.bold = True
        paragraph.font.color.rgb = WHITE
        paragraph.font.name = 'Calibri'
    cell.fill.solid()
    cell.fill.fore_color.rgb = ACCENT_BLUE

# Data rows - removed MST, Bellman-Ford, Topo Sort, and all 4 sorting algorithms
data = [
    ["M1: Trees (CO1)", "AVL Tree / BST", "Index infrastructure assets by AssetID; self-balancing ensures O(log n) search"],
    ["M1: Trees (CO1)", "In-order Traversal", "Generate sorted asset reports without extra sorting pass"],
    ["M1: Trees (CO1)", "Tree Rotations (LL/RR/LR/RL)", "Maintain AVL balance factor after insertions/deletions"],
    ["M2: Range Queries (CO2)", "Fenwick Tree (BIT)", "Cumulative traffic statistics across road segments (prefix sums)"],
    ["M3: Graphs (CO3)", "Graph (Adjacency List)", "Model city road network: intersections=vertices, roads=edges"],
    ["M3: Graphs (CO3)", "BFS", "Shortest path in unweighted roads; connectivity analysis"],
    ["M3: Graphs (CO3)", "DFS", "Cycle detection; identify disconnected infrastructure regions"],
    ["M4: Shortest Path (CO4)", "Dijkstra", "Fastest emergency vehicle route (positive weights)"],
    ["M4: Shortest Path (CO4)", "Floyd-Warshall", "All-pairs city distance matrix for urban planning"],
    ["M6: Greedy & DP (CO6)", "Activity Selection (Greedy)", "Schedule max daily maintenance tasks (RoadRepair, PaintBridge, etc)"],
    ["M6: Greedy & DP (CO6)", "Fractional Knapsack (Greedy)", "Allocate divisible city resources (asphalt, paint, concrete) optimally"],
    ["M6: Greedy & DP (CO6)", "0/1 Knapsack (DP)", "Select infrastructure projects within fixed budget (Road Expansion, etc)"],
    ["M6: Greedy & DP (CO6)", "Edit Distance — Levenshtein (DP)", "Auto-correct citizen service request text with typos"],
]

color_rows = [
    ACCENT_BLUE, ACCENT_TEAL, ACCENT_GREEN, ACCENT_ORANGE,
    RGBColor(0xE3, 0xF2, 0xFD), RGBColor(0xE0, 0xF2, 0xF1), RGBColor(0xE8, 0xF5, 0xE9),
    RGBColor(0xFD, 0xF2, 0xE3), RGBColor(0xF3, 0xE5, 0xF5),
    RGBColor(0xE0, 0xF2, 0xF1), RGBColor(0xFF, 0xEB, 0xEE), RGBColor(0xE3, 0xF2, 0xFD),
    RGBColor(0xE8, 0xF5, 0xE9),
]

for r in range(1, rows):
    for c in range(3):
        cell = table.cell(r, c)
        cell.text = data[r-1][c]
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(10)
            paragraph.font.color.rgb = TEXT_DARK
            paragraph.font.name = 'Calibri'
        cell.fill.solid()
        cell.fill.fore_color.rgb = color_rows[r-1]

add_footer(slide)


# ════════════════════════════════════════════════════════════════
# SLIDE 13: CONCLUSION
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, RGBColor(0x1A, 0x1A, 0x2E))

# Decorative circles
add_decorative_circle(slide, Inches(-1), Inches(4), Inches(3), ACCENT_BLUE, 12)
add_decorative_circle(slide, Inches(11), Inches(-1), Inches(3), ACCENT_TEAL, 10)

# Top accent
line = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(1.5), Inches(10.333), Inches(0.04)
)
line.fill.solid()
line.fill.fore_color.rgb = ACCENT_TEAL
line.line.fill.background()

add_textbox(slide, Inches(1.5), Inches(1.8), Inches(10.333), Inches(0.8),
            "Conclusion", font_size=40, color=WHITE, bold=True)

conclusion_points = [
    "✓ UrbanAI successfully demonstrates 15+ Data Structure & Algorithm implementations mapped to real-world smart city scenarios — bridging the gap between theoretical DSA concepts and practical urban management.",
    "",
    "✓ The modular architecture (5 CO-aligned modules) with PostgreSQL integration showcases production-ready software engineering practices — database persistence, OOP design, and menu-driven interaction.",
    "",
    "✓ Performance is optimized at every layer: AVL Trees for O(log n) asset search, Fenwick Trees for O(log n) traffic analytics, Graph algorithms for network optimization, and Greedy/DP for resource allocation.",
    "",
    "✓ The platform is extensible — new algorithms (B-Trees, A* Search, Trie-based geo-indexing) can be added as new modules without disrupting existing functionality.",
    "",
    "✓ UrbanAI proves that mastering Data Structures & Algorithms is the foundation for building intelligent, scalable, and responsive urban infrastructure systems."
]

add_multiline_textbox(slide, Inches(1.5), Inches(2.8), Inches(10.333), Inches(4.0),
                      conclusion_points, font_size=14, color=RGBColor(0xD0, 0xD8, 0xF0),
                      line_spacing=1.5, alignment=PP_ALIGN.LEFT)

# Bottom accent
line2 = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(6.8), Inches(10.333), Inches(0.04)
)
line2.fill.solid()
line2.fill.fore_color.rgb = ACCENT_TEAL
line2.line.fill.background()

add_textbox(slide, Inches(1.5), Inches(6.9), Inches(10.333), Inches(0.5),
            '"Building Smarter Cities, One Algorithm at a Time"',
            font_size=16, color=ACCENT_TEAL, bold=True)


# ════════════════════════════════════════════════════════════════
# SAVE THE PRESENTATION
# ════════════════════════════════════════════════════════════════
output_path = "D:\\UrbanAI\\UrbanAI_Presentation.pptx"

import os, time

# Force-kill any PowerPoint process holding the file (optional - warn only)
try:
    if os.path.exists(output_path):
        os.remove(output_path)
except (PermissionError, OSError):
    # Fallback: use timestamped name
    ts = time.strftime("%Y%m%d_%H%M%S")
    output_path = f"D:\\UrbanAI\\UrbanAI_Presentation_{ts}.pptx"

prs.save(output_path)
print(f"Presentation saved successfully to: {output_path}")
print(f"Total slides: {len(prs.slides)}")
