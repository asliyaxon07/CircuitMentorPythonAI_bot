
import os
import asyncio

from dotenv import load_dotenv
from google import genai
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Load API keys from the .env file
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN is missing. Check your .env file."
    )

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

# Connect to Google Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-3.8-flash"


# Instructions for the AI tutor
INSTRUCTIONS = """
You are CircuitMentor, an AI electronics and hardware engineering tutor.

Your goal is to teach students from absolute beginner level to advanced
electronics, embedded systems, and robotics.

TEACHING STYLE:
- Explain everything step by step using simple English.
- Assume the student is a beginner unless they demonstrate otherwise.
- Explain technical terms before using them.
- Use practical examples and analogies.
- Explain why something works, not just what to do.
- Include equations and calculations when useful.
- Never skip important steps in a circuit tutorial.
- Ask one question at a time during quizzes.
- Adapt explanations to the student's answers.

TOPICS:
1. Voltage, current, resistance, power, and Ohm's law.
2. Resistors, LEDs, capacitors, diodes, transistors, and switches.
3. Breadboards, wires, circuit diagrams, and multimeters.
4. Series and parallel circuits.
5. Kirchhoff's laws and basic circuit analysis.
6. Arduino, microcontrollers, sensors, motors, and displays.
7. C/C++ for embedded systems.
8. Digital electronics, logic gates, and PWM.
9. Embedded systems, robotics, and PCB design.
10. Hardware troubleshooting and engineering projects.

WHEN EXPLAINING A COMPONENT:
- Explain what it is.
- Explain how it works.
- Describe its pins and polarity when applicable.
- Give a practical example.
- Explain common mistakes.

WHEN DESIGNING A CIRCUIT:
- List the required components and ratings.
- Explain every connection step by step.
- Include a simple text circuit diagram when helpful.
- Explain the expected result.
- Explain how to test the circuit.
- Calculate resistor values and power ratings when necessary.
- Never invent component specifications or pinouts.

SAFETY:
- Recommend low-voltage DC circuits for beginners.
- Never instruct beginners to experiment with mains electricity.
- Explain LED current limiting and component polarity.
- Warn about short circuits, overheating, and incorrect power connections.
- Recommend checking datasheets for uncertain component specifications.
- Never claim that a physical circuit was tested unless it actually was.

RESPONSE SPEED:
- Answer directly and avoid long introductions.
- Use simple explanations, usually 100-200 words.
- Give only the steps needed to answer the question.
- Do not repeat information the student already understands.
- For simple questions, answer in 2-5 sentences.
- For complex circuit tutorials, explain one stage at a time.

Keep answers organized with headings and numbered steps when useful.
"""


# Telegram menu
MENU = [
    ["Learn electronics", "Build a circuit"],
    ["Explain a component", "Troubleshoot"],
    ["Quiz me", "Learning roadmap"],
]

keyboard = ReplyKeyboardMarkup(
    MENU,
    resize_keyboard=True,
)


# Welcome message
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "Welcome to CircuitMentor!\n\n"
        "Your AI mentor for electronics, circuits, "
        "Arduino, hardware engineering, and robotics.\n\n"
        "Choose an option from the menu or ask me "
        "any electronics question.",
        reply_markup=keyboard,
    )


# Help command
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "CIRCUITMENTOR COMMANDS\n\n"
        "/start - Open the main menu\n"
        "/help - Show available commands\n"
        "/topics - View the learning roadmap\n"
        "/reset - Start a fresh conversation\n\n"
        "You can also type any electronics question.",
        reply_markup=keyboard,
    )


