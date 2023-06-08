import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Specify the table name and secondary index name
table_name = 'your-table-name'
index_name = 'your-secondary-index-name'

# Specify the column for which you want to retrieve distinct values
column_name = 'your-column-name'

# Initialize a set to store distinct values
distinct_values = set()

# Perform the scan operation on the secondary index
response = dynamodb.scan(
    TableName=table_name,
    IndexName=index_name,
    ProjectionExpression=column_name,
    Select='SPECIFIC_ATTRIBUTES'
)

# Iterate over the results and collect distinct values
for item in response['Items']:
    value = item[column_name]['S']  # Assumes the column is of type string (change 'S' for other types)
    distinct_values.add(value)

# Continue scanning if the response is paginated
while 'LastEvaluatedKey' in response:
    response = dynamodb.scan(
        TableName=table_name,
        IndexName=index_name,
        ProjectionExpression=column_name,
        Select='SPECIFIC_ATTRIBUTES',
        ExclusiveStartKey=response['LastEvaluatedKey']
    )
    
    # Iterate over the new results and collect distinct values
    for item in response['Items']:
        value = item[column_name]['S']  # Assumes the column is of type string (change 'S' for other types)
        distinct_values.add(value)

# Print the distinct values
print(distinct_values)
