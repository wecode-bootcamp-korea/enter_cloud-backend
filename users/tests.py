import jwt
import json
import bcrypt

from django.test import TestCase, Client

from users.models import User, Host
from my_settings import SECRET, ALGORITHM

client = Client()

class UserSignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            nickname = '딸기검',
            email = 'ddalkigum@gmail.com',
            password = 'wecode123',
            phone_number = '01033334444',
            avatar_image = 'http://asdf.com/sdf'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_user_sign_up_success(self):
        data = {
            'nickname':'딸기검2',
            'email':'ddalkigum@naver.com',
            'password':'wecode123',
        }
        response = client.post('/user/signup', json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_user_sign_up_already_exist(self):
        data = {
            'nickname' : '딸기검',
            'email' : 'ddalkigum@gmail.com',
            'password' : 'wecode123',
            'phone_number' : '01033334444',
            'avatar_image' : 'http://asdf.com/sdf'
        }
        response = client.post('/user/signup', json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message":"USER_ALREADY_EXIST"})

    def test_user_sign_up_key_error(self):
        data = {
            'nicname' : '딸기검',
            'email' : 'ddalkigum@gmail.com',
            'password' : 'wecode123',
            'phone_number' : '01033334444',
            'avatar_image' : 'http://asdf.com/sdf'
        }
        response = client.post('/user/signup', json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"message":"KEY_ERROR"})

class UserSignInTest(TestCase):
    def setUp(self):
        hash_password = bcrypt.hashpw('wecode123'.encode(), salt = bcrypt.gensalt())
        User.objects.create(
            nickname = '딸기검',
            email = 'ddalkigum@gmail.com',
            password = hash_password.decode(),
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_user_sign_in_success(self):
        data = {
            'email':'ddalkigum@gmail.com',
            'password':'wecode123'
        }
    
        response = client.post("/user/signin", json.dumps(data), content_type = 'application/json')
        user     = User.objects.get(id = 1)
        bcrypt.checkpw(data["password"].encode(), user.password.encode())
        encode_jwt = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Authorization":encode_jwt})

    def test_user_sign_in_user_does_not_exist(self):

        data = {
            "email":"ddalki@gmail.com",
            "password":"wecode123"
        }
        
        response = client.post("/user/signin", json.dumps(data), content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
    
  