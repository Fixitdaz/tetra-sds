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