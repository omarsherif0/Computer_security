let logs = [];  

      async function encryptData() {
        const key = document.getElementById('key').value;
        const plaintext = document.getElementById('plaintext').value;

        if (!key || !plaintext) {
          alert('Key and plaintext are required!');
          return;
        }

        try {
          const url = `/process_encryption?key=${encodeURIComponent(key)}&plaintext=${encodeURIComponent(plaintext)}`;
          const response = await fetch(url);

          if (response.ok) {
            const result = await response.json();
            
            // Display the ciphertext
            document.getElementById('cipher').textContent = result.ciphertext;

            // Get the logs and update slider range
            logs = result.logs;
            const logsContainer = document.getElementById('logsContainer');
            logsContainer.innerHTML = ''; // Clear previous logs

            // Display the first log by default
            const firstLog = logs[0];
            logsContainer.innerHTML = `Round ${firstLog.round} - ${firstLog.step}: ${JSON.stringify(firstLog.state)}`;

            // Set the slider range based on the number of logs
            const logSlider = document.getElementById('logSlider');
            logSlider.max = logs.length - 1;

            // Listen for slider changes to display the corresponding log
            logSlider.addEventListener('input', (event) => {
              const logIndex = event.target.value;
              const log = logs[logIndex];
              logsContainer.innerHTML = `Round ${log.round} - ${log.step}: ${JSON.stringify(log.state)}`;
            });

          } else {
            const error = await response.json();
            alert('Error: ' + (error.error || 'Unknown error occurred'));
          }
        } catch (error) {
          console.error('Encryption failed:', error);
          alert('An error occurred during encryption.');
        }
      }
      async function decryptData() {
        // Retrieve user inputs
        const key = document.getElementById('key').value;
        const ciphertext = document.getElementById('Ciphertext').value;
        console.log(ciphertext)
        console.log(key)
        // Validate inputs
        if (!key || !ciphertext) {
          alert('Key and ciphertext are required!');
          return;
        }

        try {
          const url = `/process_decryption?key=${encodeURIComponent(key)}&ciphertext=${encodeURIComponent(ciphertext)}`;
          const response = await fetch(url);
          console.log(typeof(ciphertext))   
          console.log(ciphertext)
          if (response.ok) {
            const result = await response.json();
            
            // Display the ciphertext
            document.getElementById('plaintext').textContent = result.plaintext;

            // Get the logs and update slider range
            logs = result.logs;
            const logsContainer = document.getElementById('logsContainer');
            logsContainer.innerHTML = ''; // Clear previous logs

            // Display the first log by default
            const firstLog = logs[0];
            logsContainer.innerHTML = `Round ${firstLog.round} - ${firstLog.step}: ${JSON.stringify(firstLog.state)}`;

            // Set the slider range based on the number of logs
            const logSlider = document.getElementById('logSlider');
            logSlider.max = logs.length - 1;

            // Listen for slider changes to display the corresponding log
            logSlider.addEventListener('input', (event) => {
              const logIndex = event.target.value;
              const log = logs[logIndex];
              logsContainer.innerHTML = `Round ${log.round} - ${log.step}: ${JSON.stringify(log.state)}`;
            });

          } else {
            const error = await response.json();
            alert('Error: ' + (error.error || 'Unknown error occurred'));
          }
        } catch (error) {
          console.error('Decryption failed:', error);
          alert('An error occurred during encryption.');
        }
      }
  async function handle_image(){
        // Function to handle the file upload
    document.getElementById('imageUpload').addEventListener('change', function(event) {
      const file = event.target.files[0]; // Get the uploaded file
      if (file) {
        console.log(`File selected: ${file.name}`);
        
        // Check the file type (if needed)
        if (!file.type.startsWith('image/')) {
          alert('Please upload a valid image file.');
          return;
        }

        // Read the file content and encode it as Base64
        const reader = new FileReader();
        reader.onload = function(e) {
          const fileContent = e.target.result; // Base64-encoded file content
          console.log('File content loaded:', fileContent);

          // Send the file content as a GET request
          const encodedFile = encodeURIComponent(fileContent);
          const fileName = encodeURIComponent(file.name);

          const url = `/upload?fileName=${fileName}&fileContent=${encodedFile}`;
          
          fetch(url, {
            method: 'GET',
          })
          .then(response => response.json())
          .then(data => {
            console.log('File uploaded successfully:', data);
            alert('File uploaded successfully.');
          })
          .catch(error => {
            console.error('Error uploading file:', error);
            alert('Error uploading file.');
          });
        };

        reader.readAsDataURL(file); // Read as Base64-encoded string
      }
    });
  }