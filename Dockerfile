# Your Python version
FROM python:3.9

# Web port of the application
EXPOSE 5000

# Install your application
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# Start up command
CMD python test1.py