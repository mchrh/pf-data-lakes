import os
import requests

def run_api_tests():
    endpoints = [
            '/transactions/',
            '/transactions/summary/',
            '/web-logs/',
            '/web-logs/metrics/',
            '/campaigns/'
        ]
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000/api{endpoint}", auth=('work', 'test'))
            if response.status_code == 200:
                print("\u2714 API OK.")
            else:
                print(f"\u2716 API Fail, Erreur: {response.status_code}.")
        except Exception as e:
            print(f"\u2716 Erreur: {str(e)}")



if __name__ == "__main__":
    run_api_tests()
