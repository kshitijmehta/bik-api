import psycopg2
import psycopg2.extras
import secrets
from authserver import app


def run_db_query(query, args, action_performed, perform_fetch, fetch_multi=False):

    try:

        conn = psycopg2.connect(f"dbname ='{secrets.secrets['DB_NAME']}' "
                                f"user='{secrets.secrets['DB_USER']}' "
                                f"host='{secrets.secrets['DB_HOST']}' "
                                f"password='{secrets.secrets['DB_PASSWORD']}'")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # print(query)
        # print('/n')
        # print(args)
        cur.execute(query, args)
        result = None
        if perform_fetch:
            if fetch_multi:
                result = cur.fetchall()
            else:
                result = cur.fetchone()
        conn.commit()
        return result

    except Exception as e:
        print('action_performed:', action_performed)
        app.logger.debug(e)
        print(cur.query)
        return 'error'

    finally:
        cur.close()
        conn.close()


def run_db_query_multiple(query, args, action_performed, perform_fetch, can_commit):
    try:

        conn = psycopg2.connect(f"dbname ='{secrets.secrets['DB_NAME']}' "
                                f"user='{secrets.secrets['DB_USER']}' "
                                f"host='{secrets.secrets['DB_HOST']}' "
                                f"password='{secrets.secrets['DB_PASSWORD']}'")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, args)
        result = None
        if perform_fetch:
            result = cur.fetchone()['_prod_id']

        if can_commit:
            conn.commit()
            return result

    except (Exception, psycopg2.DatabaseError) as e:
        print('action_performed:', action_performed)
        print("Error in Action Reverting all other operations of a Action ", e)
        app.logger.debug(e)
        conn.rollback()
        return 'error'

    finally:
        cur.close()
        conn.close()
