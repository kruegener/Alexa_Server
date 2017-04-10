from __future__ import print_function

from .BaseBlock import BaseBlock
from .MessageBlock import MessageBlock
import sys
import pickle
class BlockChain:

    def __init__(self, name="block_chain", session=""):
        self.name = name
        self.session = session
        # List with Block instances
        self.BlockList = []
        # List with Block indices from List
        self.ConnectionList = []


        
        # inital save
        self.Chain_pickle()

    def getName(self):
        return self.name

    def addBlock(self, Block):
        self.BlockList.append(Block)

    def getBlock(self, index):
        return self.BlockList[index]

    def getBlockList(self):
        return self.BlockList

    def delBlockById(self, index):
        if index < len(self.BlockList):
            del self.BlockList[index]
            # check if list is really emptying
            self.ConnectionList = [entry if index not in entry else [] for entry in self.ConnectionList]
        else:
            print("Couldn't delete! index is not in BlockChain", file=sys.stderr)

    def delBlockByElement(self, Block):
        if Block in self.BlockList:
            self.BlockList.remove(Block)
            self.ConnectionList = [entry if self.BlockList.index(Block) not in entry else [] for entry in self.ConnectionList]

        else:
            print("Couldn't delete! Block is not in BlockChain", file=sys.stderr)

    def delBlocksAll(self):
        self.BlockList = []
        self.ConnectionList = []
        print("Blockchain empty")

    def addConnectionByElement(self, Block1, Block2):
        self.ConnectionList.append([self.BlockList.index(Block1), self.BlockList.index(Block2)])

    def addConnectionById(self, index1, index2):
        self.ConnectionList.append([index1, index2])

    def Chain_pickle(self):
        # TODO get path from somewhere
        path = "/home/alexa_server/Alexa_Server/cache/" + self.name + ".p"
        pickle.dump(self, open(path, "wb"))
        print("pickling", self)
        #f = open(path, 'wb')
        #pickle.dump(self.__dict__, f, -1)
        #f.close()

    def __str__(self):
        msg = self.name + ": Blocklist: " + str(len(self.BlockList)) + " Connections: " + str(len(self.ConnectionList))
        return msg