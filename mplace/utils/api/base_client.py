from typing import Optional

from requests import Session, Response, Request


class ClientBase:
    session: Session

    def _check_errors(self, resp: Response):
        pass

    def _auth(self, req: Request) -> Request:
        return req

    def _send_request(self, req: Request) -> dict:
        req = self._auth(req)
        req = req.prepare()
        resp = self.session.send(req)
        self._check_errors(resp)
        return resp.json()

    def _get(self, url: str, params: Optional[dict] = None) -> dict:
        return self._send_request(
            Request(
                'GET',
                url=url,
                params=params
            )
        )

    def _post(self, url: str, params: Optional[dict] = None, data: Optional[dict] = None,
              json: Optional[dict] = None) -> dict:
        return self._send_request(
            Request(
                'POST',
                url=url,
                params=params,
                data=data,
                json=json,
            )
        )
