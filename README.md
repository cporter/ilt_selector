# ILT Selector

Chooses ILTs based on the following criteria:

- Do not allow repeats within a four year window
- Make sure qualifying matches can finish on time assuming the following:
  - 5 matches per team
  - 5 minute match times
  - Qualifying matches start at 10:30
  - One hour lunch break
  - Qualifying matches end at 3:30
- Minimize driving distance for the region as a whole

Usage: `python3 ilt-selector.py`

Add seasons to the previous_seasons list once you've played them.
