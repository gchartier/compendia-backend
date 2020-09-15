import cv2
import os

def is_cover_aspect_ratio_valid(img_url):
	img = cv2.imread(img_url)
	dimensions = tuple(img.shape[1::-1]) # gives: (width, height)
	aspect_ratio = dimensions[0] / dimensions[1] # divide w / h
	if aspect_ratio < 1:
		return False
	return True


def is_cover_size_valid(img_url, mb_limit):
	image_size = os.path.getsize(img_url)
	if image_size > mb_limit:
		return False
	return True