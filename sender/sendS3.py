from datetime import date, datetime, timedelta
from log.setup import setup_log
import boto3
import constants as cons
import os
import zipfile

class SendS3:
    def __init__(self, awsconfig):
        self.logger = setup_log()
        self.client = boto3.client('s3', awsconfig['region'])
        self.buckets = self.client.list_buckets()['Buckets']
        self.bucket = awsconfig["bucket"]
        self.s3 = boto3.resource('s3')

    def bucketExists(self):
       return not self.s3.Bucket(self.bucket).creation_date is None 

    def send_folder(self, folder):
        self.logger.info(cons.STARTING_SEND_FILES)
        parentPath = os.getcwd()
        if(folder[len(folder)-1] == '/'):
            folder = folder[:-1] 
        folderName = folder.split("/")[-1]
        zipName = folderName + ".zip"
        ## defined actual data and last backup data. 
        dateLastBackup = self.getLastBackup()
        dateCurrentBackup = date.today().strftime("%Y-%m-%d")

        folderS3 = dateLastBackup + '_to_' + dateCurrentBackup + "/" + zipName
        
        try:
            zipf = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
            self.zipdir(parentPath + folder, zipf)
            zipf.close()
            
            if(self.bucketExists()):
                response = self.client.upload_file(zipName, self.bucket, folderS3)
                os.remove(zipName)
                self.logger.info('backup:{}'.format(dateCurrentBackup))
            else: 
                self.logger.error("Unsend folder - Bucket {} doesn't existis".format(self.bucket))
        except Exception as e:
            self.logger.error(cons.ERROR_SEND_ZIP.format(e.__class__))

        self.logger.info("Finishing data send to s3 bucket.")

    def getLastBackup(self): 
        infile = os.getcwd() + '/app.log'
        backups = []
        with open(infile) as f:
            f = f.readlines()

        for line in f:
            if 'backup' in line: 
                backups.append(line)

        return backups[-1].split('backup:')[-1].rstrip('\n')

    def zipdir(self, path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path, '..')))