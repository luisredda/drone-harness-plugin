import requests
import json
import os

ACCOUNT_ID = os.environ.get('PLUGIN_ACCOUNTID')
API_KEY = os.environ.get('PLUGIN_APIKEY')
APPLICATION_NAME = os.environ.get('PLUGIN_APPLICATION')
WORKFLOW_NAME = os.environ.get('PLUGIN_ENTITYNAME')
#BODY = os.environ.get('PLUGIN_BODY')
EXECUTION_TYPE = os.environ.get('PLUGIN_TYPE')
SERVICE_NAME = os.environ.get('PLUGIN_SERVICE_NAME')
BUILD_NUMBER = os.environ.get('PLUGIN_BUILD_NUMBER')
ARTIFACT_SOURCE_NAME = os.environ.get('PLUGIN_ARTIFACT_SOURCE_NAME')
USER_NAME = os.environ.get('USER_NAME')

global URL
URL = "https://app.harness.io/gateway/api/graphql?accountId=" + ACCOUNT_ID

def getAppByName(appName):
    pload = "  { \
      applicationByName(name: \"" + appName + "\"){ \
        id \
      } \
     } \
    "

    print ("Getting Harness App ID")

    response = requests.post(URL, headers={'x-api-key': API_KEY, 'Content-Type': 'text/plain'}, data=pload)

    json_response = response.json()
    appId = json_response['data']['applicationByName']['id']
    print ("appID is: " + appId)

    return(appId)


def getWfByName(AppID, WFName):
    pload = "{ \
      workflowByName( workflowName: \"" + WFName + "\", applicationId: \"" +  AppID + "\") { \
        id \
      } \
    } \
    "
    print ("Getting Harness Workflow ID")

    response = requests.post(URL, headers={'x-api-key': API_KEY, 'Content-Type': 'text/plain'}, data=pload)

    json_response = response.json()
    WFID = json_response['data']['workflowByName']['id']
    print ("WFID is: " + WFID)

    return(WFID)

def getPLByName(AppID, PLName):
    pload = " { \
        pipelineByName( pipelineName: \"" + PLName + "\", applicationId: \"" +  AppID + "\") { \
            id \
      } \
    } \
    "
    print ("Getting Harness Pipeline ID")

    response = requests.post(URL, headers={'x-api-key': API_KEY, 'Content-Type': 'text/plain'}, data=pload)

    json_response = response.json()
    PLID = json_response['data']['pipelineByName']['id']
    print ("PLID is: " + PLID)
    return(PLID)

def execute(appID, wfID):
    print("Service Name: " + SERVICE_NAME)
    print("Build Number: " + BUILD_NUMBER)
    print("Artifact Source Name: " + ARTIFACT_SOURCE_NAME)
    print("Execution Type: " + EXECUTION_TYPE)
    body = 'variableInputs: [ \
      {\
        name: "Service"\
        variableValue: {\
          type: NAME\
          value: "'+SERVICE_NAME+'"\
        }\
      }\,
      {\
        name: "User"\
        variableValue: {\
          type: NAME\
          value: "'+USER_NAME+'"\
        }\
      }\      
      ], \
      serviceInputs: [ {\
        name: "'+SERVICE_NAME+'", \
        artifactValueInput: {\
          valueType: BUILD_NUMBER\
          buildNumber: {\
            buildNumber: "'+BUILD_NUMBER+'"\
      artifactSourceName: "'+ARTIFACT_SOURCE_NAME+'"\
          }\
        }}  ]'
      
    
    pload = "mutation { \
              startExecution(input: { \
                applicationId: \"" + appID + "\" \
                entityId: \"" + wfID + "\" \
                executionType: " + EXECUTION_TYPE + ", " + body + \
              "} \
              ){ \
                clientMutationId \
                execution{ \
                  id \
                  status \
                } \
              } \
            }"
    #print("Payload: " + pload)
    response = requests.post(URL, headers={'x-api-key': API_KEY, 'Content-Type': 'text/plain'}, data=pload)
    json_response = response.json()
    print(json_response)

AppID = (getAppByName(APPLICATION_NAME))

if EXECUTION_TYPE == "WORKFLOW":
  WfID = getWfByName(AppID, WORKFLOW_NAME)
  execute(AppID, WfID)
else:
  PlID = getPLByName(AppID, WORKFLOW_NAME)
  execute(AppID, PlID)
