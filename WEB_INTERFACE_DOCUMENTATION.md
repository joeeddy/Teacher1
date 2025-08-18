# Teacher1 Web Interface - Embedded Webview Documentation

## Overview

The Teacher1 web interface provides a modern, responsive web-based chat interface with an embedded webview (iframe) component that allows users to view educational content directly within the chat interface. This feature enables seamless integration of external educational resources while maintaining security and accessibility standards.

## Features

### 🖥️ Web-Based Chat Interface
- Modern, responsive design optimized for desktop, tablet, and mobile devices
- Real-time chat with the Teacher1 learning assistant
- Touch-optimized controls for mobile and tablet usage
- Accessible design with screen reader support and keyboard navigation

### 📚 Embedded Webview Component
- Secure iframe embedding for educational content
- Automatic URL validation and domain whitelisting
- Responsive iframe that adapts to different screen sizes
- Sandboxed iframe with security restrictions
- Easy content management with open/close functionality

### 🔒 Security Features
- Domain whitelist for allowed educational sites
- Content Security Policy (CSP) headers
- URL sanitization and validation
- Iframe sandboxing with restricted permissions
- Input validation and rate limiting

### ♿ Accessibility Features
- ARIA labels and semantic HTML structure
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Reduced motion support for users with vestibular disorders

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Flask web framework
- Teacher1 project dependencies

### Installation
1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. The web interface dependencies are automatically included in the requirements.txt:
   - flask>=2.3.0
   - flask-cors>=4.0.0

### Running the Web Interface
1. Start the web server:
   ```bash
   python web_interface/app.py
   ```

2. Or with custom settings:
   ```bash
   python web_interface/app.py --host 0.0.0.0 --port 8080 --debug
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Basic Chat Interaction
1. Type your message in the chat input field
2. Press Enter or click the Send button
3. The chatbot will respond with educational assistance

### Triggering Embedded Content
The chatbot can display educational content in the embedded iframe when you use certain keywords or phrases:

#### Intent Keywords
- "show me [topic]"
- "open [topic] content" 
- "display [topic] information"
- "show educational content about [topic]"

#### Supported Topics
- **Science**: "show me science content"
- **Math/Mathematics**: "open math resources"
- **History**: "display history information"
- **Reading**: "show reading games"
- **Animals**: "show me animal information"
- **Space**: "display space content"
- **Geography**: "show geography resources"

#### Direct URL Support
You can also request specific URLs from allowed domains:
```
"Please show https://simple.wikipedia.org/wiki/Science"
```

### Managing Embedded Content
- **Open Content**: Use intent keywords or request specific URLs
- **Close Content**: Click the "✕" button in the content header
- **Responsive Viewing**: Content automatically adapts to screen size

## Configuration

### Allowed Domains
The system includes a whitelist of safe educational domains in `web_interface/config.py`:

```python
ALLOWED_DOMAINS = [
    'en.wikipedia.org',
    'simple.wikipedia.org',
    'www.khanacademy.org',
    'education.nationalgeographic.org',
    'www.mathplayground.com',
    'www.ixl.com',
    'www.abcya.com',
    'www.funbrain.com',
    'pbskids.org',
    'www.starfall.com',
    # ... more educational domains
]
```

### Adding New Domains
To add new educational domains:

1. Edit `web_interface/config.py`
2. Add the domain to the `ALLOWED_DOMAINS` list
3. Restart the web server

**Important**: Only add trusted educational domains to maintain security.

### Security Configuration
The iframe is configured with security restrictions:

```python
IFRAME_CONFIG = {
    'sandbox': 'allow-scripts allow-same-origin allow-forms',
    'loading': 'lazy',
    'referrerpolicy': 'strict-origin-when-cross-origin'
}
```

### Content Security Policy
The application uses a strict CSP to prevent XSS attacks:

```python
CSP_POLICY = {
    'default-src': "'self'",
    'script-src': "'self' 'unsafe-inline'",
    'style-src': "'self' 'unsafe-inline'",
    'img-src': "'self' data: https:",
    'frame-src': "https://[allowed-domains]",
    'connect-src': "'self' ws: wss:"
}
```

## API Reference

### Web Interface Endpoints

#### GET /
- **Description**: Serves the main chat interface
- **Response**: HTML page with chat interface and iframe component

#### POST /chat
- **Description**: Processes chat messages and returns responses
- **Content-Type**: application/json
- **Request Body**:
  ```json
  {
    "message": "User message text"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Bot response text",
    "timestamp": "2024-01-01T12:00:00.000Z",
    "embed_url": "https://example.com/content",
    "embed_title": "Content Title"
  }
  ```

#### GET /health
- **Description**: Health check endpoint
- **Response**:
  ```json
  {
    "status": "healthy",
    "chatbot_available": true,
    "version": "1.0.0"
  }
  ```

### JavaScript API
The web interface provides a JavaScript API for programmatic control:

```javascript
// Access the chat interface
const chat = window.teacher1Chat;

