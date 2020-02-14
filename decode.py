



def hex_to_binary(hex_string):
    '''Convert hex string to binary string
    '''
    # Convert using .format
    binary_string = "{0:08b}".format(int(hex_string, 16))
    # Add a 0 to the start (test temp)
    binary_string = '0'+binary_string
    return(binary_string)


def sds(hex_string):
    ''' "Main" function, takes a hex string, returns a dictionary with location information.
    '''
    binary_string = hex_to_binary(hex_string)
    
    

if __name__ == '__main__':

    #Import example hex string from file
    with open('example_hex.txt', 'r') as f:
        for line in f:
            hex_string = line.strip()
            print(f'Decoding {hex_string}')
            sds(hex_string)

    f.close()
