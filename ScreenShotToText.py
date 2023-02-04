from threading import Thread
from ClipHandlerS import Clipboard
from PIL import Image
from imageToText import Texter
import io

DEBUG = True

IMAGE_PROCESSED = 0

def processClip(clip):
    global IMAGE_PROCESSED
    IMAGE_PROCESSED += 1
    print("Cliped")
    print(f'[{IMAGE_PROCESSED}]', clip.type)

def processImage(clip):
    global IMAGE_PROCESSED
    print(f"\t[{IMAGE_PROCESSED}] Accepted image from clipboard\n{'_'*50}")
    IMAGE_PROCESSED += 1
    img = Image.open(io.BytesIO(clip))
    img_jpg = img.convert('RGB')
    TexterR = Texter()
    TexterR.setTesseractConfig(1, 1)
    print(TexterR(img_jpg).strip())
    print(f"{'‾'*50}\n\t[-] Image processed")


if __name__ == '__main__':
    if DEBUG: print(f"Starting clipboard daemon..")
    clipboard = Clipboard(on_image=processImage, check_start_clip=True)
    clipThread = Thread(target=clipboard.listen, daemon=True)
    if DEBUG: print(f"Clipboard daemon state: {clipThread}")
    clipThread.start()
    if DEBUG: print(f"Clipboard daemon state set to 'work'")
    while True:
        pass


'''
when I was on vacation watching videos about AI, then there were just all the lessons at this level, install 2 packages,
 write 2 lines and here you are progers)
это да, но мне хочется все же самому модели писать, вдруг на работе попросят что то особенное написать
а так да много готового

'''