# CSCI 3202 - Project Intermediate Report
## Mancala AI Project

### Project Status

As of now, we have the core Mancala game fully implemented and working. The game engine handles all of the rules: stone distribution going counter-clockwise, skipping the opponent's mancala, the capture rule, and end-of-game detection. One thing to note is that per our project specification, we do not grant an extra turn when the last stone lands in a player's own mancala.

We also have a random player implemented that picks a random legal move on each turn. We used this to run 100 games of random vs. random and collected statistics.

### Issues We Ran Into

Early on we ran into a bug in the `collect_remaining()` function. When one player's side was empty and the game ended, the remaining stones on the other side were being added to the wrong player's mancala. This was causing incorrect final scores and messing up our win/loss statistics. Once we tracked it down and swapped the mancala indices, the scores started making sense and all 100 games ran without error.

### 100 Game Random vs. Random Results

We ran 100 games with both players using the random move generator.

**Player 1:**
- Wins: 49 (49%)
- Losses: 47 (47%)
- Ties: 4 (4%)

**Player 2:**
- Wins: 47 (47%)
- Losses: 49 (49%)
- Ties: 4 (4%)

**Average Turns Per Game:** 43.74

### Is There a First Move Advantage?

Based on our results, there is a very slight first move advantage. Player 1 won 49 games compared to Player 2's 47 games, a difference of only 2 games. This is a small enough margin that it could just be due to randomness. With only random players, going first does not seem to provide a meaningful advantage.

### What We Have Left to Complete

- Minimax AI player with adjustable depth
- Alpha-beta pruning AI player
- Running experiments with AI players at different depths (random vs. minimax, random vs. alpha-beta)
- Collecting runtime and performance statistics for the AI players
- Final writeup with full results and analysis
