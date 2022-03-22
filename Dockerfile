FROM python:3.7.5-slim

RUN mkdir /opt/app
COPY app.py /opt/app
COPY requirements.txt /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt

#ENV PLUGIN_ACCOUNTID "AccountID"
#ENV PLUGIN_APIKEY "4P1K3Y"
#ENV PLUGIN_APPLICATION "Harness Demo Application"
#ENV PLUGIN_ENTITYNAME "CD Pipeline"
#ENV PLUGIN_TYPE "PIPELINE"
#ENV PLUGIN_SERVICE_NAME "order-service"
#ENV PLUGIN_BUILD_NUMBER "latest"
#ENV PLUGIN_ARTIFACT_SOURCE_NAME "harness_todolist-sample"

ENTRYPOINT ["python"]
CMD ["/opt/app/app.py"]
