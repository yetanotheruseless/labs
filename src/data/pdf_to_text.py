import os.path
from typing import List
import copy
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


@dataclass
class TextBlock:
    spans: List[TextSpan]
    page_num: int
    block_num: int

    def to_json(self, text_only=True):
        if text_only:
            return {
                "text": " ".join([span.text for span in self.spans]),
                "page_num": self.page_num,
                "block_num": self.block_num
            }
        else:
            return {
                "spans": [span.to_json() for span in self.spans],
                "page_num": self.page_num,
                "block_num": self.block_num
            }


def group_text_spans_by_block(text_spans: List[TextSpan]) -> List[TextSpan]:
    # First, sort the list by block_num and line_num
    text_spans.sort(key=lambda x: (x.block_num, x.line_num))
    grouped_text_spans = []
    current_span = None
    current_block_num = None
    current_text = ""
    for span in text_spans:
        current_span = span
        if current_block_num is None:
            current_block_num = span.block_num
            current_text = span.text
        elif current_block_num == span.block_num:
            current_text += (" " + span.text)
        else:
            new_span = copy.deepcopy(span)
            new_span.text = current_text
            new_span.line_num = 0
            grouped_text_spans.append(new_span)
            current_block_num = span.block_num
            current_text = span.text
    if current_text:
        new_span = copy.deepcopy(current_span)
        new_span.text = current_text
        new_span.line_num = 0
        grouped_text_spans.append(new_span)
    return grouped_text_spans


def span_to_json(span: TextSpan):
    return {
        "superscript": span.superscript,
        "italic": span.italic,
        "serifed": span.serifed,
        "sans": span.sans,
        "monospaced": span.monospaced,
        "proportional": span.proportional,
        "bold": span.bold,
        "font": span.font,
        "size": span.size,
        "color": span.color,
        "text": span.text,
        "page_num": span.page_num,
        "block_num": span.block_num,
        "line_num": span.line_num,
    }


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
    median_font_size = sorted([span.size for span in spans])[len(spans) // 2]
    return [span for span in spans if span.size >= median_font_size]


def extract_bold_and_italic(spans: List[TextSpan]):
    return [span for span in spans if span.bold or span.italic]


def concat_raw_text(span_list: List[TextSpan]) -> List[str]:
    return [span.text for span in span_list]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_to_text.py <pdf_path>")
        sys.exit(1)

    path = sys.argv[1]
    pdf_files = []
    # if the path is a directory
    if os.path.isdir(path):
        # list all files in the directory
        pdf_files = os.listdir(path)
    else:
        pdf_files.append(path)

    for pdf_path in [x for x in pdf_files if x.endswith(".pdf")]:
        out_prefix = pdf_path.replace(".pdf", "")
        out_text_path = out_prefix + ".txt"
        out_footnotes_path = out_prefix + "_footnotes.txt"

        all_spans = extract_text_blocks(pdf_path)
        bold_italic_spans = extract_bold_and_italic(all_spans)
        all_spans = drop_footnotes(all_spans)
        body_text: List[str] = concat_raw_text(all_spans)
        bold_italic_text: List[str] = concat_raw_text(bold_italic_spans)

        with open(out_text_path, "w") as f:
            for line in body_text:
                f.write(line + "\n")

        with open(out_footnotes_path, "w") as f:
            for line in bold_italic_text:
                f.write(line + "\n")
