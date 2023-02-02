
import sqlite3
from sqlite3 import Error

def create_connection(db_file):

   conn = None
   try:
       conn = sqlite3.connect(db_file)
       print(f"Connected to {db_file}, sqlite version: {sqlite3.version}")
   except Error as e:
       print(e)
   return conn


def execute_sql(conn, sql):

   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)

def add_project(conn, project):

   sql = '''INSERT INTO projects(nazwa, start_date, end_date)
             VALUES(?,?,?)'''
   cur = conn.cursor()
   cur.execute(sql, project)
   conn.commit()
   return cur.lastrowid


def add_task(conn, task):

    sql = '''INSERT INTO tasks(projekt_id, nazwa, opis, status, start_date, end_date)
             VALUES(?,?,?,?,?,?)'''

    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def select_all(conn, table):
   
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()

   return rows

def select_where(conn, table, **query):
  
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

def update(conn, table, id, **kwargs):
   
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

def delete_all(conn, table):

   sql = f'DELETE FROM {table}'
   cur = conn.cursor()
   cur.execute(sql)
   conn.commit()
   print("Deleted")

def delete_where(conn, table, **kwargs):

    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")



if __name__ == '__main__':

    create_projects_sql = """
   -- projects table
   CREATE TABLE IF NOT EXISTS projects (
      id integer PRIMARY KEY,
      nazwa text NOT NULL,
      start_date text,
      end_date text
   );
   """

    create_tasks_sql = """
   -- zadanie table
   CREATE TABLE IF NOT EXISTS tasks (
      id integer PRIMARY KEY,
      projekt_id integer NOT NULL,
      nazwa VARCHAR(250) NOT NULL,
      opis TEXT,
      status VARCHAR(15) NOT NULL,
      start_date text NOT NULL,
      end_date text NOT NULL,
      FOREIGN KEY (projekt_id) REFERENCES projects (id)
   );
   """

    db_file = "database.db"

    create_connection(db_file)

    conn = create_connection(db_file)

    if conn is not None:
        execute_sql(conn, create_projects_sql)
        execute_sql(conn, create_tasks_sql)
        print()
        add_project(conn, ("test", "coś", "test")) 
        add_task(conn, (1, "test", "inny", "test", "baza", "test")) 
        print(select_all(conn, "projects"))
        print()
        print(select_where(conn, "tasks", id = 5))
        print()
        update(conn, "tasks", 2, status="started")
        delete_where(conn, "tasks", id = 8)
        delete_all(conn, "tasks")
        conn.close()

    