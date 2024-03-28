FROM python:3.11

WORKDIR /app/aws

COPY requirements.txt /app/aws/requirements.txt

RUN pip install -r requirements.txt

COPY . /app/aws

CMD ["python", "main.py"]
