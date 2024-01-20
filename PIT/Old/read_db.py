import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('imu.db')
cursor = conn.cursor()

try:
    # Select all rows from the sensor_data table
    cursor.execute('SELECT * FROM imu')

    # Fetch all the rows
    rows = cursor.fetchall()

    # Print the column headers
    # print("ID | Acceleration X | Acceleration Y | Acceleration Z | Gyro X | Gyro Y | Gyro Z | Timestamp")

    # Print each row header
    print(f"    # |      Timestamp      | Acc. X | Acc. Y | Acc. Z | Gyro X | Gyro Y | Gyro Z")
    print( "-"*81)

    # Print each row
    for row in rows:
        print(f"{row[0]:5.0f} | {row[1]} | {row[2]:6.2f} | {row[3]:6.2f} | {row[4]:6.2f} | {row[5]:6.2f} | {row[6]:6.2f} | {row[7]:6.2f}")

finally:
    # Close the database connection
    conn.close()
