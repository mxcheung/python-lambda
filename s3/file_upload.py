import boto3

def upload_file_to_s3(file_path, bucket_name, s3_key):
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Upload the file
    try:
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"File uploaded successfully to S3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Specify the file path, bucket name, and S3 key
file_path = '/path/to/file.txt'
bucket_name = 'your-bucket-name'
s3_key = 'folder/file.txt'

# Call the function to upload the file
upload_file_to_s3(file_path, bucket_name, s3_key)
