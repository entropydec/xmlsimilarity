import shelve
import time


class DateBase:
    def __init__(self):
        self.matchedListDb = 'matchedList'

    def storeMatchedList(self, matchedList):
        db = shelve.open(self.matchedListDb, flag='n')
        i = 1
        # print('matchedListDb')
        for key, value in matchedList.items():
            # 这里的index是重写后的classIndex
            matchedNodePair = {'src': key, 'dst': value}
            # print(matchedNodePair)
            db[str(i)] = matchedNodePair
            i += 1
        db.close()

    def readDb(self):
        db = shelve.open(self.matchedListDb)
        newList = []
        # print('readDb')
        for key, value in db.items():
            newList.append(value)
            # print(value)
        db.close()
        return newList
