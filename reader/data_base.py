import psycopg2

conn = None
curr = None

def activate_base():
    try :
        global conn
        global curr
        conn = psycopg2.connect("dbname='mnreader' user='mpreader' password='MPreader'")
        curr = conn.cursor()
    except Exception, e:
        psycopg2.errorcodes.lookup(e.pgcode)
def add_trigger():
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
