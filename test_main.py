from fastapi.testclient import TestClient
import time
from main import app


# использование TestClient для подобных событий
# https://stackoverflow.com/questions/75714883/how-to-test-a-fastapi-endpoint-that-uses-lifespan-function
# https://fastapi.tiangolo.com/advanced/testing-events/
# https://fastapi.tiangolo.com/advanced/events/
def test_create_task():
    with TestClient(app) as client:
        response = client.post("/task", json={"duration": 1})
        assert response.status_code == 200
        task_id = response.json()["task_id"]

        response = client.get(f"/task/{task_id}")
        assert response.status_code == 200
        assert response.json() == {"status": "running"}

        time.sleep(2)

        response = client.get(f"/task/{task_id}")
        assert response.status_code == 200
        assert response.json() == {"status": "done"}
