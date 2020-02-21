from models import master, pdu_type, pdu_type_extension, time_type, pdu_data, time_data, location_shape, \
    location_data, velocity_data, velocity_type
from env.example import env

import time
from datetime import datetime
from dateutil import tz



def get_time_data(bits):
    '''Takes binary string, returns time information dictionary
    '''

    # Convert day (4 bits)
    time_data['bits']['day'] = bits[0:5]
    time_data['utc']['day'] = int(bits[0:5], 2)

    # Convert hour (4 bits)
    time_data['bits']['hour'] = bits[5:10]
    time_data['utc']['hour'] = int(bits[5:10], 2)

    # Convert minute (6 bits)
    time_data['bits']['minute'] = bits[10:16]
    time_data['utc']['minute'] = int(bits[10:16], 2)

    # Convert second (6 bits)
    time_data['bits']['second'] = bits[16:22]
    time_data['utc']['second'] = int(bits[16:22], 2)

    # Get current year
    time_data['utc']['year'] = datetime.utcnow().strftime('%Y')

    # Get current month
    time_data['utc']['month'] = datetime.utcnow().strftime('%m')

    # Create full datetime object
    datetime_utc = datetime(
        int(time_data['utc']['year']),
        int(time_data['utc']['month']),
        int(time_data['utc']['day']),
        int(time_data['utc']['hour']),
        int(time_data['utc']['minute']),
        int(time_data['utc']['second'])
    )

    # Save UTC to dictionary
    time_data['utc']['full'] = datetime_utc.strftime("%d/%m/%Y %H:%M:%S")
    # UTC epoc
    time_data['utc']['epoc'] = datetime_utc.timestamp()
    # Local time epoc (offset x 3600 seconds)
    time_data['local']['epoc'] = time_data['utc']['epoc'] + (env['timezone_offset'] * 3600)
    # Local time full
    datetime_local = datetime.fromtimestamp(time_data['local']['epoc'])
    # Save local time to dictionary
    time_data['local']['full'] = datetime_local.strftime("%d/%m/%Y %H:%M:%S")
    # Save time components
    time_data['local']['year'] = datetime_local.strftime("%Y")
    time_data['local']['month'] = datetime_local.strftime("%m")
    time_data['local']['day'] = datetime_local.strftime("%d")
    time_data['local']['hour'] = datetime_local.strftime("%H")
    time_data['local']['minute'] = datetime_local.strftime("%M")
    time_data['local']['second'] = datetime_local.strftime("%S")

    return(time_data)


def twos_comp(bits):
    """compute the 2's complement of int value val
    Stolen from a stack overflow like everything else
    """
    val = int(bits,2)
    bits = len(bits)

    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return(val)   

def get_longitude(bits):
    ''' Converts bit string to longitude in decimal degrees
    '''

    longitude = twos_comp(bits)*(360/(2**25))

    location_data['longitude']['decimal_degrees'] = longitude

    if longitude < 0:
        location_data['longitude']['meridian'] = 'W'
    else:
        location_data['longitude']['meridian'] = 'E'

    return(location_data)


def get_latitude(bits):
    ''' Converts bit string to latitude in decimal degrees
    '''

    latitude = twos_comp(bits)*(180/(2**24))

    location_data['latitude']['decimal_degrees'] = latitude

    if latitude < 0:
        location_data['latitude']['meridian'] = 'S'
    else:
        location_data['latitude']['meridian'] = 'N'


def get_horizontal_accuracy(bits):
    ''' Converts horizontal position accuracy bits (6) to actual value in meters
    '''

    # Convert binary to integer
    value = int(bits, 2)

    # Messed up equation according to the standard (standard doesn't conform to order of operation)
    value = (2 * ((1 + 0.2) ** (value+5))) + -4
    value = round(value)

    location_data['uncertainty'] = value


