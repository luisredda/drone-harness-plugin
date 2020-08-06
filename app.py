import requests
import json
import os

ACCOUNT_ID = os.environ.get('PLUGIN_ACCOUNTID')
API_KEY = os.environ.get('PLUGIN_APIKEY')
APPLICATION_NAME = os.environ.get('PLUGIN_APPLICATION')
WORKFLOW_NAME = os.environ.get('PLUGIN_PIPELINE')
BODY = os.environ.get('PLUGIN_BODY')

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

def executeWorkflow(appID, wfID):
    pload = "mutation { \
              startExecution(input: { \
                applicationId: \"" + appID + "\" \
                entityId: \"" + wfID + "\" \
                executionType: WORKFLOW, " + BODY + \
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
WfID = getWfByName(AppID, WORKFLOW_NAME)
executeWorkflow(AppID, WfID)
