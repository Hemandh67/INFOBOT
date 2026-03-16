document.addEventListener('DOMContentLoaded', function () {
    const chatCircle = document.getElementById('chat-circle');
    const chatBox = document.querySelector('.chat-box');
    const chatBoxToggle = document.querySelector('.chat-box-toggle');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatLogs = document.querySelector('.chat-logs');

    // Toggle Chat
    chatCircle.addEventListener('click', function () {
        chatCircle.style.display = 'none';
        chatBox.style.display = 'block';
    });

    chatBoxToggle.addEventListener('click', function () {
        chatCircle.style.display = 'flex';
        chatBox.style.display = 'none';
    });

    // Handle Submit
    chatForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const msg = chatInput.value.trim();
        if (msg) {
            generateMessage(msg, 'user');
            chatInput.value = '';

            // Send to Backend
            fetch(`/chatbot-api/?query=${encodeURIComponent(msg)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.results && data.results.length > 0) {
                        let responseHtml = "I found these notices:<br>";
                        data.results.forEach(notice => {
                            responseHtml += `<a href="${notice.url}" style="color:white; text-decoration:underline;">${notice.title}</a> (${notice.date})<br>`;
                        });
                        generateMessage(responseHtml, 'bot');
                    } else {
                        generateMessage("Sorry, I couldn't find any notices matching your query.", 'bot');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    generateMessage("Sorry, something went wrong.", 'bot');
                });
        }
    });

    function generateMessage(msg, type) {
        const str = `
        <div class="chat-msg ${type}">
            <div class="cm-msg-text">
                ${msg}
            </div>
        </div>
        <div style="clear:both;"></div>`;

        chatLogs.insertAdjacentHTML('beforeend', str);
        chatLogs.scrollTop = chatLogs.scrollHeight;
    }
});
