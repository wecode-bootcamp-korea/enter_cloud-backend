import json
import re
import jwt
import bcrypt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from django.db        import IntegrityError

from .models          import User
from my_settings      import SECRET, ALGORITHM, email_regex, PASSWORD_LENGTH
from spaces.views     import SpaceCardView
from decorators.utils import login_required, check_blank

class SignUpView(View):
    @check_blank
    def post(self, request):
        try:
            data            = json.loads(request.body)
            nickname        = data["nickname"]
            email           = data["email"]
            password        = data["password"]
            clean_email     = email_regex.match(email).string

            if  User.objects.filter(email = clean_email).exists():
                return JsonResponse({"message":"USER_ALREADY_EXIST"}, status = 401)            
            if len(password) < PASSWORD_LENGTH:
                return JsonResponse({"message":"PASSWORD_AT_LEAST_8"}, status = 401)
       
            hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            User.objects.create(nickname = nickname, email = clean_email, password = hash_password.decode())
            return JsonResponse({"message":"SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        except AttributeError:
            return JsonResponse({"message":"NOT_EMAIL_FORM"}, status = 400)

class SignInView(View):
    @check_blank
    def post(self, request):
        try:
            data        = json.loads(request.body)
            email       = data["email"]
            password    = data["password"]
            user        = User.objects.get(email = email)

            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                encoded_jwt = jwt.encode({"id":user.id}, key = SECRET, algorithm = ALGORITHM)
                return JsonResponse({"Authorization":encoded_jwt}, status = 200)
            return JsonResponse({"message":"WRONG_PASSWORD"}, status = 401)
        except User.DoesNotExist:
            return JsonResponse({"message":"USER_DOES_NOT_EXIST"}, status = 401)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 401)
        except ValueError:
            return JsonResponse({"message":"INVALID_SALT"}, status = 403)

class UserProfileView(View):
    @login_required
    def get(self, request):
        user        = request.user
        user_data   = {
            "nickname":user.nickname,
            "avatar_url":user.avatar_image,
            "email":user.email,
            "phone_numger":user.phone_number,
        }
        return JsonResponse({"user_date":user_data}, status = 200)

    @login_required
    def patch(self, request):
        try:
            data             = json.loads(request.body)
            user             = request.user
            hash_password    = lambda x : bcrypt.hashpw(x.encode("utf-8"), bcrypt.gensalt()).decode()
            user.email       = data["email"] if "email" in data.__iter__()  else user.email
            user.password    = hash_password(data["password"]) if "password" in data.__iter__() else user.password
            user.nickname    = data["nickname"] if "nickname" in data.__iter__() else user.nickname
            user.save()
            return JsonResponse({"message":"SUCCESS"}, status = 200)
        except IntegrityError:
            return JsonResponse({"message":"ALREADY_EXIST"}, status = 200)
    
    @login_required
    def delete(self, request):
        user = request.user
        user.delete()
        return JsonResponse({"message":"SUCCESS"}, status = 200)



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