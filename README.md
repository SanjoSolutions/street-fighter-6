# Street Fighter 6

**Contents:**

* [A graph](ryu.svg) with which was attempted to show which moves can be comboed into which moves.
  The data is based on the combo trials.
  There are potentially more connections.
  A Google spreadsheet with the data can be found [here](https://docs.google.com/spreadsheets/d/1DFSMj221zP8sIRzEX7HiMsM7dGdJweVsqILZt6hfyjs/edit?usp=sharing).
  This graph includes connections after "Cancel Drive Rush" which seem not possible.

## Learning

### Learning combos

It seems that learning what moves can be connected is a flexible approach
for combining moves.

## Generating the graph

```sh
cd <directory of this repository>
python generate_graph.py
```
