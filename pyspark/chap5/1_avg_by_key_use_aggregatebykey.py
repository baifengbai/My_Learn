# python 3.6
# author(learning): Scc_hy
# original url: https://github.com/mahmoudparsian/pyspark-algorithms/blob/master/code/chap05/average_by_key_use_aggregatebykey.py
# create date: 2019-12-24
# function: average_by_key_use_aggregatebykey
# data: 

import sys, os
from pyspark.sql import SparkSession
from pyspark import StorageLevel
from collections import defaultdict


def create_pair(t3):
    return (t3[0], int(t3[2]))


if __name__ == '__main__':
    spark = SparkSession.builder.appName('avg_by_key').getOrCreate()
    fil_name = r'E:\Work_My_Asset\pyspark_algorithms\chap1\sp1.fastq'
    list_of_tuples = [('alex', 'Sunnyvale', 25),
                      ('alex', 'Sunnyvale', 33),
                      ('alex', 'Sunnyvale', 45),
                      ('alex', 'Sunnyvale', 63),
                      ('mary', 'Ames', 22),
                      ('mary', 'Cupertino', 66),
                      ('mary', 'Ames', 20),
                      ('bob', 'Ames', 26)]
    rdd = spark.sparkContext.parallelize(list_of_tuples)
    print("rdd.collect() = ", rdd.collect())
    rdd_pair = rdd.map(lambda t: create_pair(t))
    print("rdd2.collect() = ", rdd_pair.collect())

    # create a (key, value) pair
    #  where
    #       key is the name
    #       value is the (sum, count)
    # https://blog.csdn.net/a1628864705/article/details/52757384
    sum_count = rdd_pair.aggregateByKey(
        (0 , 0),
        lambda zero_tuple, values_: (zero_tuple[0] + values_, zero_tuple[1] + 1),
        lambda values_, cnts: (values_[0] + cnts[0], values_[1]+cnts[1])  # reduce
    )
    print("sum_count.collect() = ", sum_count.collect())
    
    sum_count1 = rdd_pair.combineByKey(
        lambda values_: (values_, 1), # createCombiner
        lambda combined, values_: (combined[0] + values_, combined[1] + 1), # 在combined中叠加
        lambda values_, cnts: (values_[0] + cnts[0], values_[1]+cnts[1])  # reduce
    )
    print("sum_count1.collect() = ", sum_count1.collect())


    averages = sum_count.mapValues(lambda v_tuple: float(
        v_tuple[0]) / float(v_tuple[1]))
    print("averages.collect() = ", averages.collect())
    spark.stop()