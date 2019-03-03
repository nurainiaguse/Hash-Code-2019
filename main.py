import sys
import random
from copy import deepcopy
from collections import Counter

class Photo(object):
	orientation = ""
	tags = set()
	_id = -1
	# The class "constructor" - It's actually an initializer 
	def __init__(self, orientation, tags, _id):
		self.orientation = orientation
		self.tags = tags
		self._id = _id
	def print_photo(self):
		print(self._id, self.orientation, self.tags)


class Slide(object):
	photo1 = None
	photo2 = None
	tags = set()
	orientation = ""
	value = -1
	def __init__(self, photo1, photo2, tags, orientation):
		self.photo1 = photo1
		self.photo2 = photo2
		self.orientation = orientation
		self.tags = tags
	def print_slide(self):
		if self.photo2 == None:
			print(self.photo1._id, self.orientation, self.tags)
		else:
			print(self.photo1._id, self.photo2._id, self.orientation, self.tags)

class Slideshow(object):
	slides = None
	sequence = None
	score = -1

	def __init__(self, photos_h, photos_v):
		self.slides = []
		self.generate_new_slideshow(photos_h, photos_v)
		self.calc_score()

	def generate_new_slideshow(self, photos_h, photos_v):
		for photo in photos_h:
			slide = Slide(photo, None, photo.tags, photo.orientation)
			self.slides.append(slide)

		fin = len(photos_v)
		if fin%2 != 0:
			fin =- 1
		sequence_v = list(range(0, fin))
		random.shuffle(sequence_v)
		for idx in range(0,fin, 2):
			i = sequence_v[idx]
			iplus = sequence_v[idx+1]
	#         print(i, fin, len(photos_h))
			slide = Slide(photos_v[i], photos_v[iplus], photos_v[i].tags.union(photos_v[iplus].tags), "V")
			self.slides.append(slide)
		self.sequence = list(range(0, len(self.slides)))

	def calc_score(self):
		self.score = 0
		for idx in range(0, len(self.sequence) - 1):
			i = self.sequence[idx]
			iplus = self.sequence[idx+1]
	#         print(sequence, idx, iplus)
			u = self.slides[i].tags.intersection(self.slides[iplus].tags)
			similarTags = len(u)
			diffTags1 = len(self.slides[i].tags - u)
			diffTags2 = len(self.slides[iplus].tags - u)
			self.score += min(similarTags, min(diffTags1, diffTags2))
	
	def random_solver(self):
		max_score = 0
		best_sequence = None
		for r in range(100):
			random.shuffle(self.sequence)
			self.calc_score()
			if self.score > max_score:
				max_score = self.score
				best_sequence = deepcopy(self.sequence)
		self.sequence = best_sequence
		self.score = max_score
	
	def display_slides(self):
		print("Current slideshow:")
		for slide in slides:
			slide.print_slide()

	def write_to_file(self, file):
	    with open(file, 'w') as f:
	        f.write(str(len(self.sequence)) + '\n')
	        for seq in self.sequence:
	            if self.slides[seq].photo2 == None:
	                f.write(str(self.slides[seq].photo1._id) + "\n")
	            else:
	                f.write(str(self.slides[seq].photo1._id) + " " + str(self.slides[seq].photo2._id) + "\n")

def file_parse(file):
	tag_counter = Counter()
	super_tags = set()
	with open(file, 'r') as f:
		numPhotos = int(f.readline().strip())
		photos_h = []
		photos_v = []
		for i in range(numPhotos):
			line = f.readline().strip().split(' ')
			photo = Photo(line[0], set(line[2:]), i)
			if line[0] == "H":
				photos_h.append(photo)
			else:
				photos_v.append(photo)
			tag_counter.update(set(line[2:]))
	return photos_h, photos_v, tag_counter

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: ./main.py <inputfile> <outputfile>")
		exit()

	photos_h, photos_v, tag_count= file_parse(sys.argv[1])
	# display_slides(slides)
	slideshow = Slideshow(photos_h, photos_v)
	slideshow.random_solver()
	slideshow.write_to_file(sys.argv[2])

	print("Score: %d achieved"% slideshow.score)
	print("Output written to %s"% sys.argv[2])


