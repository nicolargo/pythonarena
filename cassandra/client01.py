# https://github.com/dkoepke/cassandra-python-driver/blob/master/example.py

from cassandra import AlreadyExists
from cassandra.cluster import Cluster

cluster = Cluster()
session = cluster.connect()
try:
    session.execute("""
        CREATE KEYSPACE %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % "foo")
except AlreadyExists:
    pass
session.set_keyspace("foo")
try:
    session.execute("""
        CREATE TABLE foo_tab (
            key int,
            value int,
            PRIMARY KEY (key))
        """)
except AlreadyExists:
    pass
for i in range(1, 10):
    session.execute("INSERT INTO foo_tab (key, value) VALUES (%s, %s)", [i, i * 10])

future = session.execute_async("SELECT * FROM foo_tab")
try:
    rows = future.result()
except Exception:
    pass
for r in rows:
    print(r)
