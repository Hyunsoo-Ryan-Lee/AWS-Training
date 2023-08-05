import boto3, os
from dotenv import load_dotenv
import pexpect
import time


load_dotenv()

s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket(os.environ.get('S3_BUCKET_NAME'))

path_ = 'photos/yyyy=2023/mm=08/dd=02/20230802_125429.jpg'
bucket.objects.filter(Prefix=path_).delete()

def upload_image_to_s3(file_path, bucket_name, key):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, key)
    except Exception as e:
        print('Error uploading file:', str(e))
        
        

def execute_sudo_command(command, password):
    child = pexpect.spawn(command)
    i = child.expect([pexpect.TIMEOUT, 'password:'])
    if i == 0:
        raise RuntimeError("Timed out while waiting for the password prompt.")
    else:
        child.sendline(password)
        child.expect(pexpect.EOF)
        return child.before

if __name__ == "__main__":
    command = ["sudo chown ubuntu hyunsoo-files/", "sudo chown :ubuntu hyunsoo-files/"]
    for comm in command:
        child = pexpect.spawn(comm)
        child.sendline("")
        child.expect(pexpect.EOF)
    # password = ""   
    
    # for comm in  command:
    #     time.sleep(1)
    #     output = execute_sudo_command(comm, password)