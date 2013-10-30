NAME = 'Turkportal'
ART = 'backdrop.png'
ICON = 'turkportal.png'
BASE_URL = 'http://tengildet.byethost14.com/plex/plextrkp.php?port=800'

####################################################################################################
def Start():
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
####################################################################################################
@handler('/video/turkportal', NAME, thumb=ICON, art=ART)
def MainMenu(title='ert',url=BASE_URL):
	oc = ObjectContainer(view_group='List')
	for category in XML.ElementFromURL(url).xpath('//channel'):
                title=category.xpath('./title')[0].text
                try:
                        thumb=category.xpath('./logo_30x30')[0].text
                except:
                        thumb = R(ICON)
                try :
                        url = category.xpath('.//stream_url')[0].text

                        if not ('vk' in url or 'youtube' in url or 'dailymotion' in url or 'watchfreeinhd' in url):
                        
                                oc.add(VideoClipObject(
                                        key = Callback(Lookup, url = url, title = title, thumb = thumb),
                                        rating_key = url,
                                        title = title,
                                        thumb = thumb,
                                        items = [
                                                MediaObject(
                                                        parts = [PartObject(key = url)],
                                                        optimized_for_streaming = True)]))
                        else:
                                oc.add(VideoClipObject(url = url, title = title, thumb = thumb))


                        
                except:
                        url = category.xpath('.//playlist_url')[0].text
                        oc.add(DirectoryObject(key = Callback(MainMenu, title=title, url=url),title =title, thumb=thumb))

	return oc
####################################################################################################
@route('/video/turkportal/lookup')
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
