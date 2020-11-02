#!/usr/bin/python3

#類似度を基にした抽出プログラム

import os
import glob
import codecs
import sys
import random
# create the database object

def main():
    txt = []
    count=0
    home = os.environ['HOME']
    Dir = home+"/Download/risk_txt/2017-2018/*"
    files = glob.glob(Dir)#file_name
    files.sort()
    count==0
    for file in files:
        #print(file)
        sgml = open(file)
        txt = sgml.readlines()
        for line in txt:#one text
            if ':' in line or "。" not in line:
                continue
            count+=1
       
    print(count)
    
if __name__ == "__main__":
    main()
