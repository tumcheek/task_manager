from models import Role


def seed_roles(session):
    roles = ["admin", "user"]
    for role_name in roles:
        if not session.query(Role).filter_by(name=role_name).first():
            session.add(Role(name=role_name))
    session.commit()
