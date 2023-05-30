import unittest
import mimetypes

def convert_to_multipart(file_data, filename):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    
    multipart_data = []
    multipart_data.append("--" + boundary)
    multipart_data.append('Content-Disposition: form-data; name="file"; filename="{}"'.format(filename))
    multipart_data.append("Content-Type: {}".format(content_type))
    multipart_data.append("")
    multipart_data.append(file_data)
    multipart_data.append("--" + boundary + "--")
    
    return "\r\n".join(multipart_data)

class TestMultipartFileProcessing(unittest.TestCase):
    def test_convert_to_multipart(self):
        # Create a sample CSV file content
        file_data = "name,email\nJohn Doe,john@example.com\nJane Smith,jane@example.com"
        filename = "data.csv"

        # Convert CSV to multipart form data
        result = convert_to_multipart(file_data, filename)
        
        # Check if the result is valid multipart form data
        self.assertIn("--WebKitFormBoundary7MA4YWxkTrZu0gW", result)
        self.assertIn('Content-Disposition: form-data; name="file"; filename="data.csv"', result)
        self.assertIn("Content-Type: text/csv", result)
        self.assertIn("name,email\nJohn Doe,john@example.com\nJane Smith,jane@example.com", result)
        self.assertIn("--WebKitFormBoundary7MA4YWxkTrZu0gW--", result)

if __name__ == '__main__':
    unittest.main()
