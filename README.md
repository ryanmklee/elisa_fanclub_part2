# CPSC 410 Software Visualization Project

## Group 17   
Andy Siu  
Cindy Hsu  
Gavin Ham  
Gary Gao   
Ryan Lee   

## Dataset and Project Information
[Download Dataset](http://bit.ly/2ToaBpp)  
[Project Proposal](https://bit.ly/2TjXRjK)

## Purpose

Our goal for this project is given some arbitrary Python function, we should be able to profile that function, visualize
the runtime and then output a graph which shows it's runtime in varying sizes.

We aim to do this through command line so in the end we want to have an arbitrary function and then have our program
visualize the profiled code.

User provides the function, data and input size. We handle the code profiling and visualization.

User (provides function, data, input size) -> Profile code -> Generate graph

## How to Run

To run our project by default we loaded in a KNN over a volcano dataset. Please see above to download the dataset. 

`python perf.py -c [CHART_NAME] [iterations]`  
`CHART_NAME ::= bar, stacked, table, line, area, bubble`  
`iterations ::= number*`

For example you can run the following parameters

`python perf.py -c bar 10 100`  

will profile and generate a bar graph on KNN over 10 and 100 iterations.

There are also optional arguments you can put in

'-r', '--reverse', reverse ordering of profile entries  
-t', '--track', including this flag causes the visualization to only track relevant functions from the first iteration, rather than relevant functions for each iteration