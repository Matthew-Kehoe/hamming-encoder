import math


def check_input(input_string):
    """

    :param input_string: input in String format to be tested
    :return: Boolean value indicating whether input is binary format
    """
    allowed = "01"
    return isinstance(input_string, str) and all(character in allowed for character in input_string)


def non_parity_creator(binary_input):
    """
    1. Takes binary verified string
    2. Finds the highest power in the list according to index
    3. Creates a new list with each character from the string
    4. Inserts an underscore at every 2**n index in the list
    5. Returns new list with underscores

    :param binary_input: verified user input
    :return: a new list containing underscores in the positions of each parity bit
    """

    power = int(math.log(len(binary_input) + 1, 2))

    list_with_blank_parities = list(binary_input)

    for i in range(power + 1):
        a = 2 ** i - 1
        list_with_blank_parities.insert(a, "_")

    return list_with_blank_parities


def parity_list(list_with_blank_parities):
    """
    Returns a list with the position of parity bits

    :param list_with_blank_parities: list with underscores in the position of parity bits to be generated
    :return: list of all the position of all the parities of two (other than 0)
    """

    power_of_2_list = []

    for i in range(1, list_with_blank_parities):
        if (i & (i - 1)) == 0:
            power_of_2_list.append(i)

    return power_of_2_list


def parity_positions(parity_list_result):
    """
    Returns a list with the index of parity bits

    :param parity_list_result: takes in the list of position parity bits associated with the string input
    :return: a list with the index of parity bits
    """
    for i in range(len(parity_list_result)):
        parity_list_result[i] = parity_list_result[i] - 1
    return parity_list_result


def start_position_chunk_creator(blank_parity_string, start_position, chunk_size):
    """
    This function slices the list into the relevant chunk size depending on the position of the parity bit
    to be calcualted

    :param blank_parity_string: List of input + blank parity bits
    :param start_position: position from which the bits should be counted
    :param chunk_size: the size of the sections List of input + blank parity bits to be sliced into
    :return: a list of slices of List of input + blank parity bits from the starting position to the end of the list
    """
    # slicing list to begin count from parity bit
    list_slice = blank_parity_string[start_position:]

    # for loop to slice the output into the required size
    for i in range(0, len(list_slice), chunk_size):
        yield list_slice[i:i + chunk_size]


def alt_element(chunk_list):
    """
    Given that we now have a list of the ist of input + blank parity bits in the correct size, starting at the parity
    bit to be calcualted, now we need to select every other slice.

    :param chunk_list: a list of slices of List of input + blank parity bits from starting position to end of the list
    :return: a list containing every other slice starting from the first slice in the chunk_list
    """
    return chunk_list[::2]


def hammingEncode(string_input):
    """
    1. Call binary check function on input
        a. if true proceeds with operation
            i. Calls function to insert underscores in positions of parity bits
            ii. creates a zip object with the index of parities and the position
            iii. assigns zip object to dictionary
            iv. iterates through dictionary and assigns list of slices of  relevant length to relevant parity index
            v. Filters out slices that should be skipped
            vi. Counts number of 1 bits of the remaining slices, Mod 2  results and assigns to the relevant parity index
            vii. prints out the hamming encoded result
        b. else prints out error message
    :param string_input:
    :return:
    """
    # checking input
    if check_input(string_input):

        # generating list with underscores in positions of parity bits
        final_var_store = non_parity_creator(string_input)

        # zipping  the index of parities and the position

        zip_iterator = zip(parity_positions(parity_list(len(non_parity_creator(string_input)))),
                           parity_list(len(non_parity_creator(string_input))))

        # assigning to a dictionary
        parity_dictionary= dict(zip_iterator)

        # creating new dictionary to store unfiltered slices of correct length for each parity
        non_filtered_parity = {}

        for k, v in parity_dictionary.items():
            non_filtered_parity[k] = list(start_position_chunk_creator(non_parity_creator(string_input), k, v))

        for k, v in non_filtered_parity.items():
            non_filtered_parity[k] = v[::2]

        #counting number of one bits in slices for relevant parity bits
        for k, v in non_filtered_parity.items():
            count_of_ones = 0
            for item in non_filtered_parity[k]:
                count_of_ones += item.count('1')

            #updating parity bits from underscore to final value
            final_var_store[k] = str(count_of_ones % 2)

        return "".join(final_var_store)

    else:
        return "Error: Input must be binary!"


test_string = "1100"


hammingEncode(test_string)
