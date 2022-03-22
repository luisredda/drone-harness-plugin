import requests
import json

url = "https://app.harness.io/gateway/api/graphql?accountId=4vHVRSnRT9K-mOIbeIOFmg"

payload="{\"query\":\"mutation {               \\n    startExecution(input: {                 \\n        applicationId: \\\"TaqGz-0QTcCzzPqYweoHhg\\\"                 \\n        entityId: \\\"jR-jZxrgRp-BVRwQkMEC_w\\\"                 \\n        executionType: WORKFLOW, variableInputs: [\\n            {          \\n                name: \\\"Service\\\"          \\n                variableValue: {            \\n                    type: NAME            \\n                    value: \\\"cloud-native-sample-service\\\"          \\n                }        \\n            },\\n            {\\n                name: \\\"Environment\\\"\\n                variableValue: {\\n                    type: NAME\\n                    value: \\\"dev\\\"\\n                }\\n            },\\n            {\\n                name: \\\"InfraDefinition_KUBERNETES\\\"\\n                variableValue: {\\n                    type: NAME\\n                    value: \\\"eks-transactional-carbono-dev\\\"\\n                }\\n            },\\n            {\\n                name: \\\"run_terraform\\\"\\n                variableValue: {\\n                    type: NAME\\n                    value: \\\"true\\\"\\n                }\\n            },\\n            ],         \\n            serviceInputs: [ \\n                {          \\n                    name: \\\"cloud-native-sample-service\\\",           artifactValueInput: {            \\n                            valueType: BUILD_NUMBER           \\n                            buildNumber: {              \\n                                buildNumber: \\\"latest\\\"        \\n                                artifactSourceName: \\\"cards_cloud-native-sample-service_dev\\\"\\n                            }          \\n                        }\\n                    }  \\n                ]\\n            }               \\n        )\\n        {                 \\n            clientMutationId                 \\n            execution{                   \\n                id                   \\n                status                 \\n            }               \\n        }             \\n    }\",\"variables\":{}}"
headers = {
  'x-api-key': 'NHZIVlJTblJUOUstbU9JYmVJT0ZtZzo6M1pZTmg2Nm55YmlnVkl0ZkpvNjc3SEV5eDhKdk5KblB2TE0zcVNqbW5mMG51SG1iYUxOdm1uWEVTQ3pTQkFVWU9VVHpZaHJOdHFsVm0xUVQ=',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
