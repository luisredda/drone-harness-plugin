import requests
import json
import os
import time

ACCOUNT_ID = os.environ.get("PLUGIN_ACCOUNTID")
API_KEY = os.environ.get("PLUGIN_APIKEY")
APPLICATION_NAME = os.environ.get("PLUGIN_APPLICATION")
WORKFLOW_NAME = os.environ.get("PLUGIN_ENTITYNAME")
# BODY = os.environ.get('PLUGIN_BODY')
EXECUTION_TYPE = os.environ.get("PLUGIN_TYPE")
SERVICE_NAME = os.environ.get("PLUGIN_SERVICE_NAME")
BUILD_NUMBER = os.environ.get("PLUGIN_BUILD_NUMBER")
ARTIFACT_SOURCE_NAME = os.environ.get("PLUGIN_ARTIFACT_SOURCE_NAME")
USERNAME = os.environ.get("PLUGIN_USER")

print(f"Variável PLUGIN_USER : ${USERNAME}")
print(f"Variável PLUGIN_APPLICATION : ${APPLICATION_NAME}")

global URL
URL = "https://app.harness.io/gateway/api/graphql?accountId=" + ACCOUNT_ID


def getAppByName(appName):
    pload = (
        '  { \
      applicationByName(name: "'
        + appName
        + '"){ \
        id \
      } \
     } \
    '
    )

    print("Getting Harness App ID")

    response = requests.post(
        URL, headers={"x-api-key": API_KEY, "Content-Type": "text/plain"}, data=pload
    )

    json_response = response.json()
    appId = json_response["data"]["applicationByName"]["id"]
    print("appID is: " + appId)

    return appId


def getWfByName(AppID, WFName):
    pload = (
        '{ \
      workflowByName( workflowName: "'
        + WFName
        + '", applicationId: "'
        + AppID
        + '") { \
        id \
      } \
    } \
    '
    )
    print("Getting Harness Workflow ID")

    response = requests.post(
        URL, headers={"x-api-key": API_KEY, "Content-Type": "text/plain"}, data=pload
    )

    json_response = response.json()
    WFID = json_response["data"]["workflowByName"]["id"]
    print("WFID is: " + WFID)

    return WFID


def getPLByName(AppID, PLName):
    pload = (
        ' { \
        pipelineByName( pipelineName: "'
        + PLName
        + '", applicationId: "'
        + AppID
        + '") { \
            id \
      } \
    } \
    '
    )
    print("Getting Harness Pipeline ID")

    response = requests.post(
        URL, headers={"x-api-key": API_KEY, "Content-Type": "text/plain"}, data=pload
    )

    json_response = response.json()
    PLID = json_response["data"]["pipelineByName"]["id"]
    print("PLID is: " + PLID)
    return PLID


def execute(appID, wfID):
    print("Service Name: " + SERVICE_NAME)
    print("Build Number: " + BUILD_NUMBER)
    print("Artifact Source Name: " + ARTIFACT_SOURCE_NAME)
    print("Execution Type: " + EXECUTION_TYPE)
    """"
mutation {
  startExecution(input: {
    applicationId: "MAEYgyHBQA6OPU2LbQntog"
    entityId: "sQfFcSSMR7mVDEPv7Mf7eA"
    executionType: WORKFLOW
    notes: "Iniciando Deployment",
     variableInputs: [
    {
      name: "Environment"
      variableValue: {
        type: NAME
        value: "prd"
      }
    },
    {
      name: "InfraDefinition_KUBERNETES"
      variableValue: {
        type: NAME
        value: "ocp-dc01"
      }
    },
    {
      name: "Service"
      variableValue: {
        type: NAME
        value: "cdps-officer-java-ocp"
      }
    },
    {
        name: "user"
        variableValue: {
          type: NAME
          value: "joao.limberger"
        }
            
    }
    ]
    serviceInputs: {
      name: "cdps-officer-java-ocp"
      artifactValueInput: {
        valueType:BUILD_NUMBER
        buildNumber: {
          artifactSourceName: "cdps-officer-java-ocp"
          buildNumber: "1.0.94-SNAPSHOT"
        }å
        }
      }
    }
  ) {
    clientMutationId
    execution {
      id
    }
    warningMessage
  }
}    
    """
    body = (
        '''variableInputs: [ 
        {
          name: "Service",
          variableValue: {
            type: NAME,
            value: "'''
        + SERVICE_NAME
        + '''"
          }
        }, 
        {
          name: "user",
          variableValue: {
            type: NAME,
            value: "'''
        + USERNAME
        + '''"
          }
        }
      ],
      serviceInputs: [ {
        name: "'''
        + SERVICE_NAME
        + '''", 
        artifactValueInput: {
          valueType: BUILD_NUMBER,
          buildNumber: {
            buildNumber: "'''
        + BUILD_NUMBER
        + '''", 
            artifactSourceName: "'''
        + ARTIFACT_SOURCE_NAME
        + """"
          }
        }
        }
        ]"""
    )

    pload = (
        '''mutation { 
              startExecution(input: { applicationId: "'''
        + appID
        + '''", 
              entityId: "'''
        + wfID
        + """", 
              executionType: """
        + EXECUTION_TYPE
        + """, 
              notes: "Iniciando Deployment",
"""
        + body
        + """
                } 
              )
              { 
                clientMutationId 
                execution{ 
                  id 
                  status 
                } 
                warningMessage
              } 
            }"""
    )

    print("-" * 50)
    print("Payload: " + pload)
    print("-" * 50)
    retries = 0
    while True:
        response = requests.post(
            URL,
            headers={"x-api-key": API_KEY, "Content-Type": "text/plain"},
            data=pload,
        )
        json_response = response.json()
        print(json_response)
        if not "errors" in json_response:
            break
        time.sleep(30)
        retries += 1
        print(f"Retriing ... {retries}")


AppID = getAppByName(APPLICATION_NAME)

print(f"Execution_type: {EXECUTION_TYPE}")

if EXECUTION_TYPE == "WORKFLOW":
    WfID = getWfByName(AppID, WORKFLOW_NAME)
    execute(AppID, WfID)
else:
    PlID = getPLByName(AppID, WORKFLOW_NAME)
    execute(AppID, PlID)
