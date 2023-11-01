function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const chatLog = document.getElementById("chat-log");

    // Display the user's message in the chat log
    chatLog.innerHTML += `<div class="user-message">${userInput}</div>`;

    // Send the user message to the chatbot server (replace 'your-api-endpoint' with the actual URL)
    fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        body: JSON.stringify({ user_message: userInput }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Display the chatbot's response in the chat log
        chatLog.innerHTML += `<div class="bot-message">${data.bot_response}</div>`;
    });

    // Clear the user input field
    document.getElementById("user-input").value = '';
}

