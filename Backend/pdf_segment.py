import fitz
# doc = fitz.open("blog1.pdf")

class PDFSegmenter():
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def image_crafter(self):
        doc = fitz.open(self.pdf_path)
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:       # this is GRAY or RGB
                    pix.writePNG("jina-image/data/page%s-%s.png" % (i, xref))
                else:               # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.writePNG("jina-image/data/page%s-%s.png" % (i, xref))
                    pix1 = None
                pix = None
    def text_crafter(self, save_file_name):
        with fitz.open(self.pdf_path) as doc:
            text = ""
            for page in doc:
                text += page.getText().strip()
            with open(f'jina-text/{save_file_name}.txt', 'w') as file:
                file.write(text)
            print(text)

s = PDFSegmenter('blog2.pdf')
# s.text_crafter()
s.image_crafter()