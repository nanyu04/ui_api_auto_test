import requests

def test_login():
    base = "http://127.0.0.1:8081"
    payload = {"username":"admin","password":"admin123"}

    url1 = base + "/api/login"
    r1 = requests.post(url1, json=payload)
    print(f"【测试1】url={url1}")
    print(f"code={r1.status_code}, response={repr(r1.text)}")
    print("-"*40)

    url2 = base + "/login"
    r2 = requests.post(url2, json=payload)
    print(f"【测试2】url={url2}")
    print(f"code={r2.status_code}, response={repr(r2.text)}")

if __name__ == "__main__":
    test_login()
