class Ingredient():
	def __init__(self,name,amount,amountType):
		self.name = name
		self.amount = amount
		self.amountType = amountType
class Description():
	def __init__(self,description):
		self.description = description
class Author():
	def __init__(self,name,institute):
		self.name = name
		self.institute = institute
class Metadata():
	def	__init__(self,ingredients,description,authors):
		self.ingredients = ingredients
		self.description = description
		self.authors = authors
class Project():
	def __init__(self,name,description,metadata):
		self.name = name
		self.description = description
		self.metadata = metadata

