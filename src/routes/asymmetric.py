from fastapi import APIRouter

router = APIRouter()


@router.get("/asymmetric/key")
def get_asym_key():
    """
    zwraca nowy klucz publiczny i prywatny w postaci HEX (w JSON jako dict) i ustawia go na serwerze
    """
    return {"message": "Hello World"}


@router.get("/asymmetric/key/ssh")
def get_key_ssh():
    """
    zwraca klucz publiczny i prywatny w postaci HEX zapisany w formacie OpenSSH
    """
    return {"message": "Hello World"}


@router.post("/asymmetric/key")
def post_asym_key():
    """
    ustawia na serwerze klucz publiczny i prywatny w postaci HEX (w JSON jako dict)
    """
    return {"message": "Hello World"}


@router.post("/asymmetric/verify")
def post_asym_verify():
    """
    korzystając z aktualnie ustawionego klucza publicznego, weryfikuję czy wiadomość była zaszyfrowana przy jego użyciu
    """
    return {"message": "Hello World"}


@router.post("/asymmetric/sign")
def post_asym_sign():
    """
    korzystając z aktualnie ustawionego klucza prywatnego, podpisuje wiadomość i zwracaą ją podpisaną
    """
    return {"message": "Hello World"}


@router.post("/asymmetric/encode")
def post_asym_encode():
    """
    wysyłamy wiadomość, w wyniku dostajemy ją zaszyfrowaną
    """
    return {"message": "Hello World"}


@router.post("/asymmetric/decode")
def post_asym_decode():
    """
    wysyłamy wiadomość, w wyniku dostajemy ją odszyfrowaną
    """
    return {"message": "Hello World"}