import snowflake.connector

config = {
    'account': 'BFMYMSS-MH97378',
    'user': 'Gaurav',
    'password': 'Gaurav@818',
    'warehouse': 'compute_wh',
    'database': 'firstdata_store_id',
    'schema': 'firstdatabase'
}
print("hello")
cursor = None
try:
    conn = snowflake.connector.connect(**config)
    print("connection sucess")
    cursor = conn.cursor()

  
    cursor.execute("SELECT * FROM store_status LIMIT 5")

    results = cursor.fetchall()
    for row in results:
        print(row)

except snowflake.connector.Error as e:
    print(f"Snowflake error: {e}")

finally:
    if cursor:
        cursor.close()
        conn.close()