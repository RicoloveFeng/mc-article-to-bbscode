#Settings
readFromFile = False
translator = "Staff"
aurl="https://minecraft.net/zh-hans/article/minecraft-snapshot-18w45a"

from bs4 import BeautifulSoup
from urllib import request

if readFromFile:
    f=open("urlsrc.txt","r")
    srcode=f.read()
    f.close()
else:
    page=request.urlopen(aurl)
    srcode=page.read()
Soup=BeautifulSoup(srcode,"html.parser")
f=open("bbssrc.txt","w")

def tagTrans(sentences):
    #em -> i
    #strong -> b
    #p -> color=Gray
    #li -> [*], color=Gray
    #ul -> list
    #ol -> list=1
    #code -> color=DarkOrchid
    #&lt; -> <
    #&rt; -> >
    #a href -> url=

    bbscode= {"<em>":"[i]",
        "</em>":"[/i]",
        "<strong>":"[b]",
        "</strong>":"[/b]",
        "<p>":"[color=Gray]",
        "</p>":"[/color]",
        "<li>":"[*][color=Gray]",
        "</li>":"[/color]",
        "<ul>":"[list]",
        "</ul>":"[/list]",
        "<ol>":"[list=1]",
        "</ol>":"[/list]",
        "<code>":"[color=DarkOrchid]",
        "</code>":"[/color]",
        "&lt;":"<",
        "&gt;":">",
        "<a href=\"":"[url=",
        "\">":"]",
        "</a>":"[/url]"}

    result = []
    for s in sentences:
        if s[-4:-2] in ['ul','ol']:
            s = s[:-7] + ("[/list][list]\n[*]无序列表翻译文字\n[/list]\n" if s[-4] == 'u' else "[/list][list=1]\n[*]有序列表翻译文字\n[/list]\n")
        for key in bbscode:
            s=s.replace(key, bbscode[key])
        result.append(s)
    return result

def bug_list(tag): # an ul tag
    #specifically process buglist

    bl=[]
    bl.append("[list]")
    for s in tag.contents:
        if type(s) == type(tag): #s is a li tag
            bl.append(str(s)+'\n')
            bl.append("[*]" + str(s.a) + " - ")
        else:
            bl.append(str(s))
    bl.append("[/list]")
    return bl

#1 output heading
title = Soup.find("h1").get_text().strip() #the first h1 tag contains the heading
f.write("[postbg]bg3.png[/postbg]\n") #poster
f.write("[align=center][img]"+Soup.find("img", class_='img-fluid').attrs['src']+"[/img]\n") #head image
f.write("[color=Gray][b][size=6]"+ title +"[/size]\n") #head title
f.write("[size=4]"+Soup.find("p", class_='lead text-center').get_text().strip()+"[/size][/color]\n")#subhead
f.write("[size=6]标题[/size]\n[size=4]副标题[/size][/align][/b]\n\n")

#2 dealing paragraphs
#convert tags to strs (in sentences) and convert these strs to bbscode together 
paras = Soup.find_all("div",class_=['article-paragraph','article-paragraph--image','article-paragraph--video','attributed-quote'])
get_snapshot = False
for para in paras:
    sentences = []
    if 'article-paragraph' in para.attrs['class']:
        #words
        list_counter = 0 #avoiding list nesting
        for tag in para.find_all(["p","ul","ol","h1","h2","h3","h4","h5","blockquote"]):
            if tag.name in ['p']: 
                sentences.append(str(tag) + "\n段落文本\n\n")

            elif tag.name in ['ul','ol']:
                if(tag.a and "MC-" in tag.a.string): #bug list
                    for bug in bug_list(tag):
                        sentences.append(bug)
                elif list_counter == 0: #normal list
                    list_counter = len(tag.find_all(['ul','ol']))
                    sentences.append(str(tag)+"\n")
                else: list_counter -= 1 #skip sub lists
            
            elif tag.name == 'blockquote': #green quote
                quote=tag.get_text().replace("&ldquo","\"").replace("&rdquo","\"").replace("&#39;","\'").strip()
                sentences.append("\n\n[indent][size=4][color=SeaGreen][b]|[/b][/color][color=Gray]"+ quote + "[/color][/size][/indent]")
                sentences.append("[indent][size=4][color=SeaGreen][b]|[/b][/color]引用文字[/size][/indent]\n\n")

            else:
                if tag.string == "Get the snapshot": #get into snapshot mode
                    get_snapshot = True
                    break 
                #h1 ~ h4 -> b, size= (7-level), ALL CAPS
                #h5 -> size=2, Title case
                
                else:
                    title_text=tag.contents[0] #<code>Foo bar</code> or 'Foo bar'
                    size_level = 7-int(tag.name[1])
                    if size_level > 2:
                        if type(title_text) == type(tag): title_text.string = title_text.string.upper()
                        else: title_text = title_text.upper()
                    else: size_level = 3
                    sentences.append("[b][size=" + str(size_level) + "][color=Gray]" + str(title_text) + "[/color]\n标题文本[/size][/b]\n\n") #text would apply inner color
 
    elif 'article-paragraph--image' in para.attrs['class']:
        #pics
        for tag in para.find_all(["p","img"]):
            if tag.attrs.get('src'):
                sentences.append("\n[align=center][img]" + str(tag.attrs['src']) + "[/img][/align]\n")
            else:
                sentences.append( "[align=center][b]" + str(tag) + "\n图片描述[/b][/align]\n\n")

    elif 'article-paragraph--video' in para.attrs['class']:
        #video's cover
        sentences.append("\n[align=center][img]" + str(para.img.attrs['src']) + "[/img][/align]\n")

    else:
        #quotes
        qt=para.blockquote
        quote=qt.get_text().replace("&ldquo","\"").replace("&rdquo","\"").replace("&#39;","\'")
        if 'attributed-quote__text' in qt.attrs['class']:
            sentences.append("[img=40,28]https://ooo.0o0.ooo/2017/06/14/5941457d17453.png[/img][b]————————————————————————————[/b]\n")
            sentences.append("[img=33,64]"+para.img.attrs['src']+"[/img][color=Gray]" + quote + "[/color]\n            引用文字\n            "+ para.cite.get_text())
            sentences.append("[align=right][b]————————————————————————————[/b][img=40,28]https://ooo.0o0.ooo/2017/06/14/5941457d216ca.png[/img][/align]\n")
        #else: #green quote is not put in quote para
            #sentences.append("\n\n[indent][size=4][color=SeaGreen][b]|[/b][/color]"+ quote + "[/size][/indent]\n\n")
    
    sentences = tagTrans(sentences)
    for s in sentences: f.write(s)
    if get_snapshot:
        break #normally no content would follow get-snapshot paragraph 

#3 acks
if get_snapshot:
    server_url=Soup.find("a", text="Minecraft server jar").attrs['href']
    f.write('''[align=center][table=70%,#EDFBFF]
[tr][td][align=center][size=3][color=#D6D604][b]官方服务端下载地址[/b][/color][/size][/align][/td][/tr]
[tr][td][align=center][url]{}[/url][/align][/td][/tr]
[/table][/align]'''.format(server_url))

else:
    attribution = Soup.find("dl",class_="attribution__details").find_all("dd")

    f.write("[img=16,16]https://ooo.0o0.ooo/2017/01/30/588f60bbaaf78.png[/img]\n\n")
    f.write("【" + translator + "译自[url=" + aurl + "]" + title + "[/url]】\n")
    f.write("【作者" + attribution[0].get_text() + ",发布时间" + attribution[1].get_text()+"】")

#end with closing file
f.close()