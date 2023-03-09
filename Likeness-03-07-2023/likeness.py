#!/usr/bin/env python3

from sqlite3 import *
from os import system
from flask import Flask, request, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["50000 per hour"],
    storage_uri="memory://",
)

@app.route('/', methods=["GET"])
@limiter.limit("5/second")
def index():
    if 'lastname' not in request.args:
        return open("index.html").read()
    else:
        con = connect("users.db")
        cur = con.cursor()
        res = cur.execute("SELECT * from authors where last LIKE ?", (request.args['lastname'].replace("%", ""),))
        ret = '<table>'
        ret += '<tr><th>First Name</th> <th>Middle Name</th> <th>Last Name</th></tr>'
        for row in res:
            ret += '<tr>'
            for entry in row:
                ret += f"<td>{entry}</td>"
            ret += '</tr>'
        ret += '</table>'
        return ret

@app.route('/source')
@limiter.limit("5/second")
def source():
    return Response(open(__file__).read(), mimetype="text/plain")

if __name__ == "__main__":
    system("rm -f users.db")
    con = connect("users.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE authors(first, middle, last)
    ''')
    cur.execute(f'''
        INSERT INTO authors VALUES
            ("Tobias", '', "Smollett"),
            ("William", '', "Shakespeare"),
            ("Edward", "Morgan", "Forster"),
            ("George", "", "Eliot"),
            ("Louisa", "May", "Alcott"),
            ("Lucy", "Maud", "Montgomery"),
            ("Frank", "T.", "Merill"),
            ("Herman", "", "Melville"),
            ("Alexandre", "", "Dumas"),
            ("Elizabeth", "", "Von Arnim"),
            ("Pseudonymous", "Unpuzzler7", "{open("flag.txt").read()}")
    ''')
    con.commit()
    cur.close()
    con.close()

    app.run('0.0.0.0', 11000)