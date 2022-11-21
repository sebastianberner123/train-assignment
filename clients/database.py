import pyodbc


class DatabaseClient:
    """A class that provides a db connection with context management"""

    def __init__(self, server: str, database: str, username: str, password: str):

        print(f"Connecting to database '{database}'")
        driver = "{ODBC Driver 17 for SQL Server}"
        self.dsn = f"DRIVER={driver};SERVER={server},1433;DATABASE={database};UID={username};PWD={password}"
        self.connection = pyodbc.connect(self.dsn, autocommit=False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

    def close(self):
        if self.connection:
            self.connection.close()