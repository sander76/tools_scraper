from pdfrw import PdfReader, PdfWriter, PageMerge


def fixpage(*pages):
    result = PageMerge() + (x for x in pages if x is not None)
    result[-1].x += result[0].w
    return result.render()


def make_booklet(pdf_file: str, out_put: str = None) -> None:
    out_put = out_put if out_put is not None else pdf_file
    ipages = PdfReader(pdf_file).pages

    if len(ipages) & 1:
        ipages.append(None)

    opages = []
    while len(ipages) > 2:
        opages.append(fixpage(ipages.pop(), ipages.pop(0)))
        opages.append(fixpage(ipages.pop(0), ipages.pop()))

    opages += ipages

    PdfWriter().addpages(opages).write(out_put)


if __name__ == "__main__":

    make_booklet("test/M25T data sheet.pdf", "test/output.pdf")
    make_booklet("test/M25T data sheet 1.pdf")
