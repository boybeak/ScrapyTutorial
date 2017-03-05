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

此时ScrapyTutorial目录下的结构如下图所示:

![https://github.com/boybeak/ScrapyTutorial/blob/master/pic1.jpeg](https://github.com/boybeak/ScrapyTutorial/blob/master/pic1.jpeg)

## 第一个爬虫

在ENV/tutorial/tutorial/spiders目录下，创建一个quotes_spider.py文件，输入代码：

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
```

在ENV/tutorial目录下执行命令：

```
scrapy crawl quotes
```

然后我们等待命令结束，爬虫成功后，会在ENV/tutorial目录下多两个文件，quotes-1.html和quotes-2.html。打开观察，发现只是把html爬成文本文件保存了起来。

其实在上边的代码中，start_requests方法并不是十分必要，可以简化成下边的代码：

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
```

## 提取数据

学习使用Scrapy提取数据最好的方式就是[Scrapy shell](https://doc.scrapy.org/en/latest/topics/shell.html#topics-shell)。执行以下命令：

```
scrapy shell 'http://quotes.toscrape.com/page/1/'
```

> 注意在这个命令里，url是不能带有参数的，例如?,&这样的字符不允许出现，并且在windowns命令行下，url要用双引号来包裹。
>
> ```
> scrapy shell "http://quotes.toscrape.com/page/1/"
> ```

命令结束，进入Scrapy shell模式下。退出Scrapy shell输入exit()。

```
[ ... Scrapy log here ... ]
2016-09-19 12:09:27 [scrapy.core.engine] DEBUG: Crawled (200) <GET http://quotes.toscrape.com/page/1/> (referer: None)
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x7fa91d888c90>
[s]   item       {}
[s]   request    <GET http://quotes.toscrape.com/page/1/>
[s]   response   <200 http://quotes.toscrape.com/page/1/>
[s]   settings   <scrapy.settings.Settings object at 0x7fa91d888c10>
[s]   spider     <DefaultSpider 'default' at 0x7fa91c8af990>
[s] Useful shortcuts:
[s]   shelp()           Shell help (print this help)
[s]   fetch(req_or_url) Fetch request (or URL) and update local objects
[s]   view(response)    View response in a browser
>>>
```

接下来就可以输入命令来提取数据了。接下来将以命令-结果代码块来演示如何使用命令提取数据。

```
>>> response.css('title')
[<Selector xpath='descendant-or-self::title' data='<title>Quotes to Scrape</title>'>]
```

或者只提取其中的文字部分：

```
>>> response.css('title::text').extract()
['Quotes to Scrape']
```

这里返回的结果里，实际上是一个数组的形式，我们可以用.extract_first()来直接获取第一个数据。

```
>>> response.css('title::text').extract_first()
'Quotes to Scrape'
```

另外一种写法

```
>>> response.css('title::text')[0].extract()
'Quotes to Scrape'
```

强烈建议使用第一种形式，因为第二中存在index越界的风险，而第一种形式在数据不存在的时候直接返回None。

除了使用extract()和extract_first()以外，通过正则表达式来提取数据。

```
>>> response.css('title::text').re(r'Quotes.*')
['Quotes to Scrape']
>>> response.css('title::text').re(r'Q\w+')
['Quotes']
>>> response.css('title::text').re(r'(\w+) to (\w+)')
['Quotes', 'Scrape']
```

## 使用XPath

除了CSS，还可以使用XPath表达式：

```
>>> response.xpath('//title')
[<Selector xpath='//title' data='<title>Quotes to Scrape</title>'>]
>>> response.xpath('//title/text()').extract_first()
'Quotes to Scrape'
```

实际上，CSS也是转换成XPath来做的，但是XPath比CSS更强大一些。一些更为详细的XPath教程如下：

[using XPath with Scrapy Selectors here](https://doc.scrapy.org/en/latest/topics/selectors.html#topics-selectors)

[this tutorial to learn XPath through examples](http://zvon.org/comp/r/tut-XPath_1.html)

[this tutorial to learn “how to think in XPath”](http://plasmasturm.org/log/xpath101/)

**提取其中的元素**

以 [http://quotes.toscrape.com](http://quotes.toscrape.com/) 这个链接网页为例，其中我们的解析的元素大概是这个样子的：

```
<div class="quote">
    <span class="text">“The world as we have created it is a process of our
    thinking. It cannot be changed without changing our thinking.”</span>
    <span>
        by <small class="author">Albert Einstein</small>
        <a href="/author/Albert-Einstein">(about)</a>
    </span>
    <div class="tags">
        Tags:
        <a class="tag" href="/tag/change/page/1/">change</a>
        <a class="tag" href="/tag/deep-thoughts/page/1/">deep-thoughts</a>
        <a class="tag" href="/tag/thinking/page/1/">thinking</a>
        <a class="tag" href="/tag/world/page/1/">world</a>
    </div>
</div>
```

打开Scrapy shell来解析这些数据：

```
$ scrapy shell 'http://quotes.toscrape.com'
```

```
>>> title = quote.css("span.text::text").extract_first()
>>> title
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'
>>> author = quote.css("small.author::text").extract_first()
>>> author
'Albert Einstein'
```

通过这些命令就可以学习到如何通过不同的节点访问到数据。

## 在爬虫类中提取数据

之前的提取数据，都只是在Scrapy shell脚本中，现在要把这些写入到程序中。

以前的quotes_spider.py中改成这样：

```
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
```

通过命令：

```
scrapy crawl quotes -o quotes.json
```

将爬到的数据存储到一个json文件下，执行结束后，将看到ENV/tutorial目录下多了一个quotes.json文件。