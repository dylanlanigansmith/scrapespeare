import ctypes
import os
import json
from PIL import Image
from io import BytesIO




def ocr_image(img,format='PNG'):
    # Load the dynamic library
    lib = ctypes.cdll.LoadLibrary(os.path.abspath("./libocrlib.dylib"))

    # Define the argument and return types for the Swift function
    lib.extractText.restype = ctypes.c_char_p
    lib.extractText.argtypes = [ctypes.c_void_p, ctypes.c_int]

    # Convert the image to bytes
    output = BytesIO()
    img.save(output, format=format)
    img_bytes = output.getvalue()

    # Pass the image bytes and its length to the Swift function
    result = lib.extractText(img_bytes, len(img_bytes))

    if result:
        result_json = result.decode('utf-8')
        data = json.loads(result_json)
        print("Extracted Texts and Positions:")
        print(json.dumps(data, indent=2))
        return data
    else:
        print("fail")
        return None


img = Image.open("./screenshot.png")


print(ocr_image(img))
