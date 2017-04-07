from django.db import models
from .Block import BaseBlock

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
    
class SessionFile(models.Model):
    # File available in Session
    Sess = models.ForeignKey('ClientSession')
    # possible FilePath
    filePath = models.FilePathField(path="/home/alexa_server/Desktop/Alexa_server/storage", recursive = True, allow_folders = True)
    
    def __str__(self):
        return self.Sess

class SessionVarFile(models.Model):
    # Session
    Sess = models.ForeignKey('ClientSession', on_delete=models.CASCADE)
    # Variable name for file
    VarName = models.CharField(max_length=1000)
    # associated file
    varFile = models.ForeignKey('SessionFile', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.VarName
    
class SessionVar(models.Model):
    # Session
    Sess = models.ForeignKey('ClientSession', on_delete=models.CASCADE)
    # VariableName
    VarName = models.CharField(max_length=1000)
    # VariableFile
    VarType = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.VarName

class Node(models.Model):
    # belonging to nodeFlow
    Flow = models.ForeignKey('NodeFlow', on_delete=models.CASCADE)
    # Session
    #Sess = models.ForeignKey('ClientSession', on_delete=models.CASCADE, default="help")
    # NodeID
    NodeID = models.CharField(max_length=1000)
    # associated Variables
    # TODO limit choices
    Vars = models.ManyToManyField('SessionVar', blank=True)
    
    def __str__(self):
        return self.NodeID

class NodeFlow(models.Model):
    # Session
    Sess = models.ForeignKey('ClientSession', on_delete=models.CASCADE)
    # FlowID
    FlowID = models.CharField(max_length=1000)
    # Nodes in this flow
    #Nodes = models.ManyToManyField(Node)
    
    def __str__(self):
        return self.FlowID

class BlockChain(models.Model):
    # Session
    Sess = models.ForeignKey('ClientSession', on_delete=models.CASCADE)

    
class ClientSession(models.Model):
    # id is already set by django, but lets get the messageThing
    # will be identical to either room adress or ws_id
    SessID = models.CharField(max_length=100)
    
    def __str__(self):
        return self.SessID

