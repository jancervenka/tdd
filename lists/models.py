from django.db import models

# Create your models here.

# inheriting from the Model class gives us save() method etc.
# classes inheriting from models.Model maps to tables in the database
# they have an auto-generated ID attribute (column) serving as the primary key
# other attributes (columns) must be defined. Django offers classes such as 
# models.TextField(), models.IntegerField() for the attributes.
class Item(models.Model):
	text = models.TextField(default = '') # default value for the db