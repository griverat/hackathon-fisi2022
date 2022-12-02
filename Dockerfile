### Build and install packages
FROM python:3.10 as build-python

# Install Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8000
ENV PORT 8000
ENV PYTHONUNBUFFERED 1
ENV PROCESSES 4

# Setup properly django container
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "fisinos.wsgi"]
