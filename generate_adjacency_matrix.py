import numpy as np
import argparse
from matrix import *
from multiprocessing.pool import ThreadPool
from ctypes import c_char_p
import multiprocessing as mp
import sys
import time
import math
import string

def parse_args():
    '''
    Parses arguments.
    '''
    parser = argparse.ArgumentParser(description="Produce adjacency matrix")

    parser.add_argument('--edges', nargs='?', default='net_youtube.txt',
                        help='Input edges')
    parser.add_argument('--undirected', nargs='?', default=True,
                        help='')
    parser.add_argument('--output', nargs='?', default='adjacency_matrix.txt',
                        help='output file path')

    return parser.parse_args()

def get_adj_vec_num_str(i):
	node = nodes[i]
	indexs = (edges[:,0] == node)
	neighbors = edges[indexs,1]
	num = 0
	for neighbor in neighbors:
		num = num + pow_value[alias[neighbor]]
	line = '%d %s\n' % (node,num)
	lines_proxy[i][0:len(line)] = line
	return 0

def get_adj_vec_num_str_undirected(n_i, l_i):
	node = nodes[n_i]
	to_indexs = (edges[:,0] == node)
	from_indexs = (edges[:,1] == node)
	to_neighbors = edges[to_indexs,1]
	from_neighbors = edges[from_indexs,0]
	neighbors = np.unique(np.concatenate((to_neighbors,from_neighbors)))
	num = 0
	for neighbor in neighbors:
		num = num + pow_value[alias[neighbor]]
	line = '%d %s\n' % (node,num)
	lines_proxy[l_i][0:len(line)] = line
	return 0


def initProcessForVec(ori_nodes, ori_edges, ori_size, ori_length, lines):
	global nodes
	global edges
	global alias
	global pow_value
	global size
	global length
	global pow_value
	global lines_proxy
	lines_proxy = lines
	nodes = np.array(ori_nodes)
	edges = np.array(ori_edges).reshape([ori_length, 2])
	size = ori_size
	length = ori_length
	alias = dict(zip(nodes,range(len(nodes))))
	pow_value = [(pow(2,x)) for x in range(size)]

def parse_to_adj_with_decimal(args):

	print "Process begin. Read edges from %s" % args.edges
	sys.stdout.flush()
	start = time.time()
	edges = parse_to_matrix(args.edges, data_type=int)
	print "Finish Reading edges by %s secs." % (time.time() - start)
	sys.stdout.flush()
	
	output = open(args.output,'w')
	output.truncate()
	output.close()

	length = len(edges)
	shared_edges = mp.Array('d',(length * 2))
	edges_buffer = np.frombuffer(shared_edges.get_obj())
	edges_buffer[...] = edges.reshape(length*2,)

	nodes = np.unique(edges)
	size = len(nodes)
	shared_nodes = mp.Array('d',size)
	nodes_buffer = np.frombuffer(shared_nodes.get_obj())
	nodes_buffer[...] = nodes

	part_num = 5
	if size < 10000:
		part_num = 1
	part_len = int(math.ceil(size/float(part_num)))
	line_len = size/3 + 1 + len(str(size))
	lines = [mp.Array('c', line_len) for i in range(part_len)]

	start = time.time()
	print "Init Adjacency Vectors processes ..."
	sys.stdout.flush()
	pool = mp.Pool(processes=20, initializer=initProcessForVec, initargs=(shared_nodes, shared_edges, size, length, lines))#, countor, rate))
	print "Init complete by %s secs." % (time.time() - start)
	sys.stdout.flush()
	print "The whole process is splitted into %d parts." % part_num
	sys.stdout.flush()

	node_index = 0
	for p_i in range(part_num):
		if p_i != 0:
			start = time.time()
			print "Clean lines ..."
			sys.stdout.flush()
			for line in lines:
				line[:] = ['\x00' for i in range(line_len)]
			print "Clean complete by %s secs." % (time.time() - start)
			sys.stdout.flush()

		print "The %d process begins ..." % (p_i + 1)
		sys.stdout.flush()
		start_index = p_i*part_len
		end_index = min(start_index + part_len, size)
		curr_len = end_index - start_index
	
		vec_result = []
		if args.undirected:
			for i in range(curr_len):
				task = pool.apply_async(get_adj_vec_num_str_undirected, args=(node_index + i, i))
				vec_result.append(task) 
		else:
			for i in range(curr_len):
				task = pool.apply_async(get_adj_vec_num_str, args=(node_index + i, i))
				vec_result.append(task) 
	
		count = 0
		bound = curr_len / float(100000)
		print "Begin calculate adjacency ... "
		sys.stdout.flush()
		start = time.time()
		for n_i in range(curr_len):
			if n_i >= count * bound:
				sys.stdout.write("Process reach %.2f%%	\r" % (count/float(1000)))
				sys.stdout.flush()
				count = count + 1
			vec_result[n_i].get()
		print "Finish Computing by %s secs." % (time.time() - start)
		sys.stdout.flush()
	
		print "Begin parsing adjacency string... "
		sys.stdout.flush()
		start = time.time()
		part_lines = []
		for n_i in range(curr_len):
			part_lines.append(''.join(x for x in lines[n_i][:] if x != '\x00'))
		print "Parsing finish by %s secs." % (time.time() - start)
		sys.stdout.flush()
	
		print "Begin writing adjacency ... "
		sys.stdout.flush()
		start = time.time()
		output = open(args.output,'a')
		output.writelines(part_lines)
		output.close()
		print "Writing finish. Written into %s by %s secs." % (args.output, time.time() - start)
		sys.stdout.flush()
	
		node_index  = node_index  + curr_len

	pool.close()
	pool.join()
	
args = parse_args()
parse_to_adj_with_decimal(args)
