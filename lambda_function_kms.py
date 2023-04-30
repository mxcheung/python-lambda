import os
import json
import logging
import boto3
from base64 import b64decode

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # TODO implement
    DB_HOST = os.environ['DB_HOST']
    DB_PASS_ENCRYPTED = os.environ["DB_PASS"]
    cipherTextBlob = b64decode(DB_PASS_ENCRYPTED)
#    DB_PASS_DECRYPTED = boto3.client('kms').decrypt(CiphertextBlob=cipherTextBlob)['Plaintext']
    LAMBDA_FUNCTION_NAME = os.environ['AWS_LAMBDA_FUNCTION_NAME']
    
    DB_PASS_DECRYPTED = boto3.client('kms').decrypt(
    CiphertextBlob=b64decode(DB_PASS_ENCRYPTED),
    EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
)['Plaintext'].decode('utf-8')

    DB_PASS_DECRYPTED2 = boto3.client('kms').decrypt(CiphertextBlob=cipherTextBlob,
    EncryptionContext={'LambdaFunctionName': "mypi"})['Plaintext'].decode('utf-8')

    DB_PASS_DECRYPTED3 = boto3.client('kms').decrypt(CiphertextBlob=cipherTextBlob, EncryptionContext={'LambdaFunctionName': "mypi"})['Plaintext'].decode('utf-8')

    json_region = os.environ['AWS_REGION']
    logger.info('AWS Region of %s', json_region)
    response = get_response(event)
    return {
        'statusCode': 200,
        'region': json_region,
        'LAMBDA_FUNCTION_NAME': LAMBDA_FUNCTION_NAME,
        'DB_HOST': DB_HOST,
        'DB_PASS_ENCRYPTED': DB_PASS_ENCRYPTED,
        'DB_PASS_DECRYPTED': DB_PASS_DECRYPTED,
        'body': json.dumps(response)
    }

def get_response(event):
    message = 'Hello {} {}!'.format(event['first_name'], event['last_name'])  
    return message
