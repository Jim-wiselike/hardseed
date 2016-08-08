#coding=utf-8
import urllib.request
import re
import sys,os
import http.cookiejar
import socket

EndPage   = 100
Url="http://jj.ady6.info/a/139.html"
StartPage = 1

timeout = 10
filename = ''
InTitle = 0
pageMaxnum = 24
StartNum  = 1



def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('GBK')
    return html

def getImg(html):
    reg = r'img src=["\'](\S+?\.jpg)["\'] '
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist 
def getTitle(html):
    reg = r'img src=["\'].*["\'] title=\"([^"]+)\" '
    title = re.compile(reg)
    titlelist = re.findall(title,html)
    return titlelist 
def getUrl2(html, img, url):
	reg = r'a href=["\'](\S+?\.html)["\'] .*'+img
	url2 = re.compile(reg)
	url2list = re.findall(url2,html)
	if len(url2list)<1: 	raise Exception
	for i in range(len(url2list)):
		url2list[i] = 'http://'+url+url2list[i]
	return url2list[0]
def getHead(url):
	reg2 = r'//([^/]+)/'
	urltmp = re.compile(reg2)
	urlAlist = re.findall(urltmp,url)
	return ("").join(urlAlist)

def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

def mkdir(path):
    path=path.strip()
    path=path.rstrip("\\")
    if not os.path.exists(path):
        os.makedirs(path) 
    return path

def downld_image(image_url, path):
  with opener.open(image_url) as res:
    image = res.read()
    with open(path,'wb') as file:
      file.write(image)
    file.close()

def getImg2(html):
    reg = r'img alt=["\'].*["\'] src=["\'](\S+?\.jpg)["\'] '
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    return imglist
def getPlay(html,head):
    reg = r'a title=["\']HD["\'] href=["\'](\S+?1-0\.html)["\'] '
    play = re.compile(reg)
    playadd = re.findall(play,html)
    if len(playadd)<1: 	raise Exception
    return 'http://'+head+playadd[0]
def getPlay2(html,head):
    reg = r'type=["\']text/javascript["\'] src=\"(.*\?[^"]+)\"'
    play = re.compile(reg)
    playadd = re.findall(play,html)
    if len(playadd)<1: 	raise Exception
    return 'http://'+head+playadd[0]
def getPlayF(string):
    reg = r'(xfplay://dna=\S+)\$xfplay'
    playF = re.compile(reg)
    playadd = re.findall(playF, string)
    if len(playadd)<1: 	raise Exception
    return playadd[0]
def writefile(name, string):
    with open(name,'a') as file:
      file.writelines(string+"\r\n")
    file.close()

socket.setdefaulttimeout(timeout)
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent',' Mozilla/5.0 (Windows NT 6.3; Win64; x64)\
           AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36')]
path = cur_file_dir()+'/'+filename
head = getHead(Url)

i=pageMaxnum
num=0

strinfo = re.compile('.html')
urls=[]
for i in range(StartPage,EndPage+1):
	if i!=1:
		urls.append(strinfo.sub('_{0}.html'.format(i),Url))
	else:
		urls.append(Url)

for url in urls:
	num+=1
	try:
		if i<pageMaxnum: break
		html = getHtml(url)
	except Exception as err:
		writefile(path+'/{0}-Err.txt'.format(num), 'Error:\r\nurl=\t'+url)
	else:
		try:
			titles = getTitle(html)
			imgs = getImg(html)
		except Exception as err:
			writefile(path+'/{0}-Err.txt'.format(num), 'Error:\r\nurl=\t'+url)
		
		i=0
		for title in titles:
			i+=1
			if StartNum>1: 
				StartNum-=1
				continue
			if InTitle==0 :
				path2 = path
			else:
				path2 = mkdir(path+'\\'+title)
			print( imgs[i-1] )

			try:
				downld_image(imgs[i-1], path2+'/{0}-{1}-0.jpg'.format(num,i) )
			except Exception as err:
				writefile(path2+'/{0}-{1}-0.html'.format(num,i), '<IMG src="'+imgs[i-1]+'" >')

			try:
				url2 = getUrl2(html, imgs[i-1], head)
			except Exception as err:
				writefile(path2+'/{0}-{1}-err.txt'.format(num,i), html+'\r\n\r\n')
			else:
				try:
					html2 = getHtml( url2 )
					imgs2 = getImg2(html2)
				except Exception as err:
					writefile(path2+'/{0}-{1}-Err.txt'.format(num,i), 'Error:\r\nurl=\t'+url2)
				else:
					writefile(path2+'/{0}-{1}-0.txt'.format(num,i), url2+'\r\n'+title )
					tmp=97
					for each in imgs2:
						print(each)
						try:
							downld_image(each, path2+'/{0}-{1}-1{2}.jpg'.format(num,i,chr(tmp)) )
							tmp+=1
						except Exception as err:
							writefile(path2+'/{0}-{1}-1{2}.html'.format(num,i,chr(tmp)), '<IMG src="'+each+'" >')

					try:
						Play = getPlay(html2, head)
					except Exception as err:
						writefile(path2+'/{0}-{1}-err.txt'.format(num,i), html2+'\r\n\r\n')
					else:
						try:
							html3 = getHtml( Play )
						except Exception as err:
							writefile(path2+'/{0}-{1}-Err.txt'.format(num,i), 'Error:\r\nurl=\t'+Play)		
						else:
							try:
								Play2 = getPlay2(html3, head)
							except Exception as err:
								writefile(path2+'/{0}-{1}-err.txt'.format(num,i), html+'\r\n\r\n')
							else:
								print(Play2)

								try:
									htmlF = getHtml( Play2 )
								except Exception as err:
									writefile(path2+'/{0}-{1}-Err.txt'.format(num,i), 'Error:\r\nurl=\t'+Play2 )
								else:
									PlayF = getPlayF(htmlF)
									print(PlayF)
									writefile(path2+'/{0}-{1}-2.txt'.format(num,i), PlayF)
print("END")
writefile(path2+'/END.txt', "" )
