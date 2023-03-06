# MJS with AFL

## Description / Overview of scenario
AFL running on mjs.

## How to use
- Run `sudo sysctl -w kernel.core_pattern="core"` first! Otherwise, AFL will not work and the victim container crashes!
- Then run `sudo $(which python3.7) main.py [RECORDING TIME]`

## victim:
A docker container running AFL on mjs.

## normal & exploit:
Are dummies that do nothing at all.
