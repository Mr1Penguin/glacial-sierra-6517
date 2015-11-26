from reader import activate_base
from reader import curr
from reader import conn

#def delete_old_tokens():
activate_base()
curr.execute("delete from reader_user_token where clock_timestamp()-last_use > interval '1' day")
conn.commit()
curr.close()
conn.close()