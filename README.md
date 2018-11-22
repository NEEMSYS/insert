# insert & parse_logs
## Note:
由于使用了四个GPIO引脚,分两次传输8位任务ID,因此速度引脚翻转速度非常快,需要用高速采样设备(such as FPGA)进行采样

## insert.py
插入代码到app.c 为了在使用flocklab的时候监视任务的发生

注入代码的时候需要将注入程序与app.c放入同一路径下

Usage:
```shell
chmod 755 inject.py
```
注入监视代码
```shell
./inject.py --insert
```
移除监视代码
```shell
./inject.py --remove
```
app.c可以通过下面指令编译生成可执行文件
```shell
msp430-gcc -mmcu=msp430f1611 -o main.exe -O app.c
```
生成hex文件
```shell
msp430-objcopy -O ihex main.exe main.ihex
```
通常一个任务ID占用一个字节（经验知）
目前这个注入程序的可以将MSP430的P6.0, P6.1, P6.2, P6.6作为由低到高的4为数据引脚，P6.7作为控制引脚。

#### 注入的程序实现了如下功能：
0. 监视到将要调度的任务
1. 将P6.7引脚置为0时，数据引脚表示任务ID的低四位
2. 将P6.7引脚置为1， 数据引脚表示任务ID的高四位

parse_logs.py 按照如上逻辑，根据引脚的trace记录，反向还原了任务ID。

## parse_logs.py
该程序用来还原真实的任务ID，以标准控制台输出的形式输出任务序列，如需保存，请重定向.
```shell
parse_logs.py --[logs filename]
```
parse_logs.py 只需输入一个日志文件参数即可，该日志文件应当来源于Cooja仿真， 并且执行MspCLI命令
```shell
watch 0x35 | timestamp > logs-filename
```
0x35为MSP430的P6OUT寄存器。



