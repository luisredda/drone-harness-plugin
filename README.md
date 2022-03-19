# Drone Harness Plugin

## Harness CIE / Drone Plugin to trigger Pipelines or Workflows in Harness using API key.

Limitations:

1 - Your service needs an artifact

2 - Your Workflow/Pipeline should templatize the service as "${Service}" variable as in input.

### Options

- ACCOUNTID: "AccountID"
  APIKEY: "4P1K3Y"
  APPLICATION: "Harness Application Name"
  ENTITYNAME: "Pipeline/Workflow Name"
  TYPE: "PIPELINE or WORKFLOW"
  SERVICE_NAME: "Service Name"
  BUILD_NUMBER: "Artifact Build Version"
  ARTIFACT_SOURCE_NAME: "Artifact Source Name"
  DYNAMIC_VARIABLES_INPUT: "Environment:dev,InfraDefinition_KUBERNETES:eks-transactional-carbono-dev,run_terraform:true,key:value,key2:value2" 
  WAIT_FOR_EXECUTION: "true or false"
  WAIT_FOR_EXECUTION_TIMEOUT: "Number in minutes"
  EXECUTION_NOTES: "Execution Notes"

### Usage Harness CIE

- step:
  type: Plugin
  name: Trigger Harness CD
  identifier: triggercd
  spec:
      connectorRef: account.dockerimageconnector
      image: diegokoala/drone-harness-plugin
      privileged: false
      settings:
          application: <App_Name>
          type: PIPELINE
          entityname: <PipeID>
          accountid: <AccountID>
          apikey: <ApiKey>
          service_name: <ServiceName>
          build_number: <BuildVersion>
          artifact_source_name: <ArtifactSourceName>
          dynamic_variables_input: "Environment:dev,InfraDefinition_KUBERNETES:eks-transactional-carbono-dev,run_terraform:true"
          wait_for_execution: "true"
          wait_for_execution_timeout: 30
          execution_notes: "Automated Execution"
      imagePullPolicy: Always
  when:
      stageStatus: Success
      condition: <+execution.steps.profile.output.outputVariables.PROFILE> != 'dev'
  failureStrategies: []



### Usage Drone:

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
        dynamic_variables_input: "Environment:dev,InfraDefinition_KUBERNETES:eks-transactional-carbono-dev,run_terraform:true"
        wait_for_execution: "true"
        wait_for_execution_timeout: 30
        execution_notes: "Automated Execution"



Obs: 

To run this plugin outside drone, you should create this ENV variables before the container starts.

You can add to the Dockerfile

    ENV PLUGIN_ACCOUNTID "AccountID"
    ENV PLUGIN_APIKEY "4P1K3Y"
    ENV PLUGIN_APPLICATION "Harness Demo Application"
    ENV PLUGIN_ENTITYNAME "CD Pipeline"
    ENV PLUGIN_TYPE "PIPELINE"
    ENV PLUGIN_SERVICE_NAME "order-service"
    ENV PLUGIN_BUILD_NUMBER "latest"
    ENV PLUGIN_ARTIFACT_SOURCE_NAME "harness_todolist-sample"
    ENV PLUGIN_DYNAMIC_VARIABLES_INPUT "Environment:dev,InfraDefinition_KUBERNETES:eks-transactional-carbono-dev,run_terraform:true"
    ENV PLUGIN_WAIT_FOR_EXECUTION "true"
    ENV PLUGIN_WAIT_FOR_EXECUTION_TIMEOUT "30"
    ENV PLUGIN_EXECUTION_NOTES "Automated Execution"
