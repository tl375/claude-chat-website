// Futuristic GPT Chat Interface JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatMessages = document.getElementById('chatMessages');
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const typingIndicator = document.getElementById('typingIndicator');
    const currentTimeElement = document.getElementById('currentTime');

    // Update current time
    function updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { 
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        if (currentTimeElement) {
            currentTimeElement.textContent = timeString;
        }
    }

    // Update time every second
    updateTime();
    setInterval(updateTime, 1000);

    // Create message element
    function createMessage(content, isUser = false, time = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

        const avatarDiv = document.createElement('div');
        avatarDiv.className = 'message-avatar';
        
        if (!isUser) {
            const avatarGlow = document.createElement('div');
            avatarGlow.className = 'avatar-glow';
            avatarDiv.appendChild(avatarGlow);
        }
        
        const avatarText = document.createElement('span');
        avatarText.textContent = isUser ? 'YOU' : 'GPT';
        avatarDiv.appendChild(avatarText);

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const messageText = document.createElement('p');
        messageText.textContent = content;

        const messageTime = document.createElement('span');
        messageTime.className = 'message-time';
        messageTime.textContent = time || new Date().toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });

        contentDiv.appendChild(messageText);
        contentDiv.appendChild(messageTime);

        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);

        return messageDiv;
    }

    // Add message to chat
    function addMessage(content, isUser = false, time = null) {
        const messageElement = createMessage(content, isUser, time);
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Add entrance animation
        messageElement.style.opacity = '0';
        messageElement.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            messageElement.style.transition = 'all 0.3s ease-out';
            messageElement.style.opacity = '1';
            messageElement.style.transform = 'translateY(0)';
        }, 10);
    }

    // Show typing indicator
    function showTypingIndicator() {
        typingIndicator.style.display = 'flex';
        typingIndicator.innerHTML = `
            <span>GPT is thinking</span>
            <span></span>
            <span></span>
            <span></span>
        `;
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    // Send message to API
    async function sendMessage(message) {
        try {
            showTypingIndicator();
            
            const response = await fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message
                })
            });

            const data = await response.json();
            
            // Simulate AI thinking time
            setTimeout(() => {
                hideTypingIndicator();
                
                if (data.status === 'success') {
                    addMessage(data.response, false);
                } else {
                    addMessage('Error: ' + (data.response || 'Unknown error occurred'), false);
                }
            }, 1000 + Math.random() * 2000); // Random delay between 1-3 seconds

        } catch (error) {
            hideTypingIndicator();
            addMessage('Connection error. Please check your network and try again.', false);
            console.error('Error:', error);
        }
    }

    // Handle send button click
    function handleSend() {
        const message = chatInput.value.trim();
        if (message) {
            // Add user message
            addMessage(message, true);
            
            // Clear input
            chatInput.value = '';
            
            // Send to API
            sendMessage(message);
            
            // Add button click effect
            sendButton.style.transform = 'scale(0.95)';
            setTimeout(() => {
                sendButton.style.transform = 'scale(1)';
            }, 100);
        }
    }

    // Event listeners
    sendButton.addEventListener('click', handleSend);

    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    chatInput.addEventListener('input', function() {
        // Auto-resize input if needed (future enhancement)
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });

    // Add some futuristic interactive effects
    const interactiveElements = document.querySelectorAll('.send-btn, .message-avatar, .status-dot');
    
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Add glitch effect occasionally
    function addGlitchEffect() {
        const title = document.querySelector('.title-main');
        if (title) {
            title.style.animation = 'none';
            title.style.textShadow = '2px 0 #ff0000, -2px 0 #00ffff';
            
            setTimeout(() => {
                title.style.textShadow = '0 0 30px rgba(0, 255, 255, 0.5)';
                title.style.animation = 'titleGlow 3s ease-in-out infinite alternate';
            }, 150);
        }
    }

    // Random glitch effect every 30-60 seconds
    setInterval(addGlitchEffect, 30000 + Math.random() * 30000);

    // Add particle effects on message send
    function createParticle() {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: fixed;
            width: 4px;
            height: 4px;
            background: #00ffff;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            animation: particleMove 2s ease-out forwards;
        `;
        
        const rect = sendButton.getBoundingClientRect();
        particle.style.left = (rect.left + rect.width / 2) + 'px';
        particle.style.top = (rect.top + rect.height / 2) + 'px';
        
        document.body.appendChild(particle);
        
        setTimeout(() => {
            particle.remove();
        }, 2000);
    }

    // Add particle effect on send
    const originalHandleSend = handleSend;
    handleSend = function() {
        if (chatInput.value.trim()) {
            for (let i = 0; i < 5; i++) {
                setTimeout(() => createParticle(), i * 100);
            }
        }
        originalHandleSend();
    };

    // Add CSS for particle animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes particleMove {
            0% {
                transform: translate(0, 0) scale(1);
                opacity: 1;
            }
            100% {
                transform: translate(${Math.random() * 200 - 100}px, ${Math.random() * 200 - 100}px) scale(0);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Initialize with a welcome effect
    setTimeout(() => {
        const welcomeMessages = [
            "Neural networks initialized successfully.",
            "Quantum processing units online.",
            "Ready for human interaction protocols.",
        ];
        
        welcomeMessages.forEach((msg, index) => {
            setTimeout(() => {
                addMessage(msg, false, "System");
            }, index * 1000);
        });
    }, 1000);

    console.log('🤖 GPT Interface initialized successfully');
    console.log('🔹 All systems operational');
    console.log('🔹 Ready for user interaction');
});