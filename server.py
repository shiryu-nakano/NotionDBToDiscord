from flask import Flask, request
app = Flask(__name__)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    return f"Received code: {code}"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
