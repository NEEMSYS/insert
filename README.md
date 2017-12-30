# insert
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



