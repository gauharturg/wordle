import requests
import random

# URL of the API endpoint
api_url = "https://wordle.votee.dev:8000/daily"  # Replace with the actual API URL

# Function to read words from the file
def load_word_list(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

# Function to make an API call
def make_guess(api_url, word):
    # Parameters for the API call
    params = {
        "guess": word,
        "size": len(word)
    }

    try:
        # Make the API request
        response = requests.get(api_url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            print(f"Failed to make a guess. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to update the word list based on feedback
def update_word_list(word_list, feedback, guess):
    new_word_list = []
    absent_letters = {guess[i] for i, item in enumerate(feedback) if item['result'] == 'absent'}
    present_letters = {guess[i] for i, item in enumerate(feedback) if item['result'] == 'present'}
    correct_positions = {i: guess[i] for i, item in enumerate(feedback) if item['result'] == 'correct'}

    for word in word_list:
        if any(letter in word for letter in absent_letters):
            continue
        if not all(letter in word for letter in present_letters):
            continue
        if any(word[i] != correct_positions[i] for i in correct_positions):
            continue
        new_word_list.append(word)

    return new_word_list

# Main function to make smarter guesses
def guess_until_correct(file_path):
    word_list = load_word_list(file_path)
    
    while word_list:
        random.shuffle(word_list)
        guess = random.choice(word_list)
        result = make_guess(api_url, guess)
        
        if result:
            print(f"Guess: {guess}")
            feedback = []

            for item in result:
                if item['result'] == 'correct':
                    feedback.append(f"{item['guess']} (Correct)")
                elif item['result'] == 'present':
                    feedback.append(f"{item['guess']} (Present)")
                else:
                    feedback.append(f"{item['guess']} (Absent)")

            # Display feedback for the current guess
            print("Feedback: " + ", ".join(feedback))

            # Check if all letters are correct
            all_correct = all(item['result'] == 'correct' for item in result)
            if all_correct:
                print(f"Correct word found: {guess}")
                break

            # Update the word list based on feedback
            word_list = update_word_list(word_list, result, guess)
        else:
            print("Error or no response. Trying next word...")

# Run the guess function
guess_until_correct('nyt-answers.txt')

# Run the guess function
guess_until_correct('nyt-answers.txt')