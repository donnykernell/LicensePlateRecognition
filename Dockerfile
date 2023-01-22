# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Download the english language data
RUN apt-get update && apt-get install -y git
RUN apt-get install -y tesseract-ocr tesseract-ocr-dev tesseract-ocr-script-latn tesseract-ocr-script-latn-dev tesseract-ocr-script-latn-frak tesseract-ocr-script-latn-frak-dev

#Copy repo
RUN git clone git@github.com:donnykernell/LicensePlateRecognition

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script to the container
COPY license_plate_recognition.py .

# Set environment variable for tesseract
ENV TESSDATA_PREFIX /usr/local/share/tessdata

# Run the script
CMD ["python", "car_plate_recognition.py"]
