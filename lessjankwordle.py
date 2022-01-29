

class Game_State():
    def __init__(self, answer, turn_limit, hard_mode):
        self.answer = answer
        self.word_len = len(answer)
        self.turn_limit = turn_limit
        self.curr_turn = 1
        self.hard_mode = hard_mode

    def set_answer(answer):
        self.answer = answer
        set_word_len(len(answer))
        return self.answer

    def get_answer():
        return self.answer

    def set_word_len(word_len):
        self.word_len = word_len
        return self.word_len

    def get_word_len():
        return self.word_len

    def set_turn_limit(turn_limit):
        if turn_limit <= self.curr_turn:
            return False
        self.turn_limit = turn_limit
        return self.turn_limit

    def get_turn_limit():
        return self.turn_limit

    def reset_curr_turn():
        self.curr_turn = 1
        return self.curr_turn

    def incr_curr_turn(amount = 1):
        if self.curr_turn + amount > self.turn_limit:
            return False
        self.curr_turn += amount
        return self.curr_turn

    def get_curr_turn():
        return self.curr_turn

    def set_hard_mode(hard_mode):
        self.hard_mode = hard_mode
        return self.hard_mode

    def get_hard_mode():
        return self.hard_mode

    # Calculate the incorrect letters (0),
    # correct letter, incorrect position (1),
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

    # Main guess checking function
    def guess_checker(guess, turn_num):
        # TODO: Ensure guess len = answer len in main & front end
        # TODO: Ensure guess only contains alpha(), all is_uppercase, in main & frontend
        assertEqual(len(guess), len(self.answer))

        if guess == self.answer:
            return True

        if !incr_curr_turn():
            return False
        guess_breakdown = process_guess(guess)
        return guess_breakdown
