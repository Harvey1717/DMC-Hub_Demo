class BadStatusCodeError(Exception):
    "Raised when a status code is bad"


BAD_STATUS_CODES = {
    "5**": {"message": "Server Error"},
    "4**": {"message": "Client Error"},
    "403": {"message": "Forbidden"},
    "404": {"message": "Not Found"},
    "429": {"message": "Rate Limited"},
}


def check_status_code(status_code: int, ignore_codes: list = []) -> None:
    """Checks status codes against a list of bad codes.

    Arguements:
        status_code: A HTTP status code.
        ignore_codes: A list of strings of HTTP status codes to ignore

    Raises:
        BadStatusCodeError: When a status code is declared "bad".
    """
    code = str(status_code)

    if code in ignore_codes:
        return

    matched_codes = [
        bad_code for bad_code in BAD_STATUS_CODES.keys() if bad_code[0] == code[0]
    ]

    if code in matched_codes:
        raise BadStatusCodeError(f"[{code}] - {BAD_STATUS_CODES[code]['message']}")
    elif f"{code[0]}**" in matched_codes:
        raise BadStatusCodeError(f"[{code}] - Status code in range {code[0]}**")
