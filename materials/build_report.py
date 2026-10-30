"""Typeset the final Markdown report without executing any model code."""
import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--font-dir", type=Path, default=Path("C:/Windows/Fonts"))
    args = parser.parse_args()
    for name, file in (("Report", "times.ttf"), ("Report-Bold", "timesbd.ttf"),
                       ("Report-Italic", "timesi.ttf"), ("Report-BoldItalic", "timesbi.ttf")):
        pdfmetrics.registerFont(TTFont(name, str(args.font_dir / file)))
    pdfmetrics.registerFontFamily("Report", normal="Report", bold="Report-Bold",
                                  italic="Report-Italic", boldItalic="Report-BoldItalic")
    navy = colors.black
    styles = {
        "body": ParagraphStyle("body", fontName="Report", fontSize=10.2,
                               leading=12.9, spaceAfter=5, textColor=colors.black),
        "title": ParagraphStyle("title", fontName="Report-Bold", fontSize=21,
                                leading=23, spaceAfter=13, textColor=navy),
        "h2": ParagraphStyle("h2", fontName="Report-Bold", fontSize=15,
                             leading=17, spaceBefore=10, spaceAfter=7, keepWithNext=True,
                             textColor=navy),
        "h3": ParagraphStyle("h3", fontName="Report-Bold", fontSize=12,
                             leading=15, spaceBefore=8, spaceAfter=6, keepWithNext=True),
        "cell": ParagraphStyle("cell", fontName="Report", fontSize=9.0,
                               leading=11.1, spaceAfter=0),
        "headcell": ParagraphStyle("headcell", fontName="Report-Bold", fontSize=9.0,
                                   leading=11.1, textColor=colors.black),
        "meta": ParagraphStyle("meta", fontName="Report", fontSize=9.6,
                               leading=11.5, spaceAfter=3, textColor=navy),
        "math": ParagraphStyle("math", fontName="Report", fontSize=10.5,
                               leading=16, spaceBefore=6, spaceAfter=10,
                               alignment=TA_CENTER),
    }

    def inline(value):
        value = value.replace("–", "-").replace("—", "-").replace("−", "-")
        value = value.replace("⁻¹⁰", "<super>-10</super>")
        value = value.replace("θ₀", "θ<sub>0</sub>").replace("s₀", "s<sub>0</sub>")
        value = value.replace("²", "<super>2</super>")
        # Markdown links, inline code and emphasis are the only accepted markup.
        tags = {}
        def save(text):
            key = f"ZZTAG{len(tags)}ZZ"
            tags[key] = text
            return key
        value = re.sub(r"<(/?)(super|sub)>", lambda m: save(m.group()), value)
        value = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
                       lambda m: save('<a href="' + html.escape(m.group(2), quote=True) +
                                      '" color="#000000">' + html.escape(m.group(1)) + '</a>'), value)
        value = re.sub(r"`([^`]+)`", lambda m: save('<font size="9.7">' + html.escape(m.group(1)) + '</font>'), value)
        value = html.escape(value)
        value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
        for key, tag in tags.items():
            value = value.replace(key, tag)
        return value

    text = args.source.read_text(encoding="utf-8")
    # Replace display LaTeX with compact, readable equations in the same notation.
    formulas = iter([
        "s(q,g) = φ(q,g)<super>T</super>(θ<sub>0</sub> + δ),  "
        "1,034 + 26 + 4,096 + 24 = 5,180.",
        "L(δ) = (1/|D|) Σ<sub>q in D</sub> (1/|P<sub>q</sub>|) "
        "Σ<sub>(g+,g-) in Pq</sub> log(1 + exp[-(s(q,g+) - s(q,g-))])"
        " + (λ/2)‖δ‖<super>2</super><sub>2</sub>.",
    ])
    text = re.sub(r"\\\[.*?\\\]", lambda m: "\n@@FORMULA " + next(formulas) + "\n", text, flags=re.S)
    lines = text.splitlines()
    story = []
    i = 0
    page_starts = ("## 3.", "## 4.", "### 4.3", "## 6.")
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith(page_starts):
            story.append(PageBreak())
        if line.startswith("@@FORMULA "):
            story.append(Paragraph(line[len("@@FORMULA "):], styles["math"]))
        elif line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["title"]))
        elif line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), styles["h3"]))
        elif line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), styles["h2"]))
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [v.strip() for v in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            n = len(rows[0])
            if n == 2:
                widths = [350, 145]
            elif n == 3:
                widths = [205, 110, 180]
            elif n == 4:
                widths = [225, 90, 90, 90]
            else:
                widths = [80, 50, 95, 95, 175]
            data = [[Paragraph(inline(c), styles["headcell" if r == 0 else "cell"])
                     for c in row] for r, row in enumerate(rows)]
            table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("LINEABOVE", (0, 0), (-1, 0), 1.0, colors.black),
                ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LINEBELOW", (0, -1), (-1, -1), 1.0, colors.black),
            ]))
            story.extend([table, Spacer(1, 9)])
            continue
        else:
            paragraph = line
            while (i + 1 < len(lines) and lines[i + 1].strip()
                   and not lines[i + 1].lstrip().startswith(("#", "|", "@@FORMULA"))
                   and not lines[i].endswith("  ")):
                i += 1
                paragraph += " " + lines[i].strip()
            style = "meta" if i < 6 else "body"
            story.append(Paragraph(inline(paragraph), styles[style]))
        i += 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(args.output), pagesize=A4, leftMargin=50, rightMargin=50,
                            topMargin=46, bottomMargin=43,
                            title="Selecting Reliable LLM Answers - DASE7506 MP2",
                            author="Liang Zefeng (3036798641)",
                            subject="Frozen joint ranker, evidence and reproducibility")
    def decorate(canvas, doc):
        width, height = A4
        canvas.saveState()
        canvas.setStrokeColor(colors.black)
        canvas.line(50, 34, width - 50, 34)
        canvas.setFont("Report", 8.5)
        canvas.setFillColor(colors.black)
        canvas.drawString(50, 22, "DASE7506 MP2  |  Liang Zefeng  |  3036798641")
        canvas.drawRightString(width - 50, 22, str(doc.page))
        canvas.restoreState()
    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    print(args.output)


if __name__ == "__main__":
    main()
