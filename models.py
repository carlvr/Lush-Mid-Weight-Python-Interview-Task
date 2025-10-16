from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base
import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)  # UUID stored as string.
    title = Column(String, nullable=False)  # Task title (required).
    completed = Column(Boolean, nullable=False, default=False)  # Defaults to False.
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    deadline = Column(DateTime, nullable=True)  # Optional deadline.
    priority = Column(Integer, nullable=False, default=5)  # Default priority.

    def __repr__(self):
        return (
            f"<Task(id='{self.id}', title='{self.title}', "
            f"completed={self.completed}, priority={self.priority})>"
        )
