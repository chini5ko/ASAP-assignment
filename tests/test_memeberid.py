import json


def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200


def test_member_id_validate_route(app, client):
    res = client.get('/member_id/validate')
    assert res.status_code == 200


def test_member_id_validate__fake_route(app, client):
    res = client.get('/member_id/hihi')
    assert res.status_code == 404


def test_generate_member_id(client):
    data = {
        "first_name": "hector",
        "last_name": "liang",
        "dob": "01/01/1961",
        "country": "Venezuela"
    }
    url = '/member_id'

    response = client.post(url, json=data)

    assert response.content_type == 'application/json'
    assert response.json['first_name'] == "hector"
    assert response.json['last_name'] == "liang"
    assert response.json['dob'] == "01/01/1961"
    assert response.json['country'] == "Venezuela"


def test_generate_member_id_with_wrong_first_name_field(client):
    data = {
        "firstName": "hector",
        "last_name": "liang",
        "dob": "01/01/1961",
        "country": "Venezuela"
    }
    url = '/member_id'

    response = client.post(url, json=data)
    assert response.status_code == 400
    assert response.json['message'] == "the first_name field is missing"


def test_validate_member_id(client):
    data = {
        "first_name": "hector",
        "last_name": "liang",
        "dob": "01/01/1961",
        "country": "Venezuela"
    }
    url = '/member_id'

    response = client.post(url, json=data)
    member_id = response.json['member_id']

    # validate
    url = 'member_id/validate'

    response = client.post(url, content_type='multipart/form-data', data={
        'member_id': member_id,
    })
    assert response.content_type == 'text/html; charset=utf-8'
    assert response.status_code == 200

    assert response.data == b"The " + \
        member_id.encode('UTF-8') + " is valid member id".encode('UTF-8')


def test_invalid_member_id(client):

    url = 'member_id/validate'

    response = client.post(url, content_type='multipart/form-data', data={
        'member_id': "43195906",
    })
    assert response.content_type == 'text/html; charset=utf-8'
    assert response.status_code == 200

    assert response.data == b"Sorry, the 43195906 is not registered in ASAP database<br>Please contac ASAP. Email: info@asylumadvocacy.org "
