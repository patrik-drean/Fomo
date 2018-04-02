from django.test import TestCase
import requests

response = requests.get('http://localhost:8000/catalog/index/',
    auth = ('patrikdrean@gmail.com', 'Password1'),
    params = {'categoryid': 2}
    )

print('Status code: ', response.status_code)
