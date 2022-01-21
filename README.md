# VampiresVsWerewolves
Our Implementation of a MiniMax algorithm with alpha beta pruning in the context of an in-class competition. Our Algorithm finished in first place.

## Requirements

### Go

Install a [Go toolchain](https://go.dev) (version >= 1.11 to support go modules).

### Go Server

All instructions can be found in the following [link](https://github.com/langorou/twilight). \n
All credits should be given to the github linked above.

To be noted that there are some issues/bugs but overall works well for testing. 
The official server is not made public and is, moreover, not available on Mac.

Usage of twilight:

```
  -columns int
    	total number of columns (default 10)
  -humans int
    	quantity of humans group (default 16)
  -map string
    	path to the map to load (or save if randomly generating)
  -monster int
    	quantity of monster in the start case (default 8)
  -rand
    	use a randomly generated map
  -rows int
    	total number of rows (default 10)
```

## Running the Code

### creating the map

Create a random map by running the following code in the twilight folder:

```
go run . -rand
```

### execute the code

Run the code by executing the following line of code:

```
python main.py NAME HOST PORT
```

- PORT should be 5555
- HOST should be localhost
- NAME should be the name of your AI

Please note that 2 AIs should be launched for the server to run so either run you own AI and confront it with ours or run the AI twice.

## Additional Information

## Report

A report describing our code can be found [here](https://github.com/shawn-lab-ml/VampiresVsWerewolves/tree/main/report/ZCSN_report)

The rule book can be found [here](https://github.com/shawn-lab-ml/VampiresVsWerewolves/tree/main/report/ProjectV10.pdf)
