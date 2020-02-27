
from lookup import pdu_type, pdu_type_extension, time_type, location_shape, altitude_type, velocity_type, acknowledgement_request, \
    additional_data_type, reason_for_sending

import time
from datetime import datetime
import copy



def get_time_data(bits):
    '''Takes binary string, returns time information dictionary
    '''

    # Reset to blank
    time_data = {
        'type' : '',
        'epoc' : '',
        'full': ''
    }

    # Lookup time type
    time_data['type'] = time_type[bits[0:2]]

    if time_data['type'] != "Time of position":
        raise ValueError("Only 'Time of position' (10) is currently supported.")

    # Create full datetime object
    # Year, Month, Day, Hour, Minute, Second
    datetime_utc = datetime(
        int(datetime.utcnow().strftime('%Y')),
        int(datetime.utcnow().strftime('%m')),
        int(bits[2:7], 2),
        int(bits[7:12], 2),
        int(bits[12:18], 2),
        int(bits[18:24], 2)
    )

    # Save UTC to dictionary
    time_data['full'] = datetime_utc.strftime("%d/%m/%Y %H:%M:%S")
    # UTC epoc
    time_data['epoc'] = datetime_utc.timestamp()

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

    longitude = {
        'decimal_degrees': '',
        'meridian' : ''
    }

    longitude['decimal_degrees'] = twos_comp(bits)*(360/(2**25))

    if longitude['decimal_degrees'] < 0:
        longitude['meridian'] = 'W'
    else:
        longitude['meridian'] = 'E'

    return(longitude)


def get_latitude(bits):
    ''' Converts bit string to latitude in decimal degrees
    '''

    latitude = {
        'decimal_degrees': '',
        'meridian' : ''
    }

    latitude['decimal_degrees'] = twos_comp(bits)*(180/(2**24))

    if latitude['decimal_degrees'] < 0:
        latitude['meridian'] = 'S'
    else:
        latitude['meridian'] = 'N'

    return(latitude)


def get_uncertainty(bits):
    ''' Converts horizontal position accuracy bits (6) to actual value in meters
    '''

    # Convert binary to integer
    uncertainty = int(bits, 2)

    # Messed up equation according to the standard (standard doesn't conform to order of operation)
    uncertainty = (2 * ((1 + 0.2) ** (uncertainty+5))) + -4
    uncertainty = round(uncertainty)

    return(uncertainty)


def get_altitude(bits):
    ''' Converts altitude bits (12) to actual value in meters
    This is the GPS reported altitude typically above WGS84 ellipsoid
    '''

    altitude = {
        'type' : '',
        'meters' : ''
    }

    altitude['type'] = altitude_type[bits[0]]

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

    altitude['meters'] = value

    return(altitude)


def get_location_data(bits):
    ''' Takes location data binary string and returns location data dictionary
    '''

    location_data = {
        'shape' : '',
        'longitude' : {},
        'latitude' : {},
        'uncertainty' : '',
        'altitude' : {}
    }

    # Lookup Shape
    location_data['shape'] = location_shape[bits[0:4]]
    
    # Process location data
    if location_data['shape'] != 'circle with altitude':
        raise ValueError("Only 'circle with altitude' (0101) is currently supported")

    location_data['longitude'] = get_longitude(bits[4:29])
    location_data['latitude'] = get_latitude(bits[29:53])
    location_data['uncertainty'] = get_uncertainty(bits[53:59])
    location_data['altitude'] = get_altitude(bits[59:71])

    return(location_data)


def get_velocity(bits):
    ''' Calculates horizontal velocity and direction from binary string
    '''

    velocity = {
        'type' : '',
        'kmh' : ''
    }
    
    # Lookup velocity type
    velocity['type'] = velocity_type[bits[0:3]]

    if velocity['type'] != 'Horizontal velocity with direction of travel extended':
        raise ValueError("Only 'Horizontal velocity with direction of travel extended' (101) is currently supported")

    vel = int(bits[3:10], 2)

    if 29 <= vel <= 126:
        # Simplified equation as per standard
        vel = 16 * (1.038 ** (vel - 13))
        vel = round(vel)

    velocity['kmh'] = vel

    direction = get_direction(bits[10:18])

    return(velocity, direction)


