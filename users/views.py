import json
import re
import jwt
import bcrypt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models          import User
from spaces.views     import SpaceCardView
from my_settings      import DATABASE, SECRET_KEY, ALGORITHM, validate_nickname, validate_email, validate_password
from decorators.utils import login_required

class SignupView(View):
    def post(self, request):
        
        try:
            data       = json.loads(request.body)
            encrypt_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            if not validate_nickname.match(data['nickname']):
                return JsonResponse(
                    {"message" : "INVALID_NICKNAME"}, status = 400
                )
    
            if not validate_email.match(data['email']):
                return JsonResponse(
                    {"message" : "INVALID_EMAIL"}, status = 400
                )
            
            if not validate_password.match(data['password']):
                return JsonResponse(
                    {"message" : "INVALID_PASSWORD"}, status = 400
                )

            if User.objects.filter(Q(email = data['email']) | Q(nickname = data['nickname'])).exists():
                return JsonResponse(
                    {"message" : "USER_ALREADY_EXISTS"}, status = 401
                )
            User.objects.create(
                email    = data['email'],
                password = encrypt_pw,
                nickname = data['nickname']
            )
            return JsonResponse(
                {"message" : "SIGNUP_SUCCES"}, status = 201
            )

        except KeyError:
            return JsonResponse(
                {"message" : "KEYERROR"}, status = 401
            )

        except json.decoder.JSONDecodeError:
            return JsonResponse(
                {"message" : "INVALID_DATA"}, status = 401
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
                    {"message" : "INVALID_PASSWORD"}, status =401
                )
            return JsonResponse(
                {"message" : "INVALID_USER"}, status = 401
            )

        except KeyError:
            return JsonResponse(
                {"message" : "KEYERROR"}, status = 401
            )
        except json.decoder.JSONDecodeError:
            return JsonResponse(
                {"message" : "INVALID_DATA"}, status = 401
            )

class UserLikeView(SpaceCardView):
    @login_required
    def get(self, request):
        super().get(request)
        user            = request.user
        like_card_id    = [like.space.id for like in user.like_set.all()]
        like_space_card = []

        for card in self.space_card:
            space_id = card.get("id")
            if space_id in like_card_id:
                like_space_card.append(card)
        return JsonResponse({"like_card":like_space_card}, status = 200)