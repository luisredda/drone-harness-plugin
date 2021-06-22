# Drone Harness Plugin

## Drone Plugin to trigger Pipelines or Workflows in Harness using API key.

### Usage:

    - name: Harness Plugin
      image: diegokoala/drone-harness-plugin
      settings:  
        application: "Harness Demo Application"
        type: "PIPELINE"
        entityname: "CD Pipeline"
        service: "search"
        build: "v6"
        accountid:
          from_secret: harness_acctid
        apikey: 
          from_secret: harness_secret
        service_name: "order-service"
        build_number: "latest"
        artifact_source_name: "harness_todolist-sample"



Obs: 

To run this plugin outside drone, you should create this ENV variables before the container starts.

    PLUGIN_ACCOUNTID
    PLUGIN_APIKEY
    PLUGIN_APPLICATION
    PLUGIN_ENTITYNAME
    PLUGIN_BODY
    PLUGIN_TYPE
    PLUGIN_SERVICE_NAME
    PLUGIN_BUILD_NUMBER
    PLUGIN_ARTIFACT_SOURCE_NAME
