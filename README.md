# GenerateAdjacency
generate adjacency for given graph

**Why this?**

I found it hard to generate adjacency matrix for a large graph. When I try to make it, there comes a lot of problems such as Time Cost, Space Cost and File Too Large. After working of 4 or 5 days, there comes this job.

**Good?**

For input of graph with more than 300,000 nodes, this code could finish generating adjacency by cost within 90 minites, whereas my original code needs about 40+ hours to finish. And of cource, I run this on high-efficiency server.

I use 20 processes and about 150Gb memory. And get adjacency file of 10Gb.

There seems no space for modification in my view at present.

**Input**: edges of a graph in a file. Like

1 2

2 5

...

23432 23222

**Output**: adjacency number, which is sum of pow(2,x), where x is the index of connected node.

For example, we got such edges,

1 2

1 3

The indices of nodes 1, 2, 3 are 0, 1, 2.

Then the adjacency number of 1 is "pow(2,1) + pow(2,2) = 5".

**Why Adjacency Number?**

The file for 0/1 adjacency relationship is really huge, which can be more than tens of Gb. But in decimal pattern, the file can be less than half size.

**More Explaination?**

Send me e-mail please.
