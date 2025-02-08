from connector.pair_getters.base import PairGetter
import requests


class OkxPairGetter(PairGetter):
    def __init__(self):
        link = "https://www.okx.com/api/v5/public/instruments?instType=SPOT"
        super().__init__(link)

    def get_all_pairs(self) -> list[str]:
       with requests.get(self.link) as response:
            response = response.json()
            return [i["instId"] for i in response['data']]