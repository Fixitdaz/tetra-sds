from env.example import env

import mysql.connector
from scipy.io.wavfile import write
import numpy
import struct


# Initialize mySQL connection
SQL = mysql.connector.connect(
  host=f"{env['tetra_sql_host']}",
  user=f"{env['tetra_sql_user']}",
  passwd=f"{env['tetra_sql_passwd']}",
  database=f"{env['tetra_sql_database']}"
)

CURSOR = SQL.cursor()


def voice():

        CURSOR.execute(f"SELECT \
            VoiceData \
            FROM voicegroupcall \
            WHERE DbId = 7576400 \
            ORDER BY Starttime \
            DESC LIMIT 1;"
        )

        return(CURSOR.fetchall())


blob = voice()
blob = blob[0][0]


ip = blob[0:4]
tick = blob[4:8]
length = blob[8:9]


blob_bin = blob.hex()
blob_bin = "{0:08b}".format(int(blob_bin, 16))

ip = list(ip)
tick = int.from_bytes(tick, "big")
length = length.hex()
length = "{0:08b}".format(int(length, 16))

print(len(blob))
print(len(blob_bin))
print(ip)
print(tick)
print(length)
print(list(blob[9:13]))
audio_hex = blob[9:].hex()
print(len(audio_hex))

hex_array = [audio_hex[i:i+4] for i in range(0, len(audio_hex), 4)]


int_array = [int(h, 16) for h in hex_array]

dual_array = [int_array[n:n+2] for n in range(0, len(int_array), 2)]


np_array = numpy.array(int_array)

print(type(np_array))

audio = numpy.frombuffer(np_array, numpy.int16)

write("test.wav", 8000, audio)

with open("raw.amr" , "wb") as f:
    f.write(blob[9:])
