import itertools
import math

locations = {
    'A1':(34.0699098,-118.3268349),
    'A2':(34.05388,-118.4012934),
    'B':(33.8903235,-118.22723),
    'C1':(34.1175529,-118.0643915),
    'C2':(34.1313098,-118.0027286),
    'D':(34.4043856,-118.5727834),
    'PE':(34.121758,-117.7407957),
    'F1':(33.7411605,-117.1397756),
    'F2':(33.7411605,-117.1397756),
    'I':(34.5795153,-118.0710054),
    'O':(33.635395,-117.9462162)
}

def distance(a, b):
    lata, lona = locations[a]
    latb, lonb = locations[b]
    return math.sqrt(math.pow(lata - latb, 2.0) + math.pow(lona - lonb, 2.0))

def biggest_drive():
    longest = 0
    start, finish = None, None
    for a, b in itertools.combinations(locations.keys(), 2):
        d = distance(a, b)
        if d > longest:
            start, finish = a, b
            longest = d

    return longest
