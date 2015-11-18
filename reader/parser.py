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
        #print tag
        if tag == "title":
            self.isTitle = True
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src":
                    self.curr.execute("""insert into reader_image (url, site_id, add_date, width) 
                                        values ((%s), (%s), (select clock_timestamp()), 100)""", (attr[1], self.site_id))
        if tag == "link":
            for attr in attrs:
                if attr[0] == "rel" and (attr[1] == "icon" or attr[1] == "shortcut icon"):
                    for attr2 in attrs:
                        if attr2[0] == "href":
                            self.curr.execute("""update reader_site set favicon = (%s) where id = (%s)""", [attr2[1], self.site_id])
    def handle_data(self, data):
        if self.isTitle:
            self.isTitle = False
            self.curr.execute("""update reader_site set title = (%s) where id = (%s)""", (data, self.site_id))

            