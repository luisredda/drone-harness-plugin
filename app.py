from ast import If
import requests
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = os.environ.get('PLUGIN_ACCOUNTID') 
API_KEY = os.environ.get('PLUGIN_APIKEY') 
APPLICATION_NAME = os.environ.get('PLUGIN_APPLICATION')
WORKFLOW_NAME = os.environ.get('PLUGIN_ENTITYNAME')
#BODY = os.environ.get('PLUGIN_BODY')
EXECUTION_TYPE = os.environ.get('PLUGIN_TYPE')
SERVICE_NAME = os.environ.get('PLUGIN_SERVICE_NAME')
BUILD_NUMBER = os.environ.get('PLUGIN_BUILD_NUMBER')
ARTIFACT_SOURCE_NAME = os.environ.get('PLUGIN_ARTIFACT_SOURCE_NAME')
DYNAMIC_VARIABLES_INPUT = os.environ.get('PLUGIN_DYNAMIC_VARIABLES_INPUT') or "false"
WAIT_FOR_EXECUTION = os.environ.get('PLUGIN_WAIT_FOR_EXECUTION') or "false"
WAIT_FOR_EXECUTION_TIMEOUT = int(os.environ.get('PLUGIN_WAIT_FOR_EXECUTION_TIMEOUT')) or 30
EXECUTION_NOTES = os.environ.get('PLUGIN_EXECUTION_NOTES') or "Automated Execution"


global URL
URL = "https://app.harness.io/gateway/api/graphql?accountId=" + ACCOUNT_ID
print("Using Account ID: " + ACCOUNT_ID)


def getAppByName(appName):

    pload = "{\"query\":\"{ \\n    applicationByName(name: \\\""+appName+"\\\"){ \\n        id \\n    } \\n}\",\"variables\":{}}"

    print("Getting Harness App ID")

    response = requests.post(URL, headers={'x-api-key': API_KEY,'Content-Type': 'application/json'}, data=pload)
    
    json_response = response.json()
    #print(json_response)
    appId = json_response['data']['applicationByName']['id']
    print ("appID is: " + appId)

    return appId


def getWfByName(AppID, WFName):

    print ("Getting Harness Workflow ID by workflow name: " + WFName)
    pload = "{\"query\":\"{\\n    workflowByName( workflowName: \\\""+WFName+"\\\", applicationId: \\\""+AppID+"\\\") { \\n        id \\n    } \\n}\",\"variables\":{}}"

    response = requests.post(URL, headers={'x-api-key': API_KEY,'Content-Type': 'application/json'}, data=pload)

    json_response = response.json()
    WFID = json_response["data"]["workflowByName"]["id"]
    print("WFID is: " + WFID)

    return WFID


def getPLByName(AppID, PLName):
    pload = '{ pipelineByName( pipelineName: "' + PLName + '", applicationId: "' + AppID + '") { id } }'

    print ("Getting Harness Pipeline ID")
    print(pload)
    response = requests.post(URL, headers={'x-api-key': API_KEY,'Content-Type': 'text/plain'}, data=pload)
    print(response)

    json_response = response.json()
    PLID = json_response["data"]["pipelineByName"]["id"]
    print("PLID is: " + PLID)
    return PLID


def execute(appID, wfID):
    print("Service Name: " + SERVICE_NAME)
    print("Build Number: " + BUILD_NUMBER)
    print("Artifact Source Name: " + ARTIFACT_SOURCE_NAME)
    print("Execution Type: " + EXECUTION_TYPE)

    body="\n        variableInputs: [\n            {\n                name: \"Service\"\n                variableValue: {\n                    type: NAME\n                    value: \""+SERVICE_NAME+"\"\n                }\n            },"
    if DYNAMIC_VARIABLES_INPUT != "false":
      variable_list = DYNAMIC_VARIABLES_INPUT.split(",")
      for var in variable_list:
        key,value = var.split(":")
        body += "\n            {\n                name: \""+key+"\"\n                variableValue: {\n                    type: NAME\n                    value: \""+value+"\"\n                }\n            },"
    body += "\n            ],\n            serviceInputs: [\n                {\n                    name: \""+SERVICE_NAME+"\",\n           artifactValueInput: {\n                            valueType: BUILD_NUMBER,\n                            buildNumber: {\n                                buildNumber: \""+BUILD_NUMBER+"\",\n                                artifactSourceName: \""+ARTIFACT_SOURCE_NAME+"\"\n                            }\n                        }\n                    }\n                ]\n"
    pload = "mutation {\n    startExecution(input: {\n        notes: \""+EXECUTION_NOTES+"\",\n        applicationId: \""+appID+"\"\n        entityId: \""+wfID+"\"\n        executionType: "+EXECUTION_TYPE+", "+body+"            }\n        )\n        {\n            clientMutationId\n            execution{\n                id\n                status\n            }\n        }\n    }"

    print("Payload: " + pload)
    retries = 0
    while True:
        response = requests.post(URL, headers={'x-api-key': API_KEY,'Content-Type': 'text/plain'}, data=pload)
        json_response = response.json()
        print(json_response)
        if not "errors" in json_response:
            return json_response
        time.sleep(30)
        retries += 1
        print(f"Retrying ... {retries}")

