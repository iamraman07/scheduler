import os
import json
from cryptography.fernet import Fernet
import logging

def generate_or_load_key(key_file_path):
    """Generate or load encryption key"""
    try:
        if os.path.exists(key_file_path):
            with open(key_file_path, "rb") as key_file:
                return key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file_path, "wb") as key_file:
                key_file.write(key)
            return key
    except Exception as e:
        logging.error(f"Error with encryption key: {e}")
        raise

def encrypt_data(data, key, job_id):
    """Encrypt data and save it to a file"""
    try:
        cipher_suite = Fernet(key)
        serialized_data = json.dumps(data)
        encrypted_data = cipher_suite.encrypt(serialized_data.encode())
        
        # Save the encrypted data to a file named with the job_id
        encrypted_file = f"{job_id}.enc"
        with open(encrypted_file, "wb") as file:
            file.write(encrypted_data)
        
        return encrypted_file
    except Exception as e:
        logging.error(f"Encryption error: {e}")
        raise

def decrypt_data(key, job_id):
    """Decrypt data from a file"""
    try:
        cipher_suite = Fernet(key)
        
        # Read the encrypted data from the file named with the job_id
        encrypted_file = f"{job_id}.enc"
        if not os.path.exists(encrypted_file):
            logging.error(f"No encrypted file found for job_id: {job_id}")
            return None
        
        with open(encrypted_file, "rb") as file:
            encrypted_data = file.read()
        
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return json.loads(decrypted_data)
    except Exception as e:
        logging.error(f"Decryption error for job_id {job_id}: {e}")
        return None
