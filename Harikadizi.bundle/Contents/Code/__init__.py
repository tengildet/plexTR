import re
NAME = 'Harika Dizi'
BASE_URL = 'http://www.harikadizi.net/'

ART = 'art-default.jpg'
ICON = 'icon-default.png'


####################################################################################################
def Start():

	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')

	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)

	HTTP.CacheTime = CACHE_1HOUR * 4
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'

####################################################################################################
@handler('/video/harikadizi', NAME, thumb=ICON, art=ART)
def MainMenu():
	oc = ObjectContainer(view_group='List')
	#for category in HTML.ElementFromURL(BASE_URL).xpath('//div[@class="ustmenu"]/div/ul/li'):
         #       url =category.xpath('./a/@href')[0]
          #      title=category.xpath('./a')[0].text.upper()
           #     oc.add(DirectoryObject(key = Callback(Films, url=url),title = title, thumb=R(ICON)))
        oc.add(DirectoryObject(key = Callback(Films, url='http://www.harikadizi.net/category/yerli-diziler/'),title = 'Son Eklenen Yerli Diziler', thumb=R(ICON)))
        oc.add(DirectoryObject(key = Callback(Films, url='http://www.harikadizi.net/category/yabanci-diziler/'),title = 'Son Eklenen Yabanci Diziler', thumb=R(ICON)))
        oc.add(DirectoryObject(key = Callback(Yabalf, url='http://www.harikadizi.net/'),title = 'Alfabetik Sirali Yabanci Diziler', thumb=R(ICON)))
        oc.add(DirectoryObject(key = Callback(Yeralf, url='http://www.harikadizi.net/'),title = 'Alfabetik Sirali Yerli Diziler', thumb=R(ICON)))

	return oc



####################################################################################################
@route('/video/harikadizi/films')
def Films(url):

	oc = ObjectContainer(view_group='List')

	for category in HTML.ElementFromURL(url).xpath('//div[@class="ortablokorta"]/div/a'):
		url =category.xpath('./@href')[0]
		title=category.xpath('./@title')[0]
		#thumb=category.xpath('./div/img/@src')[0]
		#summary=category.xpath('./div/div[3]/span')[0].text
		oc.add(DirectoryObject(key = Callback(Parts, title=title, url=url),title = title))

	return oc

####################################################################################################
@route('/video/harikadizi/parts')
def Parts(title, url):
	oc = ObjectContainer(view_group='List')
	for category in HTML.ElementFromURL(url).xpath('//iframe'):
		url =category.xpath('./@src')[0]
		if 'vk.com' in url or 'youtube' in url or 'dailymotion' in url:
                        oc.add(VideoClipObject(url=url,title = title))
	return oc
####################################################################################################
@route('/video/harikadizi/yabalf')
def Yabalf(url):
	oc = ObjectContainer(view_group='List')

	for category in HTML.ElementFromURL(url).xpath('//div[@id="yabancidiziler"]/a'):
		url =category.xpath('./@href')[0]
		title=category.xpath('./div')[0].text
		oc.add(DirectoryObject(key = Callback(YabalfBol, title=title, url=url),title = title))

	return oc
####################################################################################################
@route('/video/harikadizi/yabalfbol')
def YabalfBol(title, url):
	oc = ObjectContainer(view_group='List')
	for category in HTML.ElementFromURL(url).xpath('//div[@style="float:left;"]'):
		url =category.xpath('./a/@href')[0]
		title = category.xpath('./a/@title')[0]
		thumb = category.xpath('./a/div/img/@src')[0]
		oc.add(DirectoryObject(key = Callback(Parts, title=title, url=url),title = title, thumb = thumb))

	return oc
####################################################################################################
@route('/video/harikadizi/yeralf')
def Yeralf(url):
	oc = ObjectContainer(view_group='List')

	for category in HTML.ElementFromURL(url).xpath('//div[@class="art-BlockContent-body"]/ul/li'):
		url =category.xpath('./a/@href')[0]
		title=category.xpath('./a/div')[0].text
		oc.add(DirectoryObject(key = Callback(YFilms, url=url),title = title))

	return oc
####################################################################################################
@route('/video/harikadizi/yfilms')
def YFilms(url):

	oc = ObjectContainer(view_group='List')

	for category in HTML.ElementFromURL(url).xpath('//div[@class="ortablokorta"]/div/a'):
		url =category.xpath('./@href')[0]
		title=category.xpath('./@title')[0]
		#thumb=category.xpath('./div/img/@src')[0]
		#summary=category.xpath('./div/div[3]/span')[0].text
		oc.add(DirectoryObject(key = Callback(Parts, title=title, url=url),title = title))

	return oc
