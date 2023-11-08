

def test_api():
    # http://127.0.0.1:8000/api/v1/users/1/
    import requests
    # r = requests.get('http://127.0.0.1:8000/api/v1/users/1/').json()
    r = requests.get('http://127.0.0.1:8000/api/v1/users/').json()
    # print(r["id"])
    print(r)

if __name__ == "__main__":
    import random
    a = ""
    for i in range(4):
        a += f"{random.randint(1000,9999)}"
        a += "."

    print(a)