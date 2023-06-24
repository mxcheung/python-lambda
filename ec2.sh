sudo yum install python-pip
pip install awsebcli --upgrade --user
pip install camelcase


============================
# This program prints Hello, world!
print('Hello, world!')

from camelcase import CamelCase
c = CamelCase()
s = 'this is a sentence that needs CamelCasing!'
print(c.hump(s))
# This is a Sentence That Needs CamelCasing!



============================

ec2-user@ip-172-31-28-211 ~]$ python3 hello.py 
This is a Sentence That Needs CamelCasing!

============================
fWFZ1IelpKejcfgAiQM4ViDONN9H7kVXZ03Nh/nm
