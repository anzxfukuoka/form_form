#
# файл с глобальными переменными
#

import os

# paths
WORK_DIR = os.getcwd();

RES_DIR = os.path.join(WORK_DIR, "resources/")

TEMPLATES_DIR = os.path.join(WORK_DIR, "templates/")

FONTS_DIR = os.path.join(RES_DIR, "fonts/")
IMAGES_DIR = os.path.join(RES_DIR, "img/")

UI_DIR = os.path.join(RES_DIR, "ui/")

# template file end
EXT = ".tmplz"

# ui files
UI_MAIN_WINDOW = os.path.join(UI_DIR, "MainWindow.ui")
UI_TEMPLATES_MANAGER = os.path.join(UI_DIR, "TemplatesManager.ui")

IC_APP_ICON = os.path.join(RES_DIR, "ico.png")
