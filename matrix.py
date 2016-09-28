import numpy as np

def parse_to_matrix(input_file_path, div = '\t', data_type = int):
	input_file = open(input_file_path, 'r')
	matrix = [ map(data_type,line.strip().split('%s' % div)) for line in input_file if line.strip() != "" ]
	input_file.close()
	return np.array(matrix)

def parse_to_vectors(input_file_path, div = '\t', data_type = int):
	input_file = open(input_file_path, 'r')
	matrix = [ map(data_type,line.strip().split('%s' % div)) for line in input_file if line.strip() != "" ]
	input_file.close()
	return np.array(matrix)


def write_matrix_into_file(matrix, output_file_path):
	output = open(output_file_path, 'w')
	size = len(matrix)
	for row_i in range(size):
		vec = matrix[row_i]
		output.write('%s' % ' '.join(str(i) for i in vec))
		output.write('\n')
	output.close()

def write_matrix_into_file(matrix, heads, output_file_path):
	output = open(output_file_path, 'w')
	size = len(matrix)
	for row_i in range(size):
		vec = matrix[row_i]
		head = heads[row_i]
		output.write('%s' % head)
		output.write(' ')
		output.write('%s' % ' '.join(str(i) for i in vec))
		output.write('\n')
	output.close()
