import json

def lambda_handler(event, context):
    # TODO implement
    response = get_response(event)
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def get_response(event):
    message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])  
    return message
