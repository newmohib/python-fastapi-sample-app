
### Create vertual environment
- python -m venv venv
### activate the vertual environment
- windows: venv\Scripts\activate
- Linux/macOS: source venv/bin/activate
### install fastAPI inside project folder
- pip install "fastapi[standard]"
- create a file with main.py into root
- if need to be chenge port: /venv/lib/python3.11/site-packages/fastapi_cli/cli.py 8000 to another port
- fastapi dev app/main.py

#### validation pack
- pydantic

#### Database Setup
- pip install psycopg
- pip install "psycopg[binary]"
- pip install sqlalchemy // ORM
- 

