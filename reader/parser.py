from HTMLParser import HTMLParser
from PIL import Image
from io import BytesIO
import base64
import StringIO
import re
import urllib2
import datetime
import logging
from multiprocessing import Pool, Manager
import time

class HTMLImgParser(HTMLParser):
    def __init__(self, cursor, siteid, url):
        self.curr = cursor
        self.site_id = siteid
        self.isTitle = False
        self.root_url = url
        self.noScript = False
        self.process_count = 8
        self.pool = Pool(processes=self.process_count)
        self.manager = Manager()
        self.q = self.manager.Queue()
        self.resq = self.manager.Queue()
        HTMLParser.__init__(self)
    def start_parser(self, unihtml):
        args = ((ipid, self.q, self.resq) for ipid in range(self.process_count))
        self.result = self.pool.map_async(worker_loader, args)
        self.feed(unihtml)
        #while (not self.q.empty()):
            #time.sleep(0.1)
        for x in range(self.process_count):
            self.q.put(("You", "must die", None))
        self.pool.close()
        self.pool.join()
        while (not self.resq.empty()):
            img = self.resq.get()
            if (img[0]):
                if (img[1] is None):
                    self.curr.execute("""update reader_site set favicon = (%s) where id = (%s)""", [img[2], self.site_id])
                else:
                    self.curr.execute("""insert into reader_image (url, site_id, add_date, width) 
                                        values ((%s), (%s), (select clock_timestamp()), (%s))""", [img[2], self.site_id, img[1]])
    def handle_starttag(self, tag, attrs):
        if tag == "noscript":
            self.noScript = True
        if self.noScript:
            return
        if tag == "title":
            self.isTitle = True
        if tag == "img":
            for attr in attrs:
                if attr[0] == "src":
                    self.q.put((attr[1], self.root_url, False))
        if tag == "link":
            for attr in attrs:
                if attr[0] == "rel" and (attr[1] == "icon" or attr[1] == "shortcut icon"):
                    for attr2 in attrs:
                        if attr2[0] == "href":
                            self.q.put((attr2[1], self.root_url, True))
    def handle_endtag(self, tag):
        if tag == "noscript":
            self.noScript = False
    def handle_data(self, data):
        if self.isTitle:
            self.isTitle = False
            self.curr.execute("""update reader_site set title = (%s) where id = (%s)""", (data, self.site_id))
def open_picture(src, root_url, isFav):
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
        except Exception as e:
            print "dermo"
            return [False, None, None]
    if (im.size[0] >= 200) and (im.size[1] >= 200):
        return [True, im.size[0], src]
    return [False, None, None]
def worker_loader((ipid, q, resq)):
    while (True):
        try:
            object = q.get()
            #print object
            if object[2] is None:
                break;
            #object = q.get(False, 0.05)
            #print "Iam ", ipid, " work with ", object[0]
            #print "work with ", object[0]
            resq.put(open_picture(object[0], object[1], object[2]))
        #except Queue.Empty:
            #Some problems with this exception
            #print "Why I go to sleep?"
            #time.sleep(0.1)
        except Exception, e:
            print "Not quite was planned ", e
            