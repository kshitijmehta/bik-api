import psycopg2
import psycopg2.extras


def run_db_query(query, args, action_performed):
    try:
        conn = psycopg2.connect("dbname ='bik' user='postgres' host='localhost' password='kpworks'")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, args)
        result = cur.fetchone()
        conn.commit()
        return result

    except Exception as e:
        print('action_performed:', action_performed)
        print(e)

    finally:
        cur.close()
        conn.close()
