import os, shutil

class Bucket:
    
    def __init__(self, bucketPath, bucketName = 'prueba'):
        self.root = bucketPath
        self.idBucket = bucketName

    def bList(self):
        return os.listdir(self.root)

    def bNew(self, bucketName):
        path = os.path.join(self.root, bucketName)
        os.mkdir(path)

    def bSelect(self, bucketName):
        self.idBucket = bucketName

    def bDelete(self, bucketName):
        path = os.path.join(self.root, bucketName)
        shutil.rmtree(path)

    def fList(self):
        return os.listdir(os.path.join(self.root, self.idBucket))

    def fUpload(self, fileName):
        file = open(os.path.join(self.root, self.idBucket, fileName), "wb")
        return file

    def fDownload(self, fileName):
        path = os.path.join(self.root, self.idBucket, fileName)
        file = open(path, "rb")
        return file

    def fDelete(self, fileName):
        path = path = os.path.join(self.root, self.idBucket, fileName)
        os.remove(path)

    
    

    