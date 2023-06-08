import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

def get_distinct_values(table_name, column_name):
    # Set up an empty set to store distinct values
    distinct_values = set()

    # Perform a scan operation on the DynamoDB table
    response = dynamodb.scan(
        TableName=table_name,
        ProjectionExpression=column_name
    )

    # Process each item in the scan result
    for item in response['Items']:
        # Check if the column exists in the item
        if column_name in item:
            # Add the value to the set of distinct values
            distinct_values.add(item[column_name]['S'])  # Adjust for the data type if necessary

    # Continue scanning if the result is paginated
    while 'LastEvaluatedKey' in response:
        response = dynamodb.scan(
            TableName=table_name,
            ProjectionExpression=column_name,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        for item in response['Items']:
            if column_name in item:
                distinct_values.add(item[column_name]['S'])  # Adjust for the data type if necessary

    return distinct_values

# Usage
table_name = 'YourTableName'
column_name = 'YourColumnName'

distinct_values = get_distinct_values(table_name, column_name)
print(distinct_values)
