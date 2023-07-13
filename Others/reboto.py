import boto3

def list_files_and_directories(bucket_name, prefix=''):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')

    files = []
    directories = []

    if 'Contents' in response:
        files = [obj['Key'] for obj in response['Contents']]

    if 'CommonPrefixes' in response:
        directories = [prefix['Prefix'] for prefix in response['CommonPrefixes']]

    for directory in directories:
        sub_files, sub_directories = list_files_and_directories(bucket_name, prefix=directory)
        files.extend(sub_files)
        directories.extend(sub_directories)

    return files, directories


def test_list_files_and_directories(bucket_name):
    files, directories = list_files_and_directories(bucket_name)

    print("Files:")
    for file in files:
        print(file)

    print("Directories:")
    for directory in directories:
        print(directory)


bucket_name = 'awssolarchitect-test'
test_list_files_and_directories(bucket_name)
