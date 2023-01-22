import cv2
import pytesseract
import numpy as np


#read the image
image = cv2.imread('test_images/car9.jpg')


#resize the image
resized = cv2.resize(image, (700,500))
cv2.imshow("original", resized)
cv2.waitKey(0)


#convert to grayscale
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
cv2.imshow("grayed",gray)
cv2.waitKey(0)


#bilateral
bilateral= cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow("bilateral", bilateral)
cv2.waitKey(0)


#apply threshoold to create binary image
_, threshed = cv2.threshold(bilateral, 150, 220, cv2.THRESH_BINARY)
cv2.imshow("treshed",threshed)
cv2.waitKey(0)


#use morphological operations to isolate the license plate
kernel = np.ones((3,3), np.uint8)
opening = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
cv2.imshow("closing", closing)
cv2.waitKey(0)


#find contours
countours, _ = cv2.findContours(closing, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
countours = sorted(countours, key=cv2.contourArea, reverse=True)[:30]
#countours = countours[0] #if len(countours) == 2 else countours[1]
#print("Countours: ", str(len(countours)))


#draw contours on the resized image
resized_copy = resized.copy()
cv2.drawContours(resized_copy, countours, -1, (0,255,0),3)
cv2.imshow("countours", resized_copy)
cv2.waitKey(0)


plate = None
for countour in countours:
    peri = cv2.arcLength(countour, True)
    approx = cv2.approxPolyDP(countour, 0.018*peri, True)
    if len(approx) == 4:
        plate = approx
        x, y, w, h = cv2.boundingRect(countour)
        plate_image = closing[y:y+h, x:x+w]
        break


#draw license plate countour only
cv2.drawContours(resized, [plate], -1, (0,255,0), 3)
cv2.imshow("detected license plate", resized)
cv2.waitKey(0)


#show cropped license plate image
cv2.imshow("cropped", plate_image)
cv2.waitKey(0)


if plate is not None:
    #recognize the characters on the license plate
    config = ('-l eng --oem 1 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTVWUYXZ0123456789')
    text = pytesseract.image_to_string(plate_image, config=config)
    
    print("==============License Plate================")
    print("Text: ", text)
else:
    print("License plate not found")