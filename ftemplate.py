import sys
import io
import os
from abc import ABC, abstractmethod

from PyPDF2 import PdfFileWriter, PdfFileReader

from reportlab.lib.units import inch
from reportlab.lib.colors import pink, green, brown, white, black
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import pickle

# Paths
WORK_DIR = os.getcwd();

RES_DIR = os.path.join(WORK_DIR, "resources/")
TEMPLATES_DIR = os.path.join(WORK_DIR, "templates/")

FONTS_DIR = os.path.join(RES_DIR, "fonts/")
IMAGES_DIR = os.path.join(RES_DIR, "img/")

# load fonts
pdfmetrics.registerFont(TTFont('Gardens', os.path.join(FONTS_DIR, "Gardens CM Regular.ttf")))

#loads pdf file bytes
def load_file(path):
    with open(path, "rb") as f:
        data = f.read()
    return data

#Saves pdf file bytes
def save_file(data, path):
    with open(path, "wb") as f:
        f.write(data)

# Loads template from file
def load_teplate(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

# Saves template to file
def save_template(template, path):
    with open(path, 'wb') as f:
        pickle.dump(template, f)


class Form():

    def __init__(self, template, fields_values: dict):
        self.template = template
        self.fields_values = fields_values

    #draws transparent watermark on canv
    def draw_watermark(self, canv, visible=False):
        if visible:
            color = Color(0, 0, 0, 0.4)
        else:
            color = Color(0, 0, 0, 0)

        canv.setFillColor(color)
        canv.drawString(10, 10, "♥")
        return canv

    # merges template with values
    # returns marged pdf bytes
    def apply(self):
        # read template PDF data
        template_pdf = PdfFileReader(io.BytesIO(self.template.pdf_data))
        #
        pages_count = template_pdf.getNumPages()

        output = PdfFileWriter()

        #draw fields values
        for i in range(pages_count):
            # create a new PDF page with Reportlab
            packet = io.BytesIO()
            canv = canvas.Canvas(packet, pagesize=letter)

            # если ничего не нарисовать на канвасе,
            # PdfFileReader не создаст из него страницу.
            canv = self.draw_watermark(canv, visible=False)

            for field_name, field in self.template.fields.items():
                if field.page != i:
                    continue
                #draw values
                value = self.fields_values[field_name]
                canv = field.draw(canv, value)

            canv.save()

            #move to the beginning of the StringIO buffer
            packet.seek(0)
            new_pdf = PdfFileReader(packet)

            # add the fields values on template pages
            page = template_pdf.getPage(i)
            page.mergePage(new_pdf.getPage(0))
            output.addPage(page)

        output_data = io.BytesIO()
        output.write(output_data)
        output_data.flush()

        return output_data.getbuffer()


class Template:

    def __init__(self, name: str, fields: dict, pdf_data):
        # template name
        self.name = name
        # dict: {field_name: Field}
        self.fields = fields
        # pdf bytes
        self.pdf_data = pdf_data


class Field(ABC):

    def __init__(self, x = 0, y = 0, page = 0):
        # pos on page
        # (0, 0) - bottom left
        self.x = x
        self.y = y
        # page, where it'll appear
        self.page = 0

    @abstractmethod
    def draw(self, canv, value: str):
        return canv

    def __repr__(self):
        re = "{field_name}: ".format(field_name = self.__class__.__name__)
        for key, val in self.__dict__.items():
            re += "\n\t{key}: {val}".format(key=key, val=val)
        re += "\n"
        return re


class ImageField(Field):

    def __init__(self, x, y, w, h, img, page = 0):
        Field.__init__(srlf, x, y, page)
        self.w = w
        self.h = h
        self.img = img

    def draw(self, canv, value):
        return canv


class SelectField(ImageField):

    def __init__(self, x, y, w, h):
        img = ImageReader(os.path.join(IMAGES_DIR, "select.jpg"))
        ImageField.__init__(self, x, y, w, h, img)


class TextField(Field):

    def __init__(self, x, y, text, page=0, font="Gardens", font_size=10):
        Field.__init__(self, x, y, page)
        self.text = text
        self.font = font
        self.font_size = font_size

    @abstractmethod
    def draw(self, canv, value):
        return canv

class SimpleTextField(TextField):

    def draw(self, canv, value):
        return canv

class BlockTextField(TextField):

    def draw(sefl, canv, value):
        return canv


if __name__ == '__main__':
    tmp_pdf_data = load_file("test.pdf")

    fields = {
        "test_field_0": SimpleTextField(3, 4, "aaa"),
        "test_field_1": SimpleTextField(10, 10, "bbb")
    }

    temp = Template(name="zzz", fields=fields, pdf_data=tmp_pdf_data)
    save_template(temp, os.path.join(TEMPLATES_DIR, "xxx.tmplz"))

    temp2 = load_teplate(os.path.join(TEMPLATES_DIR, "xxx.tmplz"))

    print(temp2.name)
    print(temp2.fields)
    #print(temp2.pdf_data)

    values = {
        "test_field_0": "йцукенгшщз",
        "test_field_1": "\( Ф _ Ф )/♥\( = з = )/"
    }

    form = Form(template=temp2, fields_values=values)

    out_pdf_data = form.apply()

    save_file(out_pdf_data, "tttttttttt.pdf")



"""
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

"""
