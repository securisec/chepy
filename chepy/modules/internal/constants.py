from collections import Counter


class Rabbit:  # pragma: no cover
    # https://github.com/mozilla/positron/blob/master/python/PyECC/ecc/Rabbit.py
    # ------------------------------------------------------------------------------
    #
    #   R A B B I T   Stream Cipher
    #   by M. Boesgaard, M. Vesterager, E. Zenner (specified in RFC 4503)
    #
    #
    #   Pure Python Implementation by Toni Mattis
    #
    # ------------------------------------------------------------------------------
    def __init__(self, key, iv=None):
        """Initialize Rabbit cipher using a 128 bit integer/string"""
        self.WORDSIZE = 0x100000000

        self.rot08 = lambda x: ((x << 8) & 0xFFFFFFFF) | (x >> 24)
        self.rot16 = lambda x: ((x << 16) & 0xFFFFFFFF) | (x >> 16)

        if isinstance(key, str):
            # interpret key string in big endian byte order
            if len(key) < 16:
                key = "\x00" * (16 - len(key)) + key
            # if len(key) > 16 bytes only the first 16 will be considered
            k = [ord(key[i + 1]) | (ord(key[i]) << 8) for i in range(14, -1, -2)]
        else:
            # k[0] = least significant 16 bits
            # k[7] = most significant 16 bits
            k = [(key >> i) & 0xFFFF for i in range(0, 128, 16)]

        # State and counter initialization
        x = [
            (k[(j + 5) % 8] << 16) | k[(j + 4) % 8]
            if j & 1
            else (k[(j + 1) % 8] << 16) | k[j]
            for j in range(8)
        ]
        c = [
            (k[j] << 16) | k[(j + 1) % 8]
            if j & 1
            else (k[(j + 4) % 8] << 16) | k[(j + 5) % 8]
            for j in range(8)
        ]

        self.x = x
        self.c = c
        self.b = 0
        self._buf = 0  # output buffer
        self._buf_bytes = 0  # fill level of buffer

        self.next()
        self.next()
        self.next()
        self.next()

        for j in range(8):
            c[j] ^= x[(j + 4) % 8]

        self.start_x = self.x[:]  # backup initial key for IV/reset
        self.start_c = self.c[:]
        self.start_b = self.b

        if iv != None:
            self.set_iv(iv)

    def _nsf(self, u, v):
        """Internal non-linear state transition"""
        s = (u + v) % self.WORDSIZE
        s = s * s
        return (s ^ (s >> 32)) % self.WORDSIZE

    def reset(self, iv=None):
        """Reset the cipher and optionally set a new IV (int64 / string)."""

        self.c = self.start_c[:]
        self.x = self.start_x[:]
        self.b = self.start_b
        self._buf = 0
        self._buf_bytes = 0
        if iv != None:
            self.set_iv(iv)

    def set_iv(self, iv):
        """Set a new IV (64 bit integer / bytestring)."""

        if isinstance(iv, str):
            i = 0
            for c in iv:
                i = (i << 8) | ord(c)
            iv = i

        c = self.c
        i0 = iv & 0xFFFFFFFF
        i2 = iv >> 32
        i1 = ((i0 >> 16) | (i2 & 0xFFFF0000)) % self.WORDSIZE
        i3 = ((i2 << 16) | (i0 & 0x0000FFFF)) % self.WORDSIZE

        c[0] ^= i0
        c[1] ^= i1
        c[2] ^= i2
        c[3] ^= i3
        c[4] ^= i0
        c[5] ^= i1
        c[6] ^= i2
        c[7] ^= i3

        self.next()
        self.next()
        self.next()
        self.next()

    def next(self):
        """Proceed to the next internal state"""

        c = self.c
        x = self.x
        b = self.b

        t = c[0] + 0x4D34D34D + b
        c[0] = t % self.WORDSIZE
        t = c[1] + 0xD34D34D3 + t // self.WORDSIZE
        c[1] = t % self.WORDSIZE
        t = c[2] + 0x34D34D34 + t // self.WORDSIZE
        c[2] = t % self.WORDSIZE
        t = c[3] + 0x4D34D34D + t // self.WORDSIZE
        c[3] = t % self.WORDSIZE
        t = c[4] + 0xD34D34D3 + t // self.WORDSIZE
        c[4] = t % self.WORDSIZE
        t = c[5] + 0x34D34D34 + t // self.WORDSIZE
        c[5] = t % self.WORDSIZE
        t = c[6] + 0x4D34D34D + t // self.WORDSIZE
        c[6] = t % self.WORDSIZE
        t = c[7] + 0xD34D34D3 + t // self.WORDSIZE
        c[7] = t % self.WORDSIZE
        b = t // self.WORDSIZE

        g = [self._nsf(x[j], c[j]) for j in range(8)]

        x[0] = (g[0] + self.rot16(g[7]) + self.rot16(g[6])) % self.WORDSIZE
        x[1] = (g[1] + self.rot08(g[0]) + g[7]) % self.WORDSIZE
        x[2] = (g[2] + self.rot16(g[1]) + self.rot16(g[0])) % self.WORDSIZE
        x[3] = (g[3] + self.rot08(g[2]) + g[1]) % self.WORDSIZE
        x[4] = (g[4] + self.rot16(g[3]) + self.rot16(g[2])) % self.WORDSIZE
        x[5] = (g[5] + self.rot08(g[4]) + g[3]) % self.WORDSIZE
        x[6] = (g[6] + self.rot16(g[5]) + self.rot16(g[4])) % self.WORDSIZE
        x[7] = (g[7] + self.rot08(g[6]) + g[5]) % self.WORDSIZE

        self.b = b
        return self

    def derive(self):
        """Derive a 128 bit integer from the internal state"""

        x = self.x
        return (
            ((x[0] & 0xFFFF) ^ (x[5] >> 16))
            | (((x[0] >> 16) ^ (x[3] & 0xFFFF)) << 16)
            | (((x[2] & 0xFFFF) ^ (x[7] >> 16)) << 32)
            | (((x[2] >> 16) ^ (x[5] & 0xFFFF)) << 48)
            | (((x[4] & 0xFFFF) ^ (x[1] >> 16)) << 64)
            | (((x[4] >> 16) ^ (x[7] & 0xFFFF)) << 80)
            | (((x[6] & 0xFFFF) ^ (x[3] >> 16)) << 96)
            | (((x[6] >> 16) ^ (x[1] & 0xFFFF)) << 112)
        )

    def keystream(self, n):
        """Generate a keystream of n bytes"""

        res = ""
        b = self._buf
        j = self._buf_bytes
        next = self.next
        derive = self.derive

        for i in range(n):
            if not j:
                j = 16
                next()
                b = derive()
            res += chr(b & 0xFF)
            j -= 1
            b >>= 1

        self._buf = b
        self._buf_bytes = j
        return res

    def encrypt(self, data):
        """Encrypt/Decrypt data of arbitrary length."""

        res = ""
        b = self._buf
        j = self._buf_bytes
        next = self.next
        derive = self.derive

        for c in data:
            if not j:  # empty buffer => fetch next 128 bits
                j = 16
                next()
                b = derive()
            res += chr(ord(c) ^ (b & 0xFF))
            j -= 1
            b >>= 1
        self._buf = b
        self._buf_bytes = j
        return res

    decrypt = encrypt


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None


