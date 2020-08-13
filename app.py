import requests
import json
import os

ACCOUNT_ID = os.environ.get('PLUGIN_ACCOUNTID')
API_KEY = os.environ.get('PLUGIN_APIKEY')
APPLICATION_NAME = os.environ.get('PLUGIN_APPLICATION')
WORKFLOW_NAME = os.environ.get('PLUGIN_ENTITYNAME')
BODY = os.environ.get('PLUGIN_BODY')
EXECUTION_TYPE = os.environ.get('PLUGIN_TYPE')

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

    response = requests.post(URL, headers={'x-api-key': API_KEY}, data=pload)

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

    response = requests.post(URL, headers={'x-api-key': API_KEY}, data=pload)

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

    response = requests.post(URL, headers={'x-api-key': API_KEY}, data=pload)

    json_response = response.json()
    PLID = json_response['data']['pipelineByName']['id']
    print ("PLID is: " + PLID)
    return(PLID)

def execute(appID, wfID):
    pload = "mutation { \
              startExecution(input: { \
                applicationId: \"" + appID + "\" \
                entityId: \"" + wfID + "\" \
                executionType: " + EXECUTION_TYPE + ", " + BODY + \
              "} \
              ){ \
                clientMutationId \
                execution{ \
                  id \
                  status \
                } \
              } \
            }"

    response = requests.post(URL, headers={'x-api-key': API_KEY}, data=pload)
    json_response = response.json()
    print(json_response)

AppID = (getAppByName(APPLICATION_NAME))

if EXECUTION_TYPE == "WORKFLOW":
  WfID = getWfByName(AppID, WORKFLOW_NAME)
  execute(AppID, WfID)
else:
  PlID = getPLByName(AppID, WORKFLOW_NAME)
  execute(AppID, PlID)
