import os
import codecs # For handling unicode characters when reading file containing unicode characters to list

# Encode text (our secret message in clear text) to binary string, using the defined dictionary in the main program
def encode(secret_message):
    binary_secret_message = ''
    for character in secret_message:
        # Method dict.get(key) returns a value for a given key in the dictionary 'dict'
        binary_secret_message += dictionary.get(character)
    return binary_secret_message

# Decode binary string to text (our secret message in clear text), using the defined dictionary in the main program
def decode(binary_secret_message):
    secret_message = ''
    for i in range(0, len(binary_secret_message), 5):
        for key, value in dictionary.items():
            if value == binary_secret_message[i: i+5]:
                secret_message += key
    return secret_message

# Hide secret message into the container file, output to another file
def hide_secret_message(container_file_in, secret_message, container_file_out):
    # Read all characters from file 'container_file_in' into a list 'character_list' 
    character_list = [char for char in open(container_file_in).read()]
    binary_secret_message = encode(secret_message)
    number_of_replacement = 0
    j = 0
    for i in range(0, len(character_list), 1):
        if character_list[i] == pair[0][0] and binary_secret_message[j] == '0':
            character_list[i] = pair[0][1]
            number_of_replacement += 1
            j += 1
        if character_list[i] == pair[1][0] and binary_secret_message[j] == '1':
            character_list[i] = pair[1][1]
            number_of_replacement += 1
            j += 1
        # If number_of_replacement == len(secret_message_in_binary), then break the loop
        if number_of_replacement == len(binary_secret_message):
            break
    # Write an updated character list elements after hiding secret message
    f = open(container_file_out, "wb")
    for character in character_list:
        f.write(character.encode('utf8'))
    f.close()

# Unhide secret message from a container file, return secret message in clear text
def unhide_secret_message(container_file, method):
    # Read all characters from the container file into a list
    character_list = []
    with codecs.open(container_file, encoding='utf-8') as f:
        for line in f:
            for character in line:
                character_list.append(character)
    binary_secret_message = ''
    if method == '1':
        for i in range(0, len(character_list), 1):
            if character_list[i] == pair[0][1]:
                binary_secret_message += '0'
            elif character_list[i] == pair[1][1]:
                binary_secret_message += '1'
    elif method == '2' or method == '3':
        for i in range(0, len(character_list), 1):
            if character_list[i] == '\n':
                if (character_list[i - 2] + character_list[i - 1]).count(pattern) == 1:
                    binary_secret_message += '0'
                elif (character_list[i - 2] + character_list[i - 1]).count(pattern) == 2:
                    binary_secret_message += '1'
    return decode(binary_secret_message)

# The main program
if __name__ == "__main__":
    # Create a dictionary for storing {character:binary} pairs
    dictionary = {}
    for i in range(1072, 1104, 1):
        # Add a new key:value pair
        dictionary.update( {chr(i) : bin(i-1072)[2:].zfill(5)} )
        # Method dict.update({key: value}) appends a key-value pair to the dictionary 'dict'
        # Method chr(int) returns a character from an integer 'int'
        # Method bin(int)[2:] return the binary equivalent string of a given integer 'int'
        # Method binary_string.zfill(int) pads binary_string on the left with zeros to fill width 'int'
    
    print("1. Replace 'o' and 'p' in English with 'о' and 'р' in Russian")
    print("2. Add 1 or 2 spaces before '\\n'")
    print("3. Add 1 or 2 null characters before '\\n'")
    method = input("Choose one method you want to use: ")
    # The pair dictionary containing 2 tuples as its values
    pair = {}
    if method == '1':
        pair[0] = ('o', chr(1086))  # Function chr(1086) returns character 'o' in Russian, bit 0
        pair[1] = ('p', chr(1088))  # Function chr(1088) returns character 'p' in Russian, bit 1
    elif method == '2':
        pair[0] = ('\n', ' \n')     # Add 1 space right before \n character, bit 0
        pair[1] = ('\n', '  \n')    # Add 2 spaces right before \n character, bit 1
        # The following variable is used for function unhide_secret_message()
        pattern = ' '
    elif method == '3':
        pair[0] = ('\n', '\x00\n')      # Add 1 NULL character right before \n character, bit 0
        pair[1] = ('\n', '\x00\x00\n')  # Add 2 NULL characters right before \n character, bit 1
        # The following variable is used for function unhide_secret_message()
        pattern = '\x00'

    print("Current working directory:", os.getcwd())
    secret_message = input("Enter your secret message: ")

    print("Hiding secret message into the container_before file...")
    hide_secret_message('container_before.txt', secret_message, 'container_after.txt')

    print("Extract secret message from the container_after file...")
    print(unhide_secret_message('container_after.txt', method))