NAME = 'milliyet'
BASE_URL = 'http://www.milliyet.tv/Milliyet-Tv/'
SECTION_URL = 'http://www.milliyet.tv'
ART = 'bg.png'
ICON = 'logo.jpg'
RE_VIDEO_URL = Regex("videoMp4Url = '(.*?)';")
####################################################################################################
def Start():
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
####################################################################################################
@handler('/video/milliyet', NAME, thumb=ICON, art=ART)
def MainMenu():
	oc = ObjectContainer(view_group='List')
	for category in HTML.ElementFromURL(BASE_URL).xpath("//div[@class='kategoriler tumu']/div[@class='tumuBox tumuYeni']/ul/li"):
		url =str(category.xpath('./a/@href')[0])
		if not 'http'in url:
                        url = SECTION_URL + url
		title=category.xpath('./a')[0].text
		if not (('http://www.milliyet.com.tr' in url) or ('nevidyo' in url) or ('Haftanin' in url) or ('Ana Sayfa'in title)) :
                        oc.add(DirectoryObject(key = Callback(Tags, title=title, url=url),title = title))
	return oc
####################################################################################################
@route('/video/milliyet/tags')
def Tags(title,url):
	oc = ObjectContainer(view_group='List')
	for category in HTML.ElementFromURL(url).xpath("//div[@class='kategoriIn']/ul[@class='aramaList']/li"):
                url=category.xpath('./a/@href')[0]
		title=category.xpath('./h4/a')[0].text
		thumb=category.xpath("./a[@class='videoSmall']/img/@src")[0]
		summary = category.xpath("./p")[0].text.strip()
		summary1 = category.xpath("./p/strong[1]")[0].text.strip().title()
		summary2 = category.xpath("./p/strong[2]")[0].text.strip()
                #oc.add(VideoClipObject(url=url,title = title, thumb=thumb, summary = summary+summary1+'\n'+'Izlenme: '+summary2))
		oc.add(DirectoryObject(key = Callback(Play, url=url,title = title, thumb=thumb),title = title, thumb=thumb, summary = summary+summary1+'\n'+'Izlenme: '+summary2))

	return oc

####################################################################################################
@route('/video/milliyet/play')
def Play(url, title, thumb):
	data = HTTP.Request(url).content
	try:
                oc = ObjectContainer()
		video = RE_VIDEO_URL.search(data)
		oc.add(VideoClipObject(key = Callback(Lookup, url = video.group(1), title = title, thumb = thumb),	rating_key =video.group(1) ,title = title,	thumb = thumb, items = [MediaObject(parts = [PartObject(key = video.group(1))],optimized_for_streaming = True)]))
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
