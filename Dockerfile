#Use an official Python runtime as base image
FROM python:3.8

#Set the working directory
WORKDIR /app

#Download packages
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN apt-get install -y git
RUN apt-get install -y tesseract-ocr 

#Copy repo
RUN git clone https://github.com/donnykernell/LicensePlateRecognition.git

#Add test images
ADD test_images /app/test_images

#Copy requirements file to the container
COPY requirements.txt . 

#Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

#Copy script to the container
COPY car_plate_recognition.py .

#Set enviroment variable for tesseract
ENV TESDATA_PREFIX /usr/local/share/tessdata

#Run the script
CMD ["python", "car_plate_recognition.py"]
