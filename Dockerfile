FROM python:3.7.5-slim

RUN mkdir /opt/app
COPY app.py /opt/app
WORKDIR /opt/app
RUN pip install requests

#ENV PLUGIN_ACCOUNTID "AccountID"
#ENV PLUGIN_APIKEY "4P1K3Y"
#ENV PLUGIN_APPLICATION "Harness Demo Application"
#ENV PLUGIN_ENTITYNAME "CD Pipeline"
#ENV PLUGIN_TYPE "PIPELINE"
#ENV PLUGIN_SERVICE_NAME "order-service"
#ENV PLUGIN_BUILD_NUMBER "latest"
#ENV PLUGIN_ARTIFACT_SOURCE_NAME "harness_todolist-sample"

application: 
        type: 
        entityname: 
        service: "search"
        build: "v6"
        accountid:
          from_secret: harness_acctid
        apikey: 
          from_secret: harness_secret
        service_name: 
        build_number: 
        artifact_source_name: 

ENTRYPOINT ["python"]
CMD ["/opt/app/app.py"]
