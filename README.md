*Work in progress*

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

Input the SDS data as a hex string, outputs a dictionary with location and time information. String can be from a database binary blob, from a text file, csv or directly from a Tetra Air Interface API.

Once completed it will be as simple as:

```python
import tetra-sds

data = tetra-sds.decode(hex_string)
print(data)
```

Then get values in the returned dictionary, see models.py for layouts.

```python
latitude = data['latitude']['decimal_degrees']
longitude = data['longitude']['decimal_degrees']

# ...etc.
```


### Design

Design will probably change over time, however I'm basing everything around dictionaries rather than classes. Generally I am aiming to make the script run as quick as possible for batching large data sets and real-time processing. Looking up values in a key-value pair is faster than a bunch of 'if' statements inside a class.

Data types are looked up in the associated dictionary. Processed data is stored in dictionaries. Those dictionaries are then combined into the "master" dictionary.
