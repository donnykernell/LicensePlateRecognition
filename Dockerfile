#Use an official Python runtime as base image
FROM python:3.8

#Set the working directory
WORKDIR /app

#Download the english language data
RUN apt-get update && apt-get install -y git
RUN apt-get install -y tesseract-ocr tesseract-ocr-dev tesseract-ocr-script-latn tesseract-ocr-script-latn-dev tesseract-ocr-script-latn-frak tesseract-ocr-script-latn-frak-dev

#Copy repo
RUN git clone https://github.com/donnykernell/LicensePlateRecognition.git

#Copy requirements file to the container
COPY LicensePlateRecognition/requirements.txt . 

#Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

#Copy script to the container
COPY LicensePlateRecognition/license_plate_recognition.py .

#Set enviroment variable for tesseract
ENV TESDATA_PREFIX /usr/local/share/tessdata

#Run the script
CMD ["python", "license_plate_recognition.py"]
