from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_video(input_path: str, output_path: str, key: bytes = None) -> bytes:
    # Generate a 256-bit AES key if not provided
    key = key or AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(key)

    # Generate a 96-bit nonce
    nonce = os.urandom(12)

    with open(input_path, 'rb') as f:
        data = f.read()

    encrypted_data = aesgcm.encrypt(nonce, data, None)

    with open(output_path, 'wb') as f:
        f.write(nonce + encrypted_data)  # Store nonce with ciphertext

    return key  # Save securely for decryption

def decrypt_video(encrypted_path: str, output_path: str, key: bytes):
    with open(encrypted_path, 'rb') as f:
        file_data = f.read()

    nonce = file_data[:12]
    ciphertext = file_data[12:]

    aesgcm = AESGCM(key)
    decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

