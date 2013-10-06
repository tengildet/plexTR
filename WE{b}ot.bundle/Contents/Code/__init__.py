NAME = 'WE{b}ot'
ART = 'art.png'
ICON = 'icon.png'
####################################################################################################
def Start():
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	DirectoryObject.thumb = R(ICON)
####################################################################################################
@handler('/video/webot', NAME, thumb=ICON, art=ART)
def MainMenu(title='ert',url='http://smartsmart.pusku.com/enigma/zortals/webotyok.xml'):
	oc = ObjectContainer(view_group='List')
	for category in XML.ElementFromURL(url).xpath('//channel'):
                title=category.xpath('./title')[0].text
                try:
                        thumb=category.xpath('./logo_30x30')[0].text
                except:
                        thumb = R(ICON)
                try :
                        url = category.xpath('.//stream_url')[0].text
                        oc.add(VideoClipObject(url=url,title =title,thumb=thumb))
                except:
                        url = category.xpath('.//playlist_url')[0].text
                        oc.add(DirectoryObject(key = Callback(MainMenu, title=title, url=url),title =title, thumb=thumb))
        #oc.add(VideoClipObject(key = RTMPVideoURL(url = 'rtmp://live190.la3.origin.filmon.com:1935/live/',clip ='246.high.stream', rating_key = '123',title = '123')))
	return oc


