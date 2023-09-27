# FastApi

Hello My Friends, 
This repository is about creating a simple API app for sharing the prediction of Machine Learning projects with FastApi Library in Python.
In this App, I use MariaDB For the maintenance of predicted data. You can change the type of DataBase.

So I hope to help you.
Thanx for your attention

# Usage
- test post api
```python
import requests
from urllib.parse import urlencode
url = "http://localhost:8000/"

data = {
        "start_date": "2023-07-26",
        "end_date": "2023-07-26",
        "users": ["user1, user2"]
        "tagss": ["tag1, tag2"]
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```
