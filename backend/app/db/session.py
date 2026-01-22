from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.core.config import(
    DB_SERVER,DB_NAME,DB_TRUSTED_CONNECTION,DB_DRIVER,DB_USER,DB_PASSWORD
)

def make_url() -> URL:
    # SQL Server Authentication
    if DB_TRUSTED_CONNECTION in ("no", "false", "0"):
        return URL.create(
            "mssql+pyodbc",
            query={
                "odbc_connect": (
                    f"DRIVER={{{DB_DRIVER}}};"
                    f"SERVER={DB_SERVER};"
                    f"DATABASE={DB_NAME};"
                    f"UID={DB_USER};"
                    f"PWD={DB_PASSWORD};"
                    "Encrypt=yes;"
                    "TrustServerCertificate=yes;"
                )
            },
        )

        # Windows Authentication
        return URL.create(
            "mssql+pyodbc",
            query={
            "odbc_connect": (
                f"DRIVER={{{DB_DRIVER}}};"
                f"SERVER={DB_SERVER};"
                f"DATABASE={DB_NAME};"
                "Trusted_Connection=yes;"
                "Encrypt=yes;"
                "TrustServerCertificate=yes;"
            )
        },
    )


engine=create_engine(make_url(),pool_pre_ping=True)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()