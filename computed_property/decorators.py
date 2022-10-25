def computed_property(*arguments):

	def decorator(function, *args):
		"""The Property class was gotten in the python
		documentation to speed development"""

		class Property:

			def __init__(self, fget=function, fset=None, fdel=None, doc=None):
				self.fget = fget
				self.fset = fset
				self.fdel = fdel
				if doc is None and fget is not None:
					doc = fget.__doc__
				self.__doc__ = doc
				self._name = ''
				self.cache_el = {'object': {}, 'result': None}

			def has_changed(self, elements=None, obj=None):
				"""This function was built to check if the
				cached element is, in all variables that are
				its dependency, the same, thus returning afterwards
				their cached counterpart"""
				if self.cache_el['result'] is None or self.cache_el[
						'object'] is None:
					return True
				if obj is None:
					return True
				if elements is None:
					return True
				obj_el = obj.__dict__
				for element in elements:
					if self.cache_el['object'] != obj_el[element]:
						return True
				return False

			def __set_name__(self, owner, name):
				self._name = name

			def __get__(self, obj, objtype=None):
				if obj is None:
					return self
				if self.fget is None:
					raise AttributeError(f'unreadable attribute {self._name}')
				# Getting a list of elements that are relevant to this property
				elements = list(
					set(list(vars(obj).keys())).intersection(
						set(list(arguments))))
				# Elements that aren't in the arguments won't be taken into account
				changed = self.has_changed(elements, obj)
				# If changed get data again and redbuild cache
				if changed:
					self.cache_el['object'] = obj.__dict__
					self.cache_el['result'] = self.fget(obj)
				else:
					# otherwise return the cached result
					return self.cache_el['result']
				return self.fget(obj)

			def __set__(self, obj, value):
				if self.fset is None:
					raise AttributeError(f"can't set attribute {self._name}")
				self.cache_el = {'object': {}, 'result': None}
				self.fset(obj, value)

			def __delete__(self, obj):
				if self.fdel is None:
					raise AttributeError(
						f"can't delete attribute {self._name}")
				self.cache_el = {'object': {}, 'result': None}
				self.fdel(obj)

			def getter(self, fget):
				prop = type(self)(fget, self.fset, self.fdel, self.__doc__)
				prop._name = self._name
				return prop

			def setter(self, fset):
				prop = type(self)(self.fget, fset, self.fdel, self.__doc__)
				prop._name = self._name
				return prop

			def deleter(self, fdel):
				prop = type(self)(self.fget, self.fset, fdel, self.__doc__)
				prop._name = self._name
				return prop

		function = Property()
		return function

	return decorator