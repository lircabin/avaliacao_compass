from decorators import computed_property

"""This is a file to create computed properties 
using only vanilla python."""


class Circle:

	def __init__(self, radius=1):
		try:
			if int(radius):
				self.radius = radius
		except Exception as e:
			raise "Radius must be an integer"

	@computed_property('radius')
	def diameter(self):
		"""This calculates the diameter based on the radius for the circle"""
		return self.radius*2

	@diameter.setter
	def diameter(self, diameter):
		self.radius = diameter/2

	@diameter.deleter
	def diameter(self):
		self.radius = 0

