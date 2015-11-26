from .data_base import *

activate_base()
curr.execute("delete from reader_user_token where clock_timestamp()-last_use > interval '1' day")
conn.commit()
curr.close()
conn.close()