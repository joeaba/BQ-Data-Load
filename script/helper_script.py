import os
import shutil
from os import path
import datetime
TIME_ = datetime.datetime.now()
def make_copy():
  if path.exists("last_transac.txt"):
    # get the path to the file in the current directory
    src = path.realpath("last_transac.txt")
    #seperate the path from the filter
    head, tail = path.split(src)
    file_name, Extension = tail.split('.')
    #let's make a backup copy by appending "bak" to the name
    dst = head.strip('\'') + "/" + file_name.strip('\'') + "_" + str(TIME_)+ "." + Extension.strip('\'')
    # nowuse the shell to make a copy of the file
    shutil.copy(src, dst.strip('\''))
    #copy over the permissions,modification
    shutil.copystat(src,dst)
if __name__=="__main__":
  #TIME_ = datetime.datetime.now()
  main()
