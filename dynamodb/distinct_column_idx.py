import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the table name and index name
table_name = 'YourTableName'
index_name = 'YourSecondaryIndexName'

# Define the column name for which you want distinct values
column_name = 'YourColumnName'

# Define the query parameters
params = {
    'TableName': table_name,
    'IndexName': index_name,
    'ProjectionExpression': column_name
}

# Perform the query operation
response = dynamodb.query(**params)

# Extract the distinct values from the query results
distinct_values = set()
for item in response['Items']:
    value = item[column_name]['S']  # Adjust this based on your column type
    distinct_values.add(value)

# Print the distinct values
for value in distinct_values:
    print(value)
