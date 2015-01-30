from flask import Flask, request

from flask import render_template
import sqlite3
import datetime

app = Flask(__name__)

@app.route('/')
def index(date = ""):
    date = request.args.get('date')

    if not date:
        now   = datetime.datetime.now()
        date = "%02d.%02d.%04d" % (now.day, now.month, now.year)

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    res = c.execute("SELECT STRFTIME('%%H', date), AVG(temp), AVG(hum) FROM data "
        "WHERE STRFTIME('%%d.%%m.%%Y', date)='%s' "
        "GROUP BY STRFTIME('%%H', date) " % (date, ))
    hour = list()
    temp = list()
    hum = list()
    for row in res:
        hour.append(row[0])
        temp.append("%.1f" % row[1])
        hum.append("%.1f" % row[2])

    return render_template('index.html', date = date, hour = hour, temp = temp, hum = hum)

if __name__ == '__main__':
    app.debug = True
    app.run(host = "127.0.0.1", port = 8888)
