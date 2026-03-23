Mancala AI Project Plan
=======================

Goal: Implement and test a Mancala AI that follows the specified classic rules (with the one exception: no extra turn when the last seed lands in own Mancala) and then generate a writeup documenting behavior and results.

1. Confirm game rules & current engine
- Ensure the board model: 6 pits per side, 4 stones per pit initial, 2 mancalas.
- Legal play: player picks non-empty own pit, distribute CCW, skip opponent mancala, include own mancala.
- Capture rule: if last stone lands on own empty pit (and the opposite pit has stones), capture both.
- Game over rule: if either side's 6 pits are empty, move remaining stones from other side into that player's mancala.
- Winner: compare mancala counts.
- Exception: do not grant extra turn even if last stone lands in own mancala.

2. Core code TODOs (no coding yet) for `main.py` / class `Mancala`
A. Fix or confirm existing logic
- Validate current `play()` behavior in all rule branches, including: skip opponent Mancala, correct pit indexing, capture, end-game stone collection, no extra turn.
- Add explicit player-side move validation for both players in `valid_move` (current checks only initial 6 pits, it appears OK).

B. Improve game state representation and utility
- Add methods: `is_terminal()`, `get_legal_moves(player)`, `clone()`, `do_move(player, pit)`.
- Add `evaluate()` for utility function: (my mancala - opponent mancala), with optional improved heuristic.

C. AI players
- Random player (already exists for player 2; generalize for any player).
- Minimax player with depth parameter and terminal cutoff.
- Alpha-beta player with pruning and cutoff.
- Both should output chosen move and optionally profile node counts/time.

D. Game loop + experiments
- 2-player interface mode (human vs AI / AI vs AI).
- Batch mode: run X games with random vs random; random vs minimax depths 2,5; random vs alpha-beta depths 5,10.
- Track win percentages, avg moves, runtime.
- Ensure repeatability by fixing random seed and/or multiple trials.

3. Testing plan
- Unit tests for board operations: distribution, skip mancala, capture, end-of-game sweep.
- Move generation test: correct legal moves for both players per board state.
- Terminal detection test (empty row) and final score collect.
- Race conditions with extra-turn rule disabled.

4. Writeup structure (final deliverable)
- Project overview
- Rule implementation and differences from standard Khan’s Mancala (explicit one-turn exception)
- Engine design: board indexing and move execution
- AI design: utility function, minimax, alpha-beta, depth cutoff, move ordering
- Experiments and results (100 games each scenario + stats)
- Observations: first player advantage, ply effects, comparison minimax vs alpha-beta, runtime scaling.
- Optional: alternative utility function and 2nd experiment for extra credit.

5. Deliverable files
- `main.py` (game engine + AI + experiments)
- `mancala_project_plan.md` (this file)
- `mancala_results.md` (writeup results)
- `mancala_tests.py` (unit tests)

Next steps (to apply when coding starts):
- Implement missing rule cases and test with deterministic seeds.
- Integrate minimax and alpha-beta algorithms adapted for continuation behavior.
- Perform the 100-game experiments and collect data for writeup.

