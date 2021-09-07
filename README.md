# tetra-sds
Tetra Advanced Radio Digital Information System

*T.A.R.D.I.S*
(I wanted it to spell TARDIS OK.)

Decodes Tetra Terrestrial Trunked Radio Time and Location Data in *Time and Space...*

Based on the ETSI Standard:
https://www.etsi.org/deliver/etsi_ts/100300_100399/1003921801/01.03.01_60/ts_1003921801v010301p.pdf

## Overview
Tetra is a digital two-way radio standard, used not only for voice but for Short Data Services (SDS) as well. This project is a python implementation for decoding said data. 

### Usage
Input the SDS data as a hex string or raw binary, outputs a dictionary with location, velocity, direction and time information. Data can be from a database binary blob, a text file, csv or directly from a Tetra Air Interface API.

```python
import tetra-sds.decode as decode

data = decode.sds(hex_string)
print(data)
```

Then get values in the returned dictionary, print it to get layout.

```python
latitude = data['location']['latitude']['decimal_degrees']
longitude = data['location']['longitude']['decimal_degrees']
speed = data['velocity']['kmh']

# ...etc.
```

It also may be of benifit to sort by epoc (ascending)

```python
locations = sorted(locations, reverse=False, key=lambda k: k['time']['epoc']) 
```

Do what you wish with this data, such as create a list of lat,lon tuples or converting into a geojson.

```python

path = [ (pos['location']['latitude']['decimal_degrees'], pos['location']['longitude']['decimal_degrees']) for pos in locations ]

```

### Design

The various data types are matched in the "lookup.py" file.

Processed data is stored in dictionaries. Those dictionaries are then combined into the "master" dictionary.
