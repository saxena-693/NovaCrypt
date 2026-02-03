"""
ciphers.py - Classical Encryption Toolkit
This module contains implementations of various classical encryption techniques:
1. Caesar Cipher
2. Vigenère Cipher
3. Reverse Text Transformation
4. ASCII Shift Cipher (Safe Printable Range)
5. Base64 Encoding / Decoding
6. SHA-256 Hashing

⚠️Note:
These classical ciphers are meant for educational purposes only
and should NOT be used for real-world secure encryption.
"""

import base64
import hashlib


#CAESAR CIPHER
def caesar_encrypt(text: str, key: int) -> str:
    #Encrypts plaintext using Caesar Cipher

    key = key % 26  #Normalize key

    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + key) % 26 + base)
        else:
            result += char

    return result


def caesar_decrypt(text: str, key: int) -> str:
    #Decrypts Caesar Cipher text
    return caesar_encrypt(text, -key)


#VIGENÈRE CIPHER

def clean_keyword(keyword: str) -> str:
    #Removes non-alphabet characters from keyword

    return ''.join(filter(str.isalpha, keyword))


def vigenere_encrypt(text: str, keyword: str) -> str:
    #Encrypts plaintext using Vigenère Cipher

    keyword = clean_keyword(keyword)

    if not keyword:
        raise ValueError("Keyword must contain at least one alphabet character.")

    result = ""
    keyword_index = 0

    for char in text:
        if char.isalpha():
            key_char = keyword[keyword_index % len(keyword)]
            shift = ord(key_char.upper()) - ord('A')

            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)

            keyword_index += 1
        else:
            result += char

    return result


def vigenere_decrypt(text: str, keyword: str) -> str:
    #Decrypts Vigenère Cipher text

    keyword = clean_keyword(keyword)

    if not keyword:
        raise ValueError("Keyword must contain at least one alphabet character.")

    result = ""
    keyword_index = 0

    for char in text:
        if char.isalpha():
            key_char = keyword[keyword_index % len(keyword)]
            shift = ord(key_char.upper()) - ord('A')

            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)

            keyword_index += 1
        else:
            result += char

    return result

#REVERSE TEXT

def reverse_text(text: str) -> str:
    #Reverses the given text

    return text[::-1]

#ASCII SHIFT (Safe Printable Characters)

def ascii_shift(text: str, shift_val: int) -> str:
    #Shifts printable ASCII characters safely

    result = ""

    for char in text:
        ascii_code = ord(char)

        if 32 <= ascii_code <= 126:
            new_code = 32 + ((ascii_code - 32 + shift_val) % 95)
            result += chr(new_code)
        else:
            result += char  #Leave Unicode chars unchanged

    return result


def ascii_unshift(text: str, shift_val: int) -> str:
    #Reverses ASCII shifting

    return ascii_shift(text, -shift_val)


#BASE64 ENCODING

def base64_encode(text: str) -> str:
    #Encodes text into Base64 format

    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def base64_decode(text: str) -> str:
    #Decodes Base64 text back into plaintext

    try:
        return base64.b64decode(text.encode("utf-8")).decode("utf-8")
    except Exception:
        raise ValueError("Invalid Base64 input. Please check your ciphertext.")

#SHA-256 HASHING

def generate_sha256(text: str) -> str:
    #Generates a one-way SHA-256 hash of the input text

    return hashlib.sha256(text.encode("utf-8")).hexdigest()
