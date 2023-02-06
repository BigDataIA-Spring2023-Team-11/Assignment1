import os
import logging
import sqlite3
import pandas as pd
from pathlib import Path

LOGLEVEL  =  os.environ.get('LOGLEVEL','INFO').upper()

logging.basicConfig(
format='%(asctime)s %(levelname)-85 % (message)s',
level=LOGLEVEL,
datefmt='%Y-%m-%d %H:%M:%S')



database_file_name = "database.db"
# ddl_file_name = ""
database_file_path  = os.path.join(os.path.dirname(__file__),database_file_name)
# ddl_file_path  = os.path.join(os.path.dirname(__file__),ddl_file_name)



def create_df():
    year = [2022] * 51 * 24 + [2023] * 32 * 24
    days_with_leading_zeros = []
    for i in range(1,33):
        days_with_leading_zeros.append(str(i).zfill(3))
    day = list(range(209, 260)) * 24 + days_with_leading_zeros * 24
    first_ten_hours = []
    for i in range(0,10):
        first_ten_hours.append(str(i).zfill(2))
    hour =  (first_ten_hours + list(range(10, 24))) * 83
    data = {"year": year, "day": day, "hour": hour}
    df = pd.DataFrame(data)
    return df

def create_table_in_db():
    conn = sqlite3.connect(database_file_path)
    # Insert data to table here

    df = create_df()
    df.to_sql("metadata", conn, if_exists = "replace")
    print(f"Data updated to table --> {df.shape}")
    # cursor.executescript(sql_script)
    conn.close()

def create_database():
    db = sqlite3.connect(database_file_path)
    cursor = db.cursor()
    db.commit()
    db.close()

def check_database_initilization():
    print(os.path.dirname(__file__))
    if not Path(database_file_path).is_file():
        logging.info(f"Database file not found, initilizing at: {database_file_path}")
        create_database()
        create_table_in_db()
    else:
        logging.info("Database file already exist")
        create_table_in_db()


def fetch_data_from_table():
    conn = sqlite3.connect(database_file_path)
    df = pd.read_sql('SELECT * FROM metadata', conn)
    return df


def main_database_func_trigger():
    print("IN MAIN Func")
    check_database_initilization()
    # query_into_dataframe()