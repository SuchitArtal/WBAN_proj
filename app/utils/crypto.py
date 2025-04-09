from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64
from app.utils.storage import User

def generate_ecc_key_pair():
    """
    Generate an ECC key pair using the SECP256R1 curve.
    Returns a tuple of (private_key_pem, public_key_pem).
    """
    # Generate a private key for use in ECC
    private_key = ec.generate_private_key(ec.SECP256R1())
    
    # Get the public key from the private key
    public_key = private_key.public_key()
    
    # Serialize the private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    
    # Serialize the public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    
    return private_key_pem, public_key_pem

def load_private_key(private_key_pem):
    """
    Load a private key from PEM format.
    """
    return serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None
    )

def load_public_key(public_key_pem):
    """
    Load a public key from PEM format.
    """
    return serialization.load_pem_public_key(
        public_key_pem.encode()
    )

def get_private_key_from_db(user_id, db):
    """
    Retrieve the private key for a given user from the database.
    """
    try:
        # Get the private key directly from the user model
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            return user.private_key
        return None
    except Exception as e:
        print(f"Error retrieving private key: {e}")
        return None 