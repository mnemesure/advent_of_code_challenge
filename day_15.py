# Day 15
import copy
import numpy as np

class Path:
	def __init__(self, path_inds,path_sum, max_row,max_col):
		self.path_inds = path_inds # list of coords taken
		self.path_sum=path_sum # current sum
		self.max_row = max_row # max row
		self.max_col = max_col # max col
		self.path_end = self.path_inds[-1] # current end of path

		# if the path is complete
		if self.path_end[0] == max_row and self.path_end[1] == max_col:
			self.completed = True
		else:
			self.completed = False

class PathManager:
	def __init__(self,mat):
		self.sum_list = [] # store sums of completed paths
		self.mat = mat # matrix to traverse through
		self.completed_paths = [] #list of completed path objects
		self.max_row = len(self.mat) - 1 
		self.max_col = len(self.mat[0]) - 1

		# Paths to explore
		self.path_list = [Path(path_inds = [(0,0)], path_sum = 0, 
							   max_row = self.max_row, max_col = self.max_col)]
		self.point_score = {}

	def update_path(self,path,max_row,max_col): # update a single path
		update_list = [(0,1),(1,0),(-1,0),(0,-1)] # look up down left and right
		new_paths = [] # store new paths
		recent_ind = path.path_end # get the current ending point of the path
		for ind, item in enumerate(update_list): # for each direction
			new_ind = (recent_ind[0]+item[0],recent_ind[1]+item[1]) # next step

			if new_ind[0] < 0 or new_ind[0] > max_row or new_ind[1] < 0 or new_ind[1] > max_col: #make sure its in bounds
				continue
			elif new_ind in path.path_inds: # make sure it hasnt been visited
				continue
			else: # if it passes, make a new list with the added path
				new_path = copy.deepcopy(path.path_inds)
				new_path.append(new_ind)
				new_paths.append(new_path)

		return new_paths # return the list of new paths

	def update_paths(self):
		all_new_paths = [] # store all new paths given current paths
		valid_new_paths = [] # eventually store valid paths - basically the path at each unique endpoint with 
		# the minimum score

		for ind, path in enumerate(self.path_list): # loop through path list
			next_steps = self.update_path(path, self.max_row,self.max_col) # get next steps
			for ind, step in enumerate(next_steps): # loop through next steps
				val_list = [self.mat[(i[0],i[1])] for i in step[1:]]

				# make new path
				new_path = Path(step,sum(val_list),self.max_row,self.max_col)

				# if completed
				if new_path.completed: 
					self.completed_paths.append(new_path)
					self.sum_list.append(new_path.path_sum)
				# else store new path
				else:
					all_new_paths.append(new_path)

		# get the current endpoints
		end_points = [p.path_end for p in all_new_paths]
		# unique endpoints
		unique_endpoints = set(end_points)
		for item in unique_endpoints:
			sums = [] # all total scores for paths at this endpoint
			for ind, idx in enumerate(end_points):
				if item == idx:
					sums.append(all_new_paths[ind].path_sum)

			# First optimization, if an endpoint has been visited
			# If this endpoint has been reached before, make sure that 
			# at least one path at this endpoint beats the minimum
			# of a previous path reaching this endpoint

			if item in self.point_score.keys():
				if min(sums) > self.point_score[item]:
					continue

			# Find the path at this endpoint with the minimum score
			found = False
			for ind, idx in enumerate(end_points):
				if item == idx and all_new_paths[ind].path_sum == min(sums) and not found:
					valid_new_paths.append(all_new_paths[ind])
					self.point_score[idx] = min(sums)
					found=True
		
		#new paths to search
		self.path_list = valid_new_paths

def read_data(file):
	data15 = [] # Store measurements
	with open(file) as f:
	    for i in f.readlines():
	        data15.append(i.split("\n")[0])
	
	data = np.zeros((len(data15), len(data15[0])))
	for row_ind, i in enumerate(data15):
		for col_ind, j in enumerate(i):
			data[row_ind,col_ind] = int(j)

	return(data)


def p1(data):
	path_manager = PathManager(my_data)
	while path_manager.path_list != []:
		path_manager.update_paths()
		print(len(path_manager.path_list))

	return min(path_manager.sum_list)


def p2(data):
	data_list = [data]

	# Build rows
	for i in range(1,6):
		new_data = data_list[-1] + 1
		new_data = new_data % 10
		for row_ind, datapoint in enumerate(new_data):
			for col_ind, j in enumerate(datapoint):
				if j == 0:
					new_data[row_ind,col_ind] = 1
					
		data_list.append(new_data)

	big_data = np.hstack((data,data_list[1],data_list[2],data_list[3],data_list[4])) 
	data_list_big = [big_data]

	# build cols
	for i in range(1,6):
		new_data = data_list_big[-1] + 1
		new_data = new_data % 10
		for row_ind, datapoint in enumerate(new_data):
			for col_ind, j in enumerate(datapoint):
				if j == 0:
					new_data[row_ind,col_ind] = 1
					
		data_list_big.append(new_data)
	big_data = np.vstack((big_data,data_list_big[1],data_list_big[2],data_list_big[3],data_list_big[4]))
	path_manager = PathManager(big_data)
	
	while path_manager.path_list != []:
		path_manager.update_paths()
		print(len(path_manager.path_list))

	return min(path_manager.sum_list)


if __name__ == "__main__":
	
	my_data = read_data('day_15_data.txt')
	print(p1(my_data))
	print(p2(my_data))

	
	
	

