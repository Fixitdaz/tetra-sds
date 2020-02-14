



def hex_to_binary(hex_string):
    pass




def sds(hex_string):
    binary_string = hex_to_binary(hex_string)
    

   



if __name__ == '__main__':

    #Import example hex string from file
    with open('example_hex.txt', 'r') as f:
        for line in f:
            hex_string = line.strip()
            print(f'Decoding {hex_string}')
            sds(hex_string)

    f.close()
