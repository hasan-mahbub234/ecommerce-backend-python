from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# MySQL Database URL format
DATABASE_URL = "mysql+pymysql://mahbubdb:mahbub123@localhost:3306/ecommerce_website"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
def init_db():
    SQLModel.metadata.create_all(engine)


# Sync session maker
def get_session():
    # Define the sessionmaker correctly
    Session = sessionmaker(
        bind=engine,
        expire_on_commit=False,  # Keep objects attached to the session after commit
    )
    session = Session()  # Create the session synchronously
    return session