from HTMLParser import HTMLParser
from PIL import Image
from io import BytesIO
import base64
import StringIO
import re
import urllib2

class HTMLImgParser(HTMLParser):
    def __init__(self, cursor, siteid, url):
        self.curr = cursor
        self.site_id = siteid
        self.isTitle = False
        self.root_url = url
        self.noScript = False
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        #print tag
        if tag == "noscript":
            self.noScript = True
        if self.noScript:
            return
        if tag == "title":
            self.isTitle = True
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src":
                    picture = self.open_picture(attr[1], self.root_url, False)
                    if picture[0]:
                        self.curr.execute("""insert into reader_image (url, site_id, add_date, width) 
                                        values ((%s), (%s), (select clock_timestamp()), (%s))""", [picture[2], self.site_id, picture[1]])
        if tag == "link":
            for attr in attrs:
                if attr[0] == "rel" and (attr[1] == "icon" or attr[1] == "shortcut icon"):
                    for attr2 in attrs:
                        if attr2[0] == "href":
                            favicon = self.open_picture(attr2[1], self.root_url, True)
                            if favicon[0]:
                                self.curr.execute("""update reader_site set favicon = (%s) where id = (%s)""", [favicon[2], self.site_id])
    def handle_endtag(self, tag):
        if tag == "noscript":
            self.noScript = False
    def handle_data(self, data):
        if self.isTitle:
            self.isTitle = False
            self.curr.execute("""update reader_site set title = (%s) where id = (%s)""", (data, self.site_id))
    def open_picture(self, src, root_url, isFav):
        if src == "" :
            return [False, None, None]
        if re.search("""^data:image/""", src, flags = re.IGNORECASE) is not None:       
            im = Image.open(BytesIO(base64.b64decode(re.sub("""^data:image/.*?;base64,""", "", src, flags = re.IGNORECASE))))
        else:
            if re.search("""^//""", src, flags = re.IGNORECASE) is not None:
                src = "http:" + src
            try:
                if re.search("""^http://""", src, flags = re.IGNORECASE) is None:
                    img = urllib2.urlopen("http://" + src)
                    src = "http://" + src 
                else:
                    img = urllib2.urlopen(src)
            except Exception:
                try:
                    img = urllib2.urlopen(root_url + "/" + src)
                    src = root_url + "/" + src 
                except Exception:
                    return [False, None, None]
            if isFav:
                return [True, None, src]
            html = img.read()
            try :
                im = Image.open(StringIO.StringIO(html))
            except IOError as e:
                if re.search("""\.svg""", src, flags = re.IGNORECASE) is not None:
                    return [True, 600, src]
                else:
                    return [False, None, None]
        if (im.size[0] >= 200) and (im.size[1] >= 200):
            return [True, im.size[0], src]
        return [False, None, None]
               