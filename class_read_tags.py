import piexif

class ReadTags:
    def __init__(self,file_path):
        self.file_path = file_path
        self.data = piexif.load(self.file_path)
        self.subdata = self.data['0th']
        self.tags = ''
        if bool(self.subdata) and 40094 in self.subdata.keys():

            self.tags = ''.join([chr(i) for i in self.subdata[40094] if i!=0])
            self.tags = self.tags.split(';')

