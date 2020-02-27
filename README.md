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

Input the SDS data as a hex string, outputs a dictionary with location, velocity, direction and time information. String can be from a database binary blob, from a text file, csv or directly from a Tetra Air Interface API.

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

If batching in a for loop, remember to do deep copies of the dictionary:

```python
import tetra-sds.decode as decode
import copy

locations = []
hex_strings = [list_of_hex_strings]

for hex_string in hex_strings:
    location = decode.sds(hex_string)
    locations.append(copy.deepcopy(location))

```

Do what you wish with this data, such as create a list of lat,lon tuples or converting into a geojson.

```python

path = [ (pos['location']['latitude']['decimal_degrees'], pos['location']['longitude']['decimal_degrees']) for pos in locations ]

```

### Design

The various data types are matched in the "lookup.py" file.

Processed data is stored in dictionaries. Those dictionaries are then combined into the "master" dictionary.
