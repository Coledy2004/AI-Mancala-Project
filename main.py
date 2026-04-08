import random
from random import randint
import time

random.seed(109)

class Mancala:
    def __init__(self, pits_per_player=6, stones_per_pit = 4):
        """
        The constructor for the Mancala class defines several instance variables:

        pits_per_player: This variable stores the number of pits each player has.
        stones_per_pit: It represents the number of stones each pit contains at the start of any game.
        board: This data structure is responsible for managing the Mancala board.
        current_player: This variable takes the value 1 or 2, as it's a two-player game, indicating which player's turn it is.
        moves: This is a list used to store the moves made by each player. It's structured in the format (current_player, chosen_pit).
        p1_pits_index: A list containing two elements representing the start and end indices of player 1's pits in the board data structure.
        p2_pits_index: Similar to p1_pits_index, it contains the start and end indices for player 2's pits on the board.
        p1_mancala_index and p2_mancala_index: These variables hold the indices of the Mancala pits on the board for players 1 and 2, respectively.
        """
        self.pits_per_player = pits_per_player
        self.board = [stones_per_pit] * ((pits_per_player+1) * 2)  # Initialize each pit with stones_per_pit number of stones 
        self.players = 2
        self.current_player = 1
        self.moves = []
        self.p1_pits_index = [0, self.pits_per_player-1]
        self.p1_mancala_index = self.pits_per_player
        self.p2_pits_index = [self.pits_per_player+1, len(self.board)-1-1]
        self.p2_mancala_index = len(self.board)-1
        
        # Zeroing the Mancala for both players
        self.board[self.p1_mancala_index] = 0
        self.board[self.p2_mancala_index] = 0

    def display_board(self):
        """
        Displays the board in a user-friendly format
        """
        player_1_pits = self.board[self.p1_pits_index[0]: self.p1_pits_index[1]+1]
        player_1_mancala = self.board[self.p1_mancala_index]
        player_2_pits = self.board[self.p2_pits_index[0]: self.p2_pits_index[1]+1]
        player_2_mancala = self.board[self.p2_mancala_index]

        print('P1               P2')
        print('     ____{}____     '.format(player_2_mancala))
        for i in range(self.pits_per_player):
            if i == self.pits_per_player - 1:
                print('{} -> |_{}_|_{}_| <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            else:    
                print('{} -> | {} | {} | <- {}'.format(i+1, player_1_pits[i], 
                        player_2_pits[-(i+1)], self.pits_per_player - i))
            
        print('         {}         '.format(player_1_mancala))
        turn = 'P1' if self.current_player == 1 else 'P2'
        print('Turn: ' + turn)
        
    def valid_move(self, pit):
        """
        Function to check if the pit chosen by the current_player is a valid move.
        """
        pit = pit - 1

        if pit < 0 or pit >= self.pits_per_player:
            return False

        if self.current_player == 1:
            board_index = self.p1_pits_index[0] + pit
        else:
            board_index = self.p2_pits_index[0] + pit

        return self.board[board_index] != 0
        
    def random_move_generator(self, player=None):
        """Choose a random legal move for the given player (or current player by default)."""
        if player is None:
            player = self.current_player

        valid_pits = self.get_legal_moves(player)
        if not valid_pits:
            return None

        choice_index = randint(0, len(valid_pits) - 1)
        return valid_pits[choice_index]
    
    def play(self, pit):
        """
        This function simulates a single move made by a specific player using their selected pit. It primarily performs three tasks:
        1. It checks if the chosen pit is a valid move for the current player. If not, it prints "INVALID MOVE" and takes no action.
        2. It verifies if the game board has already reached a winning state. If so, it prints "GAME OVER" and takes no further action.
        3. After passing the above two checks, it proceeds to distribute the stones according to the specified Mancala rules.

        Finally, the function then switches the current player, allowing the other player to take their turn.
        """

        # Verify if the game board has reached a winning state
        if self.winning_eval():
            print("GAME OVER")
            return self.board
        
        # check if chosen pit is a valid choice for user
        if not self.valid_move(pit):
            print("INVALID MOVE")
            return self.board
        
        original_pit = pit  # 1-based
        pit_index = pit - 1  # 0-based
        player = self.current_player

        if player == 1:
            current_index = self.p1_pits_index[0] + pit_index
        else:
            current_index = self.p2_pits_index[0] + pit_index

        stones = self.board[current_index]
        self.board[current_index] = 0
            
        for _ in range(stones):
            current_index = (current_index + 1) % len(self.board)

            if player == 1 and current_index == self.p2_mancala_index:
                current_index = (current_index + 1) % len(self.board)

            if player == 2 and current_index == self.p1_mancala_index:
                current_index = (current_index + 1) % len(self.board)

            self.board[current_index] += 1
            
        last_index = current_index

        # Capture rule
        if player == 1 and last_index >= self.p1_pits_index[0] and last_index <= self.p1_pits_index[1] and self.board[last_index] == 1:
            opp_index = 12 - last_index
            if self.board[opp_index] > 0:
                self.board[self.p1_mancala_index] += self.board[last_index] + self.board[opp_index]
                self.board[last_index] = 0
                self.board[opp_index] = 0
        elif player == 2 and last_index >= self.p2_pits_index[0] and last_index <= self.p2_pits_index[1] and self.board[last_index] == 1:
            opp_index = 12 - last_index
            if self.board[opp_index] > 0:
                self.board[self.p2_mancala_index] += self.board[last_index] + self.board[opp_index]
                self.board[last_index] = 0
                self.board[opp_index] = 0
            
        self.moves.append((player, original_pit))

        if self.winning_eval():
            self.collect_remaining()
            print("GAME OVER")

        # Switch player (no extra turn as per rules)
        self.current_player = 2 if player == 1 else 1

        return self.board
    
    def winning_eval(self):
        """
        Function to verify if the game board has reached the winning state.
        Hint: If either of the players' pits are all empty, then it is considered a winning state.
        """
        p1_stones = sum(self.board[self.p1_pits_index[0]:self.p1_pits_index[1] + 1])
        p2_stones = sum(self.board[self.p2_pits_index[0]:self.p2_pits_index[1] + 1])
        return p1_stones == 0 or p2_stones == 0

    def collect_remaining(self):
        """
        Collect remaining stones into the mancala of the player who has stones left.
        """
        p1_empty = sum(self.board[self.p1_pits_index[0]:self.p1_pits_index[1] + 1]) == 0
        p2_empty = sum(self.board[self.p2_pits_index[0]:self.p2_pits_index[1] + 1]) == 0
        if p1_empty:
            remaining = sum(self.board[self.p2_pits_index[0]:self.p2_pits_index[1] + 1])
            self.board[self.p2_mancala_index] += remaining
            for i in range(self.p2_pits_index[0], self.p2_pits_index[1] + 1):
                self.board[i] = 0
        elif p2_empty:
            remaining = sum(self.board[self.p1_pits_index[0]:self.p1_pits_index[1] + 1])
            self.board[self.p1_mancala_index] += remaining
            for i in range(self.p1_pits_index[0], self.p1_pits_index[1] + 1):
                self.board[i] = 0

    def is_terminal(self):
        """Return True if the game is over (one side has no pits left with stones)."""
        return self.winning_eval()

    def get_legal_moves(self, player=None):
        """Return list of legal move pit numbers (1-based) for the specified player."""
        if player is None:
            player = self.current_player

        pit_indices = self.p1_pits_index if player == 1 else self.p2_pits_index
        moves = []
        for i in range(self.pits_per_player):
            board_index = pit_indices[0] + i
            if self.board[board_index] > 0:
                moves.append(i + 1)
        return moves

    def clone(self):
        """Deep-copy board state for tree search."""
        clone_game = Mancala(self.pits_per_player)
        clone_game.board = self.board.copy()
        clone_game.current_player = self.current_player
        clone_game.moves = self.moves.copy()
        return clone_game

    def evaluate(self, player=1):
        """Utility function for AI: mancala(player) - mancala(opponent)."""
        my_mancala = self.board[self.p1_mancala_index] if player == 1 else self.board[self.p2_mancala_index]
        opp_mancala = self.board[self.p2_mancala_index] if player == 1 else self.board[self.p1_mancala_index]
        return my_mancala - opp_mancala


# ─────────────────────────────────────────────
#  AI Players
# ─────────────────────────────────────────────

class MinimaxPlayer:
    """
    Minimax AI player with a configurable search depth.

    At each node the algorithm:
      - Returns the heuristic evaluate() score at terminal states or depth 0.
      - For the maximising player it picks the move with the highest score.
      - For the minimising player it picks the move with the lowest score.

    The AI always plays as `ai_player`; the opponent is the other player.
    node_count tracks how many nodes were expanded in the last move call.
    """

    def __init__(self, ai_player=1, depth=5):
        self.ai_player = ai_player
        self.depth = depth
        self.node_count = 0

    def choose_move(self, game):
        """Return the best pit (1-based) for the current player according to minimax."""
        self.node_count = 0
        best_move = None
        best_score = float('-inf')

        for move in game.get_legal_moves():
            child = game.clone()
            child.play(move)
            self.node_count += 1
            score = self._minimax(child, self.depth - 1, is_maximising=False)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, game, depth, is_maximising):
        """Recursive minimax search."""
        self.node_count += 1

        if depth == 0 or game.is_terminal():
            return game.evaluate(self.ai_player)

        legal_moves = game.get_legal_moves()

        if is_maximising:
            best = float('-inf')
            for move in legal_moves:
                child = game.clone()
                child.play(move)
                best = max(best, self._minimax(child, depth - 1, is_maximising=False))
            return best
        else:
            best = float('inf')
            for move in legal_moves:
                child = game.clone()
                child.play(move)
                best = min(best, self._minimax(child, depth - 1, is_maximising=True))
            return best


