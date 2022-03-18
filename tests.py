from unittest import main, TestCase
from tools import GameState, CustomGameState

class CustomUnittest(TestCase):
    def test_gamestate_init(self):
        new = GameState()
        self.assertEqual(new.word_len, 5)
        self.assertEqual(new.turn_limit, 6)
        self.assertEqual(new.hard_mode, False)

        new = GameState(7, True)
        self.assertEqual(new.turn_limit, 7)
        self.assertEqual(new.hard_mode, True)

    def test_set_daily_answer(self):
        new = GameState()
        new.date = 0
        output = new.set_daily_answer()
        new.answer = ""
        output2 = new.set_daily_answer()
        self.assertEqual(output, output2)

    def test_set_turn_limit(self):
        new = GameState()
        new.set_turn_limit(6)
        self.assertEqual(new.turn_limit, 6)

        new.set_turn_limit(10)
        self.assertEqual(new.turn_limit, 10)

        new.set_turn_limit(-1)
        self.assertEqual(new.turn_limit, 6)

    def test_incr_curr_turn(self):
        new = GameState()
        new.set_turn_limit(3)
        self.assertEqual(new.curr_turn, 0)
        output = new.incr_curr_turn()
        self.assertEqual(new.curr_turn, 1)

        output = new.incr_curr_turn()
        output = new.incr_curr_turn()
        self.assertEqual(new.curr_turn, 3)

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

    def test_set_guess(self):
        new = GameState()
        new.answer = "homes"
        new.word_len = 5
        new.curr_turn = 1
        new.turn_limit = 1
        output = new.set_guess("build")
        self.assertEqual(output, "Turn limit reached.")
        output = new.set_guess("homes")
        self.assertEqual(output, "Turn limit reached.")

        new.turn_limit = 6
        output = new.set_guess("horse")
        self.assertEqual(output, [2,2,0,1,1])
        self.assertEqual(new.guess_hist[-1], "horse")
        output = new.set_guess("build")
        self.assertEqual(output, [0,0,0,0,0])
        self.assertEqual(new.guess_hist[-1], "build")

        output = new.set_guess("homes")
        self.assertEqual(output, True)

    def test_is_valid_guess(self):
        new = GameState()
        new.answer = "word"
        new.word_len = 4
        result, output = new.is_valid_guess("123 asd")
        self.assertEqual(output, "Invalid characters.")
        result, output = new.is_valid_guess("fan-")
        self.assertEqual(output, "Invalid characters.")

        result, output = new.is_valid_guess("")
        self.assertEqual(output, "Incorrect word length.")
        result, output = new.is_valid_guess("asdfasf")
        self.assertEqual(output, "Incorrect word length.")

        result, output = new.is_valid_guess("abcd")
        self.assertEqual(output, "Invalid word.")
        result, output = new.is_valid_guess("ghjx")
        self.assertEqual(output, "Invalid word.")

        result, output = new.is_valid_guess("bird")
        self.assertEqual(output, "bird")
        result, output = new.is_valid_guess("dark")
        self.assertEqual(output, "dark")

    def test_process_guess(self):
        new = GameState()
        new.answer = "homes"
        new.word_len = 5
        output = new.process_guess("build")
        self.assertEqual(output, [0,0,0,0,0])

        output = new.process_guess("halve")
        self.assertEqual(output, [2,0,0,0,1])

        output = new.process_guess("homes")
        self.assertEqual(output, [2,2,2,2,2])

        new.answer = "books"
        new.word_len = 5
        output = new.process_guess("happy")
        self.assertEqual(output, [0,0,0,0,0])

        output = new.process_guess("hooks")
        self.assertEqual(output, [0,2,2,2,2])

        output = new.process_guess("oboes")
        self.assertEqual(output, [1,1,2,0,2])


    def test_find_partial(self):
        new = GameState()
        output = new.find_partial("birds", [1,1,0,1,1])
        self.assertEqual(output, {0:"b", 1:"i", 3:"d", 4:"s"})

        output = new.find_partial("birds", [1,2,1,0,2])
        self.assertEqual(output, {0:"b", 2:"r"})

        output = new.find_partial("reads", [2,0,2,2,0])
        self.assertEqual(output, {})

    def test_find_correct(self):
        new = GameState()
        output = new.find_correct("birds", [1,1,0,1,1])
        self.assertEqual(output, {})

        output = new.find_correct("birds", [1,2,1,0,2])
        self.assertEqual(output, {1:"i", 4:"s"})

        output = new.find_correct("reads", [2,0,2,2,0])
        self.assertEqual(output, {0:"r", 2:"a", 3:"d"})

    def test_is_valid_hard_mode(self):
        new = GameState()
        new.answer = "books"
        new.set_guess("turns")
        output = new.is_valid_hard_mode("birds")
        self.assertEqual(output, True)
        new.set_guess("birds")
        output = new.is_valid_hard_mode("about")
        self.assertEqual(output, 'Position 0 needs to be "b".')

        new = GameState()
        new.answer = "shots"
        new.set_guess("house")
        output = new.is_valid_hard_mode("shoes")
        self.assertEqual(output, True)
        new.set_guess("shoes")
        output = new.is_valid_hard_mode("shows")
        self.assertEqual(output, True)
        new.set_guess("shows")
        output = new.is_valid_hard_mode("throw")
        self.assertEqual(output, 'Position 0 needs to be "s".')

    def test_is_valid_word(self):
        new = GameState()
        output = new.is_valid_word("bird")
        self.assertEqual(output, True)

        output = new.is_valid_word("because")
        self.assertEqual(output, True)

        output = new.is_valid_word("hfzzdfasddg")
        self.assertEqual(output, False)

if __name__ == '__main__':
    main()
