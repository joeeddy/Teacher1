/**
 * Teacher1 Personalized Chat Interface JavaScript
 * Handles chat interactions, student sessions, and progress tracking
 */

class Teacher1Chat {
    constructor() {
        this.chatMessages = document.getElementById('chat-messages');
        this.messageInput = document.getElementById('message-input');
        this.chatForm = document.getElementById('chat-form');
        this.contentArea = document.getElementById('content-area');
        this.closeContentBtn = document.getElementById('close-content');
        this.loadingIndicator = document.getElementById('loading-indicator');
        this.errorMessage = document.getElementById('error-message');
        this.announcements = document.getElementById('announcements');
        
        // Student session elements
        this.studentLogin = document.getElementById('student-login');
        this.progressSection = document.getElementById('progress-section');
        this.studentNameInput = document.getElementById('student-name-input');
        this.startLearningBtn = document.getElementById('start-learning-btn');
        this.endSessionBtn = document.getElementById('end-session-btn');
        this.currentStudentName = document.getElementById('current-student-name');
        
        // Progress bars
        this.progressBars = {
            math: document.getElementById('math-progress'),
            reading: document.getElementById('reading-progress'),
            spelling: document.getElementById('spelling-progress'),
            numbers: document.getElementById('numbers-progress')
        };
        
        this.isLoading = false;
        this.messageHistory = [];
        this.sessionId = this.generateSessionId();
        this.studentName = null;
        this.sessionActive = false;
        
        this.init();
    }
    
    generateSessionId() {
        return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }
    