class AlphaBetaPlayer:
    """
    Alpha-Beta pruning AI player with a configurable search depth.

    Identical to MinimaxPlayer in decision quality but prunes branches that
    cannot affect the final result, significantly reducing node_count.

    alpha: best value the maximiser can guarantee so far (starts at -inf).
    beta:  best value the minimiser can guarantee so far (starts at +inf).
    A branch is pruned when alpha >= beta (the opponent would never allow this
    line to be reached).
    """

    def __init__(self, ai_player=1, depth=5):
        self.ai_player = ai_player
        self.depth = depth
        self.node_count = 0

    def choose_move(self, game):
        """Return the best pit (1-based) for the current player using alpha-beta."""
        self.node_count = 0
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in game.get_legal_moves():
            child = game.clone()
            child.play(move)
            self.node_count += 1
            score = self._alpha_beta(child, self.depth - 1, alpha, beta, is_maximising=False)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)

        return best_move

    def _alpha_beta(self, game, depth, alpha, beta, is_maximising):
        """Recursive alpha-beta search."""
        self.node_count += 1

        if depth == 0 or game.is_terminal():
            return game.evaluate(self.ai_player)

        legal_moves = game.get_legal_moves()

        if is_maximising:
            best = float('-inf')
            for move in legal_moves:
                child = game.clone()
                child.play(move)
                best = max(best, self._alpha_beta(child, depth - 1, alpha, beta, is_maximising=False))
                alpha = max(alpha, best)
                if alpha >= beta:
                    break  # Beta cut-off
            return best
        else:
            best = float('inf')
            for move in legal_moves:
                child = game.clone()
                child.play(move)
                best = min(best, self._alpha_beta(child, depth - 1, alpha, beta, is_maximising=True))
                beta = min(beta, best)
                if alpha >= beta:
                    break  # Alpha cut-off
            return best


