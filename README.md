# mc-article-to-bbscode
将Minecraft.net上的博文转换为bbscode的脚本。 

# 使用方法
1. 确保你已经安装Python，以及它的库BeautifulSoup4。
2. 在脚本中修改设置。
   * debug: 调试模式，会在运行时在终端输出一些信息，不需要修改。
   * ensize: 调整英文原文的字号大小。默认状态为2。
   * readFromFile: 是否从文件中读取网页源代码。如果是，则会读取urlsrc.txt中的内容。
   * translator: 你的名称/ID。
   * aurl: 如果readFromFile为False，则会从此处的url指向的页面读取源代码。
3. 运行脚本，结果储存在bbssrc.txt中。
4. 复制转换好的bbscode到论坛中，在纯文本模式下进行畅快翻译。
