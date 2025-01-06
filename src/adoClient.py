import http.client
import base64
import json
import subprocess

def get_azure_devops_token():
    azure_devops_resource_id = '499b84ac-1321-427f-aa17-267ca6975798'
    command = f'az account get-access-token --resource {azure_devops_resource_id}'
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    token = json.loads(result)['accessToken']
    return token

def get_auth_header_value(token):
    return 'Basic ' + base64.b64encode(f':{token}'.encode()).decode()

def api_call(method, path, body=None):
    conn = http.client.HTTPSConnection('dev.azure.com')
    token = get_azure_devops_token()
    headers = {
        'Authorization': get_auth_header_value(token),
        'X-VSS-ForceMsaPassThrough': 'true',
        'Content-Type': 'application/json'
    }
    conn.request(method, path, headers=headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    
    if response.status == 200:
        return json.loads(data)['value']
    else:
        raise Exception(f'Error: {response.status} {response.reason}')
