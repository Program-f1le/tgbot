from sqlalchemy import text
from database import engine
from datetime import *
from data_name import table_name
def insert_data(time: str, event: str, name: str):
    if event.lower() != 'контрольная' and event.lower() != 'олимпиада':
        name = 'all'
    year = int(time[0:4])
    month = int(time[5:7])
    day = int(time[8:10])
    hour = str(time[11:16])
    if len(hour) == 4:
        h = int(hour[0])
        m = int(hour[2::])
    else:
        h = int(hour[:2])
        m = int(hour[3::])
    if datetime(year, month, day, h, m) < datetime.now():
        return False
    with engine.connect() as conn:
        a = conn.execute(text(f'select id from {table_name}')).all()
        r = []
        b = ''
        if a == []:
            a = 0
        else:
            for j in a:
                j = str(j)
                for i in range(1, len(j)):
                    if j[i] == ',':
                        break
                    else:
                        b += str(j[i])
                b = int(b)
                r.append(b)
                b = ''
                a = max(r)
        conn.execute(text(f'''insert into {table_name} (id, year, month, day, time, event, for_who) values ({a + 1}, '{year}', '{month}', '{day}', '{hour}', '{event}', '{name}');'''))
        conn.commit()

def del_data(b: int):
    with engine.connect() as conn:
        conn.execute(text(f'''delete from {table_name} where id='{b}';'''))
        conn.execute(text(f'update {table_name} set id = id - 1 where id > {b};'))
        conn.commit()

def today_user(day: int, user: str):
    res = []
    with engine.connect() as conn:
        a = conn.execute(text(f'''select id from {table_name} where day='{day}' and for_who= '{user}';''')).all()
        for j in a:
            j = str(j)
            b = ''
            r = ''
            t = ''
            o = ''
            for i in range(1, len(j)):
                if j[i] == ',':
                    break
                else:
                    b += str(j[i])
            b = int(b)
            r = str(conn.execute(text(f'''select event from {table_name} where id='{b}';''')).first())
            t = str(conn.execute(text(f'''select time from {table_name} where id='{b}';''')).first())
            b = ''
            for i in range(2, len(r)):
                if r[i] == "'":
                    break
                else:
                    b += str(r[i])
            o += b + ' в '
            b = ''
            for i in range(2, len(t)):
                if t[i] == "'":
                    break
                else:
                    b += str(t[i])
            o += b
            res.append(o)
    return ' '.join(res)

def today_all(day: int):
    res = []
    with engine.connect() as conn:
        a = conn.execute(text(f'''select id from {table_name} where day='{day}' and for_who= 'all';''')).all()

        for j in a:
            j = str(j)
            b = ''
            o = ''
            for i in range(1, len(j)):
                if j[i] == ',':
                    break
                else:
                    b += str(j[i])
            b = int(b)
            r = str(conn.execute(text(f'''select event from {table_name} where id='{b}';''')).first())
            t = str(conn.execute(text(f'''select time from {table_name} where id='{b}';''')).first())
            b = ''
            for i in range(2, len(r)):
                if r[i] == "'":
                    break
                else:
                    b += str(r[i])
            o += b + ' в '
            b = ''
            for i in range(2, len(t)):
                if t[i] == "'":
                    break
                else:
                    b += str(t[i])
            o += b
            res.append(o)
    return ' '.join(res)

def check_data(time: str):
    if time == '':
        return False
    year = int(time[0:4])
    month = int(time[5:7])
    day = int(time[8:10])
    hour = str(time[11:16])
    if len(hour) == 4:
        h = int(hour[0])
    else:
        h = int(hour[:2])
    try:
        datetime(year, month, day, h, int(hour[3::]))
    except:
        return False
    else:
        return True
