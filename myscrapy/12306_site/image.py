#-*- coding=utf-8 -*-

import pytesser
import ImageEnhance
from PIL import Image
"""
im = Image.open('3.png')
#显示图片
#im.show()
"""
image = Image.open('3.png')
print(pytesser.Image_to_string(image))

