import string


class RawConversation:

    def __init__(self, url: string = None, method: string = None, reqheaders: string = None, req: string = None,
                 resheaders: string = None, res: string = None):
        self.url = url
        self.method = method
        self.reqheaders = reqheaders
        self.req = req
        self.resheaders = resheaders
        self.res = res

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)
