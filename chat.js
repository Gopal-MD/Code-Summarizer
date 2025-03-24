document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('code-form');
    const messagesContainer = document.getElementById('chat-messages');
    const codeInput = document.getElementById('code-input');
    const codeFile = document.getElementById('code-file');
    const languageSelect = document.getElementById('language');

    function addMessage(content, type = 'user') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.innerHTML = content;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function setLoading(isLoading) {
        const button = form.querySelector('button');
        button.disabled = isLoading;
        button.innerHTML = isLoading ? 
            '<span>Analyzing...</span><div class="loader"></div>' : 
            '<span>Analyze Code</span><svg class="send-icon" viewBox="0 0 24 24"><path fill="currentColor" d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>';
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const code = codeInput.value.trim();
        const file = codeFile.files[0];

        if (!code && !file) {
            addMessage('⚠️ Please provide some code or upload a file.', 'error');
            return;
        }

        setLoading(true);

        try {
            const formData = new FormData();
            if (file) {
                formData.append('code_file', file);
                addMessage(`📂 Analyzing file: <b>${file.name}</b>`, 'user');
            } else {
                formData.append('code', code);
                addMessage('📜 Analyzing provided code...', 'user');
            }
            formData.append('language', languageSelect.value);

            const response = await fetch('/summarize', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.redirect) {
                // ✅ Fix: Redirect manually to summary page
                window.location.href = data.redirect;
                return;
            }

            if (data.error) {
                addMessage(`❌ ${data.error}`, 'error');
            } else {
                addMessage(data.summary, 'bot');
            }

        } catch (error) {
            addMessage('❌ Sorry, there was an error processing your request.', 'error');
        } finally {
            setLoading(false);
        }
    });
});
