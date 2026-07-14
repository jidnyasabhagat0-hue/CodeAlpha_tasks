import random

# ---------------------------------------------------------
# Constants
# ---------------------------------------------------------

# At least 10 predefined words for the game to choose from
WORD_LIST = [
    "python", "hangman", "developer", "keyboard", "computer",
    "function", "variable", "terminal", "software", "algorithm",
    "internet", "database"
]

MAX_ATTEMPTS = 6  # Maximum number of incorrect guesses allowed

# ASCII art for each stage of the hangman (0 = no wrong guesses, 6 = fully hanged)
HANGMAN_STAGES = [
    """
       ------
       |    |
       |
       |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |    |
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   /
       |
    ---------
    """,
    """
       ------
       |    |
       |    O
       |   /|\\
       |   / \\
       |
    ---------
    """
]


# ---------------------------------------------------------
# Function: choose_word
# Randomly selects a word from the word list.
# ---------------------------------------------------------
def choose_word(word_list):
    return random.choice(word_list)


# ---------------------------------------------------------
# Function: display_word
# Builds a string showing guessed letters and underscores
# for letters that haven't been guessed yet.
# ---------------------------------------------------------
def display_word(word, guessed_letters):
    revealed = ""
    for letter in word:
        if letter in guessed_letters:
            revealed += letter + " "
        else:
            revealed += "_ "
    return revealed.strip()


# ---------------------------------------------------------
# Function: draw_hangman
# Prints the ASCII hangman drawing based on the number
# of incorrect guesses made so far.
# ---------------------------------------------------------
def draw_hangman(wrong_guess_count):
    print(HANGMAN_STAGES[wrong_guess_count])


# ---------------------------------------------------------
# Function: get_guess
# Prompts the player for a single letter and validates it.
# Rejects numbers, symbols, multi-character input, and
# informs the player if the letter was already guessed
# (without penalizing them).
# ---------------------------------------------------------
def get_guess(guessed_letters):
    while True:
        guess = input("\nGuess a letter: ").lower().strip()

        # Reject anything that isn't exactly one alphabet letter
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter (a-z).")
            continue

        # Inform the player if they already guessed this letter
        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try a different letter.")
            continue

        return guess


# ---------------------------------------------------------
# Function: update_game
# Updates game state based on the player's guess.
# Returns the updated remaining_attempts value.
# ---------------------------------------------------------
def update_game(word, guess, guessed_letters, incorrect_letters, remaining_attempts):
    guessed_letters.add(guess)

    if guess in word:
        print(f"Good guess! '{guess}' is in the word.")
    else:
        incorrect_letters.add(guess)
        remaining_attempts -= 1
        print(f"Sorry, '{guess}' is not in the word.")

    return remaining_attempts


# ---------------------------------------------------------
# Function: show_status
# Displays the current word, remaining attempts,
# incorrect letters, and all guessed letters.
# ---------------------------------------------------------
def show_status(word, guessed_letters, incorrect_letters, remaining_attempts):
    print("\nWord: " + display_word(word, guessed_letters))
    print("Remaining attempts:", remaining_attempts)
    print("Incorrect letters:", ", ".join(sorted(incorrect_letters)) if incorrect_letters else "None")
    print("All guessed letters:", ", ".join(sorted(guessed_letters)) if guessed_letters else "None")


# ---------------------------------------------------------
# Function: play_game
# Runs a single round of Hangman from start to finish.
# ---------------------------------------------------------
def play_game():
    word = choose_word(WORD_LIST)
    guessed_letters = set()     # All letters guessed (correct + incorrect)
    incorrect_letters = set()   # Only incorrect letters
    remaining_attempts = MAX_ATTEMPTS

    print("\n=== Welcome to Hangman! ===")
    print(f"The word has {len(word)} letters. You have {MAX_ATTEMPTS} incorrect guesses allowed.")

    # Main game loop - continues until the player wins or runs out of attempts
    while remaining_attempts > 0:
        wrong_guess_count = MAX_ATTEMPTS - remaining_attempts
        draw_hangman(wrong_guess_count)
        show_status(word, guessed_letters, incorrect_letters, remaining_attempts)

        guess = get_guess(guessed_letters)
        remaining_attempts = update_game(
            word, guess, guessed_letters, incorrect_letters, remaining_attempts
        )

        # Winning condition: every letter in the word has been guessed
        if all(letter in guessed_letters for letter in word):
            draw_hangman(MAX_ATTEMPTS - remaining_attempts)
            print("\n🎉 Congratulations! You guessed the word correctly!")
            print("The word was:", word)
            return

    # Losing condition: ran out of attempts
    draw_hangman(MAX_ATTEMPTS)
    print("\n💀 Game Over!")
    print("The correct word was:", word)


# ---------------------------------------------------------
# Function: ask_play_again
# Asks the player whether they want another round.
# ---------------------------------------------------------
def ask_play_again():
    while True:
        choice = input("\nDo you want to play again? (Y/N): ").lower().strip()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Please enter 'Y' or 'N'.")


# ---------------------------------------------------------
# Main program loop
# Keeps starting new rounds until the player chooses to quit.
# ---------------------------------------------------------
def main():
    keep_playing = True
    while keep_playing:
        play_game()
        keep_playing = ask_play_again()

    print("\nThanks for playing Hangman! Goodbye.")


# ---------------------------------------------------------
# Entry point of the program
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
