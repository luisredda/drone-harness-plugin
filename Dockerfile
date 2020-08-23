FROM python:3.7.5-slim

RUN mkdir /opt/app
COPY app.py /opt/app
WORKDIR /opt/app
RUN pip install requests

ENTRYPOINT ["python"]
CMD ["/opt/app/app.py"]
