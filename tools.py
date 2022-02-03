from datetime import date
import random
import re
from models import app, db, Word

class GameState():
    def __init__(self, length = 5, turn_limit = 6, hard_mode = False):
        self.answer = None
        self.guess = None
        self.guess_hist = []
        self.word_len = None
        self.turn_limit = None
        self.curr_turn = 1
        self.hard_mode = None
        self.date = None
        self.num_same_len_db = {}
        self.loc_same_len_db = {}
        self.min_word_len = 4
        self.max_word_len = 10

        set_word_len(length)
        set_hard_mode(hard_mode)
        set_turn_limit(turn_limit)
        init_same_len_db()
        update_date()

    # Initialize same length word information from db.
    # num_same_len_db is the number of words with the ith length.
    # loc_same_len_db is the starting location for those words of same length.
    def init_same_len_db():
        for i in range(self.min_word_len, self.max_word_len + 1):
            results = db.session.query(Word.Index).filter(Word.Length == i).all()
            self.num_same_len_db[i] = len(results)
            self.loc_same_len_db[i] = min(results)

    # Checks if the day has changed. If so, update answer.
    def update_date():
        today = date.today().strftime("%m/%d/%Y")
        if today != self.date:
            self.date == today
            set_daily_answer()
        return self.date

    # Sets the daily answer, using seed random generator.
    # The location dict is for pulling from postgres db.
    def set_daily_answer():
        random.seed(hash(self.date))
        offset = random.randint(0, self.num_same_len_db[self.length])
        todays_word = self.loc_same_len_db[self.length] + offset
        self.answer = db.session.query(Word.Value).filter(Word.Index == todays_word).first()
        return self.answer

    # Sets the current guess and pushes it to the guess history.
    # Must only contains lowercase letters, match length, and is a valid word.
    def set_guess(guess):
        temp_guess = guess.lower
        result = re.match('^[a-z]+$', temp_guess)
        if result == None:
            return "Invalid characters."
        if len(temp_guess) != self.word_len:
            return "Incorrect word length."
        if not is_valid_word(temp_guess):
            return "Invalid word."
        self.guess = temp_guess
        self.guess_hist.append(self.guess)
        return self.guess

    # Sets the word length for the puzzle, redefining the answer.
    def set_word_len(word_len):
        if (word_len >= self.min_word_len and word_len <= self.max_word_len):
            self.word_len = word_len
        else:
            self.word_len = 5
        set_daily_answer()
        return self.word_len

    # Defines the turn limit for the puzzle.
    def set_turn_limit(turn_limit):
        if turn_limit > self.curr_turn:
            self.turn_limit = turn_limit
        else:
            self.turn_limit = 6
        return self.turn_limit

    # Resets the turn counter to 1.
    def reset_curr_turn():
        self.curr_turn = 1
        return self.curr_turn

    # Incremenets the turn coutner, default by +1.
    def incr_curr_turn():
        if self.curr_turn + 1 > self.turn_limit:
            return False
        self.curr_turn += 1
        return self.curr_turn

    # Sets hard mode based on param.
    def set_hard_mode(hard_mode):
        if hard_mode == True or hard_mode == False:
            self.hard_mode = hard_mode
        else:
            self.hard_mode = False
        return self.hard_mode

    # Main guess checking function
    def guess_checker(guess):
        # TODO: Ensure guess len = answer len in main & front end
        if not incr_curr_turn():
            return False

        assertEqual(len(self.guess), len(self.answer))
        if self.guess == self.answer:
            return True
            
        guess_breakdown = process_guess(self.guess)
        return guess_breakdown

        # Calculate the incorrect letters (0),
        # partial: correct letter, incorrect position (1),
        # & correct letter & position tiles (2).
        def process_guess(guess):
            guess_breakdown = [-1] * len(guess)
            temp_answer = self.answer

            # Check for correct letter & position first.
            # Found letters are remove from temp_answer to avoid double counting.
            for i in range(len(guess)):
                if guess[i] == temp_answer[i]:
                    guess_breakdown[i] = 2
                    temp_answer[i] = ''

            # Check for correct letter * incorrect position
            # for remaining letters in guess. Else, incorrect.
            for i in range(len(guess)):
                if guess_breakdown[i] == -1:
                    idx = temp_answer.find(guess[i]) # returns -1 if not found
                    if idx > -1:
                        guess_breakdown[i] = 1
                        temp_answer[idx] = ''
                    else:
                        guess_breakdown[i] = 0

            return guess_breakdown

        # Find & return the letters from a guess & its breakdown
        # that are partially correct (correct letter, incorrect position)
        def find_partial(guess, breakdown):
            soln = {}
            for i in range(len(breakdown)):
                if breakdown[i] == 1:
                    soln[i] = guess[i]
            return soln

        # Find & return the letters from a guess & its breakdown
        # that are entirely correct (correct letter, correct position)
        def find_correct(guess, breakdown):
            soln = {}
            for i in range(len(breakdown)):
                if breakdown[i] == 2:
                    soln[i] = guess[i]
            return soln

        # Returns True if the provided guess follows hard mode rules.
        # Else, return string describing error.
        def is_valid_hard_mode(guess):
            # First guess is always valid.
            if self.curr_turn == 1:
                return True

            # Previous correct letters need to be present.
            prev_correct = find_correct(self.guess, process_guess(self.guess))
            curr_correct = find_correct(guess, process_guess(guess))
            for i in prev_correct.keys():
                if i not in curr_correct.keys():
                    return 'Position ' + str(i) + ' needs to be "' + str(prev_correct[i]) + '".'

            # Previous partially correct letters need to be present,
            # as correct or partially correct.
            prev_partial = find_partial(self.guess, process_guess(self.guess))
            curr_partial = find_partial(guess, process_guess(guess))
            for val in prev_partial.values():
                if val not in curr_correct.values() and val not in curr_partial.values():
                    return 'Need to use "' + str(val) + '".'

            return True

        # Returns True if the provided guess is a valid word. Else, False.
        def is_valid_word(guess):
            results = db.session.query(Word.Value).filter(Word.Value == guess).first()
            if results == None:
                return False
            return True


class CustomGameState(GameState):
    def __init__(self, answer, turn_limit, hard_mode):
        length = len(answer)
        super().__init__(length, turn_limit, hard_mode)

        set_custom_answer(answer)

    # Set a custom answer for this puzzle.
    def set_custom_answer(answer):
        self.answer = answer
        self.length = len(answer)
        return self.answer
