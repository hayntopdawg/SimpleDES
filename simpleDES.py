import sys

__author__ = 'Jamie Fujimoto'


def init_perm(bin_num):
    return "".join([bin_num[1], bin_num[5], bin_num[2], bin_num[0],
                    bin_num[3], bin_num[7], bin_num[4], bin_num[6]])


def split_string(in_str, out_bits):
    return in_str[:out_bits], in_str[out_bits:]


def key_perm_ten(key):
    return "".join([key[2], key[4], key[1], key[6], key[3],
                    key[9], key[0], key[8], key[7], key[5]])


def left_shift_five(key):
    return "".join([key[1], key[2], key[3], key[4], key[0]])


def key_perm_eight(key):
    return "".join([key[5], key[2], key[6], key[3],
                    key[7], key[4], key[9], key[8]])


def create_keys(init_key):
    perm_ten = key_perm_ten(init_key)
    key_left, key_right = split_string(perm_ten, 5)
    key_left = left_shift_five(key_left)
    key_right = left_shift_five(key_right)
    k1 = key_perm_eight("".join([key_left, key_right]))
    key_left = left_shift_five(key_left)
    key_right = left_shift_five(key_right)
    k2 = key_perm_eight("".join([key_left, key_right]))
    return k1, k2


def f_func(in_str, key):
    S_0 = [[1, 0, 3, 2],
           [3, 2, 1, 0],
           [0, 2, 1, 3],
           [3, 1, 3, 2]]
    S_1 = [[0, 1, 2, 3],
           [2, 0, 1, 3],
           [3, 0, 1, 0],
           [2, 1, 0, 3]]

    exp = "".join([in_str[3], in_str[0], in_str[1], in_str[2],
                   in_str[1], in_str[2], in_str[3], in_str[0]])
    p = "{0:08b}".format(int(exp, 2) ^ int(key, 2))
    p0, p1 = p[:4], p[4:]
    r = 2 * int(p0[0]) + int(p0[3])
    c = 2 * int(p0[1]) + int(p0[2])
    p2_left = S_0[r][c]
    r = 2 * int(p1[0]) + int(p1[3])
    c = 2 * int(p1[1]) + int(p1[2])
    p2_right = S_1[r][c]
    p2 = "{0:02b}{1:02b}".format(p2_left, p2_right)
    return "".join([p2[1], p2[3], p2[2], p2[0]])


def inv_init_perm(in_str):
    return "".join([in_str[3], in_str[0], in_str[2], in_str[4],
                    in_str[6], in_str[1], in_str[7], in_str[5]])


def algorithm(b_num, init_key, enc_or_dec):
    """
    Algorithm takes a binary string, initial key, and whether to encrypt or decrypt the binary string.
    It returns an encrypted or decrypted binary string.
    """

    # Initial Permutation
    perm = init_perm(b_num)

    # Split into two 4-bit blocks
    p_left, p_right = split_string(perm, 4)

    # Create k1 and k2 keys
    k1, k2 = create_keys(init_key)

    # p_right goes through F function with k1 key
    if enc_or_dec == "enc":
        p_mod = f_func(p_right, k1)
    else:
        p_mod = f_func(p_right, k2)

    # XOR p_left with p_mod
    p_left = "{0:04b}".format(int(p_left, 2) ^ int(p_mod, 2))

    # Swap p_left and p_right
    p_left, p_right = p_right, p_left

    # p_right goes through F function with k2 key
    if enc_or_dec == "enc":
        p_mod = f_func(p_right, k2)
    else:
        p_mod = f_func(p_right, k1)

    # XOR p_left with p_mod
    p_left = "{0:04b}".format(int(p_left, 2) ^ int(p_mod, 2))

    # Inverse Initial Permutation on p_left joined with p_right
    perm = inv_init_perm("".join([p_left, p_right]))
    return perm


def char_to_bin(char):
    # Convert char into integer
    n = ord(char)

    # Convert integer into 8-bit binary block
    return '{0:08b}'.format(n)


def bin_to_char(b_num):
    # Convert 8-bit binary block to integer
    n = int(b_num, 2)

    # Convert integer to char
    return chr(n)


if __name__ == "__main__":
    enc_or_dec = sys.argv[1]
    in_filename = sys.argv[2]
    out_filename = sys.argv[3]
    init_key = sys.argv[4]
    bin_list = []

    with open(out_filename, 'w') as out_file, open(in_filename, 'r') as in_file:
        in_str = in_file.read()

        # Encrypt
        if enc_or_dec == "enc":
            bin_list = [bin_to_char(algorithm(char_to_bin(c), init_key, "enc")) for c in in_str]

        # Decrypt
        elif enc_or_dec == "dec":
            bin_list = [bin_to_char(algorithm(char_to_bin(c), init_key, "dec")) for c in in_str]

        out_file.write("".join(bin_list))