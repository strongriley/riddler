# http://fivethirtyeight.com/features/should-the-grizzly-bear-eat-the-salmon/
# %matplotlib inline

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import acos, sin, cos, pi, atan2, sqrt, pow
from numpy.random import rand
from numpy import arange, mean, std

TRIALS_COUNT = 100000
MAX_KG_STEP = 0.1
MAX_KG_STOP_INCLUSIVE = 1.0
BAR_WIDTH = MAX_KG_STEP * 0.8


def trial_2hour(max_kg):
    """
    Trial a 2-hour fishing period where the first fish is eaten if
    it is less or equal to max_kg
    """
    kg_eaten = 0
    fish_sizes = rand(2)
    if fish_sizes[0] <= max_kg:
        kg_eaten += fish_sizes[0]
    # Eat the 2nd fish if it's at least as big
    if fish_sizes[1] >= kg_eaten:
        kg_eaten += fish_sizes[1]
    return kg_eaten

def solve_2hour():
    eaten = [] # 1D array in same order as max_kgs
    # Try 0, 0.1 - 1. w/ 0.1 steps to determine best rule.
    max_kgs = arange(0, MAX_KG_STOP_INCLUSIVE + MAX_KG_STEP, MAX_KG_STEP)
    for max_kg in max_kgs:
        max_kg_result = []
        for t in xrange(TRIALS_COUNT):
            max_kg_result.append(trial_2hour(max_kg))
        eaten.append(max_kg_result)

    means = []
    stdevs = []
    for i in xrange(len(max_kgs)):
        mn = mean(eaten[i])
        st = std(eaten[i])
        print "min kg {0:.2f}, mean eaten: {1:.3f}kg".format(max_kgs[i], mn)
        means.append(mn)
        stdevs.append(st)

    # Results of different max kg values
    fig, ax = plt.subplots()
    ax.bar(max_kgs, means, BAR_WIDTH, color='g', yerr=stdevs)
    ax.set_title('Average kg of fish eaten by max weight of first fish')
    fig.set_size_inches(10, 10)
    plt.show()

    # Histogram of salmon eaten when always eat the first one
    fig, ax = plt.subplots()
    ax.hist(eaten[len(max_kgs)-1], bins=20, range=(0, 2))
    ax.set_title('Average kg of fish eaten when always eating first fish')
    plt.show()

    # Histogram when only eating the first if it's less than 0.5 kg
    fig, ax = plt.subplots()
    ax.hist(eaten[5], bins=20, range=(0, 2))
    ax.set_title('Average kg of fish eaten when only eating first fish if no more than 0.5 kg')
    plt.show()

def trial_3hour(first_max_kg, second_max_kg):
    """
    Trial a 3-hour fishing period where the first fish is eaten if
    it meets first_max_kg and try to eat the second fish if it meets
    second_max_kg (assuming at least as large as first fish)
    """
    kg_eaten = 0
    last_eaten = 0
    fish_sizes = rand(3)
    if fish_sizes[0] <= first_max_kg:
        last_eaten = fish_sizes[0]
        kg_eaten += last_eaten
    if fish_sizes[1] >= last_eaten and fish_sizes[1] <= second_max_kg:
        last_eaten = fish_sizes[1]
        kg_eaten += last_eaten
    # Eat the final fish if it's at least as big as previous
    if fish_sizes[2] >= last_eaten:
        kg_eaten += fish_sizes[2]
    return kg_eaten

def solve_3hour():
    first_max_kgs = [] # X
    second_max_kgs = [] # Y
    eaten_mean = [] # Z
    eaten_stdev = [] # other
    max_kgs = arange(0, MAX_KG_STOP_INCLUSIVE + MAX_KG_STEP, MAX_KG_STEP)
    for first_max_kg in max_kgs:
        for second_max_kg in max_kgs:
            # Eliminate scenarios that don't make sense (second_max_kg < first_max_kg)
            #if second_max_kg < first_max_kg:
            #    continue
            first_max_kgs.append(first_max_kg)
            second_max_kgs.append(second_max_kg)

            fish_eaten_trials = []
            for t in xrange(TRIALS_COUNT):
                fish_eaten_trials.append(trial_3hour(first_max_kg, second_max_kg))
            eaten_mean.append(mean(fish_eaten_trials))
            eaten_stdev.append(std(fish_eaten_trials))
            print "first {0:.2f}, second {1:.2f}. mean: {2:.2f}".format(first_max_kg, second_max_kg, mean(fish_eaten_trials))

    # Now graph
    fig = plt.figure()
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(first_max_kgs, second_max_kgs, eaten_mean, c='g', marker='o')
    ax.set_xlabel('1st fish max kgs')
    ax.set_ylabel('2nd fish max kgs')
    ax.set_zlabel('Mean fish eaten')
    ax.set_title('Average kg of Fish Eaten')
    plt.show()

def main():
    solve_2hour()
    solve_3hour()

main()
