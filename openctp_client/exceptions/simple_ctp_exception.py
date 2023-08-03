class CallException(Exception):
    def __init__(self, error_id) -> None:
        super().__init__()
        self.error_id = error_id
    
    def __str__(self) -> str:
        return "ErrorID: %s" % self.error_id

class CtpException(Exception):
    def __init__(self, error_id, error_msg):
        super().__init__()
        self.error_id = error_id
        self.error_msg = error_msg

    def __str__(self):
        return "ErrorID: %s, ErrorMsg: %s" % (self.error_id, self.error_msg)
