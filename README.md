## Migrate from SQLite To PostgreSQL

Чтобы запустить программу ***"_1_migrate_use_sqlalchemy.py"***   
нужно заполнить файл ***"config_database.ini"*** в такой форме:

To run ***"_1_migrate_use_sqlalchemy.py"***,  
you must fill in the ***"config_database.ini"*** file in this form:

```py
[DEFAULT]
# SQLite database file path
sqlite_db_path = (FULLPATH)XXX/project_Working_with_KEYS/Config
# PostgreSQL connection parameters

# CREATE YOUR DATABASE USE QUERY IN POSTGRESQL ->
# CREATE DATABASE *name*
pg_database = XXX

pg_user = XXX
pg_password = XXX
pg_host = XXX
pg_port = XXX
```

# Slower Version

## Как работает эта программа? / How does the script work?

## File: '_0_Sort_tables_by_graph.py'

### Function: 'check_ref_table'

Extracts the ***'REFERENCES'*** from the query,  
i.e. the previously created tables and  
adds its predecessor keys to each table  
with the table name and builds the graph as a dictionary.

Извлечение из запроса ***'REFERENCES'***,   
то есть созданных таблиц ранее и добавляет в каждую таблицу   
ключи ее предшественников с именем таблицы и строит граф в виде словаря.  

### Function: 'topological_sort'

Then it is sorted using ***'topological sort'***

Дальше идет его сортировка с использованием ***'topological sort'***

## File: '_1_Extract_Shemas_Sqlite.py'

### Function: extract_scheme_sqlite

Вытаскивание из SQLite с помощью сортировки "topological_sort"   
для последующей загрузки схемы данных в DB PostgreSQL с использованием подключения через sqlite3

Pulling from SQLite with sorting fun "topological_sort"   
for further loading of data schema into DB PostgreSQL using sqlite3 connection

### Function: transfer_schemes

Transfer schemes from SQLite DB in PostgreSQL с использованием подключения через psycopg2

Transfer schemes from SQLite DB in PostgreSQL using psycopg2 connection

## File: '_2_Load_Data_to_PostgreSQL.py'

Загрузка данных через psycopg2 cursor через executemany

Loading data via psycopg2 cursor through executemany



# Faster Version

## File: '_1_load_tables.py'

### Conversion to Postgresql / Конвертация в PostgreSQL

### Function: 'load_tables'

1. Connect sqlite
2. create engine sqlalchemy
3. Convert to dataframe pandas to sql 
4. uploading postgresql

---

1. Подключение к sqlite
2. Создание двигателя sqlalchemy
3. Конвертация в датафрейм pandas, после в SQL
4. Загрузка в postgresql

## File: '_2_migrate_use_sqlalchemy.py'

Забирает данные с config_database и запускает дополненный конфиг с названиями таблиц с использованием подключения sqlite3

Takes data from config_database and runs extended config with table names using sqlite3 connection

<span style="font-weight:700;font-size:21px">
Test SQLite database -> 'longlist.db'
</span>
<br />
<span style="font-weight:700;font-size:21px">
Тестовая SQLite база данных -> 'longlist.db'
</span># Migrate_sqlite_to_Postgresql111
