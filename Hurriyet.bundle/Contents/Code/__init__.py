NAME = 'hurriyet'
BASE_URL = 'http://webtv.hurriyet.com.tr/'
#SECTION_URL = 'http://www.milliyet.tv'
ART = 'bg.png'
ICON = 'logo.png'
RE_VIDEO = Regex("videoMp4Url = '(.*?)';")
####################################################################################################
def Start():
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
####################################################################################################
@handler('/video/hurriyet', NAME, thumb=ICON, art=ART)
def MainMenu():
	oc = ObjectContainer(view_group='List')
	for category in HTML.ElementFromURL(BASE_URL).xpath("//div[@class='HeaderHolder']/div[@class='HeaderMenu FR']/ul[@class='MainMenu clr']/li"):
		url =str(category.xpath('./a/@href')[0])
		title=category.xpath('./a')[0].text
                oc.add(DirectoryObject(key = Callback(Tags, title=title, url=url),title = title, summary = 'Her Zaman Okudugunuz Gazeteyi Simdi Seyredin...'))
	return oc
####################################################################################################
@route('/video/hurriyet/tags')
def Tags(title,url):
	oc = ObjectContainer(title2 = title, view_group='List')
	for category in HTML.ElementFromURL(url).xpath("//ul[@class='VideoContainer clr']/li"):
                url=category.xpath('./a/@href')[0]
		title=category.xpath("./a[contains (@class,'videoTitle')]")[0].text
		thumb=category.xpath("./a/img/@src")[0]
		#summary = category.xpath("./p")[0].text.strip()
		#summary1 = category.xpath("./p/strong[1]")[0].text.strip().title()
		#summary2 = category.xpath("./p/strong[2]")[0].text.strip()
                oc.add(VideoClipObject(url=url,title = title, thumb=thumb))
	return oc
