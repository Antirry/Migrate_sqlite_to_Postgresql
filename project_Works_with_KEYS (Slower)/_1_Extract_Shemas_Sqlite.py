from sqlite3 import connect as conn_sqlite

from _0_Sort_tables_by_graph import check_ref_table, topological_sort
from psycopg2 import connect as conn_pg


def extract_scheme_sqlite(sqlite_db_path=None) -> list[tuple]:
    """Pulling from SQLite with sorting fun "topological_sort"
    for further loading of data schema into DB PostgreSQL

    Args:
        SQLITE:
            sqlite_db_path (_type_, optional): path sqlite '.DB' file. Defaults to None.

    Returns:
        List[tuple]: List names and SQL schemes tables
    """

    with conn_sqlite(sqlite_db_path) as sqlite_conn:
        schema_query = "SELECT name, sql FROM sqlite_master WHERE type='table'"
        schema_results = sqlite_conn.execute(schema_query).fetchall()

    ref_table = {}
    ref_table_list = list(map(check_ref_table, schema_results))
    list(map(ref_table.update, ref_table_list))

    table_names = topological_sort(ref_table)
    table_names = list(dict.fromkeys(table_names))

    print("Таблицы в базе данных SQLite, (В порядке их создания) -> \n", table_names)
    print('Tables in a SQLite database, (In order of their creation) -> \n',
        table_names)

    NamesQueries = sorted(schema_results, key=lambda x: table_names.index(x[0]))

    return NamesQueries



def transfer_schemes(NamesQueries: list[str],
                pg_user=None,
                pg_password=None,
                pg_host=None,
                pg_port=None,
                pg_database=None) -> None:
    """Transfer schemes from SQLite DB in PostgreSQL

    Args:
        NamesQueries (list[str]): Returned from extract_scheme_sqlite
                                (List names and SQL schemes tables)

        PostgreSQL:
            pg_user (_type_, optional): user postgresql. Defaults to None.

            pg_password (_type_, optional): password postgresql. Defaults to None.

            pg_host (_type_, optional): host postgresql. Defaults to None.

            pg_port (_type_, optional): port postgresql. Defaults to None.

            pg_database (_type_, optional): database NAME postgresql. Defaults to None.

    """

    with conn_pg(dbname=pg_database,
                        user=pg_user,
                        password=pg_password,
                        host=pg_host,
                        port=pg_port) as pg_conn:
        with pg_conn.cursor() as pg_cursor:
            [pg_cursor.execute(result[1]) for result in NamesQueries]
            print("Схема перенесена, поздравляю!")
            print('The scheme has been moved in PostgreSQL, congratulations!')
