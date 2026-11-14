from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"mensagem": "Mini estufa automatizada."}), 200

if __name__ == "__main__":
    app.run(debug=True)