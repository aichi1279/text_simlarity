#!/usr/bin/python3

#類似度を基にした抽出プログラム

import os
import math
from kyotocabinet import *
import glob
import MeCab
import codecs
import sys
mecab = MeCab.Tagger('')
# create the database object
db=DB()
N=3710

def main():
    txt = []
    home = os.environ['HOME']
    Dir = home+"/Download/risk_txt/txt/*"
    #print(Dir)
    files = glob.glob(Dir)#file_name
    #-----------------------------------------------------
    files.sort()
    for file in files:
        print(file)
        sgml = open(file)
        txt = sgml.readlines()
    
        txt2014=""
        txt2015=""
        s=""
        #-----------------------------------------------start1
        for line in txt:#one text
            factor = line.split(' ')
            pre = factor[0]
            f = pre.split('_')
            date = f[2]
        
            if "2015" in date:#--------------------->抽出期間の設定
                txt2014 += factor[1]+","
            
            elif "2016" in date:
                txt2015 += factor[1]+","


            txt1=txt2014.split(",")
            txt2=txt2015.split(",")
        #---------------------------------------------------end1
        db.open("df.kch", DB.OREADER)
        new_hash={}
        #----------------------------------------------------------------------start2
        for line2 in txt2:#2015
            hash2={}
            hash4={}
            maxi=0 #類似度のMAX
            
            hash2 =get_TF(line2)#TF2015
            hash4=get_TFIDF(line2,hash2)#TFIDF2015
            #------------------------------------------------------------------start1
            for line1 in txt1:#2014
                hash1={}
                hash3={}
                bool=True
                mecab_results1 = mecab.parse(line1)
                results1 = mecab_results1.split('\n')
                
                hash1 =get_TF(line1)#TF2014
                hash3=get_TFIDF(line1,hash1)#TFIDF2014
                
                sum1=0
                sum2=0
                multi=0
                
                for key in hash3.keys():#2014
                    sum1+=hash3[key]**2
                        
                for key in hash4.keys():#2015
                    sum2+=hash4[key]**2
              
                for key in hash3.keys():
                    if key in hash4:
                        multi += hash3[key]*hash4[key]

        
            
                if sum1 != 0 and sum2 != 0:
                    cos=multi / ((sum1**0.5)*(sum2**0.5))#---＞コサイン類似度計算
                    #print(cos)
                    if maxi < cos:
                        maxi = cos
                    
                    if cos > 0.3:#----------------------------->閾値の設定
                        bool=False
                        break
            #----------------------------------------------------------------------------end1
            if bool:#2015 & one text
                new_hash[line2]=maxi
                s += line2+':'+str(maxi)+'\n'  
                #print(key+":"+str(new_hash[key]))

        #--------------------------------------------------------------------------------end2
        name="/home/aichiasano/Download/risk_txt/2015-2016/"
        basename=os.path.basename(file)
        if s  != ":0\n":
            with codecs.open(name+"S"+basename, 'w','utf-8') as f:# file
                f.write(s)


   

def get_TF(line):#TF
    hash={}
    mecab_results = mecab.parse(line)
    results = mecab_results.split('\n')
    for line in results:
        if "名詞" in line:
            factor=line.split("\t")
            key = factor[0]
            if key in hash:
                hash[key] += 1
            else:
                hash[key] = 1
                
    return hash                    



def get_TFIDF(line,hash):
    hash2={}
    mecab_results = mecab.parse(line)
    results = mecab_results.split('\n')
    for line in results:#TFIDF
        factor=line.split("\t")
        key=factor[0]
        if "名詞" in line and key!="":
            str_DF=db.get_str(key)
            
            if  str_DF=="" or str_DF==None:
                continue
                    
            DF=float(str_DF)
            #print(key+" "+str(DF))
            TFIDF = hash[key]*math.log2(N/DF)
                    
            if key in hash2:
                hash2[key] += TFIDF
            else:
                hash2[key] = TFIDF

    return hash2

        
if __name__ == "__main__":
    main()
