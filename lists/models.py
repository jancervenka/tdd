from django.db import models

# Create your models here.

# inheriting from the Model class gives us save() method etc.
# classes inheriting from models.Model maps to tables in the database
# they have an auto-generated ID attribute (column) serving as the primary key
# other attributes (columns) must be defined. Django offers classes such as 
# models.TextField(), models.IntegerField() for the attributes.

class List(models.Model):
	pass

class Item(models.Model):
	text = models.TextField(default = '') # default value for the db
	# foreign key to link the items to their lists
	# models.CASCADE = delete all the items when the list 
	# object is deleted from the db
	list = models.ForeignKey(List, models.CASCADE, default = None)

