import unittest
import requests
from requests.auth import HTTPBasicAuth
import os
# method = "get"
# url = "http://localhost:9090/noise"
# auth = HTTPBasicAuth("usuario1", "usuario1")
# rsp = requests.request(method, url, headers=None, auth=auth)
# print(rsp.json())


class TestAPI(unittest.TestCase):
    URL_BASE = "http://localhost:9090"
    id_dummy_1 = ""
    id_dummy_2 = ""
    id_dummy_3 = ""
    id_dummy_4 = ""
    id_dummy_5 = ""
    id_dummy_6 = ""

    # def test_post_training_tag_basic_auth(self):

    #     method = "post"
    #     url = self.URL_BASE + "/training_tag"
    #     auth = HTTPBasicAuth("usuario1", "usuario1")
    #     path = (os.path.dirname(__file__))+'/audios/audio_1.mp3'
    #     audio = open(path, 'rb')
    #     files = {'files': audio}
    #     resp = requests.request(
    #         method, url, headers=None, auth=auth, files=files, data={"age_range": ">30", "gender": "Male"})
    #     self.assertEqual(resp.status_code, 200)  # 200 si conecta
    #     # self.assertTrue(len(resp.json()) == 5 or len(resp.json()) == 1)
    #     audio.close()
    #     print(len(resp.json()))
    #     TestAPI.id_dummy = resp.json()['_id']

    # def test_get_noise_bearer(self):
    #     token = ""
    #     method = "get"
    #     url = self.URL_BASE + "/noise"
    #     payload = 'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Auma-ticket&audience=flask_api&response_mode=Permissions'
    #     headers = {
    #         'Authorization': f'Bearer {token}',
    #         'Content-Type': 'application/x-www-form-urlencoded'
    #     }
    #     rsp = requests.request(method, url, headers=headers, data=payload)
    #     print(rsp.json())


if __name__ == '__main__':
    unittest.main()
