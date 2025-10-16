# Simple Task List API

This is a repository for the Lush Mid Weight Python Interview Task.
The objective was to build a basic GraphQL API server using FastAPI, Python, SQLAlchemy, and Strawberry GraphQL to manage a simple list of tasks.

## Setup

1. Clone the repository
2. Create a virtual environment `python -m venv virtualenv`
3. Activate the virtual environment `source virtualenv/bin/activate`
4. Install all dependencies using requirements.txt `pip install -r ./requirements.txt`
5. Initalise empty database `python create_db.py`

## Run server

1. Start uvicorn server `uvicorn main:app --reload`
2. In the browser, open the address - 127.0.0.1:8000/graphql

# Example usage for interacting with the database

To query all tasks with all information, the following query can be used:
```
{
  tasks{
    id
    title
    completed
    createdAt
    updatedAt
    deadline
    priority
  }
}
```

Adding a task can be done like this:
```
mutation{
  addTask(title:"First Task"){
    id
    title
    completed
    createdAt
    updatedAt
    deadline
    priority
  }
}
```

Bonus: Updating a task works in the following way (the id needs to be adapted of course):
```
mutation{
  updateTask(id:"b002fd46-3d84-41a3-8027-2dc7d17c0452", title:"First Task amended", priority:10, deadline:"2025-10-16T23:59:59"){
    id
    title
    completed
    createdAt
    updatedAt
    deadline
    priority
  }
}
```

Toggling it to mark it as completed is achieved like this:
```
mutation{
  toggleTask(id:"b002fd46-3d84-41a3-8027-2dc7d17c0452"){
    id
    title
    completed
    createdAt
    updatedAt
    deadline
    priority
  }
}
```

Displaying a single task by its id would be the following:
```
{
  task(id:"b002fd46-3d84-41a3-8027-2dc7d17c0452"){
    id
    title
    completed
    createdAt
    updatedAt
    deadline
    priority
  }
}
```

Finally, a task is deleted using this:
```
mutation{
  deleteTask(id:"b002fd46-3d84-41a3-8027-2dc7d17c0452"){
    id
    title
    completed
    createdAt
    updatedAt
    deadline
    priority
  }
}
```
