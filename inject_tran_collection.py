#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: ZhangTe
# Insert codes to app.c for task transition occurence
# , then send infomation to PC through serial port with 115200 baud.
#
import sys
import os
import re

def get_couples(path):
    """ 获得日志中所有转移的情况
    Args:
        path: str
          logcalls 文件路径
    Retval:
        couples: tuple
          包含所有出现过的转移情况e.g.((1, 2), (3, 4))
    """
    couples = list()
    with open(path, 'r') as f:
        logs = f.readlines()[1:]
    logs = map(lambda e: re.findall('0x[0-9a-f]{4}', e)[0], logs)    
    for i in range(len(logs)-1):
        if (logs[i], logs[i+1]) not in couples:
            couples.append((logs[i], logs[i+1]))
    # convert hex of task id to integer
    couples = map(lambda e: (int(e[0], 16), int(e[1], 16)), couples)
    return tuple(couples)

def get_couples_C_type(couples):
    """ 将任务转移对，转换为c语言格式的数组形式
    ex:
     ((7, 5), (2, 6)) -> {{7, 5, 0}, {2, 6, 0}}
    其中第三个item 0是转移计数的初始值，每发生一次转移该值加一
    """
    return '{' + ', '.join(['{%d, %d, 0}'%(e[0], e[1]) for e in couples]) + '}'

codes_define = '''//t2pad
#define COUPLE_AMOUNT %d  //t2pad
#define THRESHOLD %d//t2pad
static volatile uint8_t pre_task = 0;//t2pad
static volatile uint16_t collection_cnt = 0;//t2pad
static volatile uint16_t couples[COUPLE_AMOUNT][3] = %s; //t2pad
'''
codes_collect = '''{//t2pad
    uint8_t i = 0;//t2pad
    if(collection_cnt >= THRESHOLD){//t2pad
        collection_cnt = 0;//t2pad
        // send to pc through serial port//t2pad
        printf("{");//t2pad
        for(i=0; i<COUPLE_AMOUNT; i++){//t2pad
          if(i != COUPLE_AMOUNT-1) //t2pad
              printf("\\"%d->%d\\": %d, ", couples[i][0], couples[i][1], couples[i][2]);//t2pad
          else //t2pad
              printf("\\"%d->%d\\": %d", couples[i][0], couples[i][1], couples[i][2]);//t2pad
          couples[i][2] = 0;//t2pad
        }//t2pad
        printf("}\\n\\n");//t2pad
    }//t2pad
    for(i=0; i<COUPLE_AMOUNT; i++){//t2pad
        if(couples[i][0]==(uint16_t)pre_task && couples[i][1]==(uint16_t)nextTask){//t2pad
             couples[i][2]++;//t2pad
             collection_cnt++;//t2pad
             break;//t2pad
        }//t2pad
    }//t2pad
    pre_task = nextTask;//t2pad
}//t2pad
'''

saygoodbye = '\nPower by Intel, NVIDIA, Linux, Assembly, C, Python, nesC, Emacs, NetEase music.'
Usage = '''
Usage:
  --insert t=100
    Insert task monitor codes to app.c, and 't' is the threshold of send to PC
  --remove 
    Remove task monitor codes from app.c
'''
if not os.path.isfile('app.c'):
    print '[Failure] app.c does not exist in this directory.'
    print saygoodbye
    sys.exit('sorry, goodbye')

with open('app.c', 'r') as f:
    app_c_code = f.readlines()

def insert():
    global app_c_code, codes_collect, codes_define
    if '//t2pad' in app_c_code[0]:
        print 'The code has been inserted.'
        return
    app_c_code.insert(0, '//version 3: task transition collection and send //t2pad\n')

    insert_posA = 0
    insert_posB = 0
    for i in range(len(app_c_code)):
        if 'SchedulerBasicP__Scheduler__taskLoop' in app_c_code[i] and  app_c_code[i+1].strip() == '{':
            insert_posA = i
        if 'SchedulerBasicP__TaskBasic__runTask(nextTask);' in app_c_code[i]:
            insert_posB = i+1
        if insert_posA != 0 and insert_posB != 0:
            break
    app_c_code.insert(insert_posA, codes_define)
    app_c_code.insert(insert_posB, codes_collect)

    with open('app.c', 'w') as f:
        for e in app_c_code:
            f.write(e)

    print 'Insert in \n#line 0 \n#line %d \n#line %d \nsucceeded.\n\nWow' % (insert_posA, insert_posB)

def remove():
    global app_c_code
    line_cnt = list()
    if '//t2pad' not in app_c_code[0]:
        print 'Does not include the inserted codes.'
        return
    cnt = 0
    for e in app_c_code[:]:
        if '//t2pad' in e:
            line_cnt.append(cnt)
            app_c_code.remove(e)
        cnt += 1

    with open('app.c', 'w') as f:
        for e in app_c_code:
            f.write(e)
    print 'Remove from'
    for e in line_cnt:
        print '#line %d' % e
    print 'succeeded\n\nprefect\n'

if __name__ == '__main__':
    try:
        if sys.argv[1] == '--insert' and len(sys.argv) == 3:
            if 't=' == sys.argv[2].strip()[:2]:
                t = int(sys.argv[2].strip()[2:])
                
                # 根据cooja仿真日志文件获得可能的任务转移组合
                couples = get_couples('TestDiss-cooja-logcalls.txt') 
                arry = get_couples_C_type(couples) # 将任务转移组合转换为c语言数组格式
                codes_define %= (len(couples), t, arry) # 格式化插入任务转移数据到c代码
                
                insert()
            else:
                print Usage
        elif sys.argv[1] == '--remove' and len(sys.argv) == 2:
            remove()
        else:
            print Usage
    except Exception, e:
        print str(e)
        print Usage
    print saygoodbye
    


    
