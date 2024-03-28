FROM python:3.11

WORKDIR /app/gcp

COPY requirements.txt /app/gcp/requirements.txt

RUN pip install -r requirements.txt

COPY . /app/gcp

CMD ["python", "main.py"]
