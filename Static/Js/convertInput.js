function convertToBinary() {
    const inputElement = document.getElementById("key");
    let input = inputElement.value.trim();
    
    if (input === "") {
        alert("Input cannot be empty!");
        return;
    }

    let binaryRepresentation = "";

    if (/^[0-9a-fA-F]+$/.test(input)) {
        binaryRepresentation = hexToBinary(input);
        console.log("Input treated as hexadecimal.");
    } 
    else {
        binaryRepresentation = textToBinary(input);
        console.log("Input treated as plain text.");
    }

    console.log(`Binary Representation: ${binaryRepresentation}`);
    alert(`Binary Representation: ${binaryRepresentation}`);
    inputElement.value = binaryRepresentation;
}

function hexToBinary(hex) {
    return hex.split("")
        .map(h => parseInt(h, 16).toString(2).padStart(4, "0"))
        .join("");
}

// Helper Function: Convert text (UTF-8) to binary
function textToBinary(text) {
    return Array.from(new TextEncoder().encode(text)) // Convert to bytes
        .map(byte => byte.toString(2).padStart(8, "0")) // Convert each byte to 8-bit binary
        .join(" ");
}
