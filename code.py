from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

ciphertext="""0LxxtoIhjwk9iTl1moFZ48Uum1p4PBk+CxBAyPCaskabiMC3DUuNHpVX6pQHz8a0L4jJVLxjkGbmf2yOVHQAqUX/oWuBjzJgLR/6GIFOmpqDnoYrr/Ws3hQlTeJovm4rRXWFly3bzgvPXHle2dEN3HgCxjvq+aGY+imQt4HcYnQ="""
private_key_pem = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDxonD2gHrCttQuohIC77Prz7FcN14p5msojzwqi0mS3yFuDleq
L/YZjZ+I20/bpNRXYXiWk1ZkDhwHXcUW6A8VnnyhiMoLLAj7Fqa6pa7eFugbwKI6
hzZIVAd55zgXcKl0qc6IphS7VJBfzyKeWjZdhxjXa+lp1441kEqrIcfabwIDAQAB
AoGAHju89prMwWAu3EbbChMD6BVsk6U52vRBpCmH1arn4cCZZjPVNC4cFMZrl6wZ
KdpN10ES3YRB4vMA/sr0xhDzEfspPm2Xut1gtPMpiM5gxt16nBC272N2H/mPIgGR
EOKvi42x75pQLr6+PCjoSAuku7VbUQUucGGbM7XxGKaZRUECQQD+amG4KiwRwOJ3
cyroxFjwqxwwgNs5IarCE72McPuh+JxpLIbwc3r8wsQbWTkiSDVna9W/i4o/axJh
vzww1AUTAkEA8yOuvjM2m4s1ORk2k+gbzocgrUIWTSi9DJw1tteEFptrsdnJYbfy
M+68MoYuZjxZwowW4xSFblDtMuPkFhsstQJAelh2PbYqEy+KuJ6tl9o0WyguGjUd
N1A1abdMg+khWTbRINLE4YTnM/4FiJFTpGTNKbr1w3M7PFwlLtRkAacz+QJBALaA
CiHp/wsxqnl5W2YZywVymCx0dpjkA0L73bWofxUZA/UzK92VXM9uWwTxgtJqalWF
IYjBVoY/aEvSktmk/CECQQClSX2DqZnsE3Gw5PDSSaNQK4ocvvfPaBYISgt0HtG4
lrH1PHqr0vrcxj+uIr043jsY6Vkte5CAUOjkFIuNqXcO
-----END RSA PRIVATE KEY-----"""

private_key = serialization.load_pem_private_key(
    private_key_pem.encode(),
    password=None,
)


encrypted_data_base64 = ciphertext


encrypted_data = base64.b64decode(encrypted_data_base64)


decrypted_data = private_key.decrypt(
    encrypted_data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None
    )
)


decrypted_data = decrypted_data.decode('utf-8')
print(f'Decrypted data: {decrypted_data}')