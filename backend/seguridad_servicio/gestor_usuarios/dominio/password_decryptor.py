from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from gestor_usuarios.infraestructura.config import Config


def decrypt_password(encrypted_password: str) -> str:
    try:
        encrypted_data = b64decode(encrypted_password)
        
        if not encrypted_data.startswith(b"Salted__"):
            raise ValueError("Formato de contraseña cifrada no válido (no comienza con 'Salted__').")

        salt = encrypted_data[8:16]
        key, iv = _evp_bytes_to_key(Config.ENCRYPTION_KEY.encode("utf-8"), salt, 32, 16)

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data[16:])
        return _unpad(decrypted).decode("utf-8")

    except Exception as e:
        raise ValueError(f"Error al descifrar la contraseña: {str(e)}")


def _evp_bytes_to_key(password: bytes, salt: bytes, key_len: int, iv_len: int):
    d = b""
    last = b""
    while len(d) < key_len + iv_len:
        last = MD5.new(last + password + salt).digest()
        d += last
    return d[:key_len], d[key_len:key_len+iv_len]


def _unpad(s: bytes) -> bytes:
    padding_len = s[-1]
    return s[:-padding_len]
