from ciphers import (
    caesar_encrypt, caesar_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    reverse_text,
    ascii_shift, ascii_unshift,
    base64_encode, base64_decode
)
from multilayer import multi_encrypt, multi_decrypt


def print_banner():
    #Prints a welcome banner
    print("\n" + "=" * 60)
    print("CLASSICAL ENCRYPTION TOOLKIT")
    print("=" * 60)
    print("  Supports: Caesar, Vigenère, Reverse, ASCII, Base64")
    print("  Plus Multi-Layer Encryption Mode")
    print("=" * 60 + "\n")


def get_encryption_mode():
    while True:
        mode = input("Do you want to (E)ncrypt or (D)ecrypt? ").strip().lower()
        if mode in ['e', 'd', 'encrypt', 'decrypt']:
            return mode[0]  #Return first character
        print("Invalid choice. Please enter 'E' or 'D'.\n")


def get_cipher_method():
    print("\nChoose Encryption Method:")
    print("  1. Caesar Cipher")
    print("  2. Vigenère Cipher")
    print("  3. Reverse Text")
    print("  4. ASCII Shift")
    print("  5. Base64 Encoding")
    print("  6. Multi-Layer Encryption (All Combined)")

    while True:
        try:
            choice = int(input("\nEnter choice (1-6): ").strip())
            if 1 <= choice <= 6:
                return choice
            print("Invalid choice. Please enter a number between 1 and 6.\n")
        except ValueError:
            print("Invalid input. Please enter a number.\n")


def caesar_cipher_interface(mode: str):
    #Interface for Caesar Cipher
    text = input("\nEnter the text: ").strip()

    while True:
        try:
            key = int(input("Enter Caesar key (shift amount): ").strip())
            break
        except ValueError:
            print("Invalid key. Please enter an integer.\n")

    if mode == 'e':
        result = caesar_encrypt(text, key)
        print(f"\n Encrypted Text: {result}")
    else:
        result = caesar_decrypt(text, key)
        print(f"\n Decrypted Text: {result}")


def vigenere_cipher_interface(mode: str):
    #Interface for Vigenère Cipher
    text = input("\nEnter the text: ").strip()
    keyword = input("Enter Vigenère keyword: ").strip()

    if not keyword:
        print("Keyword cannot be empty.")
        return

    if mode == 'e':
        result = vigenere_encrypt(text, keyword)
        print(f"\nEncrypted Text: {result}")
    else:
        result = vigenere_decrypt(text, keyword)
        print(f"\n Decrypted Text: {result}")


def reverse_text_interface():
    #Interface for Reverse Text
    text = input("\nEnter the text: ").strip()
    result = reverse_text(text)
    print(f"\nReversed Text: {result}")


def ascii_shift_interface(mode: str):
    #Interface for ASCII Shift
    text = input("\nEnter the text: ").strip()

    while True:
        try:
            shift_val = int(input("Enter ASCII shift value: ").strip())
            break
        except ValueError:
            print("Invalid shift value. Please enter an integer.\n")

    if mode == 'e':
        result = ascii_shift(text, shift_val)
        print(f"\nASCII Shifted Text: {result}")
    else:
        result = ascii_unshift(text, shift_val)
        print(f"\nASCII Unshifted Text: {result}")


def base64_interface(mode: str):
    #Interface for Base64 Encoding
    text = input("\nEnter the text: ").strip()

    try:
        if mode == 'e':
            result = base64_encode(text)
            print(f"\nBase64 Encoded Text: {result}")
        else:
            result = base64_decode(text)
            print(f"\nBase64 Decoded Text: {result}")
    except Exception as e:
        print(f"Error: {e}")


def multi_layer_interface(mode: str):
    #Interface for Multi-Layer Encryption
    text = input("\nEnter the text: ").strip()

    print("\nEnter keys for all cipher layers:")

    #Get Caesar key
    while True:
        try:
            caesar_key = int(input("  Caesar key (shift amount): ").strip())
            break
        except ValueError:
            print("  Invalid key. Please enter an integer.")

    #Get Vigenère keyword
    vig_key = input("  Vigenère keyword: ").strip()
    if not vig_key:
        print("Keyword cannot be empty. Using default 'KEY'.")
        vig_key = "KEY"

    #Get ASCII shift
    while True:
        try:
            ascii_key = int(input("  ASCII shift value: ").strip())
            break
        except ValueError:
            print("Invalid shift value. Please enter an integer.")

    #Perform encryption or decryption
    try:
        if mode == 'e':
            result = multi_encrypt(text, caesar_key, vig_key, ascii_key, verbose=True)
        else:
            result = multi_decrypt(text, caesar_key, vig_key, ascii_key, verbose=True)
    except Exception as e:
        print(f"Error during operation: {e}")


def main():
    #Main function to run the CLI interface
    print_banner()

    while True:
        #Get encryption/decryption mode
        mode = get_encryption_mode()

        #Get cipher method
        method = get_cipher_method()

        #Execute appropriate interface
        try:
            if method == 1:
                caesar_cipher_interface(mode)
            elif method == 2:
                vigenere_cipher_interface(mode)
            elif method == 3:
                reverse_text_interface()
            elif method == 4:
                ascii_shift_interface(mode)
            elif method == 5:
                base64_interface(mode)
            elif method == 6:
                multi_layer_interface(mode)
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

        #Ask if user wants to continue
        print("\n" + "-" * 60)
        continue_choice = input("Do you want to perform another operation? (Y/N): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            print("\nThank you for using NovaCrypt -  Encryption Toolkit!")
            print("=" * 60 + "\n")
            break
        print()


if __name__ == "__main__":
    main()