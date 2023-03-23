from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine

load_dotenv()

print(f'''mysql+pymysql://{getenv("DATABASE_USERNAME")}:{getenv("DATABASE_PASSWORD")}@ap-south.connect.psdb.cloud/projects?charset=utf8mb4''')

db = create_engine(
    f'''mysql+pymysql://{getenv("DATABASE_USERNAME")}:{getenv("DATABASE_PASSWORD")}@ap-south.connect.psdb.cloud/projects?charset=utf8mb4''',
    connect_args={
        "ssl": {
            "ssl_ca": getenv("DATABASE_SSL")
        }
    }    
)
