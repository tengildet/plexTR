NAME = 'milliyet'
BASE_URL = 'http://www.milliyet.tv/Milliyet-Tv/'
SECTION_URL = 'http://www.milliyet.tv'
ART = 'bg.png'
ICON = 'logo.jpg'
RE_VIDEO = Regex("videoMp4Url = '(.*?)';")
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
                oc.add(VideoClipObject(url=url,title = title, thumb=thumb, summary = summary+summary1+'\n'+'Izlenme: '+summary2))
	return oc