    init() {
        // Bind event listeners
        this.chatForm.addEventListener('submit', this.handleMessageSubmit.bind(this));
        if (this.closeContentBtn) {
            this.closeContentBtn.addEventListener('click', this.closeEmbeddedContent.bind(this));
        }
        if (this.errorMessage) {
            this.errorMessage.querySelector('.error-close').addEventListener('click', this.hideError.bind(this));
        }
        
        // Student session event listeners
        this.startLearningBtn.addEventListener('click', this.startLearningSession.bind(this));
        this.endSessionBtn.addEventListener('click', this.endLearningSession.bind(this));
        this.studentNameInput.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                this.startLearningSession();
            }
        });
        
        // Handle keyboard navigation
        this.messageInput.addEventListener('keydown', this.handleKeyDown.bind(this));
        
        // Focus on student name input initially
        this.studentNameInput.focus();
        
        // Add accessibility announcements
        this.announceToScreenReader('Teacher1 learning interface loaded. Please enter your name to start learning.');
        
        // Start progress polling when session is active
        this.startProgressPolling();
    }
    
    handleKeyDown(event) {
        // Allow Enter to submit (unless Shift+Enter for newlines in future)
        if (event.key === 'Enter' && !event.shiftKey && this.sessionActive) {
            event.preventDefault();
            this.chatForm.dispatchEvent(new Event('submit'));
        }
    }
    
    async startLearningSession() {
        const name = this.studentNameInput.value.trim();
        if (!name) {
            this.showError('Please enter your name to start learning!');
            this.studentNameInput.focus();
            return;
        }
        
        try {
            this.setLoading(true);
            
            const response = await fetch('/start_session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    student_name: name,
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Update UI
            this.studentName = name;
            this.sessionActive = true;
            this.currentStudentName.textContent = name;
            
            // Hide login form and show progress section
            this.studentLogin.style.display = 'none';
            this.progressSection.style.display = 'block';
            
            // Add welcome message
            this.addMessage(data.message, 'bot');
            
            // Focus on chat input
            this.messageInput.focus();
            
            this.announceToScreenReader(`Welcome ${name}! Your learning session has started.`);
            
        } catch (error) {
            this.showError(`Failed to start session: ${error.message}`);
        } finally {
            this.setLoading(false);
        }
    }
    
    async endLearningSession() {
        if (!this.sessionActive) return;
        
        try {
            this.setLoading(true);
            
            const response = await fetch('/end_session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: this.sessionId
                })
            });
            
            const data = await response.json();
            
            // Add goodbye message
            if (data.message) {
                this.addMessage(data.message, 'bot');
            }
            
            // Reset UI
            this.sessionActive = false;
            this.studentName = null;
            this.sessionId = this.generateSessionId();
            
            // Show login form and hide progress section
            this.studentLogin.style.display = 'block';
            this.progressSection.style.display = 'none';
            
            // Clear student name input
            this.studentNameInput.value = '';
            this.studentNameInput.focus();
            
            this.announceToScreenReader('Learning session ended. Enter your name to start a new session.');
            
        } catch (error) {
            this.showError(`Failed to end session: ${error.message}`);
        } finally {
            this.setLoading(false);
        }
    }
    
    async updateProgress() {
        if (!this.sessionActive) return;
        
        try {
            const response = await fetch(`/progress/${this.sessionId}`);
            
            if (response.ok) {
                const progress = await response.json();
                
                // Update progress bars
                if (progress.progress) {
                    for (const [subject, data] of Object.entries(progress.progress)) {
                        if (this.progressBars[subject] && data.attempts > 0) {
                            const successRate = (data.successes / data.attempts) * 100;
                            this.progressBars[subject].style.width = `${Math.min(successRate, 100)}%`;
                            
                            // Add color coding based on performance
                            if (successRate >= 80) {
                                this.progressBars[subject].className = 'progress-fill excellent';
                            } else if (successRate >= 60) {
                                this.progressBars[subject].className = 'progress-fill good';
                            } else {
                                this.progressBars[subject].className = 'progress-fill needs-practice';
                            }
                        }
                    }
                }
            }
        } catch (error) {
            console.warn('Failed to update progress:', error);
        }
    }
    
    startProgressPolling() {
        // Update progress every 10 seconds when session is active
        setInterval(() => {
            if (this.sessionActive) {
                this.updateProgress();
            }
        }, 10000);
    }
    
    async handleMessageSubmit(event) {
        event.preventDefault();
        
        if (this.isLoading) {
            return;
        }
        
        const message = this.messageInput.value.trim();
        if (!message) {
            return;
        }
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        
        // Show loading state
        this.setLoading(true);
        
        try {
            // Send message to backend
            const response = await this.sendMessage(message);
            
            if (response.error) {
                throw new Error(response.error);
            }
            
            // Add bot response
            this.addMessage(response.message, 'bot');
            
            // Handle embedded content if provided
            if (response.embed_url) {
                this.displayEmbeddedContent(response.embed_url, response.embed_title);
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.showError('Sorry, I encountered an error. Please try again.');
            this.addMessage('Sorry, I encountered an error processing your request. Please try again.', 'bot');
        } finally {
            this.setLoading(false);
        }
    }
    
    async sendMessage(message) {
        const payload = { 
            message: message,
            session_id: this.sessionId
        };
        
        // Add student name if session is active
        if (this.sessionActive && this.studentName) {
            payload.student_name = this.studentName;
        }
        
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.setAttribute('aria-hidden', 'true');
        avatar.textContent = sender === 'bot' ? '🎓' : '👶';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Simple HTML parsing for basic formatting
        if (content.includes('<') && content.includes('>')) {
            messageContent.innerHTML = this.sanitizeHTML(content);
        } else {
            const p = document.createElement('p');
            p.textContent = content;
            messageContent.appendChild(p);
        }
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Store in history
        this.messageHistory.push({ content, sender, timestamp: new Date() });
        
        // Announce to screen readers
        const announcement = `${sender === 'bot' ? 'Bot' : 'You'}: ${content}`;
        this.announceToScreenReader(announcement);
    }
    
    sanitizeHTML(html) {
        // Very basic HTML sanitization - only allow safe tags
        const allowedTags = ['p', 'br', 'strong', 'em', 'b', 'i'];
        let sanitized = html;
        
        // Remove any script tags and event handlers
        sanitized = sanitized.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
        sanitized = sanitized.replace(/on\w+\s*=\s*"[^"]*"/gi, '');
        sanitized = sanitized.replace(/on\w+\s*=\s*'[^']*'/gi, '');
        
        return sanitized;
    }
    
    displayEmbeddedContent(url, title = 'Educational Content') {
        // Clear current content
        this.contentArea.innerHTML = '';
        
        // Create iframe
        const iframe = document.createElement('iframe');
        iframe.src = url;
        iframe.className = 'embedded-iframe';
        iframe.title = title;
        iframe.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-forms');
        iframe.setAttribute('loading', 'lazy');
        iframe.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
        
        // Add load event listener
        iframe.addEventListener('load', () => {
            this.announceToScreenReader(`Educational content loaded: ${title}`);
        });
        
        iframe.addEventListener('error', () => {
            this.showError('Unable to load the educational content.');
            this.closeEmbeddedContent();
        });
        
        this.contentArea.appendChild(iframe);
        this.closeContentBtn.style.display = 'block';
        
        // Update content title
        const contentTitle = document.querySelector('.content-title');
        contentTitle.textContent = title;
    }
    
    closeEmbeddedContent() {
        this.contentArea.innerHTML = `
            <div class="content-placeholder">
                <div class="placeholder-icon" aria-hidden="true">📚</div>
                <p>Educational content will appear here when requested</p>
                <p class="placeholder-subtext">Ask me to show you educational resources!</p>
            </div>
        `;
        
        this.closeContentBtn.style.display = 'none';
        
        // Reset content title
        const contentTitle = document.querySelector('.content-title');
        contentTitle.textContent = 'Educational Content';
        
        this.announceToScreenReader('Educational content closed');
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        const sendButton = this.chatForm.querySelector('.send-button');
        
        if (loading) {
            this.loadingIndicator.style.display = 'block';
            sendButton.disabled = true;
            sendButton.textContent = 'Sending...';
        } else {
            this.loadingIndicator.style.display = 'none';
            sendButton.disabled = false;
            sendButton.innerHTML = '<span aria-hidden="true">➤</span><span class="sr-only">Send</span>';
        }
    }
    
    showError(message) {
        const errorText = this.errorMessage.querySelector('.error-text');
        errorText.textContent = message;
        this.errorMessage.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.hideError();
        }, 5000);
        
        this.announceToScreenReader(`Error: ${message}`);
    }
    
    hideError() {
        this.errorMessage.style.display = 'none';
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    announceToScreenReader(message) {
        this.announcements.textContent = message;
        // Clear after announcement is made
        setTimeout(() => {
            this.announcements.textContent = '';
        }, 1000);
    }
    
    // Public method to programmatically display content
    showContent(url, title) {
        this.displayEmbeddedContent(url, title);
    }
    
    // Public method to get message history
    getHistory() {
        return [...this.messageHistory];
    }
    
    // Public method to clear chat
    clearChat() {
        this.chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar" aria-hidden="true">🤖</div>
                <div class="message-content">
                    <p>Hello! I'm your learning assistant. How can I help you learn today?</p>
                    <p>Try asking me to "show educational content about science" or "open learning resources"!</p>
                </div>
            </div>
        `;
        this.messageHistory = [];
        this.announceToScreenReader('Chat cleared');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.teacher1Chat = new Teacher1Chat();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Teacher1Chat;
}