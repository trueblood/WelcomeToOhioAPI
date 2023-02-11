from PIL import Image

import pytesseract


##print(pytesseract.image_to_string(Image.open('png-transparent-black-family-text-word-family-friends-word-s-white-text-presentation.png')))
print(pytesseract.image_to_string(Image.open('Scanned Document.png')))