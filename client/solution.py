
from split_share import *
import os
import filecmp

test_file = "test.txt"
tmp_folder = "tmp"
addr = "./client"
split_store(test_file)

if not os.path.exists(os.path.join(addr,tmp_folder)):
    os.makedirs(os.path.join(addr,tmp_folder))
if os.path.exists(os.path.join(addr,"mem",test_file)):
    os.rename(os.path.join(addr,"mem",test_file),os.path.join(addr,tmp_folder,test_file))

split_fetch(test_file)

file_fetched = os.path.join(addr,"mem",test_file)
file_original = os.path.join(addr,tmp_folder,test_file)

passed = filecmp.cmp(file_fetched, file_original, shallow=True)
if(passed):
    print("Success !!!")
else:
    print("Failed :(")
