import boto3

# Set the AWS profile
session = boto3.Session(profile_name='your_profile_name')

# Use the session to create AWS service clients
s3_client = session.client('s3')
ec2_client = session.client('ec2')

# Now you can use the AWS service clients to interact with AWS
# For example:
response = s3_client.list_buckets()
instances = ec2_client.describe_instances()

# Rest of your code...

Connection was closed before we received a valid response from endpoint URL: "https://s3.amazonaws.com/".
  
  
  import boto3

# Set the AWS credentials
aws_access_key_id = 'your_access_key_id'
aws_secret_access_key = 'your_secret_access_key'

# Create a session with the specified credentials
session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Use the session to create AWS service clients
s3_client = session.client('s3')
dynamodb_client = session.client('dynamodb')

# Now you can use the AWS service clients to interact with AWS
# For example:
response = s3_client.list_buckets()
tables = dynamodb_client.list_tables()

# Rest of your code...

export AWS_DEFAULT_REGION=your_desired_region

