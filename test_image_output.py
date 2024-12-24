import base64

base64_string = ""  # Full string here

base64_data = base64_string.split(",")[1]

try:
    # Decode the Base64 string into binary data
    image_data = base64.b64decode(base64_data)

    # Save the binary data as a JPEG file
    with open("output.jpg", "wb") as image_file:
        image_file.write(image_data)

    print("Decryption successful! Image saved as 'output.jpg'.")

    # Optional: Verify if the saved file is a valid JPEG
    from PIL import Image
    with Image.open("output.jpg") as img:
        img.verify()  # This checks if the file is a valid image
    print("The saved file is a valid JPEG image.")
except Exception as e:
    print(f"Decryption failed: {e}")