def get_direction(bits):
    ''' Connverts bit string to angle (direction of travel)
    '''

    direction = {
        'angle' : '',
        'direction' : ''
    }

    angle = int(bits, 2)
    # value * (360/256)
    angle = angle * 1.40625
    direction['angle'] = angle
    
    if angle >= 349 and angle <= 11:
        direction['direction'] = 'N'
    elif angle >= 12 and angle <= 33:
        direction['direction'] = 'NNE'
    elif angle >= 34 and angle <= 56:
        direction['direction'] = 'NE'
    elif angle >= 57 and angle <= 78:
        direction['direction'] = 'ENE'
    elif angle >= 79 and angle <= 101:
        direction['direction'] = 'E'
    elif angle >= 102 and angle <= 123:
        direction['direction'] = 'ESE'
    elif angle >= 124 and angle <= 146:
        direction['direction'] = 'SE'
    elif angle >= 147 and angle <= 168:
        direction['direction'] = 'SSE'
    elif angle >= 169 and angle <= 191:
        direction['direction'] = 'S'
    elif angle >= 192 and angle <= 213:
        direction['direction'] = 'SSW'
    elif angle >= 214 and angle <= 236:
        direction['direction'] = 'SW'
    elif angle >= 237 and angle <= 258:
        direction['direction'] = 'WSW'
    elif angle >= 259 and angle <= 281:
        direction['direction'] = 'W'
    elif angle >= 282 and angle <= 303:
        direction['direction'] = 'WNW'        
    elif angle >= 304 and angle <= 326:
        direction['direction'] = 'NW'
    elif angle >= 327 and angle <= 348:
        direction['direction'] = 'NNW'    

    return(direction)


def sds(hex_string):
    ''' "Main" function, takes a hex string, returns a dictionary with location information.
    '''

    # Reset dictionary
    master = {
        'pdu_type' : '',
        'pdu_type_extension' : '',
        'time' : {},
        'location' : {},
        'velocity' : {},
        'direction' : {},
        'acknowledgement' : {},
        'additional' : {},
        'reason' : ''
    }

    # Convert hex to binary (add a 0 to the start)
    binary_string = '0'+"{0:08b}".format(int(hex_string, 16))

    # Look up PDU type in pdu_type dictionary
    # Bits 1-2 (2 bits)
    master['pdu_type'] = pdu_type[binary_string[0:2]]

    # If PDU Type == "Location protocol PDU with extension"
    # Look up PDU type extension in pdu_type_extension dictionary
    # Bits 3-6 (4 bits)
    if master['pdu_type'] == 'Location protocol PDU with extension':
        master['pdu_type_extension'] = pdu_type_extension[binary_string[2:6]]
    else:
        raise ValueError("Only 'Location protocol PDU with extension' (01) is currently supported.")

    # If PDU Extension Type == "Long location report"
    # Look up time type in time_type dictionary
    # Bits 7-8 (2 bits)
    if master['pdu_type_extension'] == 'Long location report':
        master['time'] = get_time_data(binary_string[6:30])
    else:
        raise ValueError("Only 'Long location report' (0011) is currently supported.")

    # Process location data
    master['location'] = get_location_data(binary_string[30:101])

    # Process velocity and directional data
    master['velocity'], master['direction'] = get_velocity(binary_string[101:119])

    # Lookup acknowledgement type
    master['acknowledgement'] = acknowledgement_request[binary_string[119:120]]

    # Lookup additional data type
    master['additional'] = additional_data_type[binary_string[120:121]]

    # Lookup reason
    if master['additional'] == 'Reason for sending':
        reason = str(int(binary_string[121:129], 2))
        master['reason'] = reason_for_sending[reason]

    return(master)


if __name__ == '__main__':

    # Locations list to append positions
    locations = []

    #Import example hex string from file
    with open('example_hex.txt', 'r') as f:
        for line in f:
            hex_string = line.strip()
            print(f'Decoding {hex_string}')
            location = sds(hex_string)
            location = copy.deepcopy(location)
            locations.append(location)
    f.close()

    print(locations)
