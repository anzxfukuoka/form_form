import io
from abc import ABC, abstractmethod

from PyPDF2 import PdfFileWriter, PdfFileReader

from reportlab.lib.units import inch
from reportlab.lib.colors import pink, green, brown, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import pickle


#load fonts
pdfmetrics.registerFont(TTFont('Gardens', 'fonts/Gardens CM Regular.ttf'))


class Template:
    def __init__(self, name, fields_data, form_data):
        self.name = name
        self.fields_data = fields_data
        self.form_data = form_data


class Field(ABC):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self, canv):
        pass

    def __repr__(self):
        return "pos: " + str(self.x) + " : " + str(self.y)


class TextField(Field):

    def __init__(self, x, y, text, font="Gardens", font_size=10):
        Field.__init__(self, x, y)
        self.text = text
        self.font = font
        self.font_size = font_size


class AbstractFieldBuilder(ABC):
    @abstractmethod
    def create_text_field(self) -> TextField:
        pass

    @abstractmethod
    def create_select_field(self):
        pass

    @abstractmethod
    def create_image_field(self):
        pass

#temp = Template("z", [Field(3, 4), Field(10, 10)], b"\100\000")

def load_teplate(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

def save_template(template, path):
    with open(path, 'wb') as f:
        pickle.dump(template, f)


#save_template(temp, "templates/xxx.tmplz")
temp2 = load_teplate("templates/xxx.tmplz")
print(temp2.name)
print(temp2.fields_data)
print(temp2.form_data)

#packet = PdfFileReader("test.pdf")
packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(10, 10, "Hello world")

logo = logo = ImageReader('sign.png')
can.drawImage(logo, 10, 100, mask='auto')

size = 7
y = 2.3 * inch
x = 1.3 * inch



for line in ["ебанный рот", "этого казино", "блять"]:
    can.setFont("Gardens", size)
    can.setFillColor(pink)
    can.drawRightString(x, y, "%s points: " % size)
    can.drawString(x,y, line.encode("utf-8"))
    y = y - size * 1.2
    size = size + 1.5

can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(io.BytesIO(open("test.pdf", "rb").read()))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open("destination.pdf", "wb")
output.write(outputStream)
outputStream.close()

simple_template = {
"name" : "????",
"fields" : {
        "field_0" : {
            "type" : "block",
            "x": 0,
            "y": 0,
        }
    },
"original" : "ляля..."
}
