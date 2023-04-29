import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # TODO implement
    json_region = os.environ['AWS_REGION']
    logger.info('AWS Region of %s', json_region)
    response = get_response(event)
    return {
        'statusCode': 200,
        'region': json_region,
        'body': json.dumps(response)
    }

def get_response(event):
    message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])  
    return message
