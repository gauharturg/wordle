import requests
import string
import random
from collections import defaultdict

base_url = "https://wordle.votee.dev:8000"

# Initialize variables
letterProbabilities = {key: 0 for key in string.ascii_lowercase}
lettersNotAtInd = [[] for _ in range(5)]
lettersInWord = set()
absentLetters = set()
wordsAsLetters = defaultdict(list)

def guess_random_word(guess_word: str):
    response = requests.get(f"{base_url}/random", params={"guess": guess_word})
    response.raise_for_status()
    return response.json()

def load_possible_words():
    with open("nyt-answers.txt", "r") as file:
        return file.read().splitlines()

def rebalance():
    totalLetters = sum(letterProbabilities.values())
    if totalLetters > 0:
        for key in letterProbabilities:
            letterProbabilities[key] /= totalLetters
    else:
        equal_prob = 1 / len(letterProbabilities)
        for key in letterProbabilities:
            letterProbabilities[key] = equal_prob
    
    mostProbableKeys = sorted(letterProbabilities, key=letterProbabilities.get, reverse=True)[:15]
    topKeys = set(mostProbableKeys)

    wordList = []
    for word in wordsAsLetters:
        if word.issubset(topKeys):
            wordList.extend(wordsAsLetters[word])
            break

    return wordList

def validate_word(word, wordList):
    for ind, letter in enumerate(word):
        if letter.islower():
            lettersNotAtInd[ind].append(letter)
    
    absentLetters.update(letter.lower() for letter in word if letter.islower())

    validatedWordList = [
        w for w in wordList 
        if not any(letter in w for letter in absentLetters) and
        all((letter.islower() and w[ind] not in lettersNotAtInd[ind]) or
            (letter.isupper() and w[ind] == letter.lower()) or
            (letter.isupper() and letter in lettersInWord)
            for ind, letter in enumerate(word))
    ]

    return validatedWordList

def select_next_guess(possible_words):
    wordList = rebalance()
    filtered_word_list = [
        word for word in wordList 
        if not any(letter in word for letter in lettersInWord.union(absentLetters))
    ]
    print("filtered_word_list", filtered_word_list)
    print("lettersInWord", lettersInWord)
    print("absentLetters", absentLetters)
    random.shuffle(filtered_word_list)
    return filtered_word_list[0] if filtered_word_list else possible_words[0]

def update_possible_words(possible_words, result):
    if isinstance(result, list) and result:
        guess_word = result[0]['guess']
        validatedList = validate_word(guess_word, possible_words)

        for letter_info in result:
            if 'letter' in letter_info:
                if letter_info['result'] == 'correct' or letter_info['result'] == 'present':
                    lettersInWord.add(letter_info['letter'])
                elif letter_info['result'] == 'absent':
                    absentLetters.add(letter_info['letter'])

        return validatedList
    else:
        raise ValueError("Unexpected result format")

def solve_wordle():
    max_attempts = 6
    attempts = 0
    possible_words = load_possible_words()

    while attempts < max_attempts:
        current_guess = "saine" if attempts == 0 else select_next_guess(possible_words)
        result = guess_random_word(current_guess)
        attempts += 1
        print(f"Attempt {attempts}: {current_guess}")

        if all(letter['result'] == 'correct' for letter in result):
            print(f"Wordle solved in {attempts} attempts!")
            return
        else:
            possible_words = update_possible_words(possible_words, result)

    print("Failed to solve Wordle")

def main():
    solve_wordle()

if __name__ == "__main__":
    main()