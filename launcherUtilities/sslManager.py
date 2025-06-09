from OpenSSL.crypto import X509

import subprocess
import os
from OpenSSL import crypto

class SSLManager:
    def __init__(self) -> None:
        pass

    def checkForSSLInstalled(self, sslPath) -> bool:
        try:
            cert = self._load_certificate(sslPath)
            cert_serial = "{:X}".format(cert.get_serial_number()).zfill(40)
            cert_thumbprint = cert.digest('sha1').decode('utf-8').replace(':', '').upper()

            result = subprocess.run(
                ['certutil', '-store', 'Root'],
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            output = result.stdout.upper()

            if f"SERIAL NUMBER: {cert_serial}" in output and f"CERT HASH(SHA1): {cert_thumbprint}" in output:
                return True
            return False
        except Exception as e:
            print(f"Error checking SSL installation: {e}")
            return False

    def installSSL(self, sslPath) -> None:
        try:
            if not self.checkForSSLInstalled(sslPath):
                subprocess.run(
                    ['certutil', '-addstore', 'Root', sslPath],
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                print(f"Certificate installed from {sslPath}")
            else:
                print("Certificate is already installed.")
        except Exception as e:
            print(f"Error installing SSL: {e}")

    def _load_certificate(self, sslPath) -> X509:
        with open(sslPath, 'rb') as f:
            cert_data = f.read()
        return crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)