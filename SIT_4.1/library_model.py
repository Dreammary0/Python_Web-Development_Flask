import pandas as pd
def get_publisher(conn):
 return pd.read_sql("SELECT * FROM publisher", conn)

def get_genre(conn):
 return pd.read_sql("Select * from genre",conn)

def get_author(conn):
 return pd.read_sql("Select * from author",conn)

def get_book(conn):
 return pd.read_sql("Select * from book",conn)

def get_book_author(conn):
 return pd.read_sql("Select * from book_author",conn)

def get_book_reader(conn):
 return pd.read_sql("Select * from book_reader",conn)

def get_reader(conn):
 return pd.read_sql("Select * from reader",conn)

