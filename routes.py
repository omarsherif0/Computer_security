import re
from flask import Flask, redirect, url_for, render_template, jsonify, request
from aes_utils import encrypt, decrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Function to validate the AES key (32 bytes, hexadecimal)
# Function to validate the AES key (32 bytes, hexadecimal)
# Function to validate the AES key
def validate_key(key):
    # Check if the key length is between 8 and 64 characters
    if len(key) < 8 or len(key) > 64:
        return False, "Key must be between 8 and 64 characters long."
    
    # Check if the key contains at least one number, one uppercase letter, and one special character
    if not re.search(r'[0-9]', key):  # At least one number
        return False, "Key must contain at least one number."
    if not re.search(r'[A-Z]', key):  # At least one uppercase letter
        return False, "Key must contain at least one uppercase letter."
    if not re.search(r'[\W_]', key):  # At least one special character (non-alphanumeric)
        return False, "Key must contain at least one special character."
    
    return True, "Key is valid."

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

        # Validate the key
        is_valid, message = validate_key(key)
        if not is_valid:
            return render_template("Encrypt.html", error=message)

        # Perform encryption
        ciphertext = encrypt(plaintext, key)

        # Formatting the ciphertext for better readability (add spaces every 8 characters)
        formatted_ciphertext = ' '.join([ciphertext[i:i+8] for i in range(0, len(ciphertext), 8)])

        # Assuming 'logs' is available after encryption, format the logs with a line break after each array
        formatted_logs = ""
        for log in logs:
            formatted_logs += f"Round {log['round']} - {log['step']}:\n"
            for array in log['state']:
                formatted_logs += f"    {array}\n"
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

    # Validate the key
    is_valid, message = validate_key(key)
    if not is_valid:
        return jsonify({"error": message}), 400

    # Perform encryption
    ciphertext, logs = encrypt(plaintext, key)

    # Return the ciphertext and logs
    return jsonify({"ciphertext": str(ciphertext), "logs": logs})

@app.route("/process_decryption", methods=['GET'])
def process_decryption():
    key = request.args.get('key')
    ciphertext = request.args.get('ciphertext')
    ciphertext_bytes = bytes.fromhex(ciphertext)

    # Validate input
    if not key or not ciphertext:
        return jsonify({"error": "Key and ciphertext are required"}), 400

    # Validate the key
    is_valid, message = validate_key(key)
    if not is_valid:
        return jsonify({"error": message}), 400

    # Perform decryption
    plaintext, logs = decrypt(ciphertext_bytes, key)

    # Return the plaintext and logs
    return jsonify({"plaintext": plaintext.decode('utf-8'), "logs": logs})

if __name__ == "__main__":
    app.run(debug=True, port=9001)
