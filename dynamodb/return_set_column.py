import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = 'YourTableName'
index_name = 'YourIndexName'
column_name = 'YourColumnName'

table = dynamodb.Table(table_name)
index = table.indexes[index_name]

response = index.scan(ProjectionExpression=column_name)
column_values = {item[column_name] for item in response['Items']}

print(column_values)
