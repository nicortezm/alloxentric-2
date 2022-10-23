import unittest
import requests
from requests.auth import HTTPBasicAuth
import os


class TestClass(unittest.TestCase):
    URL_BASE = "http://localhost:9090"
    id_dummy = ""

    def test_get_training_tag_basic_auth(self):

        method = "get"
        url = self.URL_BASE + "/training_tag"
        auth = HTTPBasicAuth("usuario1", "usuario1")
        resp = requests.request(method, url, headers=None, auth=auth)
        self.assertEqual(resp.status_code, 200)  # 200 si conecta
        self.assertTrue(len(resp.json()) > 1)

    def test_post_training_tag_basic_auth(self):

        method = "post"
        url = self.URL_BASE + "/training_tag"
        auth = HTTPBasicAuth("usuario1", "usuario1")
        path = (os.path.dirname(__file__))+'/audios/audio_2.mp3'
        audio = open(path, 'rb')
        files = {'files': audio}
        resp = requests.request(
            method, url, headers=None, auth=auth, files=files, data={"age_range": ">30", "gender": "Male"})
        self.assertEqual(resp.status_code, 200)  # 200 si conecta
        self.assertTrue(len(resp.json()) == 4)
        audio.close()
        TestClass.id_dummy = resp.json()['_id']

    def test_z_delete_training_tag_basic_auth(self):
        method = "delete"
        url = self.URL_BASE + "/training_tag"
        auth = HTTPBasicAuth("usuario1", "usuario1")
        resp = requests.request(
            method, url, headers=None, auth=auth, data={
                'id': self.id_dummy
            })
        self.assertEqual(resp.status_code, 200)  # 200 si conecta
        # print(resp.json())
        # 5 si borra el objeto, #1 si muestra el mensaje de error
        self.assertTrue(len(resp.json()) == 4)
