NAME = 'Turkportal'
ART = 'backdrop.png'
ICON = 'turkportal.png'
BASE_URL = 'http://satura.tk/deneme/plex/json.php'
####################################################################################################
def Start():
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
####################################################################################################
@handler('/video/turkportal', NAME, thumb=ICON, art=ART)
def MainMenu(title='turkportal',url=BASE_URL, sayac=0):
	oc = ObjectContainer(view_group='List')
	for category in JSON.ObjectFromURL(url):
		summary = category['Aciklama']
		if 'img src' in summary:
                        summary = 'turkportal.org'
		title=category['Baslik']
		protect=category['Koruma']
		try:
			thumb=category['Resim']
		except:
			thumb = R(ICON)
		if category['Stream']:
                        try :
                                url = category['Stream']

                                if not ('vk' in url or 'youtube' in url or 'dailymotion' in url or 'watchfreeinhd' in url or 'api.video' in url):
                                        oc.add(VideoClipObject(
                                                key = Callback(Lookup, url = url, title = title, thumb = thumb, summary = summary,),
                                                rating_key = '3',
                                                title = title,
                                                summary = summary,
                                                thumb = thumb,
                                                items = [
                                                        MediaObject(
                                                                parts = [PartObject(key = '3')],
                                                                optimized_for_streaming = True)]))
                                else:
                                        if not ('api.video' in url):
                                                oc.add(VideoClipObject(url = url, title = title, thumb = thumb, summary = summary))


			
                        except:
                                print 'yok'
                else:
                        if (Prefs['Adult']<>'Evet'):
                                if (category['Koruma']==False):
                                        url = category['Playlist']
                                        oc.add(DirectoryObject(key = Callback(MainMenu, title=title, url=url, sayac=1),title =title, thumb=thumb, summary=summary))
                        else:                              
                                url = category['Playlist']
                                oc.add(DirectoryObject(key = Callback(MainMenu, title=title, url=url, sayac=1),title =title, thumb=thumb, summary=summary))
        if sayac==0:
                oc.add(PrefsObject(title = 'Ayarlar',summary = 'Turkportal ayarlarini buradan yapabilirsiniz.', art=ObjectContainer.art))

	return oc
####################################################################################################
@route('/video/turkportal/lookup')
def Lookup(url, title, thumb, summary):
    oc = ObjectContainer()
    oc.add(VideoClipObject(
	key = Callback(Lookup, url = url, title = title, thumb = thumb, summary = summary,),
	rating_key = '3',
	title = title,
        summary = summary,
	thumb = thumb,
	items = [
	    MediaObject(
		parts = [PartObject(key = url)],
		optimized_for_streaming = True
	    )
	]
    ))
    return oc
