from HTMLParser import HTMLParser

class HTMLImgParser(HTMLParser):
    isTitle = False
    curr = None
    site_id = None
    def __init__(self, cursor, siteid):
        self.curr = cursor
        self.site_id = siteid
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.isTitle = True
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src":
                    self.curr.execute("""insert into reader_image (url, site_id, add_date, width) 
                                        values ((%s), (%s), (select clock_timestamp()), 100)""", (attr[1], self.site_id))
    def handle_data(self, data):
        if self.isTitle:
            self.isTitle = False
            #print ":".join("{:02x}".format(ord(c)) for c in data)
            data = data.decode('cp1251').encode('utf8')
            self.curr.execute("""update reader_site set title = (%s) where id = (%s)""", (data, self.site_id))
            