class CtpConfig(object):

    def __init__(self, td_addr="", md_addr="", broker_id="", auth_code="", app_id="", user_id="", password="") -> None:
        self.td_addr = td_addr
        self.md_addr = md_addr
        self.broker_id = broker_id
        self.auth_code = auth_code
        self.app_id = app_id
        self.user_id = user_id
        self.password = password
