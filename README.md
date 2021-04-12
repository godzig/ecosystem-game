# ecosystem-game

[Ecosystem](https://www.geniusgames.org/products/ecosystem) is a game designed by Matt Simpson and released by Genius Games.

This python script runs random simulations of the game for the purposes of:
- uncovering patterns in the best and worst scoring boards
- learning how to write python that isn't completely embarrasing.

[Bazel](https://docs.bazel.build/versions/master/install.html) is required
to run the target:

```
bazel run :ecosystem -- --boards=1000 --players=3 --floor=-10 --output_csv=/tmp/results.csv
```