def get_altitude(bits):
    ''' Converts altitude bits (12) to actual value in meters
    This is the GPS reported altitude, doesn't account for latitude, longitude
    '''

    location_data['altitude']['type']['bits'] = bits[0]

    if bits[0] == '0':
        location_data['altitude']['type']['type'] = 'Altitude above WGS84 ellipsoid'
    elif bits[0] == '1':
        location_data['altitude']['type']['type'] = 'User defined altitude reference'

    # Convert remaining 11 bits to integer
    value = int(bits[1:], 2)

    if value == 0:
        # 0 is reserverd, leave blank
        pass
    elif 1 <= value <= 1201:
        value = -201 + value
    elif 1202 <= value <= 1926:
        value = 1000 + ((value - 1201) * 2)
    elif 1927 <= value <= 2047:
        value = 2450 + ((value - 1926) * 75)
    else:
        # Make it max
        value = 11525

    location_data['altitude']['meters'] = value


def get_location_data(bits):
    ''' Takes location data binary string and returns location data dictionary
    '''

    location_data['longitude']['bits'] = bits[0:25]
    location_data['latitude']['bits'] = bits[25:49]
    location_data['uncertainty']['bits'] = bits[49:55]
    location_data['altitude']['bits'] = bits[55:67]

    get_longitude(bits[0:25])
    get_latitude(bits[25:49])
    get_horizontal_accuracy(bits[49:55])
    get_altitude(bits[55:67])

    return(location_data)

def get_horizontal_velocity(bits):
    ''' Calculates horizontal velocity from binary string
    '''
    



def get_velocity_data(bits):
    '''Converts velocity data string to actual velocity information
    '''



    horizontal = int(bits[0:8], 2)
    vertical = int(bits[8:16], 2)

    # v = C × (1 + x)^(K-A) + B
    horizontal = 16 * ((1 + 0.038) ** (horizontal - 13)) + 0



def sds(hex_string):
    ''' "Main" function, takes a hex string, returns a dictionary with location information.
    '''

    master['hex_string'] = hex_string

    # Convert hex to binary (add a 0 to the start)
    binary_string = '0'+"{0:08b}".format(int(hex_string, 16))
    master['binary_string'] = binary_string

    # Look up PDU type in pdu_type dictionary
    # Bits 1-2 (2 bits)
    pdu_data['pdu_type']['bits'] = binary_string[0:2]
    pdu_data['pdu_type']['type'] = pdu_type[binary_string[0:2]]

    # If PDU Type == "Location protocol PDU with extension"
    # Look up PDU type extension in pdu_type_extension dictionary
    # Bits 3-6 (4 bits)
    if pdu_data['pdu_type']['type'] == 'Location protocol PDU with extension':
        pdu_data['pdu_type_extension']['bits'] = binary_string[2:6]
        pdu_data['pdu_type_extension']['type'] = pdu_type_extension[binary_string[2:6]]
    else:
        raise ValueError("Only 'Location protocol PDU with extension' (01) is currently supported.")

    # If PDU Extension Type == "Long location report"
    # Look up time type in time_type dictionary
    # Bits 7-8 (2 bits)
    if pdu_data['pdu_type_extension']['type'] == 'Long location report':
        time_data['type']['bits'] = binary_string[6:8]
        time_data['type']['type'] = time_type[binary_string[6:8]]
    else:
        raise ValueError("Only 'Long location report' (0011) is currently supported.")

    # Process time data
    # Bits 9-31 (22 bits)
    if time_data['type']['type'] == "Time of position":
        master['time'] = get_time_data(binary_string[8:30])
    else:
        raise ValueError("Only 'Time of position' (10) is currently supported.")

    # Lookup location shape
    location_data['shape']['bits'] = binary_string[30:34]
    location_data['shape']['type'] = location_shape[binary_string[30:34]]

    # Process location data
    # Bits [34:101] (67 bits)
    if location_data['shape']['type'] == 'circle with altitude':
        master['location'] = get_location_data(binary_string[34:101])
    else:
        raise ValueError("Only 'circle with altitude' (0101) is currently supported")

    # Lookup velocity type
    velocity_data['type']['bits'] = binary_string[101:104]
    velocity_data['type']['type'] = velocity_type[binary_string[101:104]]

    if velocity_data['type']['type'] = 'Horizontal velocity and vertical velocity':
        master['velocity'] = get_velocity_data(binary_string[104:119])



    

if __name__ == '__main__':

    # Locations list to append positions
    locations = []

    #Import example hex string from file
    with open('example_hex.txt', 'r') as f:
        for line in f:
            hex_string = line.strip()
            print(f'Decoding {hex_string}')
            sds(hex_string)


        print(master)

    f.close()
