
'''
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1C of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''


# Team ID:			[ 4078 ]
# Author List:		[ Ashish Chhabra, Mayank Singhal, Neeraj Joshi, Nitin Jayant ]
# Filename:			task_1c.py
# Functions:		computeSum
# 					[ setupModel, imgToDigit, onSideOfPath ]
# Global variables:	None
# 					[ model ]


# Import necessary modules
import cv2
import numpy as np
import os
import sys


#############	You can import other modules here	#############

# Suppress "Using TensorFlow as backend."
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras.models import load_model
sys.stderr = stderr

import requests

# Global Variables
model = None

#################################################################


def computeSum(img_file_path, shortestPath):

	"""
	Purpose:
	---
	the function takes file path of original image and shortest path as argument and returns
	list of digits in image, digits on path and sum of digits on path in the maze image

	Input Arguments:
	---
	`img_file_path` :		[ str ]
		file path of image
	`shortestPath` :		[ list ]
		list of coordinates of shortest path from initial_point to final_point

	Returns:
	---
	`digits_list` :	[ list ]
		list of all digits on image
	`digits_on_path` :	[ list ]
		list of digits adjacent to the path from initial_point to final_point
	`sum_of_digits_on_path` :	[ int ]
		sum of digits on path

	Example call:
	---
	digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

	"""

	digits_list = []
	digits_on_path = []
	sum_of_digits_on_path = 0

	#############  Add your Code here   ###############
		
	if model is None:
		setupModel()

	CELL_SIZE = task_1a.CELL_SIZE
	img = cv2.imread(img_file_path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

	BORDER_SIZE = int(CELL_SIZE/10)

	h, w = thresh.shape
	graph = task_1a.mazeToGraph(thresh)

	for row in range(0, h, CELL_SIZE):
		for col in range(0, w, CELL_SIZE):
			r = int(row/CELL_SIZE)
			c = int(col/CELL_SIZE)
			cell = thresh[row:row+CELL_SIZE, col:col+CELL_SIZE]
			contours, hierarchy = cv2.findContours(cell, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			if len(contours) >= 2:
				num_image = cell[BORDER_SIZE:-BORDER_SIZE, BORDER_SIZE: -BORDER_SIZE]
				num_image = cv2.resize(num_image, (28,28), interpolation=cv2.INTER_CUBIC)
				coordinate = (r, c)
				num = imgToDigit(num_image)
				digits_list.append(num)
				if onSideOfPath(coordinate, shortestPath, graph):
					digits_on_path.append(num)	
					sum_of_digits_on_path += num
	
	###################################################

	return digits_list, digits_on_path, sum_of_digits_on_path


#############	You can add other helper functions here		#############

def setupModel():
	global model

	if not os.path.isfile('final_4078.h5'):
		binary = requests.get('https://www.dropbox.com/s/g1fzsxg6scofvo7/final.h5?dl=1')

		with open('final_4078.h5', 'wb') as f:
			f.write(binary.content)

	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress tensorflow's debugging output
	model = load_model('final_4078.h5')


def imgToDigit(img):
	img = np.reshape((255-img),[1,28,28,1])
	arr = model.predict(img, None)
	result = np.where(arr[0]==1)[0][0]    
	return int(result)

def onSideOfPath(coordinate, shortestPath, graph):
	for pt in shortestPath:
		if coordinate in graph[pt]:
			return True
	
	return False

#########################################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling computeSum
# 					function, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1c_images' folder or not

if __name__ != '__main__':
	
	curr_dir_path = os.getcwd()

	# Importing task_1a and image_enhancer script
	try:

		task_1a_dir_path = curr_dir_path + '/../../Task 1A/codes'
		sys.path.append(task_1a_dir_path)

		import task_1a
		import image_enhancer

	except Exception as e:

		print('\ntask_1a.py or image_enhancer.pyc file is missing from Task 1A folder !\n')
		exit()

if __name__ == '__main__':
	
	curr_dir_path = os.getcwd()
	img_dir_path = curr_dir_path + '/../task_1c_images/'				# path to directory of 'task_1c_images'
	
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

	# Importing task_1a and image_enhancer script
	try:

		task_1a_dir_path = curr_dir_path + '/../../Task 1A/codes'
		sys.path.append(task_1a_dir_path)

		import task_1a
		import image_enhancer

	except Exception as e:

		print('\n[ERROR] task_1a.py or image_enhancer.pyc file is missing from Task 1A folder !\n')
		exit()

	# modify the task_1a.CELL_SIZE to 40 since maze images
	# in task_1c_images folder have cell size of 40 pixels
	task_1a.CELL_SIZE = 40

	print('\n============================================')

	print('\nFor maze0' + str(file_num) + '.jpg')

	try:
		
		original_binary_img = task_1a.readImage(img_file_path)
		height, width = original_binary_img.shape

	except AttributeError as attr_error:
		
		print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
		exit()

	
	no_cells_height = int(height/task_1a.CELL_SIZE)					# number of cells in height of maze image
	no_cells_width = int(width/task_1a.CELL_SIZE)					# number of cells in width of maze image
	initial_point = (0, 0)											# start point coordinates of maze
	final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

	try:

		shortestPath = task_1a.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

		if len(shortestPath) > 2:

			img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
			
		else:

			print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
			exit()
	
	except TypeError as type_err:
		
		print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
		exit()

	print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))

	digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

	print('\nDigits in the image = ', digits_list)
	print('\nDigits on shortest path in the image = ', digits_on_path)
	print('\nSum of digits on shortest path in the image = ', sum_of_digits_on_path)

	print('\n============================================')

	cv2.imshow('canvas0' + str(file_num), img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	choice = input('\nWant to run your script on all maze images ? ==>> "y" or "n": ')

	if choice == 'y':

		file_count = len(os.listdir(img_dir_path))

		for file_num in range(file_count):

			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

			print('\n============================================')

			print('\nFor maze0' + str(file_num) + '.jpg')

			try:
				
				original_binary_img = task_1a.readImage(img_file_path)
				height, width = original_binary_img.shape

			except AttributeError as attr_error:
				
				print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
				exit()

			
			no_cells_height = int(height/task_1a.CELL_SIZE)					# number of cells in height of maze image
			no_cells_width = int(width/task_1a.CELL_SIZE)					# number of cells in width of maze image
			initial_point = (0, 0)											# start point coordinates of maze
			final_point = ((no_cells_height-1),(no_cells_width-1))			# end point coordinates of maze

			try:

				shortestPath = task_1a.solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

				if len(shortestPath) > 2:

					img = image_enhancer.highlightPath(original_binary_img, initial_point, final_point, shortestPath)
					
				else:

					print('\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
					exit()
			
			except TypeError as type_err:
				
				print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
				exit()

			print('\nShortest Path = %s \n\nLength of Path = %d' % (shortestPath, len(shortestPath)))

			digits_list, digits_on_path, sum_of_digits_on_path = computeSum(img_file_path, shortestPath)

			print('\nDigits in the image = ', digits_list)
			print('\nDigits on shortest path in the image = ', digits_on_path)
			print('\nSum of digits on shortest path in the image = ', sum_of_digits_on_path)

			print('\n============================================')

			cv2.imshow('canvas0' + str(file_num), img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

	else:

		print('')


