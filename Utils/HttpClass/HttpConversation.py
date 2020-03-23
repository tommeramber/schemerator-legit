from .Packet import Packet


class HttpConversation:

    def __init__(self, pkt_req: Packet=None, pkt_res: Packet=None, url: str=None, method: str=None):
        """

        :param pkt_req: Packet Object that represent the request.
        :param pkt_res: Packet Object that represent the response.

        """
        self.pkt_req = pkt_req or Packet()
        self.pkt_res = pkt_res or Packet()
        self.url = url
        self.method = method

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)


