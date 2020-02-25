class TopClipException(Exception):
    def __init__(self, response_code, message):
        self.response_code = response_code
        self.message = message

    def __repr__(self):
        return f"Unexpected error:{self.response_code}:{self.message}"


class VoteException(TopClipException):
    def __init__(self, response_code, message):
        self.response_code = response_code
        self.message = message


class SubmissionException(TopClipException):
    def __init__(self, response_code, message):
        self.response_code = response_code
        self.message = message
