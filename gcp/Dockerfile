FROM python:3.9

WORKDIR /app/gcp

COPY requirements.txt /app/gcp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/gcp/requirements.txt

COPY src /app/gcp/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
