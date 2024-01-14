# import required libraries
import sqlite3
from sqlite3 import Error

# function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

# function to create a table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# main code to create the database and table
def main():
    database = r"topgame.db"

    # SQL table creation statement
    sql_create_games_table = """ CREATE TABLE IF NOT EXISTS games (
                                        game_id integer PRIMARY KEY,
                                        game_name text NOT NULL,
                                        weekly_plays integer NOT NULL,
                                        monthly_plays integer NOT NULL,
                                        last_played_week INTEGER,
                                        last_played_month INTEGER
                                    ); """
    
    sql_create_voice_activity_table = """ CREATE TABLE IF NOT EXISTS voice_activity (
                                              user_id integer PRIMARY KEY,
                                              user_name text NOT NULL,
                                              weekly_voice_minutes integer NOT NULL,
                                              monthly_voice_minutes integer NOT_NULL
                                          ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_games_table)
        create_table(conn, sql_create_voice_activity_table)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()