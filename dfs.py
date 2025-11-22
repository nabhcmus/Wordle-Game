import time
import random

class DFSSolver:
    MASTER_START_WORDS = ['SLATE', 'CRANE', 'SOARE', 'RAISE', 'TRACE']
    
    def __init__(self, word_api):
        self.word_api = word_api
        self.all_words = self.word_api.words_list.copy()
        self.secret_word = self.word_api.word
        self.start_time = 0
        self.end_time = 0
        self.expanded_nodes = 0
        
    def _calculate_feedback(self, guess, secret):
        feedback = [''] * len(secret)
        secret_list = list(secret)
        guess_list = list(guess)

        for i in range(len(secret)):
            if guess_list[i] == secret_list[i]:
                feedback[i] = 'G'
                secret_list[i] = '#'
                guess_list[i] = '$'

        for i in range(len(secret)):
            if guess_list[i] != '$' and guess_list[i] in secret_list:
                feedback[i] = 'Y'
                secret_list[secret_list.index(guess_list[i])] = '#'
        
        for i in range(len(secret)):
            if feedback[i] == '':
                feedback[i] = 'X'
        
        return feedback

    def _filter_candidates(self, candidates, guess, feedback):
        new_candidates = []
        for word in candidates:
            if self._calculate_feedback(guess, word) == feedback:
                new_candidates.append(word)
        self.expanded_nodes += len(candidates)
        return new_candidates

    def solve(self, board_state):
        self.start_time = time.time()
        
        candidate_words = self.all_words.copy()
        for guess, feedback in board_state:
            candidate_words = self._filter_candidates(candidate_words, guess, feedback)

        solution_path = []
        found_solution = False
        
        attempts_left = 6 - len(board_state)

        is_first_move = not board_state
        if is_first_move:
            first_guess = random.choice(self.MASTER_START_WORDS)
            
            solution_path.append(first_guess)
            real_feedback = self._calculate_feedback(first_guess, self.secret_word)

            if all(f == 'G' for f in real_feedback):
                found_solution = True
            else:
                candidate_words = self._filter_candidates(candidate_words, first_guess, real_feedback)
                if first_guess in candidate_words:
                    candidate_words.remove(first_guess)
            attempts_left -= 1
        for _ in range(attempts_left):
            if not candidate_words:
                break
            guess_word = candidate_words[0]
            solution_path.append(guess_word)
            
            real_feedback = self._calculate_feedback(guess_word, self.secret_word)

            if all(f == 'G' for f in real_feedback):
                found_solution = True
                break
            candidate_words = self._filter_candidates(candidate_words, guess_word, real_feedback)
            if guess_word in candidate_words:
                candidate_words.remove(guess_word)

        self.end_time = time.time()
        return solution_path

    def get_stats(self):
        """
        Return performance statistics.
        """
        return {
            "Time": f"{self.end_time - self.start_time:.4f}s",
            "Expanded Nodes": self.expanded_nodes,
            "Guesses": len(self.solution) if hasattr(self, 'solution') else 0
        }