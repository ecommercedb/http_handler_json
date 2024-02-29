import http.client
import logging.handlers

import orjson


class JsonHttpHandler(logging.handlers.HTTPHandler):
    """Formatter to dump error message into JSON"""

    def emit(self, record):
        """
        Emit a record.

        Send the record to the web server as a JSON object.
        """
        try:
            host = self.host
            h: http.client.HTTPConnection | http.client.HTTPSConnection = self.getConnection(host, self.secure)
            url = self.url
            data = orjson.dumps(self.mapLogRecord(record))
            if self.method == "GET":
                if url.find("?") >= 0:
                    sep = "&"
                else:
                    sep = "?"
                url = url + "%c%s" % (sep, data)
            h.putrequest(self.method, url)
            if self.method == "POST":
                h.putheader("Content-type", "application/json")
                h.putheader("Content-length", str(len(data)))
            if self.credentials:
                import base64

                s = ("%s:%s" % self.credentials).encode("utf-8")
                s = "Basic " + base64.b64encode(s).strip().decode("ascii")
                h.putheader("Authorization", s)
            h.endheaders()
            if self.method == "POST":
                chunks = [data[i : i + h.blocksize] for i in range(0, len(data), h.blocksize)]
                for chunk in chunks:
                    h.send(chunk)
            h.getresponse()  # can't do anything with the result
        except Exception:
            self.handleError(record)
