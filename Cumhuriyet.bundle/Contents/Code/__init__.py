# turkportal.org
NAME = 'cumhuriyet'
BASE_URL = 'http://www.cumhuriyet.com.tr/bolum/23/video.html'
PRE_URL =  'http://www.cumhuriyet.com.tr'
ART = 'bg.png'
ICON = 'logo.png'
SLOGAN = 'Bu ulkenin aydinlik insanlari. Size Cumhuriyet yakisir.'.encode('UTF-8')
RE_VIDEO_SUF = Regex('file: "(.*?)"')
####################################################################################################
def Start():
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
####################################################################################################
@handler('/video/cumhuriyet', NAME, thumb=ICON, art=ART)
def MainMenu():
	oc = ObjectContainer(view_group='List')
	for category in HTML.ElementFromURL(BASE_URL).xpath('//*[@id="page-wrapper"]/h1/span[3]/a'):
		url =PRE_URL + str(category.xpath('./@href')[0])
		title=category.xpath('.')[0].text.strip()
		oc.add(DirectoryObject(key = Callback(Tags, title=title, url=url),title = title, summary = SLOGAN))
	return oc
####################################################################################################
@route('/video/cumhuriyet/tags')
def Tags(title,url):
	oc = ObjectContainer(title2 = title, view_group='List')
	XHTML = HTML.ElementFromURL(url)
	
	for category in XHTML.xpath("//ul[@class='haber-3lu hor']/li/a"):
		url=PRE_URL + str(category.xpath('./@href')[0])
		title=category.xpath("./b")[0].text
		thumb=PRE_URL +category.xpath("./span/img/@src")[0]

		oc.add(DirectoryObject(key = Callback(Play, title = title, url = url, thumb =thumb ),title = title, thumb = thumb , summary = SLOGAN))

		  
	try:
		flink = XHTML.xpath("/html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/div[7]/span/a/@href")[0]
		fname = XHTML.xpath("/html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/div[7]/span/a")[0].text
		oc.add(DirectoryObject(key = Callback(Tags, title = fname, url = PRE_URL + flink),title = fname, summary = SLOGAN))
	except:
		no=None

	try:
		llink = XHTML.xpath("/html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/div[7]/span/a/@href")[1]
		lname = XHTML.xpath("/html/body/div[4]/div[1]/div[2]/div[1]/div/div[2]/div[7]/span/a")[1].text
		oc.add(DirectoryObject(key = Callback(Tags, title = lname, url = PRE_URL + llink),title = lname, summary = SLOGAN))
	except:
		no=None
	return oc

####################################################################################################
@route('/video/cumhuriyet/play')
def Play(url, title, thumb):
        link=HTTP.Request(url).content
	try:
                oc = ObjectContainer()
		url2 = RE_VIDEO_SUF.search(link)
		url=PRE_URL + str(url2.group(1))
		oc.add(VideoClipObject(key = Callback(Lookup, url = url, title = title, thumb = thumb),	rating_key = url,title = title,	thumb = thumb, items = [MediaObject(parts = [PartObject(key = url)],optimized_for_streaming = True)]))
		return oc

	except:
		return MessageContainer("Hata","Bu Haber Server da yok..")

####################################################################################################
@route('/video/cumhuriyet/lookup')
def Lookup(url, title, thumb):
    oc = ObjectContainer()
    oc.add(VideoClipObject(
	key = Callback(Lookup, url = url, title = title, thumb = thumb),
	rating_key = url,
	title = title,
	thumb = thumb,
	items = [
	    MediaObject(
		parts = [PartObject(key = url)],
		optimized_for_streaming = True
	    )
	]
    ))
    return oc
