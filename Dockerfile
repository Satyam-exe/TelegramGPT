# Use the official Python image as the base image
FROM python:3:9

# Install ffmpeg using apt-get
RUN apt-get update && apt-get install -y ffmpeg


ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

RUN mkdir .tmp && mkdir .tmp/mp3 && mkdir .tmp/ogg

# Run the main.py script
CMD ["python3", "main.py"]