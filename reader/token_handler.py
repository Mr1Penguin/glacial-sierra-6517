import htmlimgparser
import data_base
import urllib2

if __name__ == '__main__':
    data_base.activate_base()
    curr = data_base.curr
    conn = data_base.conn
    curr.execute("delete from reader_user_token where clock_timestamp()-last_use > interval '1' day")
    
    curr.execute("""select id, url from reader_site""")
    sites = curr.fetchall()
    for site in sites:
        url = site[1]
        try:
            response = urllib2.urlopen(url)
        except Exception as e:
            print e
            pass
        else:
            html = response.read()
            if not isinstance(html, unicode):
                try: 
                    unihtml = unicode(html, 'utf-8')
                except UnicodeError:
                    unihtml = html.decode('cp1251').encode('utf8')
            else:
                unihtml = html
            parserst = htmlimgparser.HTMLImgParser(curr, site[0], url)
            parserst.start_parser(unihtml)

    conn.commit()
    curr.close()
    conn.close()
