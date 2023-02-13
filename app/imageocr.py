from PIL import Image

import pytesseract

class ImageOCR:
    def get_Text_From_Image(imageName):
        return pytesseract.image_to_string(Image.open(imageName))
