#re"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    y = False
    sum_outcomes = 0
    for each_roll in range(num_rolls):
        x = dice()
        if x == 1:
            y = True
        else:
            sum_outcomes = x + sum_outcomes
    if not y: #if y is false; if x is NOT 1
        return sum_outcomes
    else:
        return 1



#problem 2
def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.s
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    opponent_score = str(opponent_score)
    if len(opponent_score) == 1:
        opponent_score = '0' + opponent_score
    first_pos = opponent_score[0]
    second_pos = opponent_score[1]
    int_first_pos = int(first_pos)
    int_sec_pos = int(second_pos)

    if num_rolls == 0:
        my_score = 1 + abs(int_sec_pos - int_first_pos)
    else:
        my_score = roll_dice(num_rolls,dice)
    return my_score #returns the number of points scored for a single turn

#problem 3
def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    sum_score = score + opponent_score
    if sum_score % 7 == 0:
        return four_sided
    else:
        return six_sided



def bid_for_start(bid0, bid1, goal=GOAL_SCORE):
    """Given the bids BID0 and BID1 of each player, returns three values:

    - the starting score of player 0
    - the starting score of player 1
    - the number of the player who rolls first (0 or 1)
    """
    assert bid0 >= 0 and bid1 >= 0, "Bids should be non-negative!"
    assert type(bid0) == int and type(bid1) == int, "Bids should be integers!"

    # The buggy code is below:
    if bid0 == bid1: #if both bids are equal
        return goal, goal, 1
    if bid0 == bid1 + 5: #if 0 is less than 1
        return 10, 0, 0
    if bid1 == bid0 + 5: #if 1 is greater than 0
        return 0, 10, 1
    #Otherwise, the player with the higher bid rolls first.
    # Each player starts with a number of points equal to her/his opponent's bid.
    # For example, if player 0 bids 3 and player 1 bids 4,player 1 would roll first
    # starting with 3 points and player 0 would start with 4 points.
    if bid1 > bid0:
        return bid1, bid0, 1
    else:
        return bid1, bid0, 0

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who
i = 0
def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    #score0, score1, who = bid_for_start(score0, score1, goal)
    #print(score0, score1, who)

    def score_is_double_other(s1,s2):
        return s1 == 2*s2 or s2 == 2*s1
    while score0 < goal and score1 < goal:
        if who == 0:
            player_score = score0
            opponent_score = score1
            player_strategy = strategy0
        else:
            player_score = score1
            opponent_score = score0
            player_strategy = strategy1
        num_rolls = player_strategy(player_score,opponent_score) #strategy function is defined in test cases
        dice = select_dice(player_score,opponent_score)
        #

        # print(dice)
        turn_score = take_turn(num_rolls, opponent_score, dice)
        if who == 0:
            score0 += turn_score
        else:
            score1 += turn_score
        if score_is_double_other(score0, score1):
            score1, score0 = score0, score1
        who = other(who)    #flip flops back to other player
        #print("Player {0} just took his turn, getting a score of {1}.".format(1 - who, turn_score))
        #print("Current Scores {0} {1}".format( score0, score1))
    return (score0, score1)  # You may want to change this line.
def always(n):
    return always_roll(n)

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy
# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    def printer(*args):
        i, total = 0, 0
        while i < num_samples:
            func_call = fn(*args)
            total = total + func_call
            i = i + 1
        average = total / num_samples
        return average
    return printer

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Assume that dice always
    return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    current_pos = 1
    current_max = 0
    for each_roll in range(1,11):
        roller = make_averaged(roll_dice,1000)
        a_roll = roller(each_roll,dice)
        if a_roll > current_max:
            current_max = a_roll
            current_pos = each_roll
    return current_pos

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    opponent_score = str(opponent_score)
    if len(opponent_score) == 1:
        opponent_score = '0' + opponent_score
    first_pos = opponent_score[0]
    second_pos = opponent_score[1]
    int_first_pos = int(first_pos)
    int_sec_pos = int(second_pos)
    my_score = 1 + abs(int_sec_pos - int_first_pos)

    if my_score >= margin:
        return 0
    else:
        return num_rolls

def parse_opp_score(opp):

    s = str(opp)
    if opp < 10:
        s = '0' + s
    return s

def roll_zero_score(score_s):

    return 1 + abs(int(score_s[0]) - int(score_s[1]))

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    free_bacon_score = roll_zero_score(parse_opp_score(opponent_score))

    def good_swine_swap(score,opponent_score):
        return opponent_score == 2*score #return true or false

    def bad_swine_swap(score, opponent_score):
        return opponent_score * 2 == score

    if good_swine_swap(score + free_bacon_score, opponent_score): #if it's true that opponent score is twice my score
        return 0
    elif bad_swine_swap(score + free_bacon_score, opponent_score):
        return num_rolls
    elif free_bacon_score >= margin:
        return 0
    else:
        return num_rolls

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    "*** YOUR CODE HERE ***"
    return 5 # Replace this statement


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
