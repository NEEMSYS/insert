#!/usr/bin/python
#-*- coding: utf-8 -*-
# Author: ZhangTe
# Insert codes to app.c for monitor occurence
#
import sys
import os

msp430_h = '''//t2pad
// monitor code to import 430 head file. //t2pad
#include <msp430.h> //t2pad
'''

monitor_code = '''//t2pad
// monitor code to macro definition necessary. //t2pad
// begin //t2pad
#define bit0 BIT0  //t2pad
#define bit1 BIT1 //t2pad
#define bit2 BIT2 //t2pad
#define bit3 BIT6 //t2pad
#define moved2bit3 BIT3  //t2pad
#define sele BIT7  //t2pad
#define pos_sele 7 //t2pad
#define SETLEDOUT bit0 + bit1 + bit2 + bit3 + sele  //t2pad
#define low3bits (bit0+bit1+bit2) //0b00000111  //t2pad
#define inverse(bits) (~bits) // bits=low3bits->0b11111000; bits=bit3->0b10111111  //t2pad
#define LOW4 0 //t2pad
#define HIGH4 1 //t2pad
 //t2pad
#define logcalls_init() do{\
    P6DIR |= SETLEDOUT;\
    P6OUT &= 0x38;\
  }while(0) //t2pad
//t2pad
#define logcalls_setvalue(v, s) do{\
  P6OUT = ((((((v&low3bits) | (P6OUT & inverse(low3bits)))) \
             & inverse(bit3)) + ((v&moved2bit3)<<3)) \
             & inverse(sele)) + (s<<pos_sele); \
  }while(0) //t2pad
// send ... //t2pad
#define t2pad_protocol(value) do{\
  logcalls_setvalue(value, LOW4);\
  logcalls_setvalue(value>>4, HIGH4);\
  }while(0) //t2pad
// end //t2pad
 //t2pad
  logcalls_init(); // initialization those pin p6.0, p6.1, p6.2, p6.6, p6.7 //t2pad
'''

monitor_and_assign = 't2pad_protocol(nextTask); //t2pad\n'

saygoodbye = '\nPower by Intel, NVIDIA, Linux, Assembly, C, Python, nesC, Emacs, NetEase music.'
Usage = '''
Usage:
  --insert 
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
    global app_c_code
    if '//t2pad' in app_c_code[0]:
        print 'The code has been inserted.'
        return
    app_c_code.insert(0, msp430_h)

    insert_posA = 0
    insert_posB = 0
    for i in range(len(app_c_code)):
        if 'SchedulerBasicP__Scheduler__taskLoop' in app_c_code[i] and  app_c_code[i+1].strip() == '{':
            insert_posA = i+2
        if 'SchedulerBasicP__TaskBasic__runTask(nextTask);' in app_c_code[i]:
            insert_posB = i+1
        if insert_posA != 0 and insert_posB != 0:
            break
    app_c_code.insert(insert_posA, monitor_code)
    app_c_code.insert(insert_posB, monitor_and_assign)

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
            
try:
    if sys.argv[1] == '--insert' and len(sys.argv) == 2:
        insert()
    elif sys.argv[1] == '--remove' and len(sys.argv) == 2:
        remove()
    else:
        print Usage
except:
    print Usage
print saygoodbye
