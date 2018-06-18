import operator
import math
import itertools
import random
import drive_distance
import pprint

random.seed('Rover Ruckus')

MAX_PENALTY = drive_distance.biggest_drive()

leagues = ['A1', 'A2', 'B', 'C1', 'C2', 'D', 'F1', 'F2', 'PE', 'I'] # Deal with O

# ILT Host leagues will never play each other
HOST_PENALTY = 10.0 * MAX_PENALTY
hosts = ['C2', 'F1', 'F2', 'I']

nonhosts = [l for l in leagues if l not in hosts]

# Discourage repeats of the previous years
previous_seasons = [
    # Relic Recovery
    [('A1', 'I'), ('A2', 'D'), ('B', 'C2'), ('C1', 'F1', 'O'), ('F2', 'PE')],
    # Velocity Vortex
    [('A1', 'A2'), ('C1', 'C2'), ('B', 'PE'), ('F1', 'F2'), ('D', 'I')]
]


def generate_pairings():
    all_pairs = [tuple(sorted(x)) for x in itertools.combinations(leagues, 2)]

    weight = dict((x, drive_distance.distance(*x)) for x in all_pairs)

    for a, b in zip(hosts[::2], hosts[1::2]):
        t = tuple(sorted([a, b]))
        weight[t] = weight.get(t, 0.0) + HOST_PENALTY

    for past, season in enumerate(previous_seasons[:3]):
        for previous in season:
            for pair in itertools.combinations(previous, 2):
                spair = tuple(sorted(pair))
                weight[spair] = float("inf")

    def score(tup):
        return sum(weight.get(tuple(sorted(x)), 0.0)
                   for x in itertools.combinations(tup,2))

    best = float("inf")
    winner = None
    for nhs in itertools.permutations(nonhosts):
        pairs = list(zip(list(nhs[:1]) + hosts, nhs[1:]))
        for i in range(len(pairs)):
            ps = list(pairs)
            ps[i] = tuple(ps[i] + tuple('O'))
            s = sum(score(p) for p in ps)
            if s < best:
                best = s
                winner = ps
    return winner

winner = generate_pairings()

for game in ('Rover Ruckus', 'Kitten Around', 'Ring-It-Up! 2!', 'Get Under It',
             'Cold Shot', 'Pure Chaos', 'Leftover Game Elements', u'Ragnarök'):
    winner = generate_pairings()
    previous_seasons = [winner] + previous_seasons
    print('%s:' % game)
    for pair in winner:
        print('\t- %s' % ','.join(str(x) for x in pair))
