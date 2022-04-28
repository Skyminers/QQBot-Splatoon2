import os
import json


class JsonStruct:
    def __init__(self, filename):
        self.path = os.path.join('.', 'staticData', filename + '.json')
        if not os.path.exists(self.path):
            tmp = open(self.path, 'w')
            tmp.write('{}')
            tmp.close()

    def readFile(self):
        f = open(self.path, 'r')
        content = f.read()
        f.close()
        return json.loads(content)

    # Do not call any function after save
    def save(self, content):
        f = open(self.path, 'w')
        content = json.dumps(content)
        f.write(content)
        f.close()
