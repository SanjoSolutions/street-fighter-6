# Street Fighter 6

## Strategy

### HP dynamic

When one is in the HP lead (ones character has more HP than the character of the other player),
one can potentially sit back and play very safe, because one wins the turn on time over.

When ones character has less HP than the character of the other player, then
it makes more sense to do actions which are only safe to some degree because
on time over one loses the round with the current HPs, so trying something
that potentially leads to an HP lead, makes sense.

## Characters

This repository includes work for generating all combos that seem possible based on the model that the scripts use. Only some combos might work in the game because there are some factors like position, which have been covered only a little bit right now.

The script requires data about the moves and about what moves connect for generating the combos.

The moves data can be extracted from the game via training mode with the frame meter on.

The connecting moves data can be extracted to some degree from the combo trials. The script generate_connecting_moves.py also offers a way to generate a list based on the moves data.

The scripts have been written with [Python](https://www.python.org/).

### Guile

[https://docs.google.com/spreadsheets/d/1_s_O958bg_4ZyOOxq_fX-KgQg44fp5B21ltQdZ4t2TQ/edit?usp=sharing]()

### Ryu

[https://docs.google.com/spreadsheets/d/1DFSMj221zP8sIRzEX7HiMsM7dGdJweVsqILZt6hfyjs/edit?usp=sharing]()

The data for moves is currently missing.

### Other

Other characters can be added. Steps:

* Create a directory for the character.
* Create the files moves.csv and connecting_moves.csv with its contents. I have created the contents with Google Spreadsheet and have exported it as CSV. You can check out the [Guile spreadsheet](https://docs.google.com/spreadsheets/d/1_s_O958bg_4ZyOOxq_fX-KgQg44fp5B21ltQdZ4t2TQ/edit?usp=sharing) to see how that can look.

## Scripts

### Generating the graph

```sh
cd <directory of this repository>
python generate_graph.py
```

The output files are in the directory of the character.

### Generating combos

```sh
cd <directory of this repository>
python generate_combos.py
```

The output files are in the directory of the character.

### Generating connecting moves

```sh
cd <directory of this repository>
python generate_connecting_moves.py
```

The output files are in the directory of the character.
