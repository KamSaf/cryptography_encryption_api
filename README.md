## Description

REST API application created with Python and FastAPI for Cryptography classes.
It implements Cryptography library, allowing user for symmetric and asymmetric encryption and decryption, and also for creating and verifying signatures.


## How to install (for Linux, macOS)

Create Python virtual environment, for example:

        virtualenv venv

Activate virtual environment:

        source venv/bin/activate

Run this command to install required dependencies

        pip install -r requirements.txt


## How to run

To start application run:

        python app.py

Or:

        uvicorn src.main:app --reload


## Endpoints


| **METHOD** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | **ENDPOINT** | **ACTION** | ***Parameters*** |
| ------------- | ------------- | ------------- | ------------- |
| ```/``` | ```GET``` | Returns list of avaible endpoints | N/A |
| ```/symmetric/key``` | ```GET``` | Returns randomly generated symmetric key | N/A |
| ```/asymmetric/key``` | ```GET``` | Returns new private and public asymmetric keys and sets them on the server | N/A |
| ```/asymmetric/key/ssh``` | ```GET``` | Returns new private and public asymmetric keys in an OpenSSH format | N/A |
| ```/symmetric/key``` | ```POST``` | Sets symmetric key on the server | ```key``` |
| ```/symmetric/encode``` | ```POST``` | Encrypts message using currently set symmetric key | ```message``` |
| ```/symmetric/decode``` | ```POST``` | Decrypts message using currently set symmetric key | ```message``` |
| ```/asymmetric/key``` | ```POST``` | Sets private and public asymmetric keys on the server | ```public_key```, ```private_key``` |
| ```/asymmetric/sign``` | ```POST``` | Signs given message with currently set private RSA key | ```message``` |
| ```/asymmetric/verify``` | ```POST``` | Verifies signature on a given message | ```message```, ```signature``` |
| ```/asymmetric/encode``` | ```POST``` | Encrypts and returns given message using currently set RSA public key | ```message``` |
| ```/asymmetric/decode``` | ```POST``` | Decrypts and returns given message using currently set RSA private key | ```message``` |





## Testing

To run unit test:

        python run_tests.py
