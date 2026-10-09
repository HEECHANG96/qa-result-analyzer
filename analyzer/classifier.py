
def classify_failure(error_message: str) -> str:
    """
    오류 메시지를 분석하여 실패 유형을 분류한다.

    Returns:
        ASSERTION, TIMEOUT, NETWORK, UNKNOWN
    """

    # 오류 메시지가 없으면 UNKNOWN 반환
    if not error_message or not error_message.strip():
        return "UNKNOWN"

    # 오류 메시지의 첫 줄을 소문자로 변환
    first_line = error_message.strip().splitlines()[0].lower()

    # 1. Timeout 관련 오류
    if "timeouterror" in first_line:
        return "TIMEOUT"

    # 2. Assertion 관련 오류
    if "assertionerror" in first_line:
        return "ASSERTION"

    # 3. Network 관련 오류
    network_keywords = [
        "networkerror",
        "connectionerror",
        "connectionrefusederror",
        "net::err_",
    ]

    if any(keyword in first_line for keyword in network_keywords):
        return "NETWORK"

    # 4. 분류할 수 없는 오류
    return "UNKNOWN"
