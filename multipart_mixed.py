import csv
import email
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def convert_to_multipart(file_data, filename):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    content_type = "text/csv"

    #boundary = "===============6979016840983667163=="
    multipart_data = []
    #   multipart_data.append("MIME-Version: 1.0")
   # multipart_data.append("Content-Type: multipart/mixed; boundary=\"{}\"".format(boundary))
    # multipart_data.append("Content-Type: multipart/mixed;")
    # multipart_data.append("boundary=\"{}\"".format(boundary))
    multipart_data.append("--" + boundary)
    multipart_data.append('Content-Disposition: form-data; name="file"; filename="{}"'.format(filename))
    multipart_data.append("Content-Type: {}".format(content_type))
    multipart_data.append("")
    multipart_data.append(file_data.decode())
    multipart_data.append("--" + boundary + "--")

    return "\r\n".join(multipart_data)


# file_data = b'name,email\nJohn Doe,john@example.com\nJane Smith,jane@example.com'
filename = "data.csv"

# Create a CSV attachment
csv_data = [
    ["Name", "Email"],
    ["John Doe", "john@example.com"],
    ["Jane Smith", "mary@example.com"]
]


file_data = '\n'.join([','.join(row) for row in csv_data]).encode("utf-8")

# Convert CSV to multipart form data
#message = email.message_from_bytes(file_data)

#payload = message.get_payload(decode=True)
result = convert_to_multipart(file_data, filename)

message = email.message_from_bytes(bytes(result, 'utf-8'))

# if not message.is_multipart():
#    raise ValueError("Message is not multipart")


# message = email.message_from_bytes(bytes(result, 'utf-8'))
boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
body = bytes(result, 'utf-8')
blah = "multipart/mixed; boundary=\"{}\"".format(boundary)
content_type_from_header = blah.encode()
body = (
        b'MIME-Version: 1.0\r\nContent-Type: '
        + content_type_from_header
        + b'\r\n\r\n'
        + body
)
print(body.decode("utf-8"))
message = email.message_from_bytes(body)

# print(message)
if not message.is_multipart():
    raise ValueError("Message is not multipart")

# Create a new MIMEMultipart object
multipart_message = MIMEMultipart()

# Create a CSV attachment
csv_data = [
    ["Name", "Email"],
    ["John Doe", "john@example.com"],
    ["Jane Smith", "mary@example.com"]
]
csv_filename = "data.csv"
csv_part = MIMEBase("text", "csv")
csv_part.set_payload('\n'.join([','.join(row) for row in csv_data]).encode("utf-8"))
encoders.encode_base64(csv_part)
csv_part.add_header("Content-Disposition", f"attachment; filename={csv_filename}")

multipart_message.attach(csv_part)

multipart_message_string = multipart_message.as_string()
multipart_message_bytes= bytes(multipart_message_string, 'utf-8')

message = email.message_from_bytes(multipart_message_bytes)

if multipart_message.is_multipart():
    print("The message is multipart.")
else:
    print("The message is not multipart.")

