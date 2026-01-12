# -*- coding: utf-8 -*-
import requests
import json

try:
    print("Testing API endpoint...")
    response = requests.get('http://localhost:5000/api/data', timeout=30)
    print(f"Status code: {response.status_code}")
    data = response.json()
    print(f"Data: {json.dumps(data, ensure_ascii=False, indent=2)}")
except Exception as e:
    print(f"Error: {e}")
