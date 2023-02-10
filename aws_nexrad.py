import os
import boto3
import streamlit as st
# import logging
#
# from dotenv import load_dotenv
# import re
#
# load_dotenv() # to load environments from .env file
#
# aws_s3_client = boto3.client('s3',region_name = 'us-east-1',aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))
#
def get_files_from_nexrad_bucket(dir):
    files_from_nexrad_bucket = []
    s3_client = boto3.client("s3",region_name="us-east-1",
                      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    paginator = s3_client.get_paginator('list_objects_v2')
    nexrad_bucket = paginator.paginate(Bucket = "noaa-nexrad-level2",Prefix = dir) #,PaginationConfig  = {"PageSize":2}
    for count,page in enumerate(nexrad_bucket):
        files = page.get("Contents")
        for file in files:
            files_from_nexrad_bucket.append(file['Key'])
            # print(file['Key'])
            # f = open("output1.txt", "a")?\
            # print(f"{file['Key']}",file = f)
    # print(files_from_nexrad_bucket)
    return  files_from_nexrad_bucket
#
#
# def get_dir_from_filename_nexrad(file_name):
#     ground_station = file_name[0:4]
#     year = file_name[4:8]
#     month = file_name[8:10]
#     day = file_name[10:12]
#     full_file_name = year+"/"+month+"/"+day+"/"+ground_station+"/"+file_name
#     return full_file_name
# def get_meta_data_for_db_population():
#     print("inside")
#     meta_data_for_db = []
#     files = get_files_from_nexrad_bucket("2022")
#     for file in files:
#         ydhs = []
#         splitted_str = file.split("/")
#         # match = pattern.search(file)
#         # if match:
#         year = splitted_str[0]
#         month = splitted_str[1]
#         day = splitted_str[2]
#         station = splitted_str[3]
#         ydhs.extend([year,month,day,station])
#         if ydhs not in meta_data_for_db:
#             meta_data_for_db.append(ydhs)
#     return meta_data_for_db
#
# # def get_meta_data_for_db_population():
# #     meta_data_for_db = []
# #     files = get_files_from_nexrad_bucket("2022/01/01")
# #     # print(files)
# #     for file in files:
# #         ydhs = []
# #         match = re.findall(r"(\d{4})(\d{2})(\d{2})([A-Z][0-9]{4})",file)
# #         # match = pattern.search(file)
# #         if match:
# #             year = match[0][0]
# #             print("year", year)
# #             month = match[0][1]
# #             day = match[0][2]
# #             station = match[0][3]
# #             ydhs.extend([year,month,day,station])
# #             if ydhs not in meta_data_for_db:
# #                 meta_data_for_db.append(ydhs)
# #     print(meta_data_for_db)
# #     return meta_data_for_db
#
def get_noaa_nexrad_url(filename):
    static_url_nex = "https://noaa-nexrad-level2.s3.amazonaws.com"
    generated_url = f"{static_url_nex}/{filename}"
    return generated_url

def get_my_s3_url_nex(filename):
    # print(dir_to_nex)
    print(filename)
    static_url = "https://damg7245-ass1.s3.amazonaws.com"
    filename_alone = filename.split("/")[-1]
    generated_url = f"{static_url}/{filename}"
    return generated_url

def copy_s3_nexrad_file(src_bucket_name, src_file_name, dst_bucket_name, dst_file_name):
    # s3 = boto3.client("s3",
    #                   aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
    #                   aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))

    # Creating Session With Boto3.
    session = boto3.Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
    )

     # Creating S3 Resource From the Session.
    s3 = session.resource('s3')

    # Create a Soucre Dictionary That Specifies Bucket Name and Key Name of the Object to Be Copied
    copy_source = {
        'Bucket': src_bucket_name,
        'Key': src_file_name
    }

    bucket = s3.Bucket(dst_bucket_name)
    flag = 0
    try:
        # bucket.copy(copy_source, dst_file_name)
        if not bucket.objects.filter(Prefix=dst_file_name).exists():
            bucket.copy(copy_source, dst_file_name)
            st.markdown(
                f"Object {src_file_name} copied from source bucket {src_bucket_name} to destination bucket {dst_bucket_name}.")
        else:
            st.markdown(f"Object {dst_file_name} already exists in destination bucket {dst_bucket_name}.")
        flag = 1
    except:
        st.error("File not found in NEXRAD Database, Please check the file //////")
        flag = 0

    # Printing the Information That the File Is Copied.
    print('Single File is copied')
#
def get_dir_from_filename_nexrad(file_name):
  # static_url_12 = "https://noaa-nexrad-level2.s3.amazonaws.com"
#   lis = file_name.split("_")
    full_file_name = ""
    try:
        splitted = file_name.split("_")
        ground_station = splitted[0:4]
        year = splitted[0][4:8]
        month = splitted[0][8:10]
        day = splitted[0][10:12]
        full_file_name = year+"/"+month+"/"+day+"/"+ground_station+"/"+file_name
        # print(full_file_name,"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
    except:
        print("exception in nexrad")
    return full_file_name

#
# if __name__ == "__main__":
#     # main()
#     x = get_meta_data_for_db_population()
#     print(x)
#     # get_files_from_nexrad_bucket("2022")
#     # meta_data = get_meta_data_for_db_population()
#     # copy_s3_nexrad_file("noaa-nexrad-level2","")
#
#     # print(meta_data)
#     # # piyush_func()