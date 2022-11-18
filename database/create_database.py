import psycopg2
from getpass import getpass

answer = input("Would you like to create a new database? (Y/n): ")
if answer == 'Y':
    print("Enter your postgres password")
    # typed_password = input("Enter your postgres password: ")
    typed_password = getpass()
    connection = psycopg2.connect(
        database = "postgres", user="postgres", password=typed_password, host="127.0.0.1", port="5432"
    )
    print("Connection successful!")

    connection.autocommit = True
    cursor = connection.cursor()

    sql = '''CREATE database idlescape''';

    cursor.execute(sql)
    print("Database 'idlescape' created.")

    connection.close()