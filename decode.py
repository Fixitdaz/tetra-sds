import lookup
import copy



'''
Module to decode a raw binary string in to GPS position details
'''



def lookup_binary(
        binary: str
    ) -> dict:
    '''
    Splits the binary string in to separte parts
    Looks up the value with the lookup dictionaries
    Returns the values in a dictionary
    '''

    binary_dict = {
        'pdu_type' : {},
        'time' : {},
        'location' : {
            'shape' : {}
        },
        'velocity' : {
            'type' : {}
        }
    }

    # Look up PDU type in the pdu_type dictionary
    # Bits 1-2 (2 bits)
    binary_dict['pdu_type'] = lookup.pdu_type[binary[0:2]]

    # If PDU Type == "Location protocol PDU with extension"
    # Look up PDU type extension in pdu_type_extension dictionary
    # Bits 3-6 (4 bits)
    if binary_dict['pdu_type'] == 'Location protocol PDU with extension':
        binary_dict['pdu_type_extension'] = lookup.pdu_type_extension[binary[2:6]]
    
    # If PDU Extension Type == "Long location report"
    if binary_dict['pdu_type_extension'] == 'Long location report':
        # Look up time type in time_type dictionary
        # Bits 7-8 (2 bits)
        binary_dict['time']['type'] = lookup.time_type[binary[6:8]]
        # Lookup acknowledgement type
        try:
            binary_dict['acknowledgement'] = lookup.acknowledgement_request[binary[119:120]]
        except:
            binary_dict['acknowledgement'] = None
        try:
            # Lookup additional data type
            binary_dict['additional'] = lookup.additional_data_type[binary[120:121]]
        except:
            binary_dict['additional'] = None
    
    # Lookup reason for sending
    if binary_dict['additional'] == 'Reason for sending':
        # Convert to integer then back to string
        reason = str(int(binary[121:129], 2))
        binary_dict['reason'] = lookup.reason_for_sending[reason]

    # If the time type is none
    if binary_dict['time']['type'] == 'None':
        # Look up the location shape
        binary_dict['location']['shape'] = lookup.location_shape[binary[8:12]]

    # If there is no location shape
    if binary_dict['location']['shape'] == 'No shape':
        binary_dict['velocity']['type'] = lookup.velocity_type[binary[12:15]]

    # If there is no velocity information
    if binary_dict['velocity']['type'] == 'No velocity information':
        # Lookup acknowledgement type
        binary_dict['acknowledgement'] = lookup.acknowledgement_request[binary[15:16]]
        # Lookup additional data type
        binary_dict['additional'] = lookup.additional_data_type[binary[16:17]]
        # Lookup reason

    # If additional information is 'Reason for Sending'
    if binary_dict['additional'] == 'Reason for sending':
        # Lookup reason
        # Convert to integer then back to string
        reason = str(int(binary[17:25], 2))
    
    return(binary_dict)


def get_time_data(
        bits: str
    ) -> dict:
    '''
    Takes binary string, returns time information dictionary
    '''
    # Reset to blank
    time_data = {}

    # Lookup time type
    time_data['type'] = lookup.time_type[bits[0:2]]

    # No Year or Month data in the GPS time stamp
    # Therefor unable to create a datetime object
    time_data['day'] = int(bits[2:7], 2)
    time_data['hour'] = int(bits[7:12], 2)
    time_data['minute'] = int(bits[12:18], 2)
    time_data['seconds'] = int(bits[18:24], 2)

    return(time_data)


def twos_comp(bits):
    '''
    Compute the 2's complement of int value val
    Stolen from a stack overflow like everything else
    '''
    val = int(bits,2)
    bits = len(bits)

    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value

    return(val)   


def get_longitude(
        bits: str
    ) -> dict:
    '''
    Converts bit string to longitude in decimal degrees
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


def get_latitude(
        bits: str
    ) -> dict:
    '''
    Converts bit string to latitude in decimal degrees
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


def get_uncertainty(
        bits: str
    ) -> int:
    ''' Converts horizontal position accuracy bits (6) to actual value in meters
    '''

    # Convert binary to integer
    uncertainty = int(bits, 2)

    # Messed up equation according to the standard (standard doesn't conform to order of operation)
    uncertainty = (2 * ((1 + 0.2) ** (uncertainty+5))) + -4
    uncertainty = round(uncertainty)

    return(uncertainty)


