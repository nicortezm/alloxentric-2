
import unittest
import requests
from requests.auth import HTTPBasicAuth
import os


class TestClass(unittest.TestCase):
    URL_BASE = "http://localhost:9090"
    id_dummy = ""

    def test_get_noise_basic_auth(self):
        method = "get"
        url = self.URL_BASE + "/noise"
        auth = HTTPBasicAuth("usuario1", "usuario1")
        resp = requests.request(method, url, headers=None, auth=auth)
        self.assertEqual(resp.status_code, 200)  # 200 si conecta
        """
            si el len es mayor a 1 significa que
            retornó al menos un objeto dentro del json
            """
        self.assertTrue(len(resp.json()) > 1)
        # print(resp.json())

    def test_post_noise_basic_auth(self):
        method = "post"
        url = self.URL_BASE + "/noise"
        auth = HTTPBasicAuth("usuario1", "usuario1")
        path = (os.path.dirname(__file__))+'/audios/audio_1.mp3'
        audio = open(path, 'rb')
        files = {'files': audio}
        resp = requests.request(
            method, url, headers=None, auth=auth, files=files)
        audio.close()
        self.assertEqual(resp.status_code, 200)  # 200 si conecta
        # self.assertEqual(len(resp.json()), 1)
        TestClass.id_dummy = resp.json()['_id']
        print(resp.json())

    def test_z_delete_noise_basic_auth(self):

        method = "delete"
        url = self.URL_BASE + "/noise"
        auth = HTTPBasicAuth("usuario1", "usuario1")
        resp = requests.request(
            method, url, headers=None, auth=auth, data={
                'id': self.id_dummy
            })
        self.assertEqual(resp.status_code, 200)  # 200 si conecta
        # print(resp.json())
        # 5 si borra el objeto, #1 si muestra el mensaje de error
        self.assertTrue(len(resp.json()) == 5 or len(resp.json()) == 1)
        print(resp.json())
