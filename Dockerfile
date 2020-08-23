FROM python:3.7.5-slim

COPY app.py /app
WORKDIR /app
RUN pip install requests

ENTRYPOINT ["python", "/app/app.py"]

