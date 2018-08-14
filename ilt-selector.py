import operator
import math
import itertools
import random
import drive_distance
import pprint
import os
import copy

show_advancement_estimates = os.getenv('SHOW_ADVANCEMENT_ESTIMATES') is not None

random.seed('Rover Ruckus')

INF = math.inf
MAX_PENALTY = drive_distance.biggest_drive()

REPEAT_BARIER = 5

leagues = ['A1', 'A2', 'B', 'C1', 'C2', 'D', 'F1', 'F2', 'PE', 'I', 'V', 'O']

league_sizes = {
    'A1': 14,
    'A2': 16,
    'B':  15,
    'C1': 13,
    'C2': 15,
    'D':  15,
    'PE': 15,
    'F1': 14,
    'F2': 16,
    'I':  14,
    'O':  10,
    'V':   7
}

host_names = {
    'B': 'Compton',
    'C2': 'Monrovia',
    'F1': 'Perris',
    'F2': 'Perris',
    'I': 'Palmdale',
    'PE': 'Diamond Ranch'
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
althosts = ['C2', 'I'] # hosts for the one tournament at which the "host" team does not play
locations = ['C2', 'F1', 'F2', 'I', 'I', 'C2']

class ILT(object):
    def __init__(self, host, teams):
        self.host = host
        self.teams = list(teams)

    def pushTeam(self, t):
        self.teams.append(t)

    def popTeam(self):
        self.teams.pop()

    def __repr__(self):
        return '%s (at %s, %d teams)' % (', '.join(self.teams),
                                         host_names.get(self.host, self.host),
                                         sum(league_sizes[x] for x in self.teams))

def makeILT(host, *teams):
    return ILT(host, list(teams))

# Discourage repeats of the previous years
previous_seasons = [
    # Relic Recover
    [makeILT('I', 'A1', 'I'),
     makeILT('I', 'A2', 'D'),
     makeILT('C2', 'B', 'C2'),
     makeILT('F1', 'C1', 'F1', 'O'),
     makeILT('F2', 'F2', 'PE')],
    # Velocity Vortex
    [makeILT('F1', 'A1', 'A2'),
     makeILT('F2', 'F1', 'F2'),
     makeILT('C2', 'C1', 'C2'),
     makeILT('I', 'D', 'I'),
     makeILT('PE', 'B', 'PE')],
    # Res-Q
    # PE and A1 both have their last league meet on the same weekend as the
    # Perris ILT's this year. Throw in a ghost ILT to make sure they don't
    # get scheduled there during Rover Ruckus.
    [makeILT('F2', 'F1', 'F2', 'PE', 'A1')]
]

def allpairs(xs):
    for x in itertools.combinations(xs, 2):
        yield tuple(sorted(x))

def generate_pairings():
    all_pairs = list(allpairs(leagues))

    weight = {}
    for host in hosts:
        weight[(host, host)] = 0.0
        weight[(host, 'O')] = drive_distance.distance(host, 'O')
        for nonhost in nonhosts:
            weight[(host, nonhost)] = drive_distance.distance(host, nonhost)
        for otherhost in hosts:
            if otherhost != host:
                # Just in case. This shouldn't happen.
                weight[(host, otherhost)] = INF
                
    disallowed = set()
    # Disallow repeats within 4 years, as that's how long the mode student
    # participates in FTC. So teams that start in middle school and stick
    # around through high school may get a repeat.
    for past, season in enumerate(previous_seasons[:REPEAT_BARIER]):
        for previous in season:
            for pair in allpairs(previous.teams):
                disallowed.add(pair)

    def score(ilt):
        host, teams = ilt.host, ilt.teams
        if any(x in disallowed for x in allpairs(teams)):
            return INF
        if MAX_ILT_SIZE <= sum(league_sizes[x] for x in teams):
            return INF
        return sum(weight[(host, team)] for team in teams)
    
    best = INF
    winner = None
    for nhs in itertools.permutations(nonhosts):
        side_a = hosts + list(nhs[:2])
        side_b = nhs[2:]
        if len(side_a) != len(side_b):
            raise 'WHOA'
        pairs = zip(side_a, side_b)
        # pairs = list(zip(hosts + list(nhs[:1]), nhs[1:]))
        ilts = [ILT(loc, teams) for (loc, teams) in zip(locations, pairs)]
        # print(ilts)
        s = sum(score(ilt) for ilt in ilts)
        if s < best:
            best = s
            winner = copy.deepcopy(ilts)
    return winner

winner = generate_pairings()

oldg = ['Res-Q', 'Velocity Vortex', 'Relic Recovery']
for game, winner in zip(oldg, reversed(previous_seasons)):
    print('%s:' % game)
    for ilt in winner:
        print('\t- %s' % ilt)

for game in ('Rover Ruckus', '2020', '2021', '2022', '2023', '2024', '2025'):
    winner = generate_pairings()
    previous_seasons = [winner] + previous_seasons

    if winner is None:
        print('{game}: No ILTs possible given current rules and leagues'.format(game = game))
        break
    else:
        print('%s:' % game)
        for ilt in winner:
            print('\t- %s' % ilt)
#         for pair in winner:
#             teams = sum(league_sizes[x] for x in pair)
#             num_adv = round(REGIONALS_TEAMS * teams / TOTAL_TEAMS)
#             if show_advancement_estimates:
#                 print('\t- %s (%d teams, %d advance)' % (','.join(str(x) for x in pair), teams, num_adv))
#             else:
#                 print('\t- %s (%d teams)' % (','.join(str(x) for x in pair), teams))
