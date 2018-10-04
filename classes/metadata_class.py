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
	def	__init__(self,ingredients,description,authors)
		self.ingredients = ingredients
		self.description = description
		self.authors = authors
class Project():
	def __init__(self,name,description,metadata):
		self.name = name
		self.description = description
		self.metadata = metadata

class CreateProject():
		def __init__(self,name,description,metadata):
		self.name = name
		self.description = description
		self.metadata = metadata
		ingredient_list = []
		for ingredient in ingredients:
			ingredient = Ingredient(ingredient[0],ingredient[1],ingredient[2])
			ingredient_list.append(ingredient)
		
		description = Description("testing out how a cell x reacts to 2ml mercury over y time")
		
		author_list = []
		for author in authors:
			author = Author(author[0],author[1])
			author_list.append(author)
		
		
		
		metadata = Metadata(ingredient_list,description,author_list)
		project = Project("Cell Mercury Testing","testing what mercury in the cell x will do over time of y month", metadata)
	return project