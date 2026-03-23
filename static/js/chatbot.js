document.addEventListener('DOMContentLoaded', function () {
    const chatLauncher = document.getElementById('chat-launcher');
    const chatBox = document.querySelector('.chat-box');
    const chatBoxToggle = document.querySelector('.chat-box-toggle');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatLogs = document.querySelector('.chat-logs');

    // Toggle Chat
    if (chatLauncher) {
        chatLauncher.addEventListener('click', function (e) {
            e.preventDefault();
            if (chatBox.style.display === 'block') {
                chatBox.style.display = 'none';
            } else {
                chatBox.style.display = 'block';
            }
        });
    }

    chatBoxToggle.addEventListener('click', function () {
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
                    let responseHtml = `<div><strong>${data.message}</strong></div>`;
                    if (data.results && data.results.length > 0) {
                        responseHtml += `<div class="mt-2 text-start">`;
                        data.results.forEach(notice => {
                            let title = notice.title;
                            let desc = notice.description ? `<p class="mb-2 text-muted" style="font-size:0.85rem; line-height: 1.2;">${notice.description}</p>` : "";
                            
                            responseHtml += `
                            <div class="card border-0 shadow-sm mb-2" style="background-color: rgba(255,255,255,0.8);">
                                <div class="card-body p-2">
                                    <h6 class="card-title fw-bold mb-1" style="color: var(--primary); font-size:0.95rem;">${title}</h6>
                                    ${desc}
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <span class="badge bg-secondary" style="font-size:0.75rem;">${notice.category}</span>
                                        <span class="text-muted" style="font-size:0.75rem;"><i class="bi bi-calendar3"></i> ${notice.date}</span>
                                    </div>
                                    <div class="text-center">
                                        <a href="${notice.url}" class="btn btn-sm btn-primary py-1 px-3 rounded-pill w-100" style="font-size:0.8rem; background: linear-gradient(135deg, var(--primary), #6366f1); border:none;">View Notice</a>
                                    </div>
                                </div>
                            </div>
                            `;
                        });
                        responseHtml += `</div>`;
                    }
                    generateMessage(responseHtml, 'bot');
                })
                .catch(error => {
                    console.error('Error:', error);
                    generateMessage("Sorry, something went wrong. Please try again.", 'bot');
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
