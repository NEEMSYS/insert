#!/usr/bin/python
#-*- coding: utf-8 -*-
#author: ZhangTe
#2017.12.31
import sys
import re
import os

Usage = '''
Usage: 
    parse_logs.py --[logs filename]
'''
saygoodbye = '\nPower by Intel, NVIDIA, Linux, Assembly, C, Python, nesC, Emacs, NetEase music.'

if len(sys.argv) != 2:
    print Usage
    print saygoodbye
    sys.exit()
    
if sys.argv[1][:2] != '--':
    print Usage
    print saygoodbye
    sys.exit()
    
filename = sys.argv[1][2:]

if not os.path.isfile(filename):
    print '[Failure] %s file does not exist in this directory.' % filename
    sys.exit("sorry, goodbye")
    
with open(filename, 'r') as f:
    logs_data = f.readlines()

# extract data
extract_write = filter(lambda e: 'Write from' in e, logs_data)

# 提取日志中的任务记录
encode_tasks = map(lambda e: re.findall('0x[0-9]{4,}', e)[0], extract_write)

# 将任务记录转换位二进制字符串
bin_tasks = map(lambda e: bin(int(e, 16))[2:], encode_tasks)

# 补全二级制的0到8位
front_complement_0 = map(lambda e: ''.join(['0' for i in range(8-len(e))]) + e, bin_tasks)

# 两两一组生成新的列表
merge_logs = list()
index = 0
while True:
    merge_logs.append((front_complement_0[index+1], front_complement_0[index]))
    index += 2
    if index >= len(front_complement_0):
        break
merge_logs = merge_logs[1:] # 前几条数据经常是错误的

# 验证数据是否合法
is_data_err = False
for e in merge_logs:
    if e[0][0] != '1' or e[1][0] != '0':
        print 'err date', merge_logs.index(e), e
        is_data_err = True

if is_data_err:
    sys.exit('error data! sorry, goodbye')
else:
    print '[:)] legal log data'
    
# 合并高位和低位数据
effective_bits = lambda e: e[1] + e[5:]
merge_high_and_low = map(lambda e: effective_bits(e[0])+effective_bits(e[1]), merge_logs)  
    
task_id_hex = map(lambda e:hex(int(e, 2)), merge_high_and_low)

# 补全任务id到4位十六进制
complement_id_hex = lambda e: e[:2]+''.join(['0' for i in range(6-len(e))])+e[2:]

for e in task_id_hex:
    print complement_id_hex(e)
'''
with open('t2pad_protocol_ex.txt', 'w') as f:
    map(lambda e: f.write(complement_id_hex(e)+'\n'), task_id_hex)
'''
print saygoodbye
