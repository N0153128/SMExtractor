import requests
import sys
import os



class Extractor:

	filename = sys.argv[1]
	name = filename.split(' ', 1)[0]
	img_data = None
	url = None
	safe_img_url = None
	try:
		mode = str(sys.argv[2])
	except IndexError:
		mode = 'hybrid'

	def hybrid_save(self, row):
		try:
			with open(f'{self.name}/{self.safe_img_url}', 'wb') as handler:
				handler.write(self.img_data)
				print(f'saved to {self.name}/{self.safe_img_url}')
		except Exception as e:
			with open(f'edge.txt', 'a') as f:
				row = row.split()[-1]
				f.write(f'{row}\n')
				print('updated the edge file')

	def list_save(self, row):
		with open(f'{self.name}/Links', 'a') as handler:
			row = row.split()[-1]
			handler.write(f'{row}\n')
			print(f'Listed {row}')

	def hybrid_loop(self):
		'''
		This is hybrid loop, it is used to save images into a dedicated directory. If the loop fails to save an image - a link to that file will be
		added to the "edge.txt" file, containing all edge-cases for further debug or manual download.
		'''
		with open(self.filename) as f:
			lines = f.readlines()
			for row in lines:
				if 'https://pp.userapi.com' in row:
					img_url = row.split()[-1]
					self.safe_img_url = img_url.replace('/', '1').replace('.', '0')
					self.img_data = requests.get(img_url).content
					self.hybrid_save(row)
	
	def list_loop(self):
		'''
		This is list loop, it is used to list all media files found in the backup. A link to the image will be added to the "Links.txt" in the backup\'s
		directory.
		'''
		with open(self.filename) as f:
			lines = f.readlines()
			for row in lines:
				if 'https://pp.userapi.com' in row:
					img_url = row.split()[-1]
					self.list_save(row)

	def listed_loop(self):
		'''
		WIP
		'''
		try:
			os.mkdir(f'{self.name}/fetched')
		except FileExistsError:
			pass
		with open(f'{self.name}/Links', 'r') as f:
			lines = f.readlines()
			for row in lines:
				self.img_data = requests.get(row).content
				self.safe_img_url = row.replace('/', '1').replace('.', '0')
				with open(f'{self.name}/fetched/{self.safe_img_url}', 'wb') as handler:
					handler.write(self.img_data)
					print(f'saved {row}')

	def list_listed_combo(self):
		self.list_loop()
		self.listed_loop()





if __name__ == '__main__':
	ext = Extractor()
	try:
		os.mkdir(ext.name)
	except FileExistsError:
		pass

	if ext.mode == 'hybrid':
		ext.hybrid_loop()
	elif ext.mode == 'list':
		ext.list_loop()
	elif ext.mode == 'listed':
		ext.listed_loop()
	elif ext.mode == 'combo':
		ext.list_listed_combo()
