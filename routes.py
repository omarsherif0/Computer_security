from flask import Flask, redirect, url_for, render_template, jsonify, request
# omar import
# from Project import encrypt, decrypt
from aes_utils import encrypt, decrypt
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

        # Formatting the ciphertext for better readability (add spaces every 8 characters)
        formatted_ciphertext = ' '.join([ciphertext[i:i+8] for i in range(0, len(ciphertext), 8)])

        # Assuming 'logs' is available after encryption, format the logs with a line break after each array
        formatted_logs = ""
        for log in logs:
            formatted_logs += f"Round {log['round']} - {log['step']}:\n"
            # Assuming log['state'] is a 2D array, format each array on a new line
            for array in log['state']:
                formatted_logs += f"    {array}\n"  # Add a newline after each array for better readability
            formatted_logs += "\n"  # Add a newline between log entries

        # Combine the formatted ciphertext and logs into one variable
        formatted_output = f"Ciphertext:\n{formatted_ciphertext}\n\nLogs:\n{formatted_logs}"

        # Render the result on the same page
        return render_template("imgs.html", ciphertext=formatted_output)


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
    app.run(debug=True, port=9001)