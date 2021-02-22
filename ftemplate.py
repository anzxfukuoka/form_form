import sys
import io
import os
from abc import ABC, abstractmethod

from PyPDF2 import PdfFileWriter, PdfFileReader

from reportlab.lib.units import inch, cm
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

#file end
EXT = ".tmplz"

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


# merges template with values
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
        canv.drawString(10 * cm, 10 * cm, "♥")
        return canv

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

    def __init__(self, name: str, fields: dict, pdf_data: bytes):
        # template name
        self.name = name
        # dict: {field_name: Field}
        self.fields = fields
        # pdf bytes
        self.pdf_data = pdf_data

    def __repr__(self):
        return "Template: {}\n{}".format(self.name, self.fields)


class Field(ABC):

    def __init__(self, x = 0, y = 0, page = 0):
        # pos on page in cm
        # (0, 0) - bottom left
        self.x = x * cm
        self.y = y * cm
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

    #x, y, w, h - image crop rect
    def __init__(self, x, y, w, h, page=0):
        Field.__init__(self, x, y, page)
        self.w = w * cm
        self.h = h * cm

    # value - path to image
    def draw(self, canv, value):
        img = ImageReader(value)

        img_w, img_h = img.getSize()

        #crop by min side
        if self.w > self.h:
            k = self.h / img_h
        else:
            k = self.w / img_w

        width = img_w * k
        height = img_h * k

        #center align
        cx = self.w / 2 - width / 2
        cy = self.h / 2 - height / 2

        canv.drawImage(img, self.x + cx, self.y + cy, width, height, mask='auto')

        #debug
        canv.setStrokeColor(green)
        canv.roundRect(self.x, self.y, self.w, self.h, 4, stroke=1, fill=0)

        return canv


class SelectField(ImageField):

    def __init__(self, x, y, size=1, page=0):
        ImageField.__init__(self, x, y, size, size, page)

    def draw(self, canv, value):
        return super().draw(canv, os.path.join(IMAGES_DIR, "select.png"))


class TextField(Field):

    def __init__(self, x, y, page=0, font="Gardens", font_size=10, color = black):
        Field.__init__(self, x, y, page)
        self.font = font
        self.font_size = font_size
        self.color = color

    @abstractmethod
    def draw(self, canv, value):
        #set text settings
        canv.setFont(self.font, self.font_size)
        canv.setFillColor(self.color)

        return canv

class SimpleTextField(TextField):

    def draw(self, canv, value):
        #sets text settings
        canv = super().draw(canv, value)
        #draw
        canv.drawString(self.x, self.y, value.encode("utf-8"))

        return canv

class BlockTextField(TextField):

    def __init__(self, x, y, page=0, font="Gardens", font_size=10, color = black, block_width = 4):
        TextField.__init__(self, x, y, page, font, font_size, color)
        self.block_width = block_width

    def draw(self, canv, value):
        #sets text settings
        canv = super().draw(canv, value)
        #add gaps
        value = (" " * self.block_width).join(list(value))
        #draw
        canv.drawString(self.x, self.y, value.encode("utf-8"))

        return canv


if __name__ == '__main__':
    #test

    tmp_pdf_data = load_file("test.pdf")

    fields = {
        "test_field_0": SimpleTextField(x=1, y=1),
        "test_field_1": SimpleTextField(x=10, y=10),
        "test_field_2": BlockTextField(x=1, y=16, font_size=20),
        "test_field_3": ImageField(x=6, y=16, w=10, h=6),
        "test_field_4": SelectField(x=2, y=6, size=6),
    }

    temp = Template(name="testtets", fields=fields, pdf_data=tmp_pdf_data)
    save_template(temp, os.path.join(TEMPLATES_DIR, "0xxx.tmplz"))

    temp2 = load_teplate(os.path.join(TEMPLATES_DIR, "0xxx.tmplz"))

    print(temp2.name)
    print(temp2.fields)
    #print(temp2.pdf_data)

    values = {
        "test_field_0": "йцукенгшщз",
        "test_field_1": "\( Ф _ Ф )/♥\( = з = )/",
        "test_field_2": "@@@@@@@@@@@@@@@@@",
        "test_field_3": os.path.join(WORK_DIR, "unnamed.jpg"),
        "test_field_4": None
    }

    form = Form(template=temp2, fields_values=values)

    out_pdf_data = form.apply()

    save_file(out_pdf_data, "tttttttttt.pdf")
