#turkportal
import re
NAME = 'fragg_me'
BASE_URL = 'http://fragg.me'
SECTION_URL = 'http://fragg.me/%s'
ART = 'art-default.jpg'
ICON = 'icon-default.jpg'
####################################################################################################
def Start():
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
	HTTP.CacheTime = CACHE_1HOUR * 4
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0'

####################################################################################################
@handler('/video/fragg_me', NAME, thumb=ICON, art=ART)
def MainMenu():
	oc = ObjectContainer(view_group='List')
	for category in HTML.ElementFromURL(BASE_URL, cacheTime=CACHE_1WEEK).xpath('//li'):
		url =SECTION_URL % category.xpath('./a/@href')[0]
		title=category.xpath('./a')[0].text
		oc.add(DirectoryObject(key = Callback(Tags, title=title, url=url),title = title))

	return oc

####################################################################################################
@route('/video/fragg_me/videos', page=int)
def Videos(title, url, thumb, page=1):
	page = HTTP.Request(url).content
	links = re.findall('{ file\: \"(.*?)\"', page)
	summary = re.findall('<meta property="og:description" content="(.*?)">',page)
	prefix=re.findall('{ file: ".*?", height: (.*?), width: (.*?) }',page)
	oc = ObjectContainer(title2=title, view_group='List')
	for i, link in enumerate(links):
		oc.add(CreateObject(title=prefix[i][0]+'x'+prefix[i][1]+'  '+title, thumb=thumb,url=link,summary=summary[0]))
	return oc

####################################################################################################
@route('/video/fragg_me/tags')
def Tags(title,url):


	oc = ObjectContainer(view_group='List')
	for category in HTML.ElementFromURL(url, cacheTime=CACHE_1WEEK).xpath('//td'):
		url =SECTION_URL % category.xpath('./a/@href')[0]
		title=category.xpath('./a/img/@title')[0]
		thumb=category.xpath('./a/img/@src')[0]
		oc.add(DirectoryObject(key = Callback(Videos, title=title, url=url,thumb=thumb),title = title, thumb=thumb))

	return oc

####################################################################################################
@route('/video/fragg_me/createobject')
def CreateObject(url, title, thumb, summary, include_container=False):
        if url.endswith('.mp3'):
                container = 'mp3'
                audio_codec = AudioCodec.MP3
        elif  url.endswith('.m4a') or url.endswith('.mp4') or url.endswith('MPEG4') or url.endswith('h.264') or url.endswith('webm'):
                container = Container.MP4
                audio_codec = AudioCodec.AAC
        elif url.endswith('.flv') or url.endswith('Flash+Video'):
                container = Container.FLV
        elif url.endswith('.mkv'):
                container = Container.MKV

        if url.endswith('.mp3') or url.endswith('.m4a'):
                object_type = TrackObject
        elif url.endswith('.mp4') or url.endswith('MPEG4') or url.endswith('h.264') or url.endswith('.flv') or url.endswith('Flash+Video') or url.endswith('.mkv')or url.endswith('.webm'):
                audio_codec = AudioCodec.AAC
                object_type = VideoClipObject


        new_object = object_type(key = Callback(CreateObject, url=url, title=title, summary=summary, thumb=thumb, include_container=True), rating_key = url, title = title, thumb = Resource.ContentsOfURLWithFallback(thumb, fallback=R(ICON)), summary = summary,items = [MediaObject( parts = [PartObject(key=url)],container = container,audio_codec = audio_codec,audio_channels = 2)])
        
        if include_container:
                return ObjectContainer(objects=[new_object])
        else:
                return new_object
