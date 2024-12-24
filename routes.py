from flask import Flask, redirect, url_for, render_template, jsonify, request
from Project import encrypt, decrypt
from flask_cors import CORS
import ast


app = Flask(__name__)
CORS(app)



@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/Encrypt.html", methods=['GET', 'POST'])
def Encrypt():
    if request.method == 'GET':
        # Retrieve form data
        key = request.form.get('key')
        plaintext = request.form.get('plaintext')

        # Validate input
        if not key or not plaintext:
            return render_template("Encrypt.html", error="Key and plaintext are required")

        # Perform encryption
        ciphertext = encrypt(plaintext, key)

        # Render the result on the same page
        return render_template("Encrypt.html", ciphertext=ciphertext)
    return render_template("Encrypt.html")

@app.route("/Decrypt.html")
def Decrypt():
    return render_template("Decrypt.html")

@app.route("/process_encryption", methods=['GET'])
def process_encryption():
    key = request.args.get('key')
    plaintext = request.args.get('plaintext')

    # Validate input
    if not key or not plaintext:
        return jsonify({"error": "Key and plaintext are required"}), 400

    # Perform encryption
    ciphertext, logs = encrypt(plaintext, key)

    # Return the ciphertext
    return jsonify({"ciphertext": str(ciphertext),"logs": logs})

@app.route("/process_decryption", methods=['GET'])
def process_decryption():
    key = request.args.get('key')
    ciphertext = request.args.get('ciphertext')
    ciphertext_bytes = bytes.fromhex(ciphertext)

    # Validate input
    if not key or not ciphertext:
        return jsonify({"error": "Key and ciphertext are required"}), 400

    # Perform encryption
    plaintext, logs = decrypt(ciphertext_bytes, key)

    # Return the ciphertext
    return jsonify({"plaintext": plaintext.decode('utf-8'),"logs": logs})


if __name__ == "__main__":
    app.run(debug=True)

