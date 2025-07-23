# Claude Chat Website

A modern Django web application featuring a futuristic chat interface powered by Anthropic's Claude AI.

## Features

- 🤖 **Claude AI Integration**: Chat with Anthropic's Claude using the latest API
- 🎨 **Futuristic UI**: Modern, responsive design with glowing effects and animations
- ⚡ **Real-time Chat**: Interactive chat interface with typing indicators
- 🎪 **Visual Effects**: Particle animations, glitch effects, and smooth transitions
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## Tech Stack

- **Backend**: Django 4.2.23
- **AI**: Anthropic Claude API (claude-3-5-sonnet-20241022)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite (default)
- **Python**: 3.9+

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Anthropic API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd testWebsite
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_claude_api_key_here
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   Navigate to `http://127.0.0.1:8000/`

## Project Structure

```
testWebsite/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (not in git)
├── .gitignore           # Git ignore rules
├── CLAUDE.md            # Claude Code guidance
├── README.md            # This file
├── testWebsite/         # Main project configuration
│   ├── settings.py      # Django settings
│   ├── urls.py         # Main URL routing
│   ├── wsgi.py         # WSGI configuration
│   └── asgi.py         # ASGI configuration
└── main/               # Main Django app
    ├── views.py        # View functions (Claude API integration)
    ├── urls.py         # App URL patterns
    ├── models.py       # Database models
    ├── static/         # Static files (CSS, JS)
    │   └── main/
    │       ├── css/
    │       │   └── style.css    # Futuristic styling
    │       └── js/
    │           └── script.js    # Interactive chat functionality
    └── templates/      # HTML templates
        └── main/
            ├── homepage.html    # Main chat interface
            ├── about.html       # About page
            └── contact.html     # Contact page
```

## API Configuration

This application uses Anthropic's Claude API. You'll need to:

1. Sign up for an Anthropic account at [console.anthropic.com](https://console.anthropic.com/)
2. Generate an API key
3. Add the key to your `.env` file as `ANTHROPIC_API_KEY`

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (Production)
```bash
python manage.py collectstatic
```

## Features in Detail

### Chat Interface
- Real-time messaging with Claude AI
- Typing indicators and message animations
- Particle effects on message send
- Responsive design for all screen sizes

### AI Integration
- Uses Claude 3.5 Sonnet model
- Handles API errors gracefully
- Configurable response parameters
- Fallback responses for service interruptions

### Visual Effects
- Glowing text animations
- Particle system
- Smooth message transitions
- Futuristic color scheme with cyan accents

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the [CLAUDE.md](CLAUDE.md) file for development guidance
2. Review the Django and Anthropic API documentation
3. Open an issue in the GitHub repository

## Acknowledgments

- Built with Django web framework
- Powered by Anthropic's Claude AI
- Inspired by futuristic UI design trends
- Uses modern web technologies for optimal performance

---

**Note**: Remember to keep your API keys secure and never commit them to version control.