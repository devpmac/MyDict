import psycopg2

# con = psycopg2.connect(database="testpython", user="mcondesso", password="1234", host="127.0.0.1", port="5432")
con = psycopg2.connect(database="testpython", user="mcondesso", password="1234", host="localhost", port="5432")
# con = psycopg2.connect(database="postgres", user="postgres", password="1234", host="/var/run/postgresql", port="5432")

print("Database opened successfully")