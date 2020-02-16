from location_model import location_information, time_data
from env.example import env

import time
from datetime import datetime
from dateutil import tz


def hex_to_binary(hex_string):
    '''Convert hex string to binary string
    '''
    # Convert using .format
    binary_string = "{0:08b}".format(int(hex_string, 16))
    # Add a 0 to the start (test temp)
    binary_string = '0'+binary_string
    return(binary_string)


def get_pdu_type(bits):
    '''Takes two binary bits as a string, returns PDU type,
    short location report (short) or long location report (long)
    '''
    str(bits)
    if bits == '00':
        return('short')
    elif bits == '01':
        return('long')
    else:
        raise ValueError(f'"Unknown binary input, must be either 00 or 01"')


def get_time_type(bits):
    '''Takes two binary bits as a string, returns time type,
    None, elapsed or position
    '''
    str(bits)
    if bits == '00':
        return('none')
    elif bits == '01':
        return('time_elapsed')
    elif bits == '10':
        return('time_of_position')
    else:
        raise ValueError(f'"Unknown binary input, must be either 00, 01 or 10"')


def get_time_data(bits):
    '''Takes binary string, returns time information dictionary
    '''

    # Convert day (4 bits)
    time_data['day']['bits'] = bits[0:5]
    time_data['day']['utc'] = int(bits[0:5], 2)

    # Convert hour (4 bits)
    time_data['hour']['bits'] = bits[5:10]
    time_data['hour']['utc'] = int(bits[5:10], 2)

    # Convert minute (6 bits)
    time_data['minute']['bits'] = bits[10:16]
    time_data['minute']['utc'] = int(bits[10:16], 2)

    # Convert second (6 bits)
    time_data['second']['bits'] = bits[16:22]
    time_data['second']['utc'] = int(bits[16:22], 2)

    # Get current year
    time_data['year']['utc'] = datetime.utcnow().strftime('%Y')

    # Get current month
    time_data['month']['utc'] = datetime.utcnow().strftime('%m')

    # Create full datetime object
    datetime_utc = datetime(
        int(time_data['year']['utc']),
        int(time_data['month']['utc']),
        int(time_data['day']['utc']),
        int(time_data['hour']['utc']),
        int(time_data['minute']['utc']),
        int(time_data['second']['utc'])
    )

    # Save UTC to dictionary
    time_data['full']['datetime']['utc'] = datetime_utc.strftime("%d/%m/%Y, %H:%M:%S")
    # UTC epoc
    time_data['epoc']['utc'] = datetime_utc.timestamp()
    # Local time epoc (offset x 3600 seconds)
    time_data['epoc']['local'] = time_data['epoc']['utc'] + (env['timezone_offset'] * 3600)
    # Local time full
    datetime_local = datetime.fromtimestamp(time_data['epoc']['local'])
    # Save local time to dictionary
    time_data['full']['datetime']['local'] = datetime_local.strftime("%d/%m/%Y, %H:%M:%S")
    # Save time components
    time_data['year']['local'] = datetime_local.strftime("%Y")
    time_data['month']['local'] = datetime_local.strftime("%m")
    time_data['day']['local'] = datetime_local.strftime("%d")
    time_data['hour']['local'] = datetime_local.strftime("%H")
    time_data['minute']['local'] = datetime_local.strftime("%M")
    time_data['second']['local'] = datetime_local.strftime("%S")


    return(time_data)    


def get_long_location(bits):
    pass


def sds(hex_string):
    ''' "Main" function, takes a hex string, returns a dictionary with location information.
    '''
    # Convert to binary
    location_information['binary_string'] = hex_to_binary(hex_string)

    # Get location report type
    location_information['pdu_type']['bits'] = location_information['binary_string'][:2]
    location_information['pdu_type']['type'] = get_pdu_type(location_information['pdu_type']['bits'])

    # Get time type
    location_information['time']['type']['bits'] = location_information['binary_string'][6:8]
    location_information['time']['type']['type'] = get_time_type(location_information['time']['type']['bits'])

    # Process time data
    if location_information['time']['type']['type'] == "time_of_position":
        time_data = get_time_data(location_information['binary_string'][8:30])

        print(time_data)

    '''
    # Get location
    if location_information['pdu_type']['type'] == 'long':
        # pdu type
        get_long_location(location_information['binary_string'][])
    '''

    

if __name__ == '__main__':

    #Import example hex string from file
    with open('example_hex.txt', 'r') as f:
        for line in f:
            hex_string = line.strip()
            print(f'Decoding {hex_string}')
            sds(hex_string)

    f.close()
