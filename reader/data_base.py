

conn = None
curr = None

def activate_base():
    import psycopg2
    
    try :
        global conn
        global curr
        #conn = psycopg2.connect("dbname='mnreader' user='mpreader' password='MPreader' host='127.0.0.1'")
        conn = psycopg2.connect("dbname='postgres' user='postgres' host='db'")
        curr = conn.cursor()
    except Exception, e:
        print e
        #psycopg2.errorcodes.lookup(e.pgcode)
def add_trigger():
    curr.execute("""SELECT EXISTS (
                        SELECT 1
                        FROM   information_schema.tables 
                        WHERE  table_schema = 'public'
                        AND    table_name = 'reader_image');""")
    if curr.fetchone()[0]:
        curr.execute("""create or replace function uncheck() returns trigger as $$
                        begin 
                        if exists (select 1 from reader_image where url = new.url and site_id = new.site_id)
                        then return null;
                        end if;
                        return new;
                        end $$
                        language plpgsql;""")
        curr.execute("""do
            $$
            begin
            if not exists (select * from information_schema.triggers
            where event_object_table = 'reader_image'
            and trigger_name = 'unique_checker')
            then create trigger unique_checker before insert or update on reader_image
            for each row
            execute procedure uncheck();
            end if;
            end $$;
            """)
        conn.commit()
