import json

def buildResponse(statusCode, body):
    return {
        'statusCode': statusCode,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'content-type': 'application/json'
        },
        'body': json.dumps(body)
    }
