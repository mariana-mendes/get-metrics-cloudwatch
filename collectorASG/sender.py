from datetime import date
import boto3
import tarfile
import os


def bucketExists(s3, bucket):
    return not s3.Bucket(bucket).creation_date is None

def send_files(awsconfig):
    client = boto3.client('s3', awsconfig['region'])
    buckets = client.list_buckets()['Buckets']
    bucket = awsconfig["bucket"]
    s3 = boto3.resource('s3')

    originalDir = os.getcwd()
    dirData = os.getcwd() + "/data"
    for folderName, subfolders, filenames in os.walk(dirData):
        for filename in filenames:
            filePath = os.path.join(folderName, filename)

            if filename.endswith(".csv"):

                fileNameBase = os.path.splitext(filename)[0] + ".tar.gz"
                os.chdir(folderName)

                with tarfile.open(fileNameBase, 'w:gz') as newFile:
                    newFile.add(folderName + "/" + filename,
                                arcname=filename,
                                recursive=False)

                if (bucketExists(s3, bucket)):
                    response = client.upload_file(
                        folderName + "/" + fileNameBase, bucket,
                        "data" + '/{}'.format(fileNameBase))
                os.chdir(originalDir)
