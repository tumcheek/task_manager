import pytest

from models import Task, User
from services.exeptions import TaskNotFoundError
from services.tasks import get_user_tasks_list, get_user_task_detail


def test_get_user_tasks_list_with_tasks(dbsession, user):
    """Test that a user with tasks gets all their tasks returned."""
    tasks = [
        Task(owner_id=user.id, title="Task 1", description="First task"),
        Task(owner_id=user.id, title="Task 2", description="Second task"),
    ]
    dbsession.add_all(tasks)
    dbsession.commit()

    retrieved_tasks = get_user_tasks_list(dbsession, user_id=user.id)

    assert len(retrieved_tasks) == 2
    retrieved_task_titles = {task.title for task in retrieved_tasks}
    expected_task_titles = {"Task 1", "Task 2"}
    assert retrieved_task_titles == expected_task_titles


def test_get_user_tasks_list_no_tasks(dbsession, user):
    """Test that a user with no tasks gets an empty list."""
    retrieved_tasks = get_user_tasks_list(dbsession, user_id=user.id)
    assert retrieved_tasks == []


def test_get_user_tasks_list_nonexistent_user(dbsession):
    """Test that a non-existent user ID returns an empty list."""
    retrieved_tasks = get_user_tasks_list(dbsession, user_id=999)
    assert retrieved_tasks == []


def test_get_user_task_detail_exists(dbsession, user):
    """Test that the function returns the task when it exists for the user."""
    task = Task(owner_id=user.id, title="Test Task", description="A test task")
    dbsession.add(task)
    dbsession.commit()

    retrieved_task = get_user_task_detail(dbsession, user_id=user.id, task_id=task.id)

    assert retrieved_task == task
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.owner_id == user.id


def test_get_user_task_detail_not_found(dbsession, user):
    with pytest.raises(TaskNotFoundError):
        get_user_task_detail(
            dbsession, user_id=user.id, task_id=999
        )  # Assuming 999 doesn't exist


def test_get_user_task_detail_wrong_user(dbsession, user):
    """Test that the function raises TaskNotFoundError when the task belongs to another user."""
    other_user = User(
        first_name="Other",
        last_name="User",
        email="otheruser@example.com",
        password="test1234",
    )
    dbsession.add(other_user)
    dbsession.commit()

    task = Task(
        owner_id=other_user.id,
        title="Other User Task",
        description="Another user's task",
    )
    dbsession.add(task)
    dbsession.commit()

    with pytest.raises(TaskNotFoundError):
        get_user_task_detail(dbsession, user_id=user.id, task_id=task.id)
