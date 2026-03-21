# 📊 Variance Calculator with AI Explanations

A modern Python web application for calculating population variance of test scores with comprehensive input validation, automated testing, and AI-powered explanations using OpenAI.

## ✨ Features

- **🎯 Precise Variance Calculation**: Computes population variance using the formula `σ² = Σ((xᵢ - μ)²) / N`
- **🛡️ Input Validation**: Ensures scores are integers between 0-100, with configurable limits
- **🔄 Interactive CLI**: User-friendly command-line interface with error handling and retries
- **🌐 Modern Web UI**: Responsive HTML/CSS/JavaScript frontend with real-time calculations
- **🤖 AI-Powered Explanations**: OpenAI GPT integration for contextual variance interpretations
- **🧪 Comprehensive Testing**: 16 unit tests covering edge cases, error conditions, and integration scenarios
- **📈 Audit Trail**: Automatic test result logging with timestamped reports
- **📝 Production Logging**: Structured logging with file rotation for observability and debugging
- **🏗️ Modular Architecture**: Clean separation of concerns with reusable functions and REST API

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (for AI explanations)

### Installation
```bash
git clone https://github.com/rhoolan/nww_playbox.git
cd nww_playbox
python -m pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Usage

#### Web Application (Recommended)
Start the Flask server:
```bash
python app.py
```
Open `http://localhost:8000` in your browser for the interactive web interface.

#### Command Line Interface
Run the traditional CLI calculator:
```bash
python variance.py
```

Example interaction:
```
Enter scores separated by commas (e.g. 90, 85, 88): 85,87,88
Score variance: 2.0000
```

#### API Endpoints
- `POST /api/variance` with JSON body `{ "scores": [85, 87, 88] }`
  - Returns `{ "variance": number, "input": [...] }`
- `POST /api/variance-explanation` with JSON body `{ "variance": 2.0, "scores": [85, 87, 88] }`
  - Returns `{ "explanation": "AI-generated explanation..." }`
`http://localhost:8000`

API endpoint:
- `POST /api/variance` with JSON body `{ "scores": [85, 87, 88] }`
- Returns `{ "variance": number, "input": [...] }`

## 🏗️ Architecture

### Core Functions

#### `_find_variance(scores: list[int]) -> float`
Calculates population variance with type checking and validation.
- **Input**: List of integers (0-100 range enforced elsewhere)
- **Output**: Population variance as float
- **Raises**: `TypeError` for invalid types, `ValueError` for empty lists

#### `_get_scores_from_user() -> list[int] | None`
Handles user input with validation and error recovery.
- **Features**: Parses comma-separated input, validates ranges, limits count
- **Returns**: Valid score list or `None` on invalid input

#### `find_variance_from_user_input() -> float`
Orchestrates the complete user interaction flow.

### Flask API Endpoints

#### `POST /api/variance`
Computes variance for provided scores.
- **Input**: `{"scores": [int, int, ...]}` (max 10 scores, 0-100 range)
- **Output**: `{"variance": float, "input": [int, ...]}`
- **Errors**: 400 for invalid input, 500 for server errors

#### `POST /api/variance-explanation`
Generates AI explanation of variance using OpenAI GPT.
- **Input**: `{"variance": float, "scores": [int, int, ...]}`
- **Output**: `{"explanation": string}`
- **Requirements**: OpenAI API key configured in `.env`

### Configuration Constants
- `MAX_SCORE = 100`: Maximum allowed score
- `MAX_SCORE_COUNT = 10`: Maximum number of scores per calculation

### Validation Rules
- Scores must be integers (`int`) and not boolean
- Score range: 0 through 100 inclusive
- Maximum inputs: 10 scores
- API returns 400 for invalid score count/range/type

## 🧪 Testing

### Run Tests
```bash
python -m unittest test_variance.py -v
```

### Automated Test Reporting
```bash
python update_test_readme.py
```
Generates timestamped reports in `test_results/` directory.

### Test Coverage
- ✅ Normal variance calculations
- ✅ Edge cases (single score, identical scores)
- ✅ Error handling (empty lists, wrong types, invalid ranges)
- ✅ User input validation and retry logic
- ✅ Integration testing

