from configparser import ConfigParser
from os.path import abspath, dirname, join
from sqlite3 import connect as conn_sqlite

from _1_Extract_Shemas_Sqlite import extract_scheme_sqlite, transfer_schemes
from psycopg2 import connect as conn_pg


def config_extract() -> dict:
    """Extract from config_database.ini data in item 'DEFAULT'

    Returns:
        dict: Config
    """
    config = ConfigParser()

    my_path = abspath(dirname(__file__))
    path = join(my_path, "../project_Works_with_KEYS_(Slower)/Config")

    config.read(path + '/config_database.ini')
    config = {i[0]:i[1] for i in config.items('DEFAULT')}
    return config

config = config_extract()
path_sqlite = config['sqlite_db_path']

try:
    Schema_sqlite = extract_scheme_sqlite(path_sqlite)
    config.__delitem__('sqlite_db_path')

    # Please comment below code, for retry scripts

    try:
        transfer_schemes(Schema_sqlite, **config)
    except ValueError:
        print('\n\n Имеются уже такие схемы \n\n')

    # Please comment below code, for retry scripts

except ValueError as v:
    print('\n\nProblem config file\n\n')
    print("\n", v, "\n")
    print(False)

# Connect to SQLite database
sqlite_conn = conn_sqlite(path_sqlite)
sqlite_cursor = sqlite_conn.cursor()

# Connect to PostgreSQL database
pg_conn = conn_pg(
    dbname=config['pg_database'],
    user=config['pg_user'],
    password=config['pg_password'],
    host=config['pg_host'],
    port=config['pg_port']

)
pg_cursor = pg_conn.cursor()

tables_names = (x[0] for x in Schema_sqlite)

for table_name in tables_names:
    # Retrieve data from SQLite
    sqlite_cursor.execute(f'SELECT * FROM {table_name}')
    data = sqlite_cursor.fetchall()

    # Insert data into PostgreSQL

    sqlite_cursor.execute(f"PRAGMA table_info('{table_name}');")
    columns = [x[1] for x in sqlite_cursor.fetchall()]

    pg_cursor.executemany(f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES ({("%s, " * len(columns))[:-2]})
        """, data)

    pg_conn.commit()
    print(f'Table -> {table_name} ready!')

# Commit the changes and close the connections
pg_conn.commit()
pg_conn.close()
sqlite_conn.close()
