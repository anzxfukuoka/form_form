import json





class DataField:
    def __init__(self):
        self.x = 0
        self.y = 0

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canv):
        pass

class BlockField(DataField):
    pass

class StraightField(DataField):
    pass

class ImageField(DataField):
    pass

class BoolField(BlockField):
    pass

class TextField(StraightField):
    pass

class DateField(StraightField):
    pass

class BlockTextField(BlockField):
    pass

class BlockTextField(BlockField):
    pass

class Template:
    def __init__(self, name: str, data: dict, images: list):
        self.name = name
        self.data = data
        self.images = images

    def save_to_file(template, path):
        template_data = template.__dict__()
        with open(path, "w", encoding="UTF-8") as file:
            json.dump(template_data, file)

    def load_from_file(path):
        with open(path, "r", encoding="UTF-8") as json_file:
            template_data = json.load(json_file)
        tmp = Template(template_data["name"], template_data["data"], template_data["images"])
        return tmp
