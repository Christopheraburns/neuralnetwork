from miniflow import *

#create two new Input classes
x, y, z = Input(), Input(), Input()

f = Add(x, y, z)

feed_dict = {x: 4, y: 5, z: 10}

sorted_nodes = topological_sort(feed_dict)
output = forward_pass(f, sorted_nodes)

print("{} + {} = {} (according to miniflow)".format(feed_dict[x], feed_dict[y], output))