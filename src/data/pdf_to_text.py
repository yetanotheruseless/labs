from typing import List
from dataclasses import dataclass
import fitz


@dataclass
class TextSpan:
    superscript: bool = False
    italic: bool = False
    serifed: bool = False
    sans: bool = False
    monospaced: bool = False
    proportional: bool = False
    bold: bool = False
    font: str = ""
    size: int = 0
    color: str = ""
    text: str = ""
    page_num: int = 0
    block_num: int = 0
    line_num: int = 0


def flags_decomposer(flags) -> TextSpan:
    font_flags = TextSpan()
    if flags & 2 ** 0:
        font_flags.superscript = True
    if flags & 2 ** 1:
        font_flags.italic = True
    if flags & 2 ** 2:
        font_flags.serifed = True
    else:
        font_flags.sans = True
    if flags & 2 ** 3:
        font_flags.monospaced = True
    else:
        font_flags.proportional = True
    if flags & 2 ** 4:
        font_flags.bold = True
    return font_flags


def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    spans = []
    for i, page in enumerate(doc):
        blocks = page.get_text("dict", flags=11)["blocks"]
        for j, block in enumerate(blocks):
            for k, line in enumerate(block["lines"]):
                for span in line["spans"]:
                    text_span = flags_decomposer(span["flags"])
                    text_span.font = span["font"]
                    text_span.size = span["size"]
                    text_span.color = span["color"]
                    text_span.text = span["text"]
                    text_span.page_num = i
                    text_span.block_num = j
                    text_span.line_num = k
                    spans.append(text_span)
    return spans


def drop_footnotes(spans: List[TextSpan]):
    avg_font_size = sum([span.size for span in spans]) / len(spans)
    return [span for span in spans if span.size >= avg_font_size]


def extract_bold_and_italic(spans: List[TextSpan]):
    return [span for span in spans if span.bold or span.italic]


def concat_raw_text(spans: List[TextSpan]):
    return " ".join([span.text for span in spans])


