import strawberry
from typing import List, Optional, Annotated
import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task
import uuid
import logging

logger = logging.getLogger(__name__)

@strawberry.type
class TaskType:
    id: uuid.UUID # A unique identifier (e.g., UUID string or integer).
    title: str # A string describing the task (required).
    completed: bool = False # A boolean indicating if the task is done (defaults to False).
    created_at: datetime.datetime # A timestamp indicating when the task was created.
    updated_at: datetime.datetime # A timestamp indicating when the task was last updated.
    deadline: Optional[datetime.datetime] = None # A timestamp indicating when the task has to be finished.
    priority: int # A priority for the task ranging from 0 (low priority) to 10 (high priority), defaulting to 5.

    @staticmethod
    def from_model(task: Task) -> "TaskType":
        return TaskType(
            id=uuid.UUID(task.id),
            title=task.title,
            completed=task.completed,
            created_at=task.created_at,
            updated_at=task.updated_at,
            deadline=task.deadline,
            priority=task.priority,
        )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@strawberry.type
class Query:
    @strawberry.field
    def tasks(self, search: Optional[str] = None) -> List[TaskType]:
        """ Query: tasks: Returns a list of all tasks. An optional search argument can be provided,
            which filters tasks on the title."""
        db: Session = next(get_db())
        if search is None:
            tasks = db.query(Task).all()
        else:
            tasks = db.query(Task).filter(Task.title.ilike(f"%{search}%")).all()
        return [TaskType.from_model(task) for task in tasks]

    @strawberry.field
    def task(self, id: uuid.UUID) -> TaskType | None:
        """ Query: task(id: ID!): Returns a single task by its ID. Returns null if not found."""
        db: Session = next(get_db())
        task = db.get(Task, str(id))
        if task is None:
            logger.warning(f"Task with id {id} not found in database")
            return None
        else:
            return TaskType.from_model(task)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_task(
            self,
            title: str,
            deadline: datetime.datetime = None,
            priority: int = 5
            ) -> TaskType:
        """ Mutation: add_task(title: str!): Creates a new task with the given title, assigns a
            unique ID, sets completed to False, and appropriate timestamps. Returns the newly
            created task.
        """
        db: Session = next(get_db())

        # generate uuid4 and check uniqueness
        id = uuid.uuid4()
        while db.get(Task, str(id)) is not None:
            # if the id is already present in the db, just generate a new one
            id = uuid.uuid4()
        
        new_task = Task(
            id=str(id),
            title=title,
            completed=False,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
            deadline=deadline,
            priority=priority,
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return TaskType.from_model(new_task)

    @strawberry.mutation
    def toggle_task(self, id: uuid.UUID) -> TaskType | None:
        """ Mutation: toggle_task(id: ID!): Finds a task by ID and toggles its completed status.
            Updates the updated_at timestamp. Returns the updated task or null if not found."""
        db: Session = next(get_db())

        task = db.get(Task, str(id))
        if task is None:
            logger.warning(f"Task with id {id} not found for toggling")
            return None

        task.completed = True
        task.updated_at = datetime.datetime.utcnow()

        db.commit()
        db.refresh(task)
        return TaskType.from_model(task)

    @strawberry.mutation
    def delete_task(self, id: uuid.UUID) -> TaskType | None:
        """ Mutation: delete_task(id: ID!): Deletes a task by its ID. Returns the deleted task or
            null if not found."""
        db: Session = next(get_db())

        task = db.get(Task, str(id))
        if task is None:
            logger.warning(f"Task with id {id} not found for deletion")
            return None

        db.delete(task)
        db.commit()
        return TaskType.from_model(task)

    @strawberry.mutation
    def update_task(
            self,
            id: uuid.UUID,
            title: str = None,
            deadline: datetime.datetime = None,
            priority: int = None
            ) -> TaskType | None:
        """ Mutation: update_task(id: ID!): Updates a task by its ID. Returns the updated task or
            null if not found."""
        db: Session = next(get_db())

        task = db.get(Task, str(id))
        if task is None:
            logger.warning(f"Task with id {id} not found for update")
            return None

        # update all given parameters
        if title is not None:
            task.title = title

        if deadline is not None:
            task.deadline = deadline

        if priority is not None:
            task.priority = priority

        task.updated_at = datetime.datetime.utcnow()

        db.commit()
        db.refresh(task)
        return TaskType.from_model(task)

schema = strawberry.Schema(query=Query, mutation=Mutation)
