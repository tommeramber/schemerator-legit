import mitmproxy
from mitmproxy import ctx
from mitmproxy import http
from mitmproxy import flow

import sqlite3
from sqlite3 import Error
from contextlib import closing

import json

from mitmproxy.net.http.http1.assemble import assemble_request_head, assemble_response_head

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError:
    return False
  return True

class Saver:
    def __init__(self):
        try: 
            self.conn = sqlite3.connect("/home/mitmproxy/db/db.db") # change this, the best practice is to use environment variable
            with closing(self.conn.cursor()) as cur:
                #cur.execute("drop table RawConversations;")
                cur.execute("CREATE TABLE IF NOT EXISTS RawConversations (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, method TEXT, reqheaders TEXT, req TEXT, resheaders TEXT, res TEXT)")
        except Error as e:
            ctx.log.error("db error {}".format(e))        

    def response(self, flow: http.HTTPFlow):
        if flow.request.text != "" and not is_json(flow.request.text):
            ctx.log.info("request not json")
            return

        if flow.response.text != "" and not is_json(flow.response.text):
            ctx.log.info("response not json")
            return

        with closing(self.conn.cursor()) as cur:
            # TODO :Check option that is not http1 only
            cur.execute("INSERT INTO RawConversations (url, method, reqheaders, req, resheaders, res) VALUES (?, ?, ?, ?, ?, ?)", 
                        (
                            flow.request.url.split("?")[0],
                            flow.request.method,
                            assemble_request_head(flow.request).decode('utf-8'),
                            flow.request.text,
                            assemble_response_head(flow.response).decode('utf-8'),
                            flow.response.text
                        )
            )

    # db.requests.get(origin="twiiter.com")
    def done(self):
        self.conn.commit()
        self.conn.close()


addons = [
    Saver()
]