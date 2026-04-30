from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# חיבור למסד הנתונים המקומי של הפרויקט
DATABASE_URL = "sqlite:///./school_trip.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# יצירת session לעבודה מול בסיס הנתונים
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# מחלקת בסיס לכל הטבלאות
Base = declarative_base()