## Description
This app provides a REST API for convenient and efficient 
task managing.

## Installation
1. Navigate to the app directory
2. Create a virtual environment:

    ```python -m venv venv```
3. Activate the virtual environment (for Windows):

    ```venv\Scripts\activate```
Or on Linux
```source venv/bin/activate```
4. Install the required dependencies:

   ```pip install -r requirements.txt```
5. Run the app:

   ```fastapi dev main.py```
## 📚 Documentation

FastAPI automatically generates interactive API documentation at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

To ensure the documentation is clear and helpful, **all contributors must document their code** using **Google-style docstrings**.

---

## ✍️ How to Document Code

Please follow these simple rules when writing or updating code:

- Use **Google-style docstrings** for all functions, classes, and methods.
- Write in **English**.
- Keep it concise but informative.
- This ensures consistent and clean auto-generated docs.

### ✅ Example

```python
def get_user(user_id: int) -> User:
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user object if found.

    Raises:
        HTTPException: If the user is not found.
    """
    ...

```
## 🛠 Error Monitoring with Sentry

This project integrates with [Sentry](https://sentry.io) for real-time error tracking and diagnostics.

### ✨ Features

- Automatically captures unhandled exceptions
- Logs useful debugging context: stack traces, request details, environment info
- Shows unique `error_id` values in API responses to assist with support

### ⚙️ Configuration

Sentry is configured via environment variables:

- `SENTRY_DSN` – your Sentry project DSN
- `SENTRY_ENVIRONMENT` – environment name (`development`, `staging`, `production`, etc.)

These variables are loaded on application startup.

### ✅ Best Practices

- Do not expose technical error details to users
- Include `error_id` in error responses to assist with issue tracking
- Keep environments separated in Sentry for clearer project management
