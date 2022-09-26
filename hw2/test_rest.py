import pytest
from rest_example import app, db, isnumber

@pytest.fixture()
def client():
    return app.test_client()


def test_hello(client):
    response = client.get("/hello")
    assert "HSE One Love!" in str(response.data)
    assert str(response.status) == "200 OK"

    response = client.get("/hello?abcd")
    assert "HSE One Love!" in str(response.data)
    assert str(response.status) == "200 OK"


def test_unknown(client):
    response = client.get("/aboba")
    assert str(response.status) == "405 METHOD NOT ALLOWED"


def test_set(client):
    response = client.post("/set", data = {"value": "kek", "key": "lol"})
    assert str(response.status) == "415 UNSUPPORTED MEDIA TYPE"
    assert db == dict()

    response = client.post("/set", json = {"key": "lol"})
    assert str(response.status) == "400 BAD REQUEST"
    assert db == dict()

    response = client.post("/set", json = {"value": "kek", "key": "lol"})
    assert str(response.status) == "200 OK"
    assert db == {"lol": "kek"}

    response = client.post("/set", json = {"value": "kek1", "key": "lol1"})
    assert str(response.status) == "200 OK"
    assert db == {"lol": "kek", "lol1": "kek1"}

    response = client.post("/set", json = {"value": "rofl", "key": "lol", "trash": "some data"})
    assert str(response.status) == "200 OK"
    assert db == {"lol": "rofl", "lol1": "kek1"}


def test_get(client):
    client.post("/set", json = {"value": "kek", "key": "lol"})

    response = client.get("/get/aboba")
    assert str(response.status) == "404 NOT FOUND"

    response = client.get("/get/lol")
    assert str(response.status) == "200 OK"
    assert response.json == {"key": "lol", "value": "kek"}

    client.post("/set", json = {"value": "new value", "key": "lol", "smth": "trash"})
    response = client.get("/get/lol")
    assert str(response.status) == "200 OK"
    assert response.json == {"key": "lol", "value": "new value"}


def test_isnumber():
    assert isnumber(0)
    assert isnumber(42)
    assert isnumber(-322)
    assert isnumber(1.618)
    assert isnumber(1e9)
    assert not isnumber("aboba")
    assert not isnumber("123")
    assert not isnumber("-3.1415926")


def test_divide(client):
    response = client.post("/divide", data = {"divider": 2, "dividend": 4})
    assert str(response.status) == "415 UNSUPPORTED MEDIA TYPE"

    response = client.post("/divide", json = {"divider": 2})
    assert str(response.status) == "400 BAD REQUEST"

    response = client.post("/divide", json = {"divider": "2", "dividend": 4})
    assert str(response.status) == "400 BAD REQUEST"

    response = client.post("/divide", json = {"divider": 0, "dividend": 4})
    assert str(response.status) == "400 BAD REQUEST"

    response = client.post("/divide", json = {"divider": 2, "dividend": 4})
    assert str(response.status) == "200 OK"
    assert float(response.data.decode("utf-8")) == 2.0

    response = client.post("/divide", json = {"divider": -4, "dividend": 2})
    assert str(response.status) == "200 OK"
    assert float(response.data.decode("utf-8")) == -0.5