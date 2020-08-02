import psycopg2
import psycopg2.extras
import secrets


def run_db_query(query, args, action_performed, perform_fetch):
    try:
        conn = psycopg2.connect(f"dbname ='{secrets.secrets['DB_NAME']}' "
                                f"user='{secrets.secrets['DB_USER']}' "
                                f"host='{secrets.secrets['DB_HOST']}' "
                                f"password='{secrets.secrets['DB_PASSWORD']}'")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, args)
        result = None
        if perform_fetch:
            result = cur.fetchone()
        conn.commit()
        return result

    except Exception as e:
        print('action_performed:', action_performed)
        print(e)
        return 'error'

    finally:
        cur.close()
        conn.close()
