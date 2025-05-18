from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list["User"]] = relationship("User", back_populates="role")
