import boto3, os


def partition_path(key_path, date_value, file_name):
    _path = f"{key_path}/yyyy={date_value[:4]}/mm={date_value[4:6]}/dd={date_value[6:]}/{file_name}"
    return _path

def upload_image_to_s3(file_path, bucket_name, key):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, key)
    except Exception as e:
        print('Error uploading file:', str(e))

# def delete_image_at_s3(s3, bucket_name, key):
#     try:
#         bucket_name.objects.filter(Prefix=key).delete()
#     except Exception as e:
#         print('Error uploading file:', str(e))
        
def get_size(start_path):
    total_size = 0
    fin = ''
    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:            
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    if total_size == 0:
        return 'Directory is empty'
    size_suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    size_suffix_index = 0
    while total_size > 1024 and size_suffix_index < len(size_suffixes) - 1:
        total_size /= 1024
        size_suffix_index += 1
    return '{:.2f} {}'.format(total_size, size_suffixes[size_suffix_index])