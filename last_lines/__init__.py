import io
import os

"""
This file builds the MyFileReader class
This class is supposed to read data in a file
in reverse order.
Notice that each iteration gets the next buffer
and if the line hasn't ended, it contines until it does so
"""


class MyFileReader:

	def __init__(self, file_path, buffer_size):
		try:
			fh = open(file_path)
		except IOError as e:
			# File hasn't been found
			print("File not found")
			exit()
		else:
			# Initializing class
			self.file_path = file_path
			self.buffer_size = buffer_size
			# Starting from the start :)
			self.offset = 0
			# We start with no Buffer
			self.buffer = None
			with fh:
				fh.seek(0, os.SEEK_END)
				# Since we haven't iterated the file, the file_size = remaining_size
				self.file_size = self.remaining_size = fh.tell()

	def __iter__(self):
		# Iterate only if there's still file to read
		if self.remaining_size > 0:
			try:
				fh = open(self.file_path)
			except IOError as e:
				# File hasn't been found
				print("File not found")
				exit()
			else:
				with fh:
					# The offset is the minimum value between the file_size
					# and the sum between the buffer and the previous offset
					# If file is bigger than the buffer_size then read all file
					# Otherwise read bits by bits
					self.offset = min(self.file_size, self.offset + self.buffer_size)
					fh.seek(self.file_size - self.offset)
					prev_buffer = None
					if self.buffer:
						prev_buffer = self.buffer
					self.buffer = fh.read(
						min(self.remaining_size, self.buffer_size))
					self.remaining_size -= self.buffer_size
					if prev_buffer:
						if prev_buffer[-1] != '\n':
							# The line wasn't finished, let's iterate until
							# We finish the line, always reading the specific ammount of data
							self.buffer = self.buffer + prev_buffer
							iter(self)
					self.lines = self.buffer.split('\n')
					self.last_line = self.lines[-1]
		return self

	def __next__(self):
		# Hotfix for next()
		if not self.buffer:
			self = iter(self)
			if not self.buffer:
				raise StopIteration
		if self.lines:
			# We have lines to read
			self.last_line = to_print = self.lines[-1]
			del self.lines[-1]
			if not self.lines:
				if self.remaining_size > 0:
					self = iter(self)
					self.last_line = to_print = self.lines[-1]
					del self.lines[-1]
			return to_print + '\n'
		else:
			# File is over
			raise StopIteration

# last_lines function only creates and returns iterable of MyFileReader
# Notice that we are using default buffer_size
def last_lines(file_path, buffer_size=io.DEFAULT_BUFFER_SIZE):
	return iter(MyFileReader(file_path=file_path, buffer_size=buffer_size))


lines = last_lines('my_file.txt')
for line in lines:
	print(line, end='')