import hashlib
import re

def generate_hash(string):
    # encode the string as UTF-8 before hashing
    encoded_string = string.encode('utf-8')
    
    # create a new SHA-256 hash object
    hash_object = hashlib.sha256()
    
    # update the hash object with the encoded string
    hash_object.update(encoded_string)
    
    # get the hexadecimal string representation of the hash
    hex_dig = hash_object.hexdigest()
    
    return hex_dig

def extract_file_path(message):
    # Match URLs with the http or https scheme
    url_match = re.findall(
        r"\bhttps?://[\w./-]+\.[a-z]+(?:[\w./-]+)*\b", message)
    if url_match:
        return ("url", url_match[0])

    # Match local file paths (absolute or relative)
    file_match = re.findall(
        r"[A-Za-z0-9]+/[A-Za-z]+_[0-9]+\.[A-Za-z0-9]+", message)
    if file_match:
        return ("file", file_match[0])

    return (None, None)