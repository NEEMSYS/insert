#-*- coding: utf-8 -*-

def dec_to_hex(num):
    """ num : string
    range: 0x00-0x00ff
    """
    t = int(num)
    assert 0x00ff, "out of range: " + str(t)
    r = hex(t)
    result = None
    if t > 0x000f:
        result = '0x00' +r[-2:]
    else:
        result = '0x000' +r[-1]
    return result

def get_task_id(task_path):
    global task_line
    with open(task_path) as f:
        line = f.readlines()
		
    task_line = filter(lambda e: '__runTask()' in e , line)
    tasks_name = list()

    for e in task_line:
        if '/*' not in e and e not in tasks_name:
            tasks_name.append(e.strip())
        elif '/*' in e:
            tasks_name.append(e[e.index('*/')+2:].strip())

    temp_tasks_name = map(lambda x: x[:-12], tasks_name) 
    temp_tasks_id = list() #用于存放含有对任务名定义的行
    temp_list = list() #存放分割后的 temp_tasks_id
    temp_task_define = list() ##用于仅仅存放含有对任务名定义的行
    task_id_temp = list()
    task_id = list() 
    
    for e in temp_tasks_name:
        for i in line:
            if e in i and ' = ' in i and 'U' in i:
                temp_tasks_id.append(i.strip())
    
    map(lambda e: temp_list.append(e.split(' ')), temp_tasks_id)
        
    for e in temp_tasks_name:
        for i in temp_list:
            if e == i[0] and i not in temp_task_define:
                temp_task_define.append(i)
    
    map(lambda e: task_id_temp.append(e[-1][:-1]), temp_task_define)    

    map(lambda e: task_id.append(dec_to_hex(e)), task_id_temp)
    
    return task_id, task_id_temp # 分别以十六进制和十进制表示

if __name__ == '__main__':
    a, b = get_task_id('./app.c')
    print a, '\n\n', b
