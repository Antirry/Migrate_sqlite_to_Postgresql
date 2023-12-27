from configparser import ConfigParser
from os.path import abspath, dirname, join

from _1_load_tables import load_tables, sqlite_connect

config = ConfigParser()

my_path = abspath(dirname(__file__))
path = join(my_path, "../project/Config/config_database.ini")

config.read(path)
config = {i[0]:i[1] for i in config.items('DEFAULT')}

# Connect to the SQLite database

table_names = [name[0] for name in sqlite_connect(config['sqlite_db_path'])]

print(table_names)

config.update({'table_names': table_names})

# Call the function to load multiple tables
load_tables(**config)
