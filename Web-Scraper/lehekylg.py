from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:5491"

# Pärida scrape'itud andmeid
@app.route("/")
def index():
    try:
        tooted = requests.get(f"{API_URL}/riistad")
        tooted.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 500)
        riistad = tooted.json()
        return render_template("index.html", riistad=riistad)
    except requests.exceptions.RequestException as e:
        # Handle API request errors
        error_message = f"API request failed: {e}"
        return render_template("error.html", error_message=error_message)
    except ValueError as e:
        # Handle JSON decode errors
        error_message = f"Invalid JSON response from API: {e}"
        return render_template("error.html", error_message=error_message)

# Pärida andmeid mis on vähemalt X eur väärtusega
@app.route("/filter")
def filter():
    min_price = request.args.get("min_price", default=0, type=float)
    tooted = requests.get(f"{API_URL}/riistad?min_price={min_price}")
    riistad = tooted.json()
    return render_template("index.html", riistad=riistad)

if __name__ == "__main__":
    app.run(debug=True, port=5001)