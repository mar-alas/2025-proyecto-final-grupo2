import pytest
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import pad
from gestor_usuarios.dominio.password_decryptor import decrypt_password


# Patch la clave de configuración
class DummyConfig:
    ENCRYPTION_KEY = "CLAVE_SECRETA_DE_TEST"

def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int, iv_len: int):
    d = b""
    last = b""
    while len(d) < key_len + iv_len:
        last = MD5.new(last + password + salt).digest()
        d += last
    return d[:key_len], d[key_len:key_len+iv_len]

def encrypt_password_cryptojs_compatible(plain_password: str, key: str) -> str:
    salt = b"12345678"  # 8 bytes, como usa CryptoJS
    key_bytes, iv = evp_bytes_to_key(key.encode(), salt, 32, 16)

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(plain_password.encode(), AES.block_size))

    final_data = b"Salted__" + salt + encrypted
    return b64encode(final_data).decode()

def test_decrypt_password(monkeypatch):
    # Preparar
    plain_password = "MiClaveSegura123"
    test_key = DummyConfig.ENCRYPTION_KEY
    encrypted_password = encrypt_password_cryptojs_compatible(plain_password, test_key)

    # Mock de Config.ENCRYPTION_KEY
    from gestor_usuarios.infraestructura import config
    monkeypatch.setattr(config.Config, "ENCRYPTION_KEY", test_key)

    # Ejecutar
    resultado = decrypt_password(encrypted_password)

    # Afirmar
    assert resultado == plain_password


def test_decrypt_password_invalid_data(monkeypatch):
    # Simula clave errónea o texto corrupto
    encrypted_data = "no-es-base64"

    with pytest.raises(ValueError) as excinfo:
        decrypt_password(encrypted_data)

    assert "Error al descifrar la contraseña" in str(excinfo.value)


def test_decrypt_password_raises_with_invalid_encrypted_block(monkeypatch):
    from gestor_usuarios.infraestructura import config
    monkeypatch.setattr(config.Config, "ENCRYPTION_KEY", "CLAVE_SECRETA_DE_TEST")

    # Base64 válido con contenido inválido (simula un bloque corrupto)
    invalid_but_base64 = b64encode(b"Salted__12345678" + b"datos_corruptos").decode()

    with pytest.raises(ValueError) as excinfo:
        decrypt_password(invalid_but_base64)

    assert "Error al descifrar la contraseña" in str(excinfo.value)


def test_decrypt_password_invalid_cipher(monkeypatch):
    from gestor_usuarios.infraestructura import config
    monkeypatch.setattr(config.Config, "ENCRYPTION_KEY", "CLAVE_SECRETA_DE_TEST")

    # Encrypted con IV correcto pero datos cifrados corruptos (fallará al hacer unpad)
    from base64 import b64encode
    corrupt_cipher_data = b"1234567890123456" + b"datos_invalidos123"
    encrypted_password = b64encode(corrupt_cipher_data).decode()

    with pytest.raises(ValueError) as excinfo:
        decrypt_password(encrypted_password)

    assert "Error al descifrar la contraseña" in str(excinfo.value)
