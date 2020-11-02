#!/usr/bin/python3

#類似度を基にした抽出プログラム

import os
import math
import glob
import MeCab
import sys
mecab = MeCab.Tagger('')
# create the database object



def main():
    txt = []
    home = os.environ['HOME']
    Dir = home+"/Download/risk_txt/txt/E31256.txt"
    #print(Dir)
    files = glob.glob(Dir)#file_name
    for file in files:
        sgml = open(file)
        txt = sgml.readlines()
        
    txt2014=""
    txt2015=""
    
    for line in txt:
        factor = line.split(' ')
        pre = factor[0]
        f = pre.split('_')
        date = f[2]
        
        if "2014" in date:
            txt2014 += factor[1]+","
            
        elif "2015" in date:
            txt2015 += factor[1]+","


    txt1=txt2014.split(",")
    txt2=txt2015.split(",")
    
    #-------------------------------------------------
    new_hash={}
    for line2 in txt2:
        hash2={}
        maxi=0 #2015と全2014を比べ、最も大きい数を保存する
        mecab_results2 = mecab.parse(line2)
        results2 = mecab_results2.split('\n')
        
        for line in results2:
            if "名詞" in line:
                factor=line.split("\t")
                if factor[0] in hash2:
                    hash2[factor[0]] += 1
                else:
                    hash2[factor[0]] = 1
        #------------------------------------------------
        for line1 in txt1:
            hash1={}
            bool=True
            mecab_results1 = mecab.parse(line1)
            results1 = mecab_results1.split('\n')
            
            for line in results1:
                if "名詞" in line:
                    factor=line.split("\t")
                    if factor[0] in hash1:
                        hash1[factor[0]] += 1
                    else:
                        hash1[factor[0]] = 1

            sum1=0
            sum2=0
            multi=0

            for key in hash1.keys():
                sum1+=hash1[key]**2
                
            for key in hash2.keys():
                sum2+=hash2[key]**2
              
            for key in hash1.keys():
                if key in hash2:
                    multi += hash1[key]*hash2[key]

        
            
            if sum1 != 0 and sum2 != 0:
                cos=multi / ((sum1**0.5)*(sum2**0.5))#---＞コサイン類似度計算
                #print(cos)
                if maxi < cos:
                    maxi = cos
                    
                if cos > 0.8:#閾値の設定
                    bool=False
                    break
        #---------------------------------------------------

        if bool:
            new_hash[line2]=maxi
        
    for key in new_hash.keys():
        print(key+":"+str(new_hash[key]))
        
        
if __name__ == "__main__":
    main()
