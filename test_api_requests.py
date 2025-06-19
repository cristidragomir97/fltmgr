import requests
from pprint import pprint

BASE_URL = "http://localhost:8000/api/v1"


def create_user(username: str, email: str, password: str) -> str:
    r = requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "email": email,
        "password": password,
    })
    if r.status_code not in (200, 201):
        print("Register failed", r.status_code, r.text)
    r = requests.post(f"{BASE_URL}/auth/login", json={
        "username": username,
        "password": password,
    })
    token = r.json().get("access_token")
    return token


def test_crud():
    token = create_user("tester", "tester@example.com", "secret")
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    robot = {
        "id": "test-robot",
        "name": "Test Robot",
        "ros_domain": 5,
        "agent_host": "main-control",
        "components": ["nav2"],
        "hosts": [],
        "watch_topics": ["/cmd_vel"],
    }
    r = requests.post(f"{BASE_URL}/robots/", json=robot, headers=headers)
    print("Create robot", r.status_code)
    pprint(r.json())

    r = requests.get(f"{BASE_URL}/robots/", headers=headers)
    print("List robots", r.status_code, r.json())

    robot["name"] = "Updated Robot"
    r = requests.put(f"{BASE_URL}/robots/{robot['id']}", json=robot, headers=headers)
    print("Update robot", r.status_code, r.json())

    host = {
        "id": "host-1",
        "name": "Main Control",
        "type": "x86",
        "robot_id": robot["id"],
        "portainer_endpoint_id": 1,
    }
    r = requests.post(f"{BASE_URL}/hosts/", json=host, headers=headers)
    print("Create host", r.status_code)
    pprint(r.json())

    r = requests.get(f"{BASE_URL}/hosts/", headers=headers)
    print("List hosts", r.status_code, r.json())

    host["name"] = "Updated Host"
    r = requests.put(f"{BASE_URL}/hosts/{host['id']}", json=host, headers=headers)
    print("Update host", r.status_code)
    pprint(r.json())

    app = {
        "id": "app-1",
        "name": "Test App",
        "description": "An example app",
        "owner_id": "tester-id",
        "compose_templates": {"x86": "version: '3'"},
        "default_env": {"DEBUG": "1"},
    }
    r = requests.post(f"{BASE_URL}/apps/", json=app, headers=headers)
    print("Create app", r.status_code)
    pprint(r.json())

    r = requests.get(f"{BASE_URL}/apps/", headers=headers)
    print("List apps", r.status_code, r.json())

    app["description"] = "Updated description"
    r = requests.put(f"{BASE_URL}/apps/{app['id']}", json=app, headers=headers)
    print("Update app", r.status_code)
    pprint(r.json())

    dep = {
        "id": "dep-1",
        "app_id": app["id"],
        "robot_id": robot["id"],
        "owner_id": "tester-id",
        "notes": "test deployment",
        "image_tags": ["example:latest"],
        "status": "pending",
    }
    r = requests.post(f"{BASE_URL}/deployments/", json=dep, headers=headers)
    print("Create deployment", r.status_code)
    pprint(r.json())

    r = requests.get(f"{BASE_URL}/deployments/", headers=headers)
    print("List deployments", r.status_code, r.json())

    r = requests.delete(f"{BASE_URL}/deployments/{dep['id']}", headers=headers)
    print("Delete deployment", r.status_code)

    r = requests.delete(f"{BASE_URL}/hosts/{host['id']}", headers=headers)
    print("Delete host", r.status_code)

    r = requests.delete(f"{BASE_URL}/apps/{app['id']}", headers=headers)
    print("Delete app", r.status_code)

    r = requests.delete(f"{BASE_URL}/robots/{robot['id']}", headers=headers)
    print("Delete robot", r.status_code)

if __name__ == "__main__":
    test_crud()
