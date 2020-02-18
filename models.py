master = {
    'hex' : '',
    'binary' : '',
    'location' : {},
    'time' : {}
}

pdu_type = {
    '00' : 'Short location report',
    '01' : 'Location protocol PDU with extension',
    '10' : 'Reserved',
    '11' : 'Reserved'
}

pdu_type_extension = {
    '0000' : 'Reserved for further extension',
    '0001' : 'Immediate location report request',
    '0010' : 'Reserved',
    '0011' : 'Long location report',
    '0100' : 'Location report acknowledgement',
    '0101' : 'Basic location parameters request/response',
    '0110' : 'Add/modify trigger request/response',
    '0111' : 'Remove trigger request/response',
    '1000' : 'Report trigger request/response',
    '1001' : 'Report basic location parameters request/response',
    '1010' : 'Location reporting enable/disable request/response',
    '1011' : 'Location reporting temporary control request/response',
    '1100' : 'Reserved',
    '1101' : 'Reserved',
    '1110' : 'Reserved',
    '1111' : 'Reserved'
}

time_type = {
    '00' : 'None',
    '01' : 'Time elapsed',
    '10' : 'Time of position',
    '11' : 'Reserved' 
}

location_shape = {
    '0000' : 'No shape',
    '0001' : 'point',
    '0010' : 'circle',
    '0011' : 'ellipse',
    '0100' : 'point with altitude',
    '0101' : 'circle with altitude',
    '0110' : 'ellipse with altitude',
    '0111' : 'circle with altitude and altitude uncertainty',
    '1000' : 'ellipse with altitude and altitude uncertainty',
    '1001' : 'arc',
    '1010' : 'point and position error',
    '1011' : 'Reserved',
    '1100' : 'Reserved',
    '1101' : 'Reserved',
    '1110' : 'Reserved',
    '1111' : 'Location shape extension'
}

pdu_data = {
    'pdu_type' : {
        'type' : '',
        'bits' : ''
    },
    'pdu_type_extension' : {
        'type' : '',
        'bits' : ''
    }
}

time_data = {
    'type' : {
        'bits' : '',
        'type' : ''
    },
    'bits' : {
        'day' : '',
        'hour' : '',
        'minute' : '',
        'second' : ''       
    },
    'utc' : {
        'epoc' : '',
        'full' : '',
        'year' : '',
        'month' : '',
        'day' : '',
        'hour' : '',
        'minute' : '',
        'second' : ''
    },
    'local' : {
        'epoc' : '',
        'full' : '',
        'year' : '',
        'month' : '',
        'day' : '',
        'hour' : '',
        'minute' : '',
        'second' : ''       
    }
}

location_data = {
    'shape' : {
        'bits' : '',
        'type' : ''
    },
    'longitude' : {
        'bits' : ''
    },
    'latitude' : {
        'bits' : ''
    },
    'uncertainty' : {
        'bits' : ''
    },
    'altitude' : {
        'bits' : ''
    }

}