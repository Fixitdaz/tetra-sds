from models import master, pdu_type, pdu_type_extension, time_type, pdu_data, time_data
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



def sds(hex_string):
    ''' "Main" function, takes a hex string, returns a dictionary with location information.
    '''

    master['hex_string'] = hex_string

    # Convert to binary (add a 0 to the start)
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
        get_time_data(binary_string[8:30])
        print(time_data)
    else:
        raise ValueError("Only 'Time of position' (10) is currently supported.")

    

if __name__ == '__main__':

    #Import example hex string from file
    with open('example_hex.txt', 'r') as f:
        for line in f:
            hex_string = line.strip()
            print(f'Decoding {hex_string}')
            sds(hex_string)

    f.close()
