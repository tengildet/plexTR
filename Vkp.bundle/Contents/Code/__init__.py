import re
NAME = 'VK Porn'
ART = 'art.png'
ICON = 'icon.png'
PROXY = 'http://smartsmart.pusku.com/enigma/prox.php?url='
BASE_URL = 'http://vkporno.com'
RE_VIDEO_URLS = Regex('<option.*?value=(.*?)>')
RE_VIDEO_URL = Regex ("id='film_main' src='(.*?)'")
####################################################################################################
def Start():
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
####################################################################################################
@handler('/video/vkp', NAME, thumb=ICON, art=ART)
def MainMenu():
	oc = ObjectContainer(view_group='List')
	for category in HTML.ElementFromURL(BASE_URL).xpath("//a[contains (@class, 'vkcat')]"):
		url =str(category.xpath('./@href')[0])
		title=category.xpath('.')[0].text
		oc.add(DirectoryObject(key = Callback(Tags, title=title, url=url),title = url[19:-1].upper()))
	return oc
####################################################################################################
@route('/video/vkp/tags')
def Tags(title,url, pag=1):
        tagsurl = url + 'page/' + str(pag)+'/' 
	oc = ObjectContainer(view_group='List')
	XHTML = HTML.ElementFromURL(tagsurl)
	for category in XHTML.xpath("//div[@id='videokno']"):
                urla=category.xpath("./div[@class='pornolink']/h2/a/@href")[0]
                title=category.xpath("./div[@class='pornolink']/h2/a")[0].text
                thumb=category.xpath("./a/img[@class='grab']/@src")[0]
                oc.add(DirectoryObject(key = Callback(Videom, title=title, url=urla, thumb = thumb),title = title, thumb=thumb, summary = 'turkportal.org'))
        if XHTML.xpath('//*[@id="navi"]'):
                pagx = int(pag)+1
                oc.add(DirectoryObject(key = Callback(Tags, title=title, url=url, pag=pagx),title = 'Next Page', thumb=thumb, summary = 'turkportal.org'))
                
	return oc
####################################################################################################
@route('/video/vkp/videom')
def Videom(title, url, thumb):
	oc = ObjectContainer(view_group='List')
	data = HTTP.Request(url).content
	videos = re.findall('<option.*?value=(.*?)>',data)
	if videos:
		for i, vid in enumerate(videos):
			oc.add(VideoClipObject(url=vid.replace('vkontakte.ru', 'vk.com').replace('\"','').replace('\'',''),title = 'PART'+str(i+1) + ' ' + title, thumb = thumb))
	else:
		video = RE_VIDEO_URL.search(data)
		oc.add(VideoClipObject(url=video.group(1).replace('vkontakte.ru', 'vk.com'),title = title, thumb = thumb))
	return oc



