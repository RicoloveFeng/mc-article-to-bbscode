# mc-article-to-bbscode
将Minecraft.net上的博文转换为bbscode的脚本。 
A script for translating articles on Minecraft.net to bbscode.

# 使用方法
1. 确保你已经安装Python，以及它的库BeautifulSoup4。
2. 在脚本中修改设置。
   * readFromFile: 是否从文件中读取网页源代码。如果是，则会读取urlsrc.txt中的内容。
   * translator: 你的名称/ID。
   * aurl: 如果readFromFile为False，则会从此处的url指向的页面读取源代码。
3. 运行脚本，结果储存在bbssrc.txt中。
4. 复制转换好的bbscode到论坛中，在纯文本模式下进行畅快翻译。

# Usage
1. Ensure that you have installed python and BeautifulSoup4 library.
2. Change the settings.
   * readFromFile: Whether to read page source from file. If set to True, the script would read source from urlsrc.txt.
   * translator: Your name/ID.
   * aurl: If readFromFile is set to False, the script would read source specified here.
3. Run the script and the result would save in bbssrc.txt.
4. Copy the result bbscode to the forum, and translate the text freely and fluently.
