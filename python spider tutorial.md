# Scrapy tutorial

这是一篇学习用Scrapy实现爬虫的学习笔记。

英文文档地址:[https://doc.scrapy.org/en/latest/intro/tutorial.html](https://doc.scrapy.org/en/latest/intro/tutorial.html)

在用实机的python搭建Scrapy环境等时候，遇到了一些问题以及解决方式如下:

**macOs:**

> -bash: pip: command not found

```python
sudo easy_install pip
```



> OSError: [Errno 1] Operation not permitted

```python
sudo pip install --ignore-installed six
```



**Windows:**

> ImportError: No module named win32api

```python
pip install pypiwin32
```

不过最后还是在mac上栽在下边这个问题上了。

> 'module' object has no attribute 'OP_NO_TLSv1_1'

所以，我还是按照官方的说法，先搭建一个虚拟环境，然后在虚拟环境下，进行学习尝试工作。

## virtualenv环境搭建

参考文档:[https://doc.scrapy.org/en/latest/intro/install.html#intro-using-virtualenv](https://doc.scrapy.org/en/latest/intro/install.html#intro-using-virtualenv)

virtualenv环境使用指南:[https://virtualenv.pypa.io/en/stable/userguide/](https://virtualenv.pypa.io/en/stable/userguide/)

创建一个工作目录，名为ScrapyTutorial，在此目录下执行以下步骤。

**环境安装**

```
$ [sudo] pip install virtualenv
```

执行成功后，只是安装了虚拟环境功能，还没有创建一个虚拟环境，创建一个虚拟环境需要执行以下命令。

```
$ virtualenv ENV
```

执行成功后，会在这个目录下生成一个ENV文件夹，你可以查看一下该目录，该目录下有独立完整的python环境，这样就能避免与系统本身的环境产生冲突了。

**使用虚拟环境**

在ENV目录下，执行以下命令，就开始在虚拟环境下工作了。

```
$ source bin/activate
```

退出虚拟环境需要执行以下命令。

```
$ deactivate
```

## 在虚拟环境下安装Scrapy

进入虚拟环境后，执行以下命令。

```
pip install Scrapy
```

安装成功Scrapy后就可以开始创建爬虫项目了。

```
scrapy startproject tutorial
```

命令执行成功后，在ENV目录下会生成一个tutorial目录，这就是我们的爬虫项目目录了，废了这么大劲，终于到这步了。

