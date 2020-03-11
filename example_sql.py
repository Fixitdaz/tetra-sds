from env.example import env

from decode import sds
import mysql.connector



# Initialize mySQL connection
SQL = mysql.connector.connect(
  host=f"{env['tetra_sql_host']}",
  user=f"{env['tetra_sql_user']}",
  passwd=f"{env['tetra_sql_passwd']}",
  database=f"{env['tetra_sql_database']}"
)

CURSOR = SQL.cursor()


def latestPosition(ssi):
        ssi = str(ssi)
        CURSOR.execute(f"SELECT \
            Timestamp, \
            UserData \
            FROM sdsdata \
            WHERE CallingSsi = {ssi} \
            AND UserDataLength = 129 \
            ORDER BY Timestamp \
            DESC LIMIT 1;"
        )

        return(CURSOR.fetchall())


pos = latestPosition(23071)
hex_string = pos[0][1].hex()
hex_string = hex_string.rstrip("0")
print(hex_string)
location = sds(hex_string)
print(location)