# Learning roadmap
async def topics(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "CIRCUITMENTOR LEARNING ROADMAP\n\n"
        "Level 1: Electricity fundamentals\n"
        "Voltage, current, resistance, and Ohm's law.\n\n"
        "Level 2: Electronic components\n"
        "Resistors, LEDs, capacitors, diodes, and transistors.\n\n"
        "Level 3: Basic circuits\n"
        "Breadboards, series and parallel circuits, and multimeters.\n\n"
        "Level 4: Circuit analysis\n"
        "Kirchhoff's laws, power, and circuit calculations.\n\n"
        "Level 5: Arduino and sensors\n"
        "Inputs, outputs, displays, motors, and practical projects.\n\n"
        "Level 6: Digital electronics\n"
        "Logic gates, binary, and digital signals.\n\n"
        "Level 7: Embedded systems\n"
        "Microcontrollers, embedded C/C++, and communication protocols.\n\n"
        "Level 8: Advanced hardware\n"
        "Robotics, PCB design, and system integration.\n\n"
        "Send 'Teach me Level 1' to begin.",
        reply_markup=keyboard,
    )


# Reset the conversation history
async def reset(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.user_data.pop("history", None)

    await update.message.reply_text(
        "Your conversation has been reset. "
        "What would you like to learn?",
        reply_markup=keyboard,
    )


# Respond to messages using Gemini
async def answer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    question = update.message.text.strip()

    if not question:
        return

    # Convert menu selections into useful instructions
    menu_prompts = {
        "Learn electronics":
            "Start teaching me electronics from zero. "
            "Begin with the first essential concept and "
            "give me a small example.",

        "Build a circuit":
            "Guide me through building my first safe, "
            "low-voltage DC circuit step by step. "
            "List components, connections, and tests.",

        "Explain a component":
            "Ask me which electronic component I want "
            "to learn about. Give me a few examples.",

        "Troubleshoot":
            "Help me troubleshoot my circuit. Ask me "
            "about the components, wiring, power supply, "
            "and symptoms before suggesting possible fixes.",

        "Quiz me":
            "Give me a beginner electronics quiz. Ask "
            "one question at a time and wait for my answer. "
            "Explain the answer after I respond.",

        "Learning roadmap":
            "Create a practical learning roadmap from "
            "beginner electronics to advanced hardware "
            "engineering, with projects at each level.",
    }

    prompt = menu_prompts.get(question, question)

    await update.message.reply_text(
        "CircuitMentor is thinking..."
    )

    try:
        # Keep a separate conversation history for each Telegram user
        history = context.user_data.setdefault("history", [])

        # Send recent context to Gemini
        contents = []

        for item in history[-4:]:
            contents.append(
                {
                    "role": item["role"],
                    "parts": [{"text": item["text"]}],
                }
            )

        contents.append(
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        )

        response = await asyncio.to_thread(
            client.models.generate_content,
            model=MODEL,
            contents=contents,
            config={
                "system_instruction": INSTRUCTIONS,
            },
        )

        result = response.text

        if not result:
            result = (
                "I couldn't generate a response. "
                "Please try asking in a different way."
            )

        # Save the exchange for future context
        history.append(
            {"role": "user", "text": prompt}
        )
        history.append(
            {"role": "model", "text": result}
        )

        # Keep the most recent messages to limit context size
        context.user_data["history"] = history[-4:]

        # Telegram limits the length of a single message
        for start_index in range(0, len(result), 4000):
            await update.message.reply_text(
                result[start_index:start_index + 4000]
            )

    except Exception as error:
        # Details appear in the terminal, not in the Telegram chat
        print("Gemini API error:", repr(error))

        await update.message.reply_text(
            "I couldn't get an AI response.\n\n"
            "Please check:\n"
            "1. Your Gemini API key in the .env file.\n"
            "2. Whether your selected Gemini model is available.\n"
            "3. Your internet connection.\n"
            "4. Your Google AI API usage limits.\n\n"
            "The exact error is printed in your terminal."
        )


# Start the Telegram bot
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("topics", topics))
    app.add_handler(CommandHandler("reset", reset))

    # Handle ordinary text messages and menu selections
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            answer,
        )
    )

    print("CircuitMentor is running!")

    app.run_polling()


if __name__ == "__main__":
    main()
