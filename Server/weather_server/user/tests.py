from django.test import TestCase
import json
str01 = '{"username": "213123", "password": "2131223113"}'
dict01 = json.loads(str01)
print(type(dict01))
# Create your tests here.
