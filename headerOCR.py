import os
import cv2
import pytesseract
import re

input_path = 'C:\\Users\\Parsa\\Desktop\\ECG\\OCR\\ECG_Record\\'
out_path = 'C:\\Users\\Parsa\\Desktop\\ECG\\OCR\\out\\'

prog1 = re.compile('.*\D(\d+)\D*')
prog2 = re.compile('.*\D(\d+)\D+(\d+)\D*')
prog3 = re.compile('.*\D(\d+)\D+(\d+)\D+(\d+)\D*')

def process(string):
    extracted = ''
    if string.startswith('Heart'):
        result = prog1.match(string)
        extracted = 'Heart Rate: ' + result.group(1) + ' bpm'
    if string.startswith('PR'):
        result = prog1.match(string)
        extracted = 'PR int.: ' + result.group(1) + ' ms'
    if string.startswith('QR'):
        result = prog1.match(string)
        extracted = 'QRS dur.: ' + result.group(1) + ' ms'
    if string.startswith('QT'):
        result = prog2.match(string)
        extracted = 'QT/QTc: ' + result.group(1) + '/' + result.group(2) + ' bpm'
    if string.startswith('P-R'):
        result = prog3.match(string)
        extracted = 'P-R-T axes: ' + result.group(1) + '-' + result.group(2) + '-' + result.group(3) + ' bpm'
    return extracted
    
    

def ocr(file_path, config = '--psm 11'):
    image = cv2.imread(file_path)
    head = image[:222, :]
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    text = pytesseract.image_to_string(head, lang='eng', config=config)
    res = ''
    for line in text.split('\n'):
        if line.startswith('Heart') or line.startswith('PR') or line.startswith('QRS') or line.startswith('QT') or line.startswith('P-R'):
            res = res + process(line) + '\n'

    f = open(out_path + file_path.split('\\')[-1] + '.txt', 'w')
    f.write(text)
    f.close()
    f = open(out_path + file_path.split('\\')[-1] + 'info.txt', 'w')
    f.write(res)
    f.close()
def main(input_path=input_path, out_path=out_path):
    files = os.listdir(input_path)
    for file in files:
        if os.path.isfile(input_path + file):
            ocr(input_path + file)

if __name__=='__main__':
    main()

'''boxes = pytesseract.image_to_boxes(image, lang='eng', config=config)
f = open('boxes.txt', 'w')
f.write(boxes)
f.close()

data = pytesseract.image_to_data(image, lang='eng', config=config, output_type=pytesseract.Output.DICT)
f = open('data.txt', 'w')
f.write(boxes)
f.close()'''
