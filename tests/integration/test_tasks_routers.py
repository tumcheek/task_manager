import pytest
from datetime import timedelta, datetime

from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.auth import create_access_token
from models import Task, User


@pytest.fixture
def token(user):
    """Create a JWT token for the test user."""
    access_token_expires = timedelta(minutes=15)
    return create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )


def test_get_user_task(
    client: TestClient, user: User, user_task: Task, token: str, dbsession: Session
):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/api/v1/tasks/{user_task.id}/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Task for testing"
    assert data["owner_id"] == user.id


def test_get_user_task_not_found(
    client: TestClient, user: User, token: str, task_detail_url: str
):
    non_existent_task_id = 9999
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(
        task_detail_url.format(task_id=non_existent_task_id), headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Task not found"


def test_get_user_task_unauthorized(client: TestClient, task_detail_url):
    response = client.get(task_detail_url.format(task_id=1))
    assert response.status_code == 403


def test_get_user_task_unauthorized_access(
    client, user, another_user_task, token, task_detail_url
):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(
        task_detail_url.format(task_id=another_user_task.id), headers=headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Task not found"


def test_get_user_task_with_mock_database_error(
    client, user, token, task_detail_url, mocker
):
    mock_get_user_task_detail = mocker.patch("routers.tasks.get_user_task_detail")
    mock_get_user_task_detail.side_effect = HTTPException(
        status_code=500, detail="Simulated database error"
    )

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(task_detail_url.format(task_id=1), headers=headers)

    assert response.status_code == 500
    assert response.json()["detail"] == "Simulated database error"
