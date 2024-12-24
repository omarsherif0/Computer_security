function validateAndPadKey() {
    const keyInput = document.getElementById("key");
    let key = keyInput.value.trim();

    const hexRegex = /^[0-9a-fA-F]+$/;
    if (!hexRegex.test(key)) {
        alert("Invalid key: The key must be a valid hexadecimal string.");
        return; 
    }

    let keyBytes = hexToBytes(key);
    const keyLength = keyBytes.length;
    const validSizes = [16, 24, 32]; 

    let nearestSize = validSizes.find(size => size >= keyLength) || 32;

    if (keyLength < nearestSize) {
        const paddingLength = nearestSize - keyLength;
        const padding = new Uint8Array(paddingLength).fill(paddingLength); // PKCS#7 padding bytes
        const paddedKey = new Uint8Array([...keyBytes, ...padding]);

        key = bytesToHex(paddedKey); 
        console.log(`Key padded to ${nearestSize * 8} bits: ${key}`);
    } else if (validSizes.includes(keyLength)) {
        console.log(`Key is already valid (${keyLength * 8} bits).`);
    } else {
        console.error(`Invalid key size (${keyLength * 8} bits). Unable to pad.`);
        return;
    }

    keyInput.value = key;
}

function hexToBytes(hex) {
    const bytes = new Uint8Array(hex.length / 2);
    for (let i = 0; i < hex.length; i += 2) {
        bytes[i / 2] = parseInt(hex.substr(i, 2), 16);
    }
    return bytes;
}

function bytesToHex(bytes) {
    return Array.from(bytes).map(b => b.toString(16).padStart(2, "0")).join("");
}


  

function encryptData() {
    validateAndPadKey();
    const key = document.getElementById("key").value;
    const plaintext = document.getElementById("plaintext").value;
    document.getElementById("traceContent").innerText = ""; // Clear trace steps
}

function showTrace() {
    const key = document.getElementById("key").value;
    const plaintext = document.getElementById("plaintext").value;
    let traceSteps = "Step 1: Key entered: " + key + "\n";
    traceSteps += "Step 2: Plaintext entered: " + plaintext + "\n";
    traceSteps += "Step 3: Performing encryption... (Mock Step)\n";
    traceSteps += "Step 4: Encryption Complete.";

    document.getElementById("traceContent").innerText = traceSteps;
    document.getElementById("traceBox").style.display = "block";
}

function clearFields() {
    document.getElementById("key").value = "";
    document.getElementById("plaintext").value = "";
    document.getElementById("traceContent").innerText = "Steps will appear here...";
}

function copyToClipboard() {
    const plaintext = document.getElementById("plaintext");
    plaintext.select();
    plaintext.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(plaintext.value);
    alert("Copied to clipboard: " + plaintext.value);
}