import random
import re
import datetime

# ---------------------------------------------------------
# Jokes and fun facts (randomly selected from a list)
# ---------------------------------------------------------
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why do Python programmers wear glasses? Because they can't C!",
    "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'",
    "Why did the function break up with the loop? It felt used.",
    "There are 10 types of people: those who understand binary and those who don't.",
    "Why did the developer go broke? Because they used up all their cache."
]

FACTS = [
    "Honey never spoils - archaeologists found 3000-year-old honey that was still edible.",
    "The first computer bug was an actual moth found in a relay in 1947.",
    "Python was named after the comedy group Monty Python, not the snake.",
    "A single Google search uses about the same energy as a light bulb for a few seconds.",
    "The first computer programmer was Ada Lovelace, in the 1840s.",
    "Bananas are berries, but strawberries aren't."
]

# ---------------------------------------------------------
# Intent map: each intent has a list of trigger keywords/phrases
# and one or more possible replies. Using keyword lists (instead
# of exact matches) lets JARVIS understand phrases like
# "hey there, how are you doing?" and not just "how are you".
# ---------------------------------------------------------
INTENTS = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "yo", "good morning", "good evening"],
        "replies": [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! I'm here and ready to help."
        ]
    },
    "how_are_you": {
        "keywords": ["how are you", "how's it going", "how are things"],
        "replies": ["I'm just a program, but I'm running smoothly! Thanks for asking."]
    },
    "bot_name": {
        "keywords": ["what is your name", "who are you", "your name"],
        "replies": ["I'm JARVIS, your virtual assistant."]
    },
    "creator": {
        "keywords": ["who created you", "who made you", "who built you"],
        "replies": ["I was created by Jidnyasa Bhagat as a Python learning project."]
    },
    "capabilities": {
        "keywords": ["what can you do", "your features", "help me with"],
        "replies": ["I can chat with you, tell jokes, share facts, do simple math, "
                     "and tell you the date/time. Type 'help' for the full list."]
    },
    "thanks": {
        "keywords": ["thank you", "thanks", "appreciate it"],
        "replies": ["You're welcome! Happy to help.", "Anytime!"]
    },
    "mood_good": {
        "keywords": ["i am fine", "i'm fine", "i am good", "i'm good", "doing well"],
        "replies": ["Glad to hear that!"]
    },
}

# Words/phrases that end the conversation
EXIT_COMMANDS = {"bye", "exit", "quit", "goodbye", "see you"}


# ---------------------------------------------------------
# Function: display_welcome
# Shows the welcome banner and asks for the user's name.
# ---------------------------------------------------------
def display_welcome():
    print("=" * 40)
    print("        Python AI Chatbot - JARVIS")
    print("=" * 40)
    print("Hello! I'm your virtual assistant.")
    print("Type 'help' to see available commands.")
    print("Type 'bye' to exit.\n")


# ---------------------------------------------------------
# Function: show_help
# Displays a list of all supported commands.
# ---------------------------------------------------------
def show_help():
    print("\nHere's what you can ask me:")
    print("- hello / hi / hey")
    print("- how are you")
    print("- what is your name")
    print("- who created you")
    print("- what can you do")
    print("- tell me a joke")
    print("- tell me a fact")
    print("- today's date")
    print("- current time")
    print("- calculate <expression>   (e.g., calculate 12 + 8)")
    print("- save chat                (saves the conversation to a text file)")
    print("- thank you")
    print("- help")
    print("- bye / exit / quit")


# ---------------------------------------------------------
# Function: show_date
# Returns the current date as a formatted string.
# ---------------------------------------------------------
def show_date():
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today's date is {today}."


# ---------------------------------------------------------
# Function: show_time
# Returns the current time as a formatted string.
# ---------------------------------------------------------
def show_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {now}."


# ---------------------------------------------------------
# Function: calculate_expression
# Safely evaluates a simple arithmetic expression typed by
# the user (supports +, -, *, /, parentheses, decimals).
# Uses only digits/operators - no external libraries, and
# rejects anything that isn't a safe math expression.
# ---------------------------------------------------------
def calculate_expression(expression):
    allowed_characters = set("0123456789+-*/(). ")

    # Reject expressions containing anything other than numbers/operators
    if not expression or not set(expression) <= allowed_characters:
        return "I can only calculate simple math expressions using numbers and + - * / ( )."

    try:
        result = eval(expression, {"__builtins__": {}})  # restricted eval - no built-ins
        return f"The result is {result}."
    except ZeroDivisionError:
        return "I can't divide by zero!"
    except Exception:
        return "That doesn't look like a valid expression. Try something like '12 + 8'."


