FROM python:3.7.5-slim

COPY . /app
WORKDIR /app
RUN pip install requests

ENTRYPOINT ["python"]
CMD ["app.py"]
