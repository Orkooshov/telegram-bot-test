from sqlalchemy import create_engine
from core.config import DatabaseConfig as db_conf
from database import entities


engine = create_engine(db_conf.connection_str,
                       echo=db_conf.echo,
                       pool_size=db_conf.pool_size)

def initialize_database() -> None:
    entities.Base.metadata.create_all(bind=engine)
