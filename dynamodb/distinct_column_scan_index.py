import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

def get_distinct_values(table_name, index_name, column_name):
    # Set up an empty set to store distinct values
    distinct_values = set()

    # Perform a query operation on the DynamoDB index
    response = dynamodb.query(
        TableName=table_name,
        IndexName=index_name,
        ProjectionExpression=column_name
    )

    # Process each item in the query result
    for item in response['Items']:
        # Check if the column exists in the item
        if column_name in item:
            # Add the value to the set of distinct values
            distinct_values.add(item[column_name]['S'])  # Adjust for the data type if necessary

    # Continue querying if the result is paginated
    while 'LastEvaluatedKey' in response:
        response = dynamodb.query(
            TableName=table_name,
            IndexName=index_name,
            ProjectionExpression=column_name,
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        for item in response['Items']:
            if column_name in item:
                distinct_values.add(item[column_name]['S'])  # Adjust for the data type if necessary

    return distinct_values

# Usage
table_name = 'YourTableName'
index_name = 'YourIndexName'
column_name = 'YourColumnName'

distinct_values = get_distinct_values(table_name, index_name, column_name)
print(distinct_values)