class Ciphers:
    @staticmethod
    def gen_polybius_square(keyword):
        alpha = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        pol_array = list(keyword.upper() + alpha)
        pol_array = sorted(
            list(set(pol_array)),
            key=lambda x: (pol_array.index(x) // 5, pol_array.index(x) % 5),
        )
        polybius = []

        for i in range(5):
            polybius.append(pol_array[i * 5 : i * 5 + 5])

        return polybius

    @staticmethod
    def build_huffman_tree(data):
        char_freq = dict(Counter(data))
        nodes = [HuffmanNode(char, freq) for char, freq in char_freq.items()]

        while len(nodes) > 1:
            nodes = sorted(nodes, key=lambda x: x.freq)
            left = nodes.pop(0)
            right = nodes.pop(0)
            parent = HuffmanNode(None, left.freq + right.freq)
            parent.left = left
            parent.right = right
            nodes.append(parent)

        return nodes[0]

    @staticmethod
    def build_huffman_codes(root, current_code, huffman_codes):
        if root is None:  # pragma: no cover
            return

        if root.char is not None:
            huffman_codes[root.char] = current_code
            return

        Ciphers.build_huffman_codes(root.left, current_code + "0", huffman_codes)
        Ciphers.build_huffman_codes(root.right, current_code + "1", huffman_codes)


class Encoding(object):
    UPSIDE_DOWN = {
        "!": "¡",
        '"': '"',
        "#": "#",
        "$": "$",
        "%": "%",
        "&": "⅋",
        "'": ",",
        "(": ")",
        ")": "(",
        "*": "*",
        "+": "+",
        ",": "'",
        "-": "-",
        ".": ".",
        "/": "\\",
        "0": "0",
        "1": "Ɩ",
        "2": "ᄅ",
        "3": "Ɛ",
        "4": "ㄣ",
        "5": "ϛ",
        "6": "9",
        "7": "ㄥ",
        "8": "8",
        "9": "6",
        ":": ":",
        ";": ";",
        "<": ">",
        "=": "=",
        ">": "<",
        "?": "¿",
        "@": "@",
        "A": "∀",
        "B": "q",
        "C": "Ɔ",
        "D": "D",
        "E": "Ǝ",
        "F": "ſ",
        "G": "פ",
        "I": "I",
        "K": "ʞ",
        "L": "˥",
        "M": "W",
        "N": "N",
        "O": "O",
        "P": "Ԁ",
        "Q": "Q",
        "R": "ɹ",
        "S": "S",
        "T": "┴",
        "U": "∩",
        "V": "Λ",
        "W": "M",
        "X": "X",
        "Y": "⅄",
        "Z": "Z",
        "[": "]",
        "]": "[",
        "a": "ɐ",
        "b": "q",
        "c": "ɔ",
        "d": "p",
        "e": "ǝ",
        "f": "ɟ",
        "g": "ƃ",
        "h": "ɥ",
        "i": "ᴉ",
        "j": "ɾ",
        "k": "ʞ",
        "l": "l",
        "m": "ɯ",
        "n": "u",
        "p": "d",
        "q": "b",
        "r": "ɹ",
        "s": "s",
        "t": "ʇ",
        "u": "n",
        "v": "ʌ",
        "w": "ʍ",
        "x": "x",
        "y": "ʎ",
        "z": "z",
    }

    BACON_26 = {
        "A": "aaaaa",
        "B": "aaaab",
        "C": "aaaba",
        "D": "aaabb",
        "E": "aabaa",
        "F": "aabab",
        "G": "aabba",
        "H": "aabbb",
        "I": "abaaa",
        "J": "abaab",
        "K": "ababa",
        "L": "ababb",
        "M": "abbaa",
        "N": "abbab",
        "O": "abbba",
        "P": "abbbb",
        "Q": "baaaa",
        "R": "baaab",
        "S": "baaba",
        "T": "baabb",
        "U": "babaa",
        "V": "babab",
        "W": "babba",
        "X": "babbb",
        "Y": "bbaaa",
        "Z": "bbaab",
    }

    BACON_24 = {
        "A": "aaaaa",
        "B": "aaaab",
        "C": "aaaba",
        "D": "aaabb",
        "E": "aabaa",
        "F": "aabab",
        "G": "aabba",
        "H": "aabbb",
        "I": "abaaa",
        "J": "abaaa",
        "K": "ababa",
        "L": "ababb",
        "M": "abbaa",
        "N": "abbab",
        "O": "abbba",
        "P": "abbbb",
        "Q": "baaaa",
        "R": "baaab",
        "S": "baaba",
        "T": "baabb",
        "U": "babaa",
        "V": "babaa",
        "W": "babba",
        "X": "babbb",
        "Y": "bbaaa",
        "Z": "bbaab",
    }

    BASE91_ALPHABET = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "!",
        "#",
        "$",
        "%",
        "&",
        "(",
        ")",
        "*",
        "+",
        ",",
        ".",
        "/",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
        "[",
        "]",
        "^",
        "_",
        "`",
        "{",
        "|",
        "}",
        "~",
        '"',
    ]
    LEETCODE = char_map = [
        ["A", "a", "4", "@"],
        ["B", "b", "8"],
        ["C", "c"],
        ["D", "d"],
        ["E", "e", "3"],
        ["F", "f"],
        ["G", "g", "6", "9"],
        ["H", "h"],
        ["I", "i", "1"],
        ["J", "j"],
        ["K", "k"],
        ["L", "l", "1"],
        ["M", "m"],
        ["N", "n"],
        ["O", "o", "0"],
        ["P", "p"],
        ["Q", "q"],
        ["R", "r"],
        ["S", "s", "5", "$"],
        ["T", "t", "7"],
        ["U", "u"],
        ["V", "v"],
        ["W", "w"],
        ["X", "x"],
        ["Y", "y"],
        ["Z", "z", "2"],
    ]

    NATO_CONSTANTS_DICT = {
        "A": "Alpha",
        "B": "Bravo",
        "C": "Charlie",
        "D": "Delta",
        "E": "Echo",
        "F": "Foxtrot",
        "G": "Golf",
        "H": "Hotel",
        "I": "India",
        "J": "Juliett",
        "K": "Kilo",
        "L": "Lima",
        "M": "Mike",
        "N": "November",
        "O": "Oscar",
        "P": "Papa",
        "Q": "Quebec",
        "R": "Romeo",
        "S": "Sierra",
        "T": "Tango",
        "U": "Uniform",
        "V": "Victor",
        "W": "Whiskey",
        "X": "Xray",
        "Y": "Yankee",
        "Z": "Zulu",
        "-": "Dash",
        ".": "Dot",
        "0": "Zero",
        "1": "One",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
    }

    py_encodings = [
        "ascii",
        "big5",
        "big5hkscs",
        "cp037",
        "cp424",
        "cp437",
        "cp500",
        "cp737",
        "cp775",
        "cp850",
        "cp852",
        "cp855",
        "cp856",
        "cp857",
        "cp860",
        "cp861",
        "cp862",
        "cp863",
        "cp864",
        "cp865",
        "cp866",
        "cp869",
        "cp874",
        "cp875",
        "cp932",
        "cp949",
        "cp950",
        "cp1006",
        "cp1026",
        "cp1140",
        "cp1250",
        "cp1251",
        "cp1252",
        "cp1253",
        "cp1254",
        "cp1255",
        "cp1256",
        "cp1257",
        "cp1258",
        "euc_jp",
        "euc_jis_2004",
        "euc_jisx0213",
        "euc_kr",
        "gb2312",
        "gbk",
        "gb18030",
        "hz",
        "iso2022_jp",
        "iso2022_jp_1",
        "iso2022_jp_2",
        "iso2022_jp_2004",
        "iso2022_jp_3",
        "iso2022_jp_ext",
        "iso2022_kr",
        "latin_1",
        "iso8859_2",
        "iso8859_3",
        "iso8859_4",
        "iso8859_5",
        "iso8859_6",
        "iso8859_7",
        "iso8859_8",
        "iso8859_9",
        "iso8859_10",
        "iso8859_13",
        "iso8859_14",
        "iso8859_15",
        "johab",
        "koi8_r",
        "koi8_u",
        "mac_cyrillic",
        "mac_greek",
        "mac_iceland",
        "mac_latin2",
        "mac_roman",
        "mac_turkish",
        "ptcp154",
        "shift_jis",
        "shift_jis_2004",
        "shift_jisx0213",
        "utf_16",
        "utf_16_be",
        "utf_16_le",
        "utf_7",
        "utf_8",
    ]

    py_text_encodings = [
        "base64_codec",
        "bz2_codec",
        "hex_codec",
        "idna",
        "palmos",
        "punycode",
        "quopri_codec",
        "raw_unicode_escape",
        "rot_13",
        "unicode_escape",
        "uu_codec",
        "zlib_codec",
    ]

    asciichars = [
        " ",
        "!",
        '"',
        "#",
        "$",
        "%",
        "&",
        "",
        "(",
        ")",
        "*",
        "+",
        ",",
        "-",
        ".",
        "/",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "[",
        "\\",
        "]",
        "^",
        "_",
    ]

    brailles = [
        "⠀",
        "⠮",
        "⠐",
        "⠼",
        "⠫",
        "⠩",
        "⠯",
        "⠄",
        "⠷",
        "⠾",
        "⠡",
        "⠬",
        "⠠",
        "⠤",
        "⠨",
        "⠌",
        "⠴",
        "⠂",
        "⠆",
        "⠒",
        "⠲",
        "⠢",
        "⠖",
        "⠶",
        "⠦",
        "⠔",
        "⠱",
        "⠰",
        "⠣",
        "⠿",
        "⠜",
        "⠹",
        "⠈",
        "⠁",
        "⠃",
        "⠉",
        "⠙",
        "⠑",
        "⠋",
        "⠛",
        "⠓",
        "⠊",
        "⠚",
        "⠅",
        "⠇",
        "⠍",
        "⠝",
        "⠕",
        "⠏",
        "⠟",
        "⠗",
        "⠎",
        "⠞",
        "⠥",
        "⠧",
        "⠺",
        "⠭",
        "⠽",
        "⠵",
        "⠪",
        "⠳",
        "⠻",
        "⠘",
        "⠸",
    ]

    wingdings = {
        "!": 128393,
        '"': 9986,
        "#": 9985,
        "$": 128083,
        "%": 128365,
        "&": 128366,
        "'": 128367,
        "(": 128383,
        ")": 9990,
        "*": 128386,
        "+": 128387,
        ",": 128234,
        "-": 128235,
        ".": 128236,
        "/": 128237,
        "0": 128193,
        "1": 128194,
        "2": 128196,
        "3": 128463,
        "4": 128464,
        "5": 128452,
        "6": 8987,
        "7": 128430,
        "8": 128432,
        "9": 128434,
        ":": 128435,
        ";": 128436,
        "<": 128427,
        "=": 128428,
        ">": 9991,
        "?": 9997,
        "@": 128398,
        "A": 9996,
        "B": 128076,
        "C": 128077,
        "D": 128078,
        "E": 9756,
        "F": 9758,
        "G": 9757,
        "H": 9759,
        "I": 128400,
        "J": 9786,
        "K": 128528,
        "L": 9785,
        "M": 128163,
        "N": 9760,
        "O": 127987,
        "P": 127985,
        "Q": 9992,
        "R": 9788,
        "S": 128167,
        "T": 10052,
        "U": 128326,
        "V": 10014,
        "W": 128328,
        "X": 10016,
        "Y": 10017,
        "Z": 9770,
        "[": 9775,
        "\\": 2384,
        "]": 9784,
        "^": 9800,
        "_": 9801,
        "`": 9802,
        "a": 9803,
        "b": 9804,
        "c": 9805,
        "d": 9806,
        "e": 9807,
        "f": 9808,
        "g": 9809,
        "h": 9810,
        "i": 9811,
        "j": 128624,
        "k": 128629,
        "l": 9679,
        "m": 128318,
        "n": 9632,
        "o": 9633,
        "p": 128912,
        "q": 10065,
        "r": 10066,
        "s": 11047,
        "t": 10731,
        "u": 9670,
        "v": 10070,
        "w": 11045,
        "x": 8999,
        "y": 11193,
        "z": 8984,
        "{": 10048,
        "|": 127990,
        "}": 10077,
        "~": 128631,
        " ": " ",
    }


