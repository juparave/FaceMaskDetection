import datetime as dt
import requests

URL="https://counter.solucionesmaster.com.mx/api/v1/count/"
DEVICE="jetson2gb"
NAME="proto"
VERSION="0.1"

class Counter():

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
        try:
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
            for delayed_data in self.delayed[:]:
                response = requests.get(URL + data_url)
                if response.ok:
                    # remove delayed_data from delayed
                    self.delayed.remove(delayed_data)
                else:
                    raise

            print(response)
        except:
            print("Error updating... Do I have Internet conection?")
            # save data_url for later
            self.delayed.append(data_url)

    def post_pending(self):
        now = dt.datetime.now()
        if (now > (self.last + dt.timedelta(minutes=1))):
            if self.exiting_max != 0 or self.entering_max != 0:
                self.post_now()
                self.entering_max = 0
                self.exiting_max = 0
                self.last = now
