import json
import re
import jwt
import bcrypt


from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models          import User
from my_settings      import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        vali_nickname     = '^[a-zA-Z0-9가-힣]{3,}$'
        vali_email        = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        vali_password     = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{6,}$'
        validate_nickname = re.compile(vali_nickname)
        validate_email    = re.compile(vali_email)
        validate_password = re.compile(vali_password)
        

        try:
            data       = json.loads(request.body)
            password   = data.get('password')
            password1  = data.get('password1')
            encode_pw  = password.encode("utf-8")
            encrypt_pw = bcrypt.hashpw(encode_pw, bcrypt.gensalt()).decode("utf-8")

            if not validate_nickname.match(data['nickname']):
                return JsonResponse(
                    {"MESSAGE" : "Invalid_nickname"}, status = 400
                )
    
            if not validate_email.match(data['email']):
                return JsonResponse(
                    {"MESSAGE" : "Invalid_email"}, status = 400
                )
            
            if not validate_password.match(data['password']):
                return JsonResponse(
                    {"MESSAGE" : "Invalid_password"}, status = 400
                )
            
            if password != password1:
                return JsonResponse(
                    {"MESSAGE" : "Password_mismatch"}, status = 401
                )

            if User.objects.filter(Q(email = data['email']) | Q(nickname = data['nickname'])).exists():
                return JsonResponse(
                    {"MESSAGE" : "User_already_exists"}, status = 401
                )
            User.objects.create(
                email    = data['email'],
                password = encrypt_pw,
                nickname = data['nickname']
            )
            return JsonResponse(
                {"MESSAGE" : "Signup_SUCCES"}, status = 201
            )

        except KeyError:
            return JsonResponse(
                {"MESSAGE" : "KeyError"}, status = 401
            )
            
        except json.decoder.JSONDecodeError:
            return JsonResponse(
                {"MESSAGE" : "Invalid_data"}, status = 401
            )


class SigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])
                if bcrypt.checkpw(data['password'].encode("utf-8"), user.password.encode("utf-8")):
                    token = jwt.encode({"id" : user.id}, SECRET_KEY, ALGORITHM)
                    return JsonResponse(
                        {"TOKEN" : token}, status = 201
                    )
                return JsonResponse(
                    {"MESSAGE" : "Invalid_password"}, status =401
                )
            return JsonResponse(
                {"MESSAGE" : "Invalid_user"}, status = 401
            )

        except KeyError:
            return JsonResponse(
                {"MESSAGE" : "KeyError"}, status = 401
            )
        except json.decoder.JSONDecodeError:
            return JsonResponse(
                {"MESSAGE" : "Invalid_data"}, status = 401
            )
