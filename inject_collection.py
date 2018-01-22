#/usr/bin/python2
#-*- coding: utf-8 -*-
# Author: ZhangTe
# Insert codes to app.c for monitor occurence
#
import sys
import os
from get_taskid import get_task_id #获取任务数量

app_c_path = './app.c'
tasks, _ =  get_task_id(app_c_path)

monitor_code = '''//t2pad
#define TASK_AMOUNT %d  //t2pad
static uint16_t collection_task[TASK_AMOUNT] = {0};//t2pad
static uint16_t collectiion_cnt = 0;//t2pad
'''%(len(tasks))

monitor_and_assign = '''//t2pad
      collection_task[nextTask]++; //t2pad
      collectiion_cnt++;   //t2pad
      { //t2pad
        uint8_t i = 0; //t2pad
        if(collectiion_cnt >= %s){  //t2pad
          collectiion_cnt = 0;    //t2pad
          printf("{"); //for json format //t2pad
          for(i = 0; i < TASK_AMOUNT; i++){   //t2pad
            if(i != TASK_AMOUNT-1)  //t2pad
                  printf("\\"%%d\\":%%d,", i, collection_task[i]);  //t2pad
             else printf("\\"%%d\\":%%d", i, collection_task[i]);  //t2pad
            collection_task[i] = 0;    //t2pad
          }    //t2pad
          printf("}\\n"); //t2pad
        }      //t2pad
      }        //t2pad
'''

saygoodbye = '\nPower by Intel, NVIDIA, Linux, Assembly, C, Python, nesC, Emacs, NetEase music.'
Usage = '''
Usage:
  --insert cnt=100
    Insert task monitor codes to app.c
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
    global app_c_code, monitor_code, monitor_and_assign
    if '//t2pad' in app_c_code[0]:
        print 'The code has been inserted.'
        return
    app_c_code.insert(0, '//t2pad\n')

    insert_posA = 0
    insert_posB = 0
    for i in range(len(app_c_code)):
        if 'SchedulerBasicP__Scheduler__taskLoop' in app_c_code[i] and  app_c_code[i+1].strip() == '{':
            insert_posA = i
        if 'SchedulerBasicP__TaskBasic__runTask(nextTask);' in app_c_code[i]:
            insert_posB = i+1
        if insert_posA != 0 and insert_posB != 0:
            break
    app_c_code.insert(insert_posA, monitor_code)
    app_c_code.insert(insert_posB, monitor_and_assign)

    with open('app.c', 'w') as f:
        for e in app_c_code:
            f.write(e)
    print 'The number of task is {}'.format(len(tasks))
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
            if 'cnt=' == sys.argv[2].strip()[:4]:
                cnt = sys.argv[2].strip()[4:]
                monitor_and_assign = monitor_and_assign%(cnt)
                insert()
            else:
                print Usage
        elif sys.argv[1] == '--remove' and len(sys.argv) == 2:
            remove()
        else:
            print Usage
    except Exception, e:
        print Usage
    print saygoodbye
