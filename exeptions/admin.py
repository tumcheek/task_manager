class AdminAccessRequired(Exception):
    """Raised when a non-admin user attempts to perform an admin-only action."""
