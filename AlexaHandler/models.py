from django.db import models

# Create your models here.

class Person(models.Model):
	first_name = models.CharField(max_length=30)

	def save_and_file(self, fName, *args, **kwargs):
		super(Person, self).save(*args, **kwargs)
		File.objects.create(person=self, fileName=fName)

	def __str__(self):
		return self.first_name

class File(models.Model):
	person = models.ForeignKey('Person')
	fileName = models.CharField(max_length=100)

	def __str__(self):
		return self.fileName