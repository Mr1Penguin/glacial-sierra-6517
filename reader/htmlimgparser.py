from HTMLParser import HTMLParser
from PIL import Image
from io import BytesIO
import base64
import StringIO
import re
import urllib2
import datetime
import logging
import psycopg2
from multiprocessing import Pool, Manager
import time
import numbers
import gzip

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
        self.picture_count = 0
        HTMLParser.__init__(self)
    def start_parser(self, unihtml):
        args = ((ipid, self.q, self.resq) for ipid in range(self.process_count))
        self.result = self.pool.map_async(worker_loader, args)
        self.feed(unihtml)
        for x in range(self.process_count):
            self.q.put(("You", "must die", None))
        count = 0
        while (count < self.picture_count):
            count = count + 1
            img = self.resq.get()
            if (img[0]):
                if (isinstance(img[1], numbers.Number)):
                    self.curr.execute("""insert into reader_image (url, site_id, add_date, width) 
                                            values ((%s), (%s), (select clock_timestamp()), (%s))""", [img[2], self.site_id, img[1]])
                else:
                    if (img[1] == "shortcut icon"):
                        self.curr.execute("""update reader_site set favicon = (%s) where id = (%s)""", [img[2], self.site_id])
                    else:
                        self.curr.execute("""update reader_site set favicon = (%s) where id = (%s) and favicon is null""", [img[2], self.site_id])
        self.pool.close()
        self.pool.join()
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
                    self.picture_count = self.picture_count + 1
                    self.q.put((attr[1], self.root_url, False))
        if tag == "link":
            for attr in attrs:
                if attr[0] == "rel" and (attr[1] == "icon" or attr[1] == "shortcut icon"):
                    for attr2 in attrs:
                        if attr2[0] == "href":
                            self.picture_count = self.picture_count + 1
                            self.q.put((attr2[1], self.root_url, attr[1]))
    def handle_endtag(self, tag):
        if tag == "noscript":
            self.noScript = False
    def handle_data(self, data):
        if self.isTitle:
            self.isTitle = False
            self.curr.execute("""update reader_site set title = (%s) where id = (%s)""", (data, self.site_id))

def load_picture(src, root_url, isFav):
    if src == "" :
        return [False, None, None]
    src = src.strip()   
    if re.search("""^data:image/""", src, flags = re.IGNORECASE) is not None:  
        ima = Image.open(BytesIO(base64.b64decode(re.sub("""^data:image/.*?;base64,""", "", src, flags = re.IGNORECASE))))
        picture = [True, ima, None]
    else:
        if re.search("""^//""", src, flags = re.IGNORECASE) is not None:
            src = "http:" + src
        try:
            if re.search("""^https?://""", src, flags = re.IGNORECASE) is None:
                img = urllib2.urlopen("http://" + src)
                src = "http://" + src 
            else:
                img = urllib2.urlopen(src)
            picture = open_picture(img, src)
            if (not picture[0]):
                raise Exception()
        except Exception:
            try:
                parse_url = re.findall("(^.*/.*)\?.*", root_url, flags = re.IGNORECASE)
                if parse_url:
                    new_root = parse_url[0]
                else:
                    new_root = root_url
                img = urllib2.urlopen(new_root + "/" + src)
                picture = open_picture(img, src)
                if (not picture[0]):
                    raise Exception()
                src = new_root + "/" + src
            except Exception:
                while (True):
                    try:
                        parse_url2 = re.findall("^(.*\/.+)\/.+|^(.*)\/.+\/$", new_root, flags = re.IGNORECASE)
                        if parse_url2:
                            if parse_url2[0][1]:
                                new_root2 = parse_url2[0][1]
                            else:
                                if parse_url2[0][0]:
                                    new_root2 = parse_url2[0][0]
                                else:
                                    print "Fail with1", src
                                    return [False, None, None]
                        else:
                            print "Fail with2", src
                            return [False, None, None]
                        img = urllib2.urlopen(new_root2 + "/" + src)
                        picture = open_picture(img, src)
                        if (not picture[0]):
                            raise Exception()
                        src = new_root2 + "/" + src 
                        break
                    except Exception:
                        new_root = new_root2
        if (not picture):
            return [False, None, None]
        if (not picture[0]):
            return [False, None, None]
        if (picture[1] is None):
            return [True, picture[2], src]
        if (isFav):
            return [True, isFav, src]
    im = picture[1]
    if (im.size[0] >= 200) and (im.size[1] >= 200):
        return [True, im.size[0], src]
    return [False, None, None]
def open_picture(img, src):
    if img.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(img.read())
        gzip_f = gzip.GzipFile(fileobj=buf)
        html = gzip_f.read()
    else:
        html = img.read()
    try :
        im = Image.open(StringIO.StringIO(html))
    except IOError as e:
        if re.search("""\.svg""", src, flags = re.IGNORECASE) is not None:
            return [True, None, 600]
        else:
            return [False, None, None]
    except Exception as e:
        return [False, None, None]
    return [True, im, None]
def worker_loader((ipid, q, resq)):
    while (True):
        try:
            object = q.get()
            if object[2] is None:
                break;
            #print "Iam ", ipid, " work with ", object[0]
            resq.put(load_picture(object[0], object[1], object[2]))
        except Exception, e:
            print "Not quite was planned ", e
            
