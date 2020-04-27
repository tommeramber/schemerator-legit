from flask import Flask, render_template, abort
import sqlite3
from prettytable import from_db_cursor

app = Flask(__name__)

@app.route('/')
def hello_world():
    connection = sqlite3.connect("/home/db/db.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Schemas")
    mytable = from_db_cursor(cursor)
    return render_template('layout.html', table=mytable.get_html_string())

if __name__ == "__main__":
  app.run(host='0.0.0.0' ,port=8080)