def get_altitude(
        bits: str
    ) -> dict:
    '''
    Converts altitude bits (12) to actual value in meters
    This is the GPS reported altitude typically above WGS84 ellipsoid
    '''

    altitude = {
        'type' : '',
        'meters' : ''
    }

    altitude['type'] = lookup.altitude_type[bits[0]]

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


def get_velocity(
        bits: str
    ) -> dict:
    '''
    Calculates horizontal velocity and direction from binary string
    '''

    velocity = {
        'type' : '',
        'kmh' : ''
    }
    
    # Lookup velocity type
    velocity['type'] = lookup.velocity_type[bits[0:3]]

    if velocity['type'] == 'Horizontal velocity with direction of travel extended':

        vel = int(bits[3:10], 2)

        if 29 <= vel <= 126:
            # Simplified equation as per standard
            vel = 16 * (1.038 ** (vel - 13))
            vel = round(vel)

        velocity['kmh'] = vel

        direction = get_direction(bits[10:18])

        return(velocity, direction)


def get_direction(
        bits: str
    ) -> dict:
    ''' 
    Connverts bit string to angle (direction of travel)
    '''

    direction = {
        'angle' : '',
        'direction' : ''
    }

    angle = int(bits, 2)
    # value * (360/256)
    angle = angle * 1.40625
    direction['angle'] = angle
    
    if 11 >= angle >= 349:
        direction['direction'] = 'N'
    elif 33 >= angle >= 12:
        direction['direction'] = 'NNE'
    elif 56 >= angle >= 34:
        direction['direction'] = 'NE'
    elif 78 >= angle >= 57:
        direction['direction'] = 'ENE'
    elif 101 >= angle >= 79:
        direction['direction'] = 'E'
    elif 123 >= angle >= 102:
        direction['direction'] = 'ESE'
    elif 146 >= angle >= 124:
        direction['direction'] = 'SE'
    elif 168 >= angle >= 147:
        direction['direction'] = 'SSE'
    elif 191 >= angle >= 169:
        direction['direction'] = 'S'
    elif 213 >= angle >= 192:
        direction['direction'] = 'SSW'
    elif 236 >= angle >= 214:
        direction['direction'] = 'SW'
    elif 258 >= angle >= 237:
        direction['direction'] = 'WSW'
    elif 281 >= angle >= 259:
        direction['direction'] = 'W'
    elif 303 >= angle >= 282:
        direction['direction'] = 'WNW'        
    elif 326 >= angle >= 304:
        direction['direction'] = 'NW'
    elif 348 >= angle >= 327:
        direction['direction'] = 'NNW'    

    return(direction)


def sds(
        data: bytes
    ) -> dict:
    ''' 
    "Main" function, takes raw bytearray, returns a dictionary with location information.
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

    if type(data) == bytearray:
        data = data.hex()

    # Convert hex to binary (add a 0 to the start)
    bits = '0'+"{0:08b}".format(int(data, 16))

    # Split the binary string and lookup the values
    data_types = lookup_binary(bits)

    # If the time type is 'Time of position'
    if data_types['time']['type'] == 'Time of position':
        ####################################
        # Decode the time data (bits 7-30) #
        ####################################
        master['time'] = get_time_data(bits[6:30])

        #######################################
        # Process location data (bits 31-101) #
        #######################################
        # Lookup Shape (bits 31-34)
        master['location']['shape'] = lookup.location_shape[bits[30:34]]
        
        # Decode the location data binary
        if master['location']['shape'] == 'circle with altitude':
            master['location']['longitude'] = get_longitude(bits[34:59])
            master['location']['latitude'] = get_latitude(bits[59:83])
            master['location']['uncertainty'] = get_uncertainty(bits[83:89])
            master['location']['altitude'] = get_altitude(bits[89:101])
        
        #########################################
        # Process velocity and directional data #
        #########################################
        master['velocity'], master['direction'] = get_velocity(bits[101:119])

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
