# pip install psycopg2
from sqlite3 import connect

from pandas import read_sql_query
from sqlalchemy import create_engine


def load_tables(sqlite_db_path=None,
                pg_user=None,
                pg_password=None,
                pg_host=None,
                pg_port=None,
                pg_database=None,
                table_names=None
                ) -> bool | None:
    """
    Connect sqlite - create engine sqlalchemy -
    Convert to dataframe pandas to sql - uploading postgresql

    Args:
        SQLITE:
            sqlite_db_path (_type_, optional): path sqlite '.DB' file. Defaults to None.

        PostgreSQL:
            pg_user (_type_, optional): user postgresql. Defaults to None.

            pg_password (_type_, optional): password postgresql. Defaults to None.

            pg_host (_type_, optional): host postgresql. Defaults to None.

            pg_port (_type_, optional): port postgresql. Defaults to None.

            pg_database (_type_, optional): database NAME postgresql. Defaults to None.

        SQLITE:
            table_names (_type_, optional): names table in SQLITE. Defaults to None.

    Returns:
        _type_: None
    """

    if not any(
        [sqlite_db_path,
            pg_user,
            pg_password,
            pg_host,
            pg_port,
            pg_database,
            table_names]
        ):
        print('\n\nProblem config file\n\n')
        return False

    # Create a SQLite connection
    sqlite_conn = connect(sqlite_db_path)

    # Create a PostgreSQL connection
    pg_engine = create_engine(
        f'postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}'
    )

    for table_name in table_names:
        # Read data from SQLite into a Pandas DataFrame
        query = f'SELECT * FROM {table_name}'
        df = read_sql_query(query, sqlite_conn)

        # Upload the Pandas DataFrame to PostgreSQL
        df.to_sql(table_name, pg_engine, index=False, if_exists='replace')

        print(f"Data upload for table {table_name} to PostgreSQL successful!")

    # Close SQLite connection
    sqlite_conn.close()


def sqlite_connect(sqlite_db_path:str) -> None:
    with connect(sqlite_db_path) as sqlite_conn:
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables_data = sqlite_cursor.fetchall()
        sqlite_cursor.close()

    return tables_data
