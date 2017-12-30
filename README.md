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



