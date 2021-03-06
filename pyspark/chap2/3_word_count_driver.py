# python 3.6
# author(learning): Scc_hy
# original url: https://github.com/mahmoudparsian/pyspark-algorithms/blob/master/code/chap02/word_count_driver.py
# create date: 2019-12-17
# function: word_count_driver
# data: https://github.com/mahmoudparsian/pyspark-algorithms/blob/master/code/chap02/sample_file.txt

import sys, os
from pyspark.sql import SparkSession
import collections 

def create_pair(record):
    tokens = record.split(',')
    return (str(tokens[0]), int(tokens[1]))



if __name__ == '__main__':
    spark = SparkSession.builder.appName('Wod-Count-App').getOrCreate()
    fil_name = r'E:\Work_My_Asset\pyspark_algorithms\chap1\sample_file.txt'

    record = spark.sparkContext.textFile(fil_name)
    print("records.count(): ", record.count()) # 一行一条记录
    print("records.collect(): ", record.collect())
    
    words = record.filter(lambda x: len(x) > 0).flatMap(lambda line: line.lower().split(" "))
    
    words_count = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y)
    print("words_count.count(): ", words_count.count())
    print("words_count.collect(): ", words_count.collect())
    # 增加groupByKey
    words_count_group = words.map(lambda x: (x, 1)).groupByKey().mapValues(lambda x : sum(x))
    print("words_count_group.collect(): ", words_count_group.collect())
    
    # 增加sort 
    words_count_sort = words_count.sortBy(lambda x: x[1], ascending = False)
    print("words_count_sort.collect(): ", words_count_sort.collect())
    
    # 增加filter
    filtered = words_count.filter(lambda x: x[1] > 2)
    print("filtered.collect(): ", filtered.collect())
    
    # 增加python 读取方法
    f = open(fil_name)
    f_list =  f.read().replace('\n', ' ').split(' ')
    count_dict = collections.Counter(f_list)
    print(count_dict)
    f.close()

    spark.stop()


