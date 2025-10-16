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



