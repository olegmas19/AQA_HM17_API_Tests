import requests
import json
from jsonschema import validate
from data.resourse import DATA_DIR


def test_get_list_user():
    url = "https://reqres.in/api/users"
    params = {"page": 2, "per_page": 4}
    response = requests.get(params=params, url=url)

    assert response.json()["page"] == 2
    assert response.json()["per_page"] == 4
    assert response.status_code == 200


def test_get_single_user_checking_scheme_positive():
    url = "https://reqres.in/api/users/2"

    response = requests.get(url=url)
    print(response.text)

    body = response.json()

    assert response.status_code == 200
    assert body["data"]["id"] == 2
    assert body["data"]["email"] == "janet.weaver@reqres.in"
    assert body["data"]["first_name"] == "Janet"
    assert body["data"]["last_name"] == "Weaver"
    with open(DATA_DIR + "/get_single_user.json") as file:
        validate(body, schema=json.loads(file.read()))


def test_get_single_user_not_found_negative():
    url = "https://reqres.in/api/users/0"

    response = requests.get(url=url)

    assert response.status_code == 404


def test_get_list_resource():
    url = "https://reqres.in/api/unknown"

    response = requests.get(url=url)
    print(response.text)

    assert response.status_code == 200


def test_get_single_resource():
    url = "https://reqres.in/api/unknown/2"

    response = requests.get(url=url)
    print(response.text)

    assert response.status_code == 200


def test_get_single_resource_not_found():
    url = "https://reqres.in/api/unknown/23"

    response = requests.get(url=url)

    assert response.status_code == 404


def test_post_user_checking_scheme():
    url = "https://reqres.in/api/users"
    payload = json.dumps({"name": "morpheus", "job": "leader"})
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=payload, headers=headers)
    print(response.text)

    body = response.json()

    assert response.status_code == 201
    with open(DATA_DIR + "/post_users.json") as file:
        validate(body, schema=json.loads(file.read()))


def test_put_update_user_checking_scheme():
    url = "https://reqres.in/api/users/2"

    payload = json.dumps({"name": "morpheus", "job": "leader"})

    headers = {"Content-Type": "application/json"}

    response = requests.put(url=url, data=payload, headers=headers)
    print(response.text)

    body = response.json()

    assert response.status_code == 200
    with open(DATA_DIR + "/put_user.json") as file:
        validate(body, schema=json.loads(file.read()))


def test_patch_update_user():
    url = "https://reqres.in/api/users/2"

    payload = json.dumps({"name": "morpheus", "job": "zion resident"})
    headers = {"Content-Type": "application/json"}

    response = requests.patch(url=url, data=payload, headers=headers)
    print(response.text)

    assert response.status_code == 200


def test_delete_user_no_answer():
    url = "https://reqres.in/api/users/2"

    response = requests.delete(url=url)

    assert response.text == ""
    assert response.status_code == 204


def test_post_register_user_successful():
    url = "https://reqres.in/api/users/2"

    payload = json.dumps({"email": "eve.holt@reqres.in", "password": "pistol"})
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=payload)
    print(response.text)

    assert response.status_code == 201


def test_post_register_user_bad_request_checking_scheme():
    url = "https://reqres.in/api/register"
    payload = json.dumps({"email": "sydney@fife"})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=payload, headers=headers)
    print(response.text)

    body = response.json()

    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"
    with open(DATA_DIR + "/post_register_bad_request.json") as file:
        validate(body, schema=json.loads(file.read()))


def test_post_login_user_successful():
    url = "https://reqres.in/api/login"
    payload = json.dumps({"email": "eve.holt@reqres.in", "password": "cityslicka"})
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=payload)
    print(response.text)

    assert response.status_code == 200


def test_post_login_user_unsuccessful():
    url = "https://reqres.in/api/login"
    payload = json.dumps({"email": "peter@klaven"})
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, headers=headers, data=payload)
    print(response.text)

    assert response.status_code == 400


def test_get_users_delayed_response():
    url = "https://reqres.in/api/users"
    params = {"delay": 3}

    response = requests.get(url, params=params)
    print(response.text)

    assert response.status_code == 200