# ---------------------------------------------------------
# Function: find_intent
# Searches the user's message for known keywords and returns
# the matching intent name, or None if nothing matches.
# Uses whole-word/phrase boundaries (via regex) so short
# keywords like "yo" don't accidentally match inside longer
# words like "you" or "your". Longer, more specific keywords
# are checked first so "who created you" isn't swallowed by
# a shorter, less specific match.
# ---------------------------------------------------------
def find_intent(cleaned_input):
    # Collect every (keyword, intent_name) pair, longest keyword first
    all_keywords = []
    for intent_name, intent_data in INTENTS.items():
        for keyword in intent_data["keywords"]:
            all_keywords.append((keyword, intent_name))
    all_keywords.sort(key=lambda pair: len(pair[0]), reverse=True)

    for keyword, intent_name in all_keywords:
        # \b matches a word boundary, so "yo" won't match inside "you"
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, cleaned_input):
            return intent_name
    return None


# ---------------------------------------------------------
# Function: get_response
# Takes the user's raw input and the user's name, and returns
# an appropriate chatbot reply. Handles case-insensitivity,
# special commands (joke, fact, date, time, calculate, help)
# and falls back to keyword-based intent matching.
# ---------------------------------------------------------
def get_response(user_input, user_name):
    cleaned_input = user_input.lower().strip()

    # Special commands that need dynamic content
    if "joke" in cleaned_input:
        return random.choice(JOKES)
    elif "fact" in cleaned_input:
        return random.choice(FACTS)
    elif "date" in cleaned_input:
        return show_date()
    elif "time" in cleaned_input:
        return show_time()
    elif cleaned_input.startswith("calculate"):
        expression = cleaned_input.replace("calculate", "", 1).strip()
        return calculate_expression(expression)
    elif cleaned_input == "help":
        show_help()
        return None  # show_help() already prints its own output

    # Try to match a known intent using keywords
    intent = find_intent(cleaned_input)
    if intent:
        reply = random.choice(INTENTS[intent]["replies"])
        # Personalize the greeting with the user's name, if known
        if intent == "greeting" and user_name:
            reply = f"{reply.rstrip('.!')}, {user_name}!"
        return reply

    # Fallback response for unrecognized input
    return "Sorry, I don't understand that. Type 'help' to see available commands."


# ---------------------------------------------------------
# Function: chat
# Runs the main conversation loop. Keeps chatting until the
# user types an exit command. Returns the message count and
# the full conversation transcript (list of strings).
# ---------------------------------------------------------
def chat(user_name):
    message_count = 0
    transcript = []  # Stores every line of the conversation for saving later

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nJARVIS: Session interrupted.")
            break

        if user_input == "":
            print("JARVIS: Please type something, or type 'help' for commands.")
            continue

        message_count += 1
        transcript.append(f"You: {user_input}")

        # Check for exit commands (case-insensitive, matches whole message)
        if user_input.lower() in EXIT_COMMANDS:
            break

        # Bonus command: save the conversation transcript to a file
        if user_input.lower() == "save chat":
            save_transcript(transcript)
            continue

        # Get and display the chatbot's response (wrapped for safety)
        try:
            reply = get_response(user_input, user_name)
        except Exception as error:
            reply = f"Oops, something went wrong on my end ({error})."

        if reply is not None:
            print("JARVIS:", reply)
            transcript.append(f"JARVIS: {reply}")

    return message_count, transcript


# ---------------------------------------------------------
# Function: save_transcript
# Writes the conversation so far to 'chat_history.txt'.
# ---------------------------------------------------------
def save_transcript(transcript):
    try:
        with open("chat_history.txt", "w", encoding="utf-8") as file:
            file.write(f"JARVIS Chat Log - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 40 + "\n")
            file.write("\n".join(transcript))
        print("JARVIS: Conversation saved to 'chat_history.txt'.")
    except OSError as error:
        print(f"JARVIS: Sorry, I couldn't save the file ({error}).")


# ---------------------------------------------------------
# Function: main
# Displays the welcome message, collects the user's name,
# runs the chat loop, shows a goodbye message with session
# stats, then optionally restarts the chatbot.
# ---------------------------------------------------------
def main():
    keep_running = True

    while keep_running:
        display_welcome()

        user_name = input("Before we start, what's your name? ").strip().title()
        if user_name:
            print(f"\nJARVIS: Nice to meet you, {user_name}!\n")

        start_time = datetime.datetime.now()
        total_messages, transcript = chat(user_name)
        end_time = datetime.datetime.now()
        duration_seconds = int((end_time - start_time).total_seconds())

        # Goodbye message
        print("\nJARVIS: Thank you for chatting!")
        print("JARVIS: Have a wonderful day!")

        # Session stats
        print(f"\n(You sent {total_messages} message(s) over {duration_seconds} second(s).)")

        # Offer to save the transcript if it wasn't already saved
        if transcript:
            save_choice = input("Save this conversation to a file? (Y/N): ").strip().lower()
            if save_choice == "y":
                save_transcript(transcript)

        # Ask if the user wants to restart
        restart_choice = input("\nWould you like to start a new chat? (Y/N): ").strip().lower()
        if restart_choice != "y":
            keep_running = False
            print("\nGoodbye!")


# ---------------------------------------------------------
# Entry point of the program
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
