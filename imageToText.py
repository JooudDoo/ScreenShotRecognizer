import cv2
import numpy as np
from pytesseract import pytesseract
from PIL import Image

path_to_tesseract = r"D:/tools/TesseractPython/tesseract.exe"
pytesseract.tesseract_cmd = path_to_tesseract

tesseract_config = r'--oem 1 --psm 1'

SCALE_COEFF : int = 5

class Texter():

    def __init__(self):
        pass

    @staticmethod
    def _extractContoursFromImage(img):
        cvimg = np.array(img)
        h,w,_ = cvimg.shape
        cvimg = cv2.resize(cvimg, (w * SCALE_COEFF, h * SCALE_COEFF))
        grayImg = cv2.cvtColor(cvimg, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(grayImg, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        dilation = cv2.dilate(
            thresh,
            cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12)),
            iterations=3
        )
        contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours, grayImg

    def __call__(self, img) -> str:
        contours, cvimg = self._extractContoursFromImage(img)
        resultText = ''
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            cropped = cvimg[y:y + h, x:x + w]
            newLine = pytesseract.image_to_string(cropped, lang='rus+eng', config=tesseract_config).strip()
            if newLine == '\n': newLine = ''
            resultText += newLine
        return resultText
    
    @staticmethod
    def setTesseractConfig(oem : int, psm : int) -> None:
        global tesseract_config
        tesseract_config = f"--oem {oem} --psm {psm}"

    @staticmethod
    def setScaleCoefficent(newCoef : int) -> None:
        global SCALE_COEFF
        SCALE_COEFF = newCoef if newCoef > 0 else None