def status(exec_id):
    print("Execution Type: " + EXECUTION_TYPE)
    print("Execution ID: " + exec_id)
    body = "{\"query\":\"{\\n  execution(executionId:\\\""+exec_id+"\\\"){\\n    id\\n    status\\n    ... on PipelineExecution {\\n      id\\n      status\\n      pipelineStageExecutions {\\n        pipelineStageElementId\\n        pipelineStageName\\n        pipelineStepName\\n        ... on ApprovalStageExecution {\\n          approvalStepType\\n          status\\n        }\\n        ... on WorkflowStageExecution {\\n          runtimeInputVariables {\\n            allowedValues\\n            defaultValue\\n            allowMultipleValues\\n            fixed\\n            name\\n            required\\n            type\\n          }\\n          status\\n          workflowExecutionId\\n        }\\n      }\\n    }\\n    ... on WorkflowExecution {\\n      id\\n      outcomes{\\n        nodes{\\n          execution {\\n            id\\n            endedAt\\n            startedAt\\n          }\\n        }\\n      }\\n    }\\n  }\\n}\\n\",\"variables\":{}}"

    #print("Payload: " + body)
    response = requests.post(URL, headers={'x-api-key': API_KEY,'Content-Type': 'application/json'}, data=body)
    json_response = response.json()
    print(json_response)
    return json_response

print("Search for Application Name: " + APPLICATION_NAME)
AppID = (getAppByName(APPLICATION_NAME))

if EXECUTION_TYPE == "WORKFLOW":
  WfID = getWfByName(AppID, WORKFLOW_NAME)
  execution_id = execute(AppID, WfID)
  workflow_status = status(execution_id['data']['startExecution']['execution']['id'])['data']['execution']['status']
  print("Status:" + workflow_status)
  if WAIT_FOR_EXECUTION == "true":
    timeout = time.time() + 60*WAIT_FOR_EXECUTION_TIMEOUT   # 30 minutes from now
    while workflow_status == "RUNNING" or workflow_status == "PAUSED":
        time.sleep(15)
        workflow_status = status(execution_id['data']['startExecution']['execution']['id'])['data']['execution']['status']
        if workflow_status != "RUNNING" or time.time() > timeout:
            break
  print(workflow_status)

else:
  PlID = getPLByName(AppID, WORKFLOW_NAME)
  
  execution_id = execute(AppID, PlID)
  pipeline_status = status(execution_id['data']['startExecution']['execution']['id'])['data']['execution']['status']
  print("Status:" + pipeline_status)
  if WAIT_FOR_EXECUTION == "true":
    timeout = time.time() + 60*30   # 30 minutes from now
    while pipeline_status == "RUNNING" or pipeline_status == "PAUSED" or pipeline_status == "PAUSING" or pipeline_status == "QUEUED" or pipeline_status == "WAITING":
        time.sleep(15)
        pipeline_status = status(execution_id['data']['startExecution']['execution']['id'])['data']['execution']['status']
        if time.time() > timeout:
            break
  print(pipeline_status)



""" status("DsCaP1eJSJSePbsYK4td2Q")
status("Inrzd03aQ967s141m9XsWQ")
status("bO3xZz_iQcSYruJY8GJqqQ") """
