import operator
import math
import itertools
import random
import drive_distance
import pprint

random.seed('Rover Ruckus')

INF = math.inf
MAX_PENALTY = drive_distance.biggest_drive()

leagues = ['A1', 'A2', 'B', 'C1', 'C2', 'D', 'F1', 'F2', 'PE', 'I'] # Deal with O

league_sizes = {
    'A1': 18, # 15,
    'A2': 16, # 12,
    'B':  13, # 12,
    'C1': 11,
    'C2': 15,
    'D':  15, # 16,
    'PE': 15, # 12, #
    'F1': 14,
    'F2': 10, # 12,
    'I':  14, # 15,
    'O':  9 # + 2
}

REGIONALS_TEAMS = 48
TOTAL_TEAMS = sum(league_sizes.values())

# Assume 5 minute match turnarounds
PER_MATCH_TIME = 300.
# Qualifying matches are scheduled for 10:30 to 3:30 with an hour for lunch
AVAILABLE_MATCH_TIME = 3600 * 4.
# Every team plays 5 matches, 4 teams per match
MAX_ILT_SIZE = AVAILABLE_MATCH_TIME / ((5./4.) * PER_MATCH_TIME)

# ILT Host leagues will never play each other

hosts = ['C2', 'F1', 'F2', 'I']

nonhosts = [l for l in leagues if l not in hosts]

# Discourage repeats of the previous years
previous_seasons = [
    # Relic Recovery
    [('A1', 'I'), ('A2', 'D'), ('B', 'C2'), ('C1', 'F1', 'O'), ('F2', 'PE')],
    # Velocity Vortex
    [('A1', 'A2'), ('C1', 'C2'), ('B', 'PE'), ('F1', 'F2'), ('D', 'I')],
    # PE and A1 both have their last league meet on the same weekend as the
    # Perris ILT's this year. Throw in a ghost ILT to make sure they don't
    # get scheduled there during Rover Ruckus.
    [('F1', 'F2', 'PE', 'A1')]
]

def allpairs(xs):
    for x in itertools.combinations(xs, 2):
        yield tuple(sorted(x))

def generate_pairings():
    all_pairs = list(allpairs(leagues))

    weight = dict((x, drive_distance.distance(*x)) for x in all_pairs)

    disallowed = set()
    # Disallow repeats within 4 years, as that's how long the mode student
    # participates in FTC. So teams that start in middle school and stick
    # around through high school may get a repeat.
    for past, season in enumerate(previous_seasons[:3]):
        for previous in season:
            for pair in allpairs(previous):
                disallowed.add(pair)

    def score(tup):
        if any(x in disallowed for x in allpairs(tup)):
            return INF
        if MAX_ILT_SIZE <= sum(league_sizes[x] for x in tup):
            return INF
        if any(x in hosts for x in tup):
            return sum(weight.get(tuple(sorted(x)), 0.0)
                       for x in itertools.combinations(tup,2))
        else:
            # If it's a no-home-league tournament, use the closer of
            # Monrovia or Palmdale
            return min(sum(weight.get(tuple(sorted(['C2', x])), 0.0) for x in tup),
                       sum(weight.get(tuple(sorted(['I', x])), 0.0) for x in tup))

    combinations = 0
    best = float("inf")
    winner = None
    for nhs in itertools.permutations(nonhosts):
        combinations = 1 + combinations
        pairs = list(zip(list(nhs[:1]) + hosts, nhs[1:]))
        for i in range(len(pairs)):
            ps = list(pairs)
            ps[i] = tuple(ps[i] + tuple('O'))
            s = sum(score(p) for p in ps)
            if s < best:
                best = s
                winner = ps
    print ('Checked %d combinations' % combinations)
    return winner

winner = generate_pairings()

oldg = ['Date Overlap', 'Velocity Vortex', 'Relic Recovery']
for game, winner in zip(oldg, reversed(previous_seasons)):
    print('%s:' % game)
    for pair in winner:
        print('\t- %s (%d teams)' % (','.join(str(x) for x in pair), sum(league_sizes[x] for x in pair)))

for game in ('Rover Ruckus', '2020', '2021', '2022', '2023', '2024', '2025'):
    winner = generate_pairings()
    previous_seasons = [winner] + previous_seasons
    print('%s:' % game)

    for pair in winner:
        teams = sum(league_sizes[x] for x in pair)
        num_adv = round(REGIONALS_TEAMS * teams / TOTAL_TEAMS)
        print('\t- %s (%d teams, %d advance)' % (','.join(str(x) for x in pair), teams, num_adv))