class EncryptionConsts(object):
    MORSE_CODE_DICT = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "0": "-----",
        ", ": "--..--",
        ".": ".-.-.-",
        "?": "..--..",
        "/": "-..-.",
        "-": "-....-",
        "(": "-.--.",
        ")": "-.--.-",
        "=": "-...-",
        "@": ".-...",
        "_": "..--.-",
        "$": "...-..-",
        "@": ".--.-.",
        "!": "-.-.--",
    }


class PcapUSB:
    qwerty_map = {
        "04": "a",
        "05": "b",
        "06": "c",
        "07": "d",
        "08": "e",
        "09": "f",
        "0a": "g",
        "0b": "h",
        "0c": "i",
        "0d": "j",
        "0e": "k",
        "0f": "l",
        "10": "m",
        "11": "n",
        "12": "o",
        "13": "p",
        "14": "q",
        "15": "r",
        "16": "s",
        "17": "t",
        "18": "u",
        "19": "v",
        "1a": "w",
        "1b": "x",
        "1c": "y",
        "1d": "z",
        "1e": "1",
        "1f": "2",
        "20": "3",
        "21": "4",
        "22": "5",
        "23": "6",
        "24": "7",
        "25": "8",
        "26": "9",
        "27": "0",
        "2d": "-",
        "2e": "=",
        "2f": "[",
        "30": "]",
        "31": "\\",
        "32": "#",
        "33": ";",
        "34": "'",
        "35": "`",
        "36": ",",
        "37": ".",
        "38": "/",
        "28": "ENTER\n",
        "2c": " ",
        "4f": "RIGHTARROW",
        "50": "LEFTARROW",
        "51": "DOWNARROW",
        "52": "UPARROW",
        "4c": "DEL",
        "2a": "BACKSPACE",
        "3a": "F1",
        "3b": "F2",
        "3c": "F3",
        "3d": "F4",
        "3e": "F5",
        "3f": "F6",
        "40": "F7",
        "41": "F8",
        "42": "F9",
        "43": "F10",
        "44": "F11",
        "45": "F12",
    }
    qwerty_modifier = {
        "1e": "!",
        "1f": "@",
        "20": "#",
        "21": "$",
        "22": "%",
        "23": "^",
        "24": "&",
        "25": "*",
        "26": "(",
        "27": ")",
        "2b": "\t",
        "2c": " ",
        "2d": "_",
        "2e": "+",
        "2f": "{",
        "30": "}",
        "31": "|",
        "32": "~",
        "33": ":",
        "34": '"',
        "35": "~",
        "36": "<",
        "37": ">",
        "38": "?",
    }

    dvorak = {
        "04": "a",
        "05": "x",
        "06": "j",
        "07": "e",
        "08": ".",
        "09": "u",
        "0a": "i",
        "0b": "d",
        "0c": "c",
        "0d": "h",
        "0e": "t",
        "0f": "n",
        "10": "m",
        "11": "b",
        "12": "r",
        "13": "l",
        "14": "'",
        "15": "p",
        "16": "o",
        "17": "y",
        "18": "g",
        "19": "k",
        "1a": ",",
        "1b": "q",
        "1c": "f",
        "1d": ";",
        "1e": "1",
        "1f": "2",
        "20": "3",
        "21": "4",
        "22": "5",
        "23": "6",
        "24": "7",
        "25": "8",
        "26": "9",
        "27": "0",
        "2d": "[",
        "2e": "]",
        "2f": "/",
        "30": "=",
        "31": "\\",
        "33": "s",
        "34": "-",
        "35": "`",
        "36": "w",
        "37": "v",
        "38": "z",
    }

    dvorak_modifier = {
        "1e": "!",
        "1f": "@",
        "20": "#",
        "21": "$",
        "22": "%",
        "23": "^",
        "24": "&",
        "25": "*",
        "26": "(",
        "27": ")",
        "2b": "\t",
        "2c": " ",
        "2d": "{",
        "2e": "}",
        "2f": "?",
        "30": "+",
        "31": "|",
        "32": "~",
        "33": "S",
        "34": "_",
        "35": "~",
        "36": "<",
        "37": ">",
        "38": "?",
    }
