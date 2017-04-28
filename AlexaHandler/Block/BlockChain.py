from __future__ import print_function

# import here for easier import in consumers
#from .BaseBlock import BaseBlock
#from .MessageBlock import MessageBlock
#from .ImageBlock import ImageBlock
import sys
import os
import pickle
from django.conf import settings

class BlockChain:

    def __init__(self, name="block_chain", session=""):
        self.name = name
        self.session = session
        # List with Block instances
        self.BlockList = []
        # TODO: implement List with Block indices from List
        self.ConnectionList = []
        # varList as a list of lists
        self.varList = []

        # inital save
        self.Chain_pickle()

    def getName(self):
        return self.name

    def addBlock(self, Block):
        self.BlockList.append(Block)
        # TODO: check IDs...
        new_vars = [var for var in Block.vars]
        self.varList.append(new_vars)

    def getBlock(self, index):
        return self.BlockList[index]

    def getBlockList(self):
        return self.BlockList

    def getBlockListLength(self):
        return len(self.BlockList)

    def delBlockByIndex(self, index):
        if index < len(self.BlockList):
            del self.BlockList[index]
            # check if list is really emptying
            self.ConnectionList = [entry if index not in entry else [] for entry in self.ConnectionList]
            del self.varList[index]
            # TODO reindexing UI side
        else:
            print("Couldn't delete! index is not in BlockChain", file=sys.stderr)

    def delBlockByElement(self, Block):
        if Block in self.BlockList:
            id = self.BlockList.index(Block)
            self.BlockList.remove(Block)
            self.ConnectionList = [entry if self.BlockList.index(Block) not in entry else [] for entry in self.ConnectionList]
            del self.varList[id]
        else:
            print("Couldn't delete! Block is not in BlockChain", file=sys.stderr)

    def getBlockId(self, Block):
        return self.BlockList.index(Block)

    def delBlocksAll(self):

        for block in self.BlockList:
            block.delBlock()

        self.BlockList = []
        self.ConnectionList = []
        self.varList = []
        print("Blockchain emptied")
        self.Chain_pickle()

    def addConnectionByElement(self, Block1, Block2):
        self.ConnectionList.append([self.BlockList.index(Block1), self.BlockList.index(Block2)])

    def addConnectionById(self, index1, index2):
        self.ConnectionList.append([index1, index2])

    def addVarToBlock(self, num, var):
        self.varList[num].append(var)

    def getVarsForBlock(self, num):
        return self.varList[num]

    def setVarsForBlock(self, num, vars):
        if type(vars) != list:
            raise "vars must be list"
        else:
            self.varList[num] = vars

    def Chain_pickle(self):
        path = settings.CACHE_DIR + "/" + self.session
        # checking if dir already exists
        if not os.path.exists(path):
            os.makedirs(path)
        file = path + "/" + self.name + ".p"
        pickle.dump(self, open(file, "wb"))
        print("pickling", self)

    def __str__(self):
        msg = "BlockChain: " + self.name + ": Blocklist: " + str(len(self.BlockList)) + " Connections: " + str(len(self.ConnectionList)) + " Vars: " + str(sum(len(li) for li in self.varList))
        return msg