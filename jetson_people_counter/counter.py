import datetime as dt
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import http as HTTP

URL="https://counter.solucionesmaster.com.mx/api/v1/count/"
DEVICE="jetson2gb"
NAME="proto"
VERSION="0.2"
DEFAULT_TIMEOUT = 5 # seconds

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)

# enabling http debug
HTTP.client.HTTPConnection.debuglevel = 1


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


class Counter():
    # Mount it for both http and https usage
    adapter = TimeoutHTTPAdapter(timeout=2.5, max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    last = None
    entering_max = 0
    exiting_max = 0
    delayed = []

    def __init__(self) -> None:
        self.last = dt.datetime.now()

    def post_counter(self, entering, exiting):
        # /device/name/entering/exiting/{{$timestamp}}/version
        now = dt.datetime.now()

        # self.entering_max = entering if entering > self.entering_max else self.entering_max
        # self.exiting_max = exiting if exiting > self.exiting_max else self.exiting_max
        self.entering_max += entering
        self.exiting_max += exiting

        if (now > (self.last + dt.timedelta(minutes=1))):
            self.post_now()
            self.entering_max = 0
            self.exiting_max = 0
            self.last = dt.datetime.now()

    def post_now(self):
        now = dt.datetime.now()
        data_url = ("/" +
                        DEVICE +
                        "/" +
                        NAME + 
                        "/" +
                        str(self.entering_max) +
                        "/" +
                        str(self.exiting_max) +
                        "/" +
                        now.isoformat() +
                        "/" +
                        VERSION)
        self.delayed.append(data_url)
        try:
            for delayed_data in self.delayed[:]:
                response = self.http.get(URL + delayed_data)
                if response and response.ok:
                    # remove delayed_data from delayed
                    self.delayed.remove(delayed_data)
                    print(response)
                else:
                    raise

        except:
            print("Error updating... Do I have Internet conection?")

    def post_pending(self):
        now = dt.datetime.now()
        if (now > (self.last + dt.timedelta(minutes=1))):
            # if self.exiting_max != 0 or self.entering_max != 0:
            self.post_now()
            self.entering_max = 0
            self.exiting_max = 0
            self.last = now
