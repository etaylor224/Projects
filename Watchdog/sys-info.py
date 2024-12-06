import platform
import datetime
import psycopg
import psutil
from watcher_conf import dev_db

def gather_stats():
    hostname = platform.node()
    cpu = psutil.cpu_percent(1)
    mem = psutil.virtual_memory()[2]
    sys_os = platform.system()
    pg_instert(hostname, cpu, mem, sys_os)

def pg_instert(hostname, cpu, mem, sys_os):
    
    query = """INSERT INTO table(
        hostname,
        os,
        cpu_util_perc,
        mem_util_perc,
        run_ts
        )
    VALUES(%s, %s, %s, %s, %s)   
    """
    today = datetime.datetime.today()
    with psycopg.connect(dev_db) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (hostname, sys_os, int(cpu), int(mem), today))
        conn.commit()

if __name__ == "__main__":
    run = True
    while run:
        try:
            gather_stats()
            now = datetime.datetime.now()
            time.sleep(3600) # Run every 12 hours
        except Exception as e:
            run = False
