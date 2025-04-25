import os
import psycopg2
from dotenv import load_dotenv 

load_dotenv()


class NewDatabaseConnection:
    def __init__(self) -> None:
        pass

    @staticmethod
    def _connection():
        """
            Args: None
            Returns: New postgres connection
        """

        return psycopg2.connect(
                                user = os.getenv("PG_USER"),
                                password = os.getenv("PG_PASS"),
                                database = os.getenv("PG_DB"),
                                host = os.getenv("PG_HOST"),
                                port = os.getenv("PG_PORT")
                            )
        
