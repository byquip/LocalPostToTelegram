import imaplib
from email import policy, message_from_bytes


class ReceiveMails:
    def __init__(self, conf):
        self.n = 0
        self.heads = []
        self.froms = []
        self.text = []
        self.filepath = []
        self.__conf = conf
        self.__server = self.__conf['user']['server']

    def __call__(self):
        mail = imaplib.IMAP4_SSL(self.__server)
        _,_ = mail.login(self.__conf['user']['email'],
                         self.__conf['user']['password'])
        mail.list()
        mail.select('inbox')
        self.n = 0
        self.heads = []
        self.froms = []
        (retcode, messages) = mail.search(None, '(UNSEEN)')
        if retcode == 'OK':
            for num in messages[0].split():
                print('Processing ')
                self.n += 1
                typ, data = mail.fetch(num, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        original = message_from_bytes(response_part[1], policy=policy.default)
                        self.froms.append(original['From'])
                        self.heads.append(original['Subject'])
                        _, _ = mail.store(num, '+FLAGS', '\\Seen')

            return self.n, self.froms, self.heads