// Programmatically display content
chat.showContent('https://simple.wikipedia.org/wiki/Science', 'Science Content');

// Get message history
const history = chat.getHistory();

// Clear chat
chat.clearChat();
```

## Responsive Design

### Breakpoints
- **Desktop**: 1200px and above (two-column layout)
- **Tablet**: 768px to 1199px (single-column layout)
- **Mobile**: 767px and below (optimized touch interface)

### Touch Optimization
- Minimum touch target size of 44px for buttons
- Touch-friendly spacing and padding
- Optimized input field sizing for mobile keyboards

## Accessibility Features

### Screen Reader Support
- Semantic HTML structure with proper headings
- ARIA labels for interactive elements
- Live regions for dynamic content updates
- Screen reader announcements for important actions

### Keyboard Navigation
- Tab navigation through all interactive elements
- Enter key support for form submission
- Escape key support for closing content
- Focus indicators for all interactive elements

### Visual Accessibility
- High contrast color scheme
- Scalable fonts and responsive design
- Support for prefers-contrast and prefers-reduced-motion
- Color-blind friendly color palette

## Security Considerations

### Domain Whitelisting
- Only predetermined educational domains are allowed
- URLs are validated against the whitelist before embedding
- Automatic HTTPS enforcement for all external content

### Input Validation
- Message length limits (500 characters max)
- URL format validation
- HTML sanitization for chat messages

### Iframe Sandboxing
- Restricted sandbox permissions
- Prevent navigation to unsafe domains
- Lazy loading for performance and security

### Headers and Policies
- Content Security Policy to prevent XSS
- X-Frame-Options to prevent clickjacking
- Referrer policy for privacy protection

## Troubleshooting

### Common Issues

#### Content Not Loading
- **Cause**: Domain not in whitelist
- **Solution**: Add domain to `ALLOWED_DOMAINS` in config.py

#### Iframe Blocked
- **Cause**: Browser security policies
- **Solution**: Ensure HTTPS and proper CSP configuration

#### Mobile Touch Issues
- **Cause**: Touch targets too small
- **Solution**: Verify 44px minimum touch target size

#### Accessibility Issues
- **Cause**: Missing ARIA labels or semantic structure
- **Solution**: Check HTML structure and ARIA attributes

### Debug Mode
Enable debug mode for detailed error information:
```bash
python web_interface/app.py --debug
```

### Logs
Check the console for detailed error messages and security warnings.

## Development

### Testing
Run the test suite to verify functionality:
```bash
python test_web_interface.py
```

### Code Structure
```
web_interface/
├── app.py              # Main Flask application
├── config.py           # Configuration and security settings
├── templates/
│   └── index.html      # Main HTML template
└── static/
    ├── css/
    │   └── style.css   # Responsive styles
    └── js/
        └── chat.js     # Chat interface logic
```

### Contributing
When adding new features:
1. Update security configurations as needed
2. Add appropriate tests
3. Update documentation
4. Ensure accessibility compliance
5. Test on multiple devices and browsers

## Browser Compatibility

### Supported Browsers
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Mobile Browsers
- Chrome Mobile 80+
- Safari Mobile 13+
- Firefox Mobile 75+

## Performance Considerations

### Optimization Features
- Lazy loading for iframes
- CSS and JS minification in production
- Responsive images and content
- Efficient event handling

### Monitoring
- Health check endpoint for status monitoring
- Error logging for debugging
- Performance metrics collection

## Future Enhancements

### Planned Features
- [ ] Multi-language support
- [ ] Advanced content filtering
- [ ] Offline content caching
- [ ] Voice interaction integration
- [ ] Enhanced analytics and reporting
- [ ] Custom domain management interface

### Extensibility
The web interface is designed to be extensible:
- Add new educational content sources
- Integrate additional AI systems
- Customize themes and branding
- Add new interaction modalities

## Support

For technical support or questions:
1. Check this documentation first
2. Review the troubleshooting section
3. Check the project's GitHub issues
4. Create a new issue if needed

## License

This web interface is part of the Teacher1 project and follows the same licensing terms.