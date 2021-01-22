import json
import re
import jwt
import bcrypt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models          import User
from my_settings      import SECRET, ALGORITHM, validate_nickname, validate_email, validate_phone_number
from spaces.views     import SpaceCardView
from decorators.utils import login_required

class SignupView(View):
    def post(self, request):
        try:
            PASSWORD_LENGTH  = 8
            data             = json.loads(request.body)
            password         = data["password"]
            encrypt_pw       = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            if not validate_nickname.match(data['nickname']):
                return JsonResponse(
                    {"message" : "INVALID_NICKNAME"}, status = 400
                )
    
            if not validate_email.match(data['email']):
                return JsonResponse(
                    {"message" : "INVALID_EMAIL"}, status = 400
                )
            
            if len(password) < PASSWORD_LENGTH:
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
                    token = jwt.encode({"id" : user.id}, SECRET, ALGORITHM)
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

class UserProfileView(View):
    @login_required
    def get(self, request):
        user    = request.user
        profile = {
            "avatar_image" : user.avatar_image,
            "nickname"     : user.nickname,
            "email"        : user.email,
            "phone_number" : user.phone_number
        }        
        return JsonResponse({"profile" : profile}, status = 200)

    @login_required
    def post(self, request):
        data               = json.loads(request.body)
        user               = request.user
        PASSWORD_LENGTH    = 8
        
        try:
            new_password       = data.get("new_password")
            new_avatar_image   = data.get("new_avatar_image")
            new_nickname       = data.get("new_nickname")
            new_phone_number   = data.get("new_phone_number")

            if not (new_password or new_avatar_image or new_nickname or new_phone_number):
                return JsonResponse({"message" : "KEYERROR"}, status = 400)

            if new_password:
                if len(new_password) < PASSWORD_LENGTH:
                    return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
                if not bcrypt.checkpw(data['password'].encode("utf-8"), user.password.encode("utf-8")):
                    return JsonResponse({"message" : "PASSWORD_MISMATCH"}, status = 401)
                encrypt_new_pw = bcrypt.hashpw(data["new_password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                User.objects.filter(id = user.id).update(password = encrypt_new_pw)
                return JsonResponse({"message" : "PASSWORD_CHANGE_COMPLETE"}, status = 201)
    
            if new_avatar_image:
                User.objects.filter(id = user.id).update(avatar_image = new_avatar_image)
                return JsonResponse({"message" : "AVATAR_CHANGE_COMPLETE"}, status = 201)
                
            if new_phone_number:
                if not validate_phone_number.match(new_phone_number):
                    return JsonResponse({"message" : "INVALID_PHONE_NUMBER"})
                update_data              = user
                update_data.phone_number = new_phone_number
                update_data.save()
                return JsonResponse({"message" : "PHONE_NUMBER_CHANGE_COMPLETE"}, status = 201)
                
            if new_nickname:
                if User.objects.filter(nickname = new_nickname).exists():
                    return JsonResponse({"message" : "ALREADY_IN_USE"})
                User.objects.filter(id = user.id).update(nickname = new_nickname)
                return JsonResponse({"message" : "NICKNAME_CHANGE_COMPLETE"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEYERROR"},  status = 401)