License Plate Recognition
This project aims to detect and recognize the license plate number in an image using OpenCV and pytesseract. The script first prompts the user to enter the number of the image (1-9) to be processed, and then reads the image from the specified file path. The image is then resized, converted to grayscale, and processed using a bilateral filter to reduce noise. The image is then thresholded to create a binary image, and morphological operations are applied to isolate the license plate. Contours are then found and drawn on the resized image, and the license plate is identified by its approximate polygon shape. The license plate is then cropped from the image and passed to pytesseract for character recognition, which returns the text of the license plate number.

Getting started
Prerequisites
Python 3.8
OpenCV
pytesseract
tesseract-ocr
tesseract-ocr-script-latn
Installing
The project can be installed using pip and the requirements.txt file:

Copy code
pip install -r requirements.txt
Running the script
To run the script, simply execute the following command:

Copy code
python license_plate_recognition.py
Docker support
A Dockerfile is provided to build an image of the project, including all the necessary dependencies.
To build the image use:

Copy code
docker build -t <image_name> .
To run the container:

Copy code
docker run <image_name>
Contributing
All contributions and pull requests are welcome!

Acknowledgements
OpenCV documentation
pytesseract documentation
This code uses open source libraries, please see the individual libraries for their respective licenses and acknowledgement.
