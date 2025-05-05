from flask import Flask, request, jsonify
import sqlite3
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, parse_qs
#from multiprocessing import Process

app = Flask(__name__)

# Andmebaasi pärimine
def query_db():#query, args=()):#, one=False):
    conn = sqlite3.connect("amblik.db")
    conn.row_factory = sqlite3.Row
    return conn

# Pärida scrape'itud andmeid (GET)
@app.route("/riistad", methods=["GET"])
def get_scraped_products():
    min_price = request.args.get("min_price", default=0, type=float)

    conn = query_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM andmed WHERE Price >= ?", (min_price,))
    riistad = cur.fetchall()
    conn.close()

    return jsonify([dict(row) for row in riistad])

if __name__ == "__main__":
    app.run(debug=True, port=5491)