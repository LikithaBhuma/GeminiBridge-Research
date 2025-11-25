# Multilingual Language Understanding Interface

A modern web interface for multilingual intent detection and slot filling using Google Gemini AI. This project provides a beautiful, responsive web application that can analyze text in multiple languages to detect user intents and extract slot information.

## 🌟 Features

- **Multilingual Support**: English, Spanish, Persian, Thai, Bengali, and Telugu
- **Intent Detection**: Identify user intents from natural language utterances
- **Slot Filling**: Extract structured information from text
- **Modern UI**: Beautiful, responsive web interface
- **Real-time Analysis**: Instant results using Gemini AI
- **Translation Support**: Automatic translation of results to English
- **Multiple Domains**: Support for reminder and alarm domains

## 🚀 Quick Start

### Prerequisites

- Python 3.7
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd language-understanding-gemini
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   The application is already configured with a Gemini API key. If you need to use your own:
   
   - Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Replace the API key in `app.py` line 12:
     ```python
     genai.configure(api_key="YOUR_API_KEY_HERE")
     ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   
   Navigate to: http://localhost:5000

## 📖 Usage

### Web Interface

1. **Enter Text**: Type or paste your text in the input field
2. **Select Language**: Choose the language of your text
3. **Choose Domain**: Select between "Reminder" or "Alarm" domain
4. **Analyze**: Click "Analyze Text" to get results
5. **View Results**: See both intent detection and slot filling results with English translations

### Example Inputs

**English:**
- "Remind me to call mom at 5 PM"
- "Set an alarm for 7 AM tomorrow"

**Spanish:**
- "Recuérdame llamar a mamá a las 5 PM"
- "Configura una alarma para mañana a las 7 AM"

**Persian:**
- "یادآوری کن که به مامان زنگ بزنم ساعت ۵ عصر"
- "ساعت را برای ساعت ۷ صبح فردا تنظیم کن"

**Thai:**
- "เตือนฉันให้โทรหาคุณแม่ตอน 5 โมงเย็น"
- "ตั้งนาฬิกาปลุกสำหรับพรุ่งนี้ตอน 7 โมงเช้า"

**Bengali:**
- "আমাকে বিকেল ৫টায় মাকে ফোন করার কথা মনে করিয়ে দাও"
- "আগামীকাল সকাল ৭টায় একটি অ্যালার্ম সেট করো"

**Telugu:**
- "మధ్యాహ్నం 5 గంటలకు అమ్మకు ఫోన్ చేయమని నాకు గుర్తు చేయండి"
- "రేపు ఉదయం 7 గంటలకు అలారం సెట్ చేయండి"

## 🏗️ Architecture

### Core Components

- **Flask Web Server**: Handles HTTP requests and serves the web interface
- **Gemini AI Integration**: Uses Google's Gemini model for natural language processing
- **Few-shot Learning**: Implements few-shot prompting for better accuracy
- **Multilingual Support**: Pre-configured examples for each supported language

### File Structure

```
language-understanding-gemini/
├── app.py                 # Main Flask application
├── evaluate_model.py      # Model Evaluation
├── test_data.py           # Test data
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface template
└── data/                 # Language datasets
    ├── ES/               # Spanish data
    ├── TH/               # Thai data
    ├── FA/               # Persian data
    ├── BN/               # Bengali data
    └── TE/               # Telugu data
```

### API Endpoints

- `GET /` - Main web interface
- `POST /analyze` - Analyze text for intent and slots
- `GET /examples/<language>` - Get example utterances for a language
- `GET/evaluate-metrics-ui'` - Get the evaluation metrics
- `GET /health` - Health check endpoint

## 🔧 Configuration

### Environment Variables

You can configure the application using environment variables:

```bash
export GEMINI_API_KEY="your_api_key_here"
export FLASK_ENV="development"
export FLASK_DEBUG=1
```

### Customization

#### Adding New Languages

1. Add language configuration to `LANGUAGES` in `app.py`
2. Add example datasets to `example_datasets`
3. Update the web interface template if needed

#### Adding New Domains

1. Add domain examples to each language in `example_datasets`
2. Update the domain selector in the HTML template
3. Test with domain-specific examples

## 🧪 Testing

### Manual Testing

1. Start the application: `python app.py`
2. Open http://localhost:5000
3. Test with various languages and domains
4. Check the health endpoint: http://localhost:5000/health
5. For evaluation use: `python evaluate_model.py --language language_name`

### API Testing

Test the analysis endpoint directly:

```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "utterance": "Remind me to call mom at 5 PM",
    "language": "english",
    "domain": "reminder"
  }'
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Gemini API key is valid and has sufficient quota
2. **Import Errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`
3. **Port Already in Use**: Change the port in `app.py` or kill the process using port 5000
4. **Unicode Issues**: Ensure your terminal supports UTF-8 encoding

### Debug Mode

Run the application in debug mode for detailed error messages:

```bash
export FLASK_DEBUG=1
python app.py
```

## 📊 Performance

- **Response Time**: Typically 2-5 seconds per analysis
- **Accuracy**: High accuracy with few-shot learning approach
- **Scalability**: Can handle multiple concurrent requests
- **Memory Usage**: Low memory footprint (~100MB)

## 🔒 Security

- API keys are embedded in the code (consider using environment variables for production)
- No user data is stored or logged
- HTTPS recommended for production deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for providing the language model
- Flask framework for the web application
- Font Awesome for icons
- The open-source community for various libraries and tools

## 📞 Support

For questions or issues:

1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub
4. Contact the development team

---

## Licnese
Done by students for research project