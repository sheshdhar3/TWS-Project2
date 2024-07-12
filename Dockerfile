FROM python:3.9-slim

WORKDIR /SD

COPY requirements.txt /SD/

RUN pip install -r requirements.txt

COPY . /SD/

EXPOSE 82

CMD ["python", "app.py"]

