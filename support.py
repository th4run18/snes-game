from setting import * 
from os import walk #allows iteration of directories and files
from os.path import join

def import_image(*path, alpha = True, format = 'png'): #*path builds a full file path
	full_path = join(*path) + f'.{format}' # joins path and appends .png 
	return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
	# load the image using pygame

def import_folder(*path):
	frames = [] # importing all the images into a list
	for folder_path, subfolders, image_names in walk(join(*path)):
		for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
			# sorts images numerically to be able to animated 
			full_path = join(folder_path, image_name)
			frames.append(pygame.image.load(full_path).convert_alpha())
	return frames  # returns the list of images
	# Loading a folder of animation.

def import_folder_dict(*path):
	frame_dict = {} # storing the images in a dictionary
	for folder_path, _, image_names in walk(join(*path)): # looping through all images
		for image_name in image_names:
			full_path = join(folder_path, image_name)
			surface = pygame.image.load(full_path).convert_alpha()
			frame_dict[image_name.split('.')[0]] = surface
	return frame_dict #returning the dict of named imgs
	#allows me to access the images directly if needed

def import_sub_folders(*path):
	frame_dict = {} #storing images that are stored in subfolders
	for _, sub_folders, __ in walk(join(*path)): 
		if sub_folders:
			for sub_folder in sub_folders:
				frame_dict[sub_folder] = import_folder(*path, sub_folder)
				#import_folder to load all the avaliable frames
	return frame_dict # returns a dictionary to animate from subfolder