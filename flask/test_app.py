import unittest
from flask import Flask, url_for
from app import create_app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app(test_config={"TESTING": True})
        self.client = self.app.test_client()


    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_worker_login_page(self):
        response = self.client.get('/workerlogin')
        self.assertEqual(response.status_code, 200)

    def test_patient_login_page(self):
        response = self.client.get('/patientlogin')
        self.assertEqual(response.status_code, 200)

    def test_worker_login_do_success(self):
        data = {'Username': 'test_user', 'Password': 'test_password'}

        response = self.client.post('/workerlogin/do', data=data, follow_redirects=True)


        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Health Worker Homepage', response.data)




if __name__ == '__main__':
    unittest.main()
