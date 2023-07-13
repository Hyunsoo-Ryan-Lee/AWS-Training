import boto3

bucket_name = "awssolarchitect-test"
prefix = "Athena_Logs/"



def count_files_in_s3(bucket_name, prefix):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    file_names = [obj['Key'].split('/')[-1] for obj in response.get('Contents', [])]
    file_names = [i for i in file_names if i]
    file_count = len(file_names)
    return file_names, file_count


def explore_subdirectories_cnt_file(bucket_name, prefix):
    s3_client = boto3.client('s3')
    
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter='/')
    
    # prefix 내에 있는 디렉토리 이름과 개수
    subdirectory_names = [obj['Prefix'].split('/')[-2] for obj in response.get('CommonPrefixes', [])]
    subdirectory_count = len(subdirectory_names)
    
    # 제일 하위 디렉토리까지 재귀적으로 탐색 후 파일 count
    if subdirectory_count == 0:
        deepest_subfolder = prefix.rstrip('/')
        # print(deepest_subfolder)
        file_names, file_count = count_files_in_s3(bucket_name, deepest_subfolder)
        print([prefix] + file_names)
        # print(f"Files in subfolder '{deepest_subfolder}': {file_count}")
    else:
        file_names = [obj['Key'].split('/')[-1] for obj in response.get('Contents', [])]
        file_names = [i for i in file_names if i]
        print([prefix] + file_names)
    
    for subdirectory_name in subdirectory_names:
        subdirectory_prefix = f"{prefix}{subdirectory_name}/"
        explore_subdirectories_cnt_file(bucket_name, subdirectory_prefix)
    
    return subdirectory_names, subdirectory_count

def list_files_and_directories(bucket_name):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name, Delimiter='/')
    files = []
    directories = []

    if 'Contents' in response:
        files = [obj['Key'] for obj in response['Contents']]
    
    if 'CommonPrefixes' in response:
        directories = [prefix['Prefix'] for prefix in response['CommonPrefixes']]
    print(files+directories)
    for dirs in directories:
        subdirectory_names, subdirectory_count = explore_subdirectories_cnt_file(bucket_name, dirs)


list_files_and_directories(bucket_name)