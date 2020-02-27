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

altitude_type = {
    '0' : 'Altitude above WGS84 ellipsoid',
    '1' : 'User defined altitude reference'
}

velocity_type = {
    '000' : 'No velocity information',
    '001' : 'Horizontal velocity',
    '010' : 'Horizontal velocity with uncertainty',
    '011' : 'Horizontal velocity and vertical velocity',
    '100' : 'Horizontal velocity and vertical velocity with uncertainty',
    '101' : 'Horizontal velocity with direction of travel extended',
    '110' : 'Horizontal velocity with direction of travel extended and uncertainty',
    '111' : 'Horizontal velocity and vertical velocity with direction of travel extended and uncertainty'
}

acknowledgement_request = {
    '0' : 'No acknowledgement requested',
    '1' : 'Acknowledgement requested'
}

additional_data_type = {
    '0' : 'Reason for sending',
    '1' : 'User defined data'
}

reason_for_sending = {
    '0' : 'Subscriber unit is powered ON',
    '1' : 'Subscriber unit is powered OFF',
    '2' : 'Emergency condition is detected',
    '3' : 'Push-to-talk condition is detected',
    '4' : 'Status',
    '5' : 'Transmit inhibit mode ON',
    '6' : 'Transmit inhibit mode OFF',
    '7' : 'System access (TMO ON)',
    '8' : 'DMO ON', 
    '9' : 'Enter service (after being out of service)',
    '10' : 'Service loss', 
    '11' : 'Cell reselection or change of serving cell',
    '12' : 'Low battery',
    '13' : 'Subscriber unit is connected to a car kit',
    '14' : 'Subscriber unit is disconnected from a car kit',
    '15' : 'Subscriber unit asks for transfer initialization configuration',
    '16' : 'Arrival at destination Destination',
    '17' : 'Arrival at a defined location',
    '18' : 'Approaching a defined location',
    '19' : 'SDS type-1 entered',
    '20' : 'User application initiated',
    '21' : 'Lost ability to determine location',
    '22' : 'Regained ability to determine location',
    '23' : 'Leaving point',
    '24' : 'Ambience Listening call is detected',
    '25' : 'Start of temporary reporting',
    '26' : 'Return to normal reporting',
    '27' : 'Reserved',
    '31' : 'Reserved',
    '32' : 'Response to an immediate location request',
    '33' : 'Reserved',
    '128' : 'Reserved',
    '129' : 'Maximum reporting interval exceeded since the last location information report',
    '130' : 'Maximum reporting distance limit travelled since last location information report',
    '131' : 'Reserved',
    '255' : 'Reserved'
}