# ─────────────────────────────────────────────
#  Helper: run a batch of games between two AI strategies
# ─────────────────────────────────────────────

def run_batch(p1_strategy, p2_strategy, n_games=100, label=""):
    """
    Run n_games between two strategy callables.

    Each strategy callable accepts a Mancala game object and returns a pit (1-based).
    Returns a dict with win/loss/tie counts, average turns, and timing info.
    """
    p1_wins = p2_wins = ties = 0
    total_turns = 0
    total_time = 0.0

    for _ in range(n_games):
        game = Mancala()
        turns = 0
        t_start = time.time()

        while not game.is_terminal():
            if game.current_player == 1:
                move = p1_strategy(game)
            else:
                move = p2_strategy(game)
            game.play(move)
            turns += 1

        total_time += time.time() - t_start
        total_turns += turns

        p1_score = game.board[game.p1_mancala_index]
        p2_score = game.board[game.p2_mancala_index]

        if p1_score > p2_score:
            p1_wins += 1
        elif p2_score > p1_score:
            p2_wins += 1
        else:
            ties += 1

    return {
        "label": label,
        "p1_wins": p1_wins,
        "p2_wins": p2_wins,
        "ties": ties,
        "avg_turns": total_turns / n_games,
        "avg_time_s": total_time / n_games,
    }


def print_batch_results(results):
    r = results
    print(f"  Scenario : {r['label']}")
    print(f"  P1 Wins  : {r['p1_wins']} ({r['p1_wins']}%)")
    print(f"  P2 Wins  : {r['p2_wins']} ({r['p2_wins']}%)")
    print(f"  Ties     : {r['ties']} ({r['ties']}%)")
    print(f"  Avg Turns: {r['avg_turns']:.1f}")
    print(f"  Avg Time : {r['avg_time_s']:.3f}s per game")
    if r['p1_wins'] > r['p2_wins']:
        print(f"  First-move advantage: YES  (P1 won {r['p1_wins'] - r['p2_wins']} more games)")
    elif r['p2_wins'] > r['p1_wins']:
        print(f"  First-move advantage: NO   (P2 won {r['p2_wins'] - r['p1_wins']} more games)")
    else:
        print("  First-move advantage: NO CLEAR ADVANTAGE")
    print()


# ─────────────────────────────────────────────
#  Part 1: Original demo (unchanged)
# ─────────────────────────────────────────────

def main():
    print("=" * 50)
    print("AI vs Random: 100 games")
    print("=" * 50 + "\n")

    ai_player = AlphaBetaPlayer(ai_player=2, depth=5)
    results = run_batch(
        p1_strategy=lambda g: g.random_move_generator(),
        p2_strategy=lambda g: ai_player.choose_move(g),
        n_games=100,
        label="Random (P1) vs Alpha-Beta depth=5 (P2)"
    )

    print_batch_results(results)
    print(f"AI wins (P2): {results['p2_wins']} out of 100 games")


if __name__ == "__main__":
    main()
