from unittest import main, TestCase
from tools import GameState, CustomGameState

class CustomUnittest(TestCase):
    def test_gamestate_init(self):
        new = GameState()
        self.assertEqual(new.word_len, 5)
        self.assertEqual(new.turn_limit, 6)
        self.assertEqual(new.hard_mode, False)

        new = GameState(6, 7, True)
        self.assertEqual(new.word_len, 6)
        self.assertEqual(new.turn_limit, 7)
        self.assertEqual(new.hard_mode, True)

    def test_set_daily_answer(self):
        new = GameState()
        new.date = 0
        output = new.set_daily_answer()
        new.answer = ""
        output2 = new.set_daily_answer()
        assertEqual(output, output2)

    def test_set_guess(self):
        new = GameState()
        new.answer = "word"
        new.word_len = 4
        output = new.set_guess("123 asd")
        assertEqual(output, "Invalid characters.")
        output = new.set_guess("fan-")
        assertEqual(output, "Invalid characters.")

        output = new.set_guess("")
        assertEqual(output, "Incorrect word length.")
        output = new.set_guess("asdfasf")
        assertEqual(output, "Incorrect word length.")

        output = new.set_guess("abcd")
        assertEqual(output, "Invalid word.")
        output = new.set_guess("ghjx")
        assertEqual(output, "Invalid word.")

        output = new.set_guess("bird")
        assertEqual(new.guess, "bird")
        assertEqual(new.guess_hist[-1], "bird")
        output = new.set_guess("dark")
        assertEqual(new.guess, "dark")
        assertEqual(new.guess_hist[-1], "dark")

    def test_set_word_len(self):
        new = GameState()
        new.set_word_len(5)
        self.assertEqual(new.word_len, 5)

        new.set_word_len(7)
        self.assertEqual(new.word_len, 7)

        new.set_word_len(35)
        self.assertEqual(new.word_len, 5)

    def test_set_turn_limit(self):
        new = GameState()
        new.set_turn_limit(6)
        self.assertEqual(new.word_len, 6)

        new.set_word_len(10)
        self.assertEqual(new.word_len, 10)

        new.set_word_len(-1)
        self.assertEqual(new.word_len, 6)

    def test_incr_curr_turn(self):
        new = GameState()
        new.set_turn_limit(3)
        self.assertEqual(new.curr_turn, 1)
        output = new.incr_curr_turn()
        self.assertEqual(new.curr_turn, 2)

        output = new.incr_curr_turn()
        self.assertEqual(new.word_len, 3)

        output = new.incr_curr_turn()
        self.assertEqual(output, False)

    def test_set_hard_mode(self):
        new = GameState()
        new.set_hard_mode(6)
        self.assertEqual(new.hard_mode, False)

        new.set_hard_mode(True)
        self.assertEqual(new.hard_mode, True)

        new.set_hard_mode(False)
        self.assertEqual(new.hard_mode, False)

    def test_guess_checker(self):
        new = GameState()
        new.answer = "homes"
        new.word_len = 5
        new.curr_turn = 1
        new.turn_limit = 1
        output = new.guess_checker("build")
        assertEqual(output, False)
        output = new.guess_checker("homes")
        assertEqual(output, False)

        new.turn_limit = 6
        output = new.guess_checker("homes")
        assertEqual(output, True)

        output = new.guess_checker("horse")
        assertEqual(output, [2,2,0,1,1])
        output = new.guess_checker("build")
        assertEqual(output, [0,0,0,0,0])

    def test_process_guess(self):
        new = GameState()
        new.answer = "homes"
        new.word_len = 5
        output = new.process_guess("build")
        assertEqual(output, [0,0,0,0,0])

        output = new.process_guess("halve")
        assertEqual(output, [2,0,0,0,1])

        output = new.process_guess("homes")
        assertEqual(output, [2,2,2,2,2])

        new.answer = "books"
        new.word_len = 5
        output = new.process_guess("happy")
        assertEqual(output, [0,0,0,0,0])

        output = new.process_guess("hooks")
        assertEqual(output, [0,2,2,2,2])

        output = new.process_guess("oboes")
        assertEqual(output, [0,2,2,2,2])


    def test_find_partial(self):
        new = GameState()
        output = new.find_partial("birds", [1,1,0,1,1])
        assertEqual(output, {0:"b", 1:"i", 3:"r", 4:"s"})

        output = new.find_partial("birds", [1,2,1,0,2])
        assertEqual(output, {0:"b", 2:"r"})

        output = new.find_partial("reads", [2,0,2,2,0])
        assertEqual(output, {})

    def test_find_correct(self):
        new = GameState()
        output = new.find_correct("birds", [1,1,0,1,1])
        assertEqual(output, {})

        output = new.find_correct("birds", [1,2,1,0,2])
        assertEqual(output, {1:"i", 4:"s"})

        output = new.find_correct("reads", [2,0,2,2,0])
        assertEqual(output, {0:"r", 2:"a", 3:"d"})

    def test_is_valid_hard_mode(self):
        new = GameState()
        new.answer = "books"
        new.set_guess("turns")
        output = new.is_valid_hard_mode("birds")
        assertEqual(output, True)
        output = new.is_valid_hard_mode("about")
        assertEqual(output, False)

        new = GameState()
        new.answer = "shots"
        new.set_guess("house")
        output = new.is_valid_hard_mode("shoes")
        assertEqual(output, True)
        output = new.is_valid_hard_mode("those")
        assertEqual(output, True)
        output = new.is_valid_hard_mode("throw")
        assertEqual(output, False)

    def test_is_valid_word(self):
        new = GameState()
        output = new.is_valid_word("bird")
        assertEqual(output, True)

        output = new.is_valid_word("because")
        assertEqual(output, True)

        output = new.is_valid_word("hfzzdfasddg")
        assertEqual(output, False)
