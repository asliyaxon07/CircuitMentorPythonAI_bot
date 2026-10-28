# CircuitAIMentor_bot

**Your AI-powered electronics and hardware engineering tutor.**

CircuitMentor is a Telegram bot that helps beginners learn electronics, build circuits, explore Arduino, and understand hardware engineering with the help of Google Gemini AI.

The goal of this project is to make electronics easier to understand through simple explanations, practical examples, quizzes, and troubleshooting guidance.

## Features

- **Learn Electronics:** Understand voltage, current, resistance, and Ohm's law.
- **Build a Circuit:** Get step-by-step instructions for beginner-friendly circuits.
- **Explain a Component:** Learn about resistors, LEDs, capacitors, transistors, and other components.
- **Troubleshoot:** Get help identifying possible circuit problems.
- **Quiz Me:** Test your electronics knowledge with interactive questions.
- **Learning Roadmap:** Explore a structured path from basic electricity to robotics.
- **AI-Powered Tutor:** Ask questions and receive explanations using Google Gemini.

## Technologies Used

- Python
- Telegram Bot API
- python-telegram-bot
- Google Gemini API
- google-genai
- python-dotenv

## Project Structure

```text
CircuitMentor/
├── bot.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

**Note:** The `.env` file is stored locally and must never be uploaded to GitHub because it contains private API keys.

## Getting Started

### 1. Requirements

Before running the project, install:

- Python
- A Telegram account
- A Telegram bot token from [BotFather](https://t.me/BotFather)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 2. Install the required libraries

Open a terminal in the project folder and run:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure API keys

Create a file named `.env` in the same folder as `bot.py`.

Add the following lines and replace the example values with your own API keys:

```text
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

Never share your API keys or upload the `.env` file to GitHub.

### 4. Start the bot

In the terminal, run:

```bash
python bot.py
```

If the setup is correct, the terminal will display:

```text
CircuitMentor is running!
```

Open your bot in Telegram and send `/start`.

## Available Commands

| Command | Description |
|---|---|
| `/start` | Open the main menu |
| `/help` | Display available commands |
| `/topics` | View the electronics learning roadmap |
| `/reset` | Reset the conversation history |

You can also select options from the Telegram menu or type your own electronics questions.

## Safety

CircuitMentor is designed to encourage safe, low-voltage electronics experimentation.

Always check component ratings, polarity, and wiring before powering a circuit. Beginners should avoid experimenting with mains electricity.

## Future Improvements

- Faster AI responses
- More Arduino tutorials
- Additional electronics quizzes
- Personalised learning paths
- Practical hardware engineering projects

## Author

Created as a personal learning project to explore Python, artificial intelligence, electronics, and hardware engineering.
