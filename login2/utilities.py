import logging
import bcrypt

def setup_logger():
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)s [%(levelname)s] %(message)s'
        )
    logging.debug('Logger initialized')


def get_hash(plaintext):
    try:
        # convert plaintext to bytes
        password_bytes = plaintext.encode('utf-8')
        # generate hash
        hash_value = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        # convert to string for DB storage
        return hash_value.decode('utf-8')
    except Exception as e:
        logging.error(f'Hash generation failed, error: {e}')
    return None
