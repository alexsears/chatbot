function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    var customInstruction = document.getElementById('custom-instruction-input').value; // Get custom instruction
    document.getElementById('user-input').value = ''; // Clear the user input field

    // Update UI to show user's message
    var chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div>User: ${userInput}</div>`;

    // Send input to Python backend using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_message", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            chatBox.innerHTML += `<div>Chatbot: ${response.message}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the latest message
        }
    };
    var data = JSON.stringify({"message": userInput, "custom_instruction": customInstruction});
    xhr.send(data);
}


function addMessageToChatBox(sender, message) {
    var messageElement = document.createElement('div');
    messageElement.textContent = `${sender}: ${message}\n\n`; // Adding two line breaks after the message
    messageElement.style.whiteSpace = 'pre-wrap'; // Preserve whitespaces and line breaks
    document.getElementById('chat-box').appendChild(messageElement);
}
function sendCustomInstruction() {
    var instruction = document.getElementById('custom-instruction-input').value;
    document.getElementById('custom-instruction-input').value = '';

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_custom_instruction", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        console.log(xhr.responseText); 
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            console.log(response);  // Log the response to see its structure
            if (response && response.response) {
                addMessageToChatBox("Custom Response", response.response);
            } else {
                addMessageToChatBox("Custom Response", "No response or unexpected format received.");
            }
        }
    };
    var data = JSON.stringify({"instruction": instruction});
    xhr.send(data);
}

// You can reuse the addMessageToChatBox function from your previous implementation


