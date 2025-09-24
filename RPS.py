import random

class Player:
    def __init__(self):
        self.opponent_history = []
        self.self_history = []

    def __call__(self, prev_play):
        return self.play(prev_play)

    def play(self, prev_play):
        if prev_play != "":
            self.opponent_history.append(prev_play)

        # Default move
        guess = "R"

        # Keep track of our own history
        if len(self.self_history) < len(self.opponent_history):
            self.self_history.append(guess)

        # --- Strategy for Quincy (cycle bot) ---
        if len(self.opponent_history) > 0:
            idx = len(self.opponent_history) % 5
            next_move = ["P", "P", "S", "R", "R"][idx]
            guess = {"R": "P", "P": "S", "S": "R"}[next_move]

        # --- Strategy for Kris ---
        if len(self.self_history) > 0:
            last_self = self.self_history[-1]
            beat_kris = {"R": "S", "P": "R", "S": "P"}
            guess = beat_kris[last_self]

        # --- Strategy for Mrugesh (frequency bot) ---
        if len(self.opponent_history) >= 5:
            freq = {"R": 0, "P": 0, "S": 0}
            for move in self.opponent_history:
                freq[move] += 1
            most_common = max(freq, key=freq.get)
            guess = {"R": "P", "P": "S", "S": "R"}[most_common]

        # --- Strategy for Abbey (predicts based on our last 2 moves) ---
        if len(self.self_history) >= 2:
            last_two = "".join(self.self_history[-2:])
            outcomes = {}
            for i in range(len(self.self_history) - 2):
                seq = "".join(self.self_history[i:i+2])
                if seq == last_two:
                    next_move = self.opponent_history[i+2]
                    outcomes[next_move] = outcomes.get(next_move, 0) + 1
            if outcomes:
                predicted = max(outcomes, key=outcomes.get)
                guess = {"R": "P", "P": "S", "S": "R"}[predicted]

        # Save our move
        if len(self.self_history) == len(self.opponent_history) and len(self.self_history) > 0:
            self.self_history[-1] = guess
        else:
            self.self_history.append(guess)

        return guess

player = Player()
