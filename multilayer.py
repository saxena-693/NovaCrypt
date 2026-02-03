"""
Multi-Layer Encryption Module
This module implements a multi-layer encryption system that combines
multiple classical ciphers in sequence for enhanced obfuscation.

Encryption Order:-
1. Caesar Cipher
2. Vigenère Cipher
3. Reverse Text
4. ASCII Shift
5. Base64 Encode

Decryption Order (reverse):-
1. Base64 Decode
2. ASCII Unshift
3. Reverse Text
4. Vigenère Decrypt
5. Caesar Decrypt
"""

from ciphers import (
    caesar_encrypt, caesar_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    reverse_text,
    ascii_shift, ascii_unshift,
    base64_encode, base64_decode
)


def multi_encrypt(text: str, caesar_key: int, vig_key: str, ascii_key: int, verbose: bool = True) -> str:
    #Encrypts text using multiple layers of classical ciphers

    if verbose:
        print("\n" + "=" * 60)
        print("MULTI-LAYER ENCRYPTION PROCESS")
        print("=" * 60)
        print(f"Original Text: {text}")
        print("-" * 60)

    #Step 1: Caesar Cipher
    step1 = caesar_encrypt(text, caesar_key)
    if verbose:
        print(f"Step 1 - Caesar Cipher (key={caesar_key}):")
        print(f"  Result: {step1}")

    #Step 2: Vigenère Cipher
    step2 = vigenere_encrypt(step1, vig_key)
    if verbose:
        print(f"Step 2 - Vigenère Cipher (keyword='{vig_key}'):")
        print(f"  Result: {step2}")

    #Step 3: Reverse Text
    step3 = reverse_text(step2)
    if verbose:
        print(f"Step 3 - Reverse Text:")
        print(f"  Result: {step3}")

    #Step 4: ASCII Shift
    step4 = ascii_shift(step3, ascii_key)
    if verbose:
        print(f"Step 4 - ASCII Shift (shift={ascii_key}):")
        print(f"  Result: {step4}")

    #Step 5: Base64 Encode
    step5 = base64_encode(step4)
    if verbose:
        print(f"Step 5 - Base64 Encode:")
        print(f"  Result: {step5}")
        print("=" * 60)
        print(f"FINAL ENCRYPTED TEXT: {step5}")
        print("=" * 60 + "\n")

    return step5


def multi_decrypt(text: str, caesar_key: int, vig_key: str, ascii_key: int, verbose: bool = True) -> str:
    #Decrypts multi-layer encrypted text by reversing all transformations

    if verbose:
        print("\n" + "=" * 60)
        print("MULTI-LAYER DECRYPTION PROCESS")
        print("=" * 60)
        print(f"Encrypted Text: {text}")
        print("-" * 60)

    #Step 1: Base64 Decode
    step1 = base64_decode(text)
    if verbose:
        print(f"Step 1 - Base64 Decode:")
        print(f"  Result: {step1}")

    #Step 2: ASCII Unshift
    step2 = ascii_unshift(step1, ascii_key)
    if verbose:
        print(f"Step 2 - ASCII Unshift (shift={ascii_key}):")
        print(f"  Result: {step2}")

    #Step 3: Reverse Text
    step3 = reverse_text(step2)
    if verbose:
        print(f"Step 3 - Reverse Text:")
        print(f"  Result: {step3}")

    #Step 4: Vigenère Decrypt
    step4 = vigenere_decrypt(step3, vig_key)
    if verbose:
        print(f"Step 4 - Vigenère Decrypt (keyword='{vig_key}'):")
        print(f"  Result: {step4}")

    #Step 5: Caesar Decrypt
    step5 = caesar_decrypt(step4, caesar_key)
    if verbose:
        print(f"Step 5 - Caesar Decrypt (key={caesar_key}):")
        print(f"  Result: {step5}")
        print("=" * 60)
        print(f"FINAL DECRYPTED TEXT: {step5}")
        print("=" * 60 + "\n")

    return step5


def test_multi_layer():
    #Test function to verify multi-layer encryption and decryption work correctly

    print("\n" + "TESTING MULTI-LAYER ENCRYPTION SYSTEM" + "\n")

    #Test case 1
    original = "Hello World"
    caesar_k = 3
    vig_k = "KEY"
    ascii_k = 2

    print(f"Test Case: '{original}'")
    print(f"Keys: Caesar={caesar_k}, Vigenère='{vig_k}', ASCII={ascii_k}\n")

    #Encrypt
    encrypted = multi_encrypt(original, caesar_k, vig_k, ascii_k, verbose=True)

    #Decrypt
    decrypted = multi_decrypt(encrypted, caesar_k, vig_k, ascii_k, verbose=True)

    #Verify
    if decrypted == original:
        print("SUCCESS: Decryption restored original text!")
    else:
        print("FAILURE: Decryption did not restore original text")
        print(f"Expected: {original}")
        print(f"Got: {decrypted}")

    return decrypted == original


if __name__ == "__main__":
    #Run test when module is executed directly
    test_multi_layer()