import env
from decode import sds
import mysql.connector
import copy




'''
Example script for bulk decoding of Tetra sds data from a MySQL database
Create a env.py file with your connection variables
'''



def connectMySQL() -> mysql.connector:
	'''
	Establishes the MySQL connection
	Returns the connector object
	'''
	SQL = mysql.connector.connect(
		host=env.tetra_sql_host,
		user=env.tetra_sql_user,
		passwd=env.tetra_sql_passwd,
		database=env.tetra_sql_database
		)
	return(SQL)


def getPositions(
		CURSOR: mysql.connector,
		ssi: int,
		points: int
	) -> list:
	'''
	Performs the MySQL query
	Returns the result as a list
	'''
	CURSOR.execute(f"SELECT \
		Timestamp, \
		UserData \
		FROM sdsdata \
		WHERE CallingSsi = {ssi} \
		AND UserDataLength = 129 \
		ORDER BY Timestamp \
		DESC LIMIT {points};"
	)
	results = CURSOR.fetchall()
	results = list(results)

	return(results)


def run() -> list:
	'''
	Run example
	'''
	results = []
	SQL = connectMySQL()
	CURSOR = SQL.cursor()
	positions = getPositions(CURSOR, 23071, 100)

	for position in positions:
		data = position[1]
		decoded = sds(data)
		results.append(decoded)
	
	return(results)


if __name__ == "__main__":
	results = run()
	
	for result in results:
		print(result['time']['seconds'])
