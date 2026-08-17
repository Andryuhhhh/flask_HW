import requests
#
#
BASE_URL = "http://127.0.0.1:5000"



def create_advert():
    data = {
        "header": "Продам машину",
        "description": "BMW 3 series, хорошее состояние",
        "owner": "Андрей"
    }

    response = requests.post(
        f"{BASE_URL}/adverts/",
        json=data
    )

    print("POST")
    print(response.status_code)
    print(response.json())
    print()


def get_advert(advert_id):
    response = requests.get(
        f"{BASE_URL}/adverts/{advert_id}"
    )

    print("GET")
    print(response.status_code)

    if response.headers.get("Content-Type", "").startswith("application/json"):
        print(response.json())
    else:
        print(response.text)

    print()

    return response

def update_advert(advert_id):
    data = {
        "description": "BMW 3 series, отличное состояние"
    }

    response = requests.patch(
        f"{BASE_URL}/adverts/{advert_id}",
        json=data
    )

    print("PATCH")
    print(response.status_code)

    if response.headers.get("Content-Type", "").startswith("application/json"):
        print(response.json())
    else:
        print(response.text)

    print()

    return response


def delete_advert(advert_id):
    response = requests.delete(
        f"{BASE_URL}/adverts/{advert_id}"
    )

    print("DELETE")
    print(response.status_code)
    print(response.json())
    print()


if __name__ == "__main__":
    create_advert()

    # Здесь поставь ID созданного объявления
    advert_id = 1

    get_advert(advert_id)
    update_advert(advert_id)
    delete_advert(advert_id)

