import os
import json


class JsonStruct:
    def __init__(self, filename):
        self.path = os.path.join('.', 'staticData', filename + '.json')
        if not os.path.exists(self.path):
            self.clear()

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

    def clear(self):
        f = open(self.path, 'w')
        f.write('{}')
        f.close()

