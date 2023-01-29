import cv2
import pytesseract
import numpy as np


while True:
    choice = input("Enter number of the image (1-9): ")
    path = "test_images/car"+choice+".jpg"
    #read the image
    image = cv2.imread(path)


    #resize the image
    resized = cv2.resize(image, (700,500))
    cv2.imshow("Resized image", resized)
    cv2.waitKey(0)


    #convert to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayed image",gray)
    cv2.waitKey(0)


    #bilateral filter
    bilateral= cv2.bilateralFilter(gray, 11, 17, 17)
    cv2.imshow("Bilateral filtered image", bilateral)
    cv2.waitKey(0)


    #apply threshoold to create binary image
    _, threshed = cv2.threshold(bilateral, 150, 220, cv2.THRESH_BINARY)
    cv2.imshow("Threshed image",threshed)
    cv2.waitKey(0)


    #use morphological operations to isolate the license plate
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(threshed, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("Morphology closing image", closing)
    cv2.waitKey(0)


    #find contours
    countours, _ = cv2.findContours(closing, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    countours = sorted(countours, key=cv2.contourArea, reverse=True)[:30]
    

    #draw contours on the resized image
    resized_copy = resized.copy()
    cv2.drawContours(resized_copy, countours, -1, (0,255,0),3)
    cv2.imshow("Countours image", resized_copy)
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
    cv2.imshow("Detected license plate image", resized)
    cv2.waitKey(0)


    #show cropped license plate image
    cv2.imshow("Cropped license plate image", plate_image)
    cv2.waitKey(0)


    if plate is not None:

        #for Windows this is required by installing Tesseract-OCR
        #pytesseract.pytesseract.tesseract_cmd = r"{Your Tesseract-OCR directory}"

        #recognize the characters on the license plate
        config = ('-l eng --oem 1 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTVWUYXZ0123456789')
        text = pytesseract.image_to_string(plate_image, config=config)
        
        print("==============License Plate================")
        print("License plate in string: ", text)
        print("===========================================")
    else:
        print("License plate not found")

    cv2.destroyAllWindows()
    cv2.waitKey(0)

    replay = input("Replay? (Y/N): ").lower()
    print("============================================")
    if replay != "y":
        break
