"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime
import math


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    count = 0
    for prg in paragraphs:
        if select(prg):
            if count == k:
                return prg
            else:
                count += 1
    return ""
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), "topics should be lowercase."
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"

    def contain_topic(paragragh):
        tmp = lower(remove_punctuation(paragragh))
        check_paragraph = split(tmp)
        for key_words in topic:
            if key_words in check_paragraph:
                return True
        return False

    return contain_topic
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    correctness, position, type_length, check_length = (
        0,
        0,
        len(typed_words),
        min(len(typed_words), len(reference_words)),
    )
    if check_length == 0:
        return 0.0
    while position < check_length:
        if typed_words[position] == reference_words[position]:
            correctness += 1
        position += 1
    return correctness / type_length * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, "Elapsed time must be positive"
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    if len(typed) == 0:
        return 0.0
    word_num = len(typed) / 5
    return word_num / elapsed * 60
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if user_word in valid_words:
        return user_word
    else:
        result = user_word
        min_diff = math.inf
        for test_word in valid_words:
            tmp_diff = diff_function(user_word, test_word, limit)
            if tmp_diff < min_diff:
                result = test_word
                min_diff = tmp_diff
        if min_diff > limit:
            result = user_word
        return result

    # END PROBLEM 5


def shifty_shifts(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """

    # BEGIN PROBLEM 6
    def memory(start, goal, limit, count):
        if count > limit:
            return limit + 1
        elif len(start) == 0:
            return len(goal)
        elif len(goal) == 0:
            return len(start)
        else:
            if start[0] == goal[0]:
                return memory(start[1:], goal[1:], limit, count)
            else:
                return memory(start[1:], goal[1:], limit, count + 1) + 1

    return memory(start, goal, limit, 0)
    # END PROBLEM 6


def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.

    NOTE:
    This function seems to be complicated, but if we stuck to the mind of using recursion, it would be clear to think.
    "Stuck to the mind of using recursion" means we are operating objects with similar properties every single turn.
    Then we may find it hard to choose which way to use when doing recursion loops.
    So, why not just operate the first letter every turn? Let's try.

    First:  3 different diffs have been given. So we may think what these numbers should do.In fact, they are the manipulation
    of the first letter of the "start" word.
    Second: According to different operations, we return different recursion expressions.
    Third:  As they are different ways to start with the whole process of the function, we choose the minimum one.
    """

    if len(start) == 0 or len(goal) == 0:  # Fill in the condition
        # BEGIN
        "*** YOUR CODE HERE ***"
        return len(start) + len(goal)
        # END

    elif limit < 0:  # Feel free to remove or add additional cases
        # BEGIN
        "*** YOUR CODE HERE ***"
        return 0
        # END
    elif start[0] == goal[0]:
        return pawssible_patches(start[1:], goal[1:], limit)
    else:
        add_diff = 1 + pawssible_patches(start, goal[1:], limit - 1)
        remove_diff = 1 + pawssible_patches(start[1:], goal, limit - 1)
        substitute_diff = 1 + pawssible_patches(start[1:], goal[1:], limit - 1)
        # BEGIN
        "*** YOUR CODE HERE ***"
        return min(add_diff, remove_diff, substitute_diff)

        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, "Remove this line to use your final_diff function"


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"

    correct, position = 0, 0
    while position < len(typed):
        if typed[position] == prompt[position]:
            correct += 1
        else:
            break
        position += 1
    result = correct / len(prompt)
    current_score = {"id": user_id, "progress": result}
    send(current_score)
    return result
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ""
    for i in range(len(fastest)):
        words = ",".join(fastest[i])
        report += "Player {} typed these fastest: {}\n".format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    for player in range(len(times_per_player)):
        times_per_player[player] = [
            times_per_player[player][i + 1] - times_per_player[player][i]
            for i in range(len(times_per_player[player]) - 1)
        ]
    return game(words, times_per_player)

    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))  # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    result_list = [[] for _ in player_indices]
    for word_index in word_indices:
        fastest_player = -1
        shortest_time = math.inf
        for player in player_indices:
            time_used = time(game, player, word_index)
            if time_used < shortest_time:
                fastest_player = player
                shortest_time = time_used
        word = word_at(game, word_index)
        result_list[fastest_player].append(word)
    return result_list
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), "words should be a list of strings"
    assert all([type(t) == list for t in times]), "times should be a list of lists"
    assert all(
        [isinstance(i, (int, float)) for t in times for i in t]
    ), "times lists should contain numbers"
    assert all(
        [len(t) == len(words) for t in times]
    ), "There should be one word per time."
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])


enable_multiplayer = True  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file("data/sample_paragraphs.txt")
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print("No more paragraphs about", topics, "are available.")
            return
        print("Type the following paragraph and then press enter/return.")
        print("If you only type part of it, you will be scored only on that part.\n")
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print("Goodbye.")
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print("Words per minute:", wpm(typed, elapsed))
        print("Accuracy:        ", accuracy(typed, reference))

        print("\nPress enter/return for the next paragraph or type q to quit.")
        if input().strip() == "q":
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument("topic", help="Topic word", nargs="*")
    parser.add_argument("-t", help="Run typing test", action="store_true")

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