## 🤖 AI Features

### OpenAI Integration
The application integrates with OpenAI's GPT models to provide contextual explanations of variance calculations.

### Configuration
- Set `OPENAI_API_KEY` in your `.env` file
- Uses `gpt-3.5-turbo` model for explanations
- Configurable temperature and max tokens for response control

### Explanation Features
- Generates 2-3 sentence explanations of variance meaning
- References actual input scores in explanations
- Indicates whether variance represents high or low spread
- Explains practical implications for data consistency

### Example AI Explanation
*For scores [85, 87, 88] with variance 2.0000:*
"The scores 85, 87, and 88 show low variance of 2.0000, indicating that the values are closely clustered around their mean of 86.67. This suggests consistent performance with minimal spread between the individual scores."

## 📝 Logging

### Log Configuration
The application uses Python's built-in logging module with structured output and file rotation:
- **Log Level**: INFO and above (INFO, WARNING, ERROR, CRITICAL)
- **File Location**: `logs/variance_calculator.log`
- **Rotation**: Automatic rotation at 10MB with 5 backup files
- **Format**: Timestamp, log level, module, function, and message

### Log Levels Used
- **INFO**: Successful operations and key application events
- **WARNING**: Non-critical issues that don't stop execution
- **ERROR**: Errors that prevent normal operation
- **CRITICAL**: Severe errors requiring immediate attention

### Viewing Logs
```bash
# View recent log entries
tail -f logs/variance_calculator.log

# View all log files (including rotated ones)
ls -la logs/

# Search for specific log entries
grep "ERROR" logs/variance_calculator.log
```

### Log Examples
```
2024-01-15 10:30:15,123 - INFO - variance - _find_variance - Starting variance calculation for 3 scores
2024-01-15 10:30:15,124 - INFO - variance - _find_variance - Variance calculated successfully: 2.0000
2024-01-15 10:30:16,001 - WARNING - variance - _get_scores_from_user - Invalid input format, retrying...
2024-01-15 10:30:16,002 - ERROR - variance - find_variance_from_user_input - Failed to get valid scores after retries
```

## 📊 Example Calculations

| Scores | Mean | Variance | Interpretation |
|--------|------|----------|----------------|
| [85, 87, 88] | 86.67 | 2.00 | Low variance - consistent performance |
| [50, 70, 85, 95, 100] | 80.00 | 300.00 | High variance - wide performance range |
| [90, 90, 90] | 90.00 | 0.00 | No variance - identical scores |

## 🎯 Use Cases

### Education
- **Assessment Analysis**: Evaluate test consistency and fairness
- **Student Performance**: Identify outliers and learning gaps
- **Grade Distribution**: Understand score spread in classrooms

### Quality Control
- **Process Monitoring**: Measure consistency in manufacturing
- **Performance Metrics**: Analyze system reliability
- **Data Validation**: Ensure measurement accuracy

### Research
- **Statistical Analysis**: Foundation for more complex statistical measures
- **Data Quality**: Detect anomalies in datasets
- **Comparative Studies**: Benchmark performance across groups

## 📁 Project Structure

```
nww_playbox/
├── app.py                    # Flask web application with AI explanations
├── variance.py               # Core variance calculation logic
├── test_variance.py          # Unit test suite
├── update_test_readme.py     # Test automation script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API keys)
├── logs/                     # Application log files
│   └── variance_calculator.log  # Main log file (rotating)
├── static/                   # Web UI assets
│   ├── index.html            # Main web interface
│   └── styles.css            # Responsive styling
├── test_results/             # Audit trail directory
│   └── test_results_*.md     # Timestamped test reports
├── README.md                 # This file
└── __pycache__/             # Python bytecode
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install dependencies (`pip install -r requirements.txt`)
4. Set up environment variables (copy `.env.example` if available)
5. Run tests (`python update_test_readme.py`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

## 🔗 Links

- **Repository**: [GitHub](https://github.com/rhoolan/nww_playbox)
- **Issues**: [Report Bugs](https://github.com/rhoolan/nww_playbox/issues)
- **Discussions**: [Q&A](https://github.com/rhoolan/nww_playbox/discussions)

---

*Built with ❤️ for educational and analytical purposes*