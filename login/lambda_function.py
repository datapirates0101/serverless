import service.register as reg
import service.login as log
import json

healthPath = '/health'
registerPath = '/register'
loginPath = '/login'
verifyPath = '/verify'


def lambda_handler(event, context):
    print(event)
    print(json.dumps(event))
    if(not event['body']):
        data = {}
    else:
        data = json.loads(event['body'])
    responseOk = {'statusCode': 200, 'body': 'OK'}
    response = {}
    responseNotFound = {'statusCode': 404, 'body': 'Not Found'}
    if event['path'] == healthPath:
        response = responseOk
    elif event['path'] == registerPath:
        response = reg.register(data)
    elif event['path'] == loginPath:
        response = log.login(data)
    elif event['path'] == verifyPath:
        return responseOk
    else:
        return responseNotFound

    return response
