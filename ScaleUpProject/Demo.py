import cv2
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
from fpdf import FPDF
import os
url = 'http://192.168.43.1:8080/video'
cap = cv2.VideoCapture(url)
ret = True
f1 = 0
i = 0
while ret:
    ret, frame = cap.read()
    if f1 == 0:
        print("Press \"S\" to SCAN THE DOCUMENT")
        f1 = f1 + 1
    cv2.imshow("CAMERA FEED", frame)
    k = cv2.waitKey(1)
    if k == ord("s"):
        cv2.destroyWindow("CAMERA FEED")
        cv2.imshow("SCANNED PHOTO", frame)
        print("Press \"U\" if IT IS UNREADABLE")
        print("Press \"B\" to CONVERT INTO B&W")
        k1 = cv2.waitKey(0)
        if k1 == ord("u"):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            new = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 155, 1)
            cv2.imwrite("C://pdf//scanned%d.jpg" % i, new)
            i = i + 1
            continue
        elif k1 == ord("b"):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("C://pdf//scanned%d.jpg" % i, gray)
            i = i + 1
            continue

    if k == ord("q"):
        ret = False
        break

cv2.destroyAllWindows()
imagelist = os.listdir("C://pdf")
pdf = FPDF()
for image in imagelist:
    image = "C://pdf//" + image
    imagetext = Image.open(image)
    text = tess.image_to_string(imagetext)
    print(text)
    pdf.add_page(image)
    pdf.image(image)
    pdf.output("C://pdf//your_file.pdf")

