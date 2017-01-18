from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import (TokenAuthentication,SessionAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.contrib.gis import geos
from django.contrib.gis import measure

import json
import random
from core.models import  *
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse 

from django.core.validators import validate_email
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
 
from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from allauth.socialaccount.helpers import complete_social_login
import threading
from django.core.files import File
import datetime
from rest_framework.authentication import SessionAuthentication


class AccountSignup(APIView):
    #authentication_classes = (SessionAuthentication, TokenAuthentication)
    #permission_classes = (IsAuthenticated,)
    #renderer_classes = (JSONRenderer,)
    def post(self, request, format=None):
        """ sign up new account. """
        if request.META.get('CONTENT_TYPE') is None:
            return Response({'error':"invalid_header"},status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.META.get('CONTENT_TYPE') == "application/json":
                if request.data['signup_type']:
                    if request.data['signup_type'] == "phone":
                        if UserProfile.objects.filter(phonenumber = request.data['phonenumber']).exists():
                            return Response({'status':'phone_existed'},status=802)
                        else:
                            newuser = User.objects.create_user(username=request.data['phonenumber'],password=request.data['password'])
                            UserProfile.objects.create(user=newuser,phonenumber=request.data['phonenumber'])
                            return Response({'status':"success",'userid':newuser.pk}, status=status.HTTP_200_OK)
                    if request.data['signup_type'] == "email":
                        if User.objects.filter(email = request.data['email']).exists():
                            return Response({'status':'email_existed'},status=801)
                        else:
                            newuser = User.objects.create_user(username=request.data['email'],email=request.data['email'],password=request.data['password'])
                            UserProfile.objects.create(user=newuser)
                            return Response({'status':"success",'userid':newuser.pk}, status=status.HTTP_200_OK)
                else: 
                    return Response({'error': "missing_or_invalid_params"}, status=402)
            else:
                return Response({'error':"unsupport_type"},status=403)
        
class AccountSignin(APIView):
    def post(self, request, format=None):
        """ sign up new account. """
        if not (("email" in request.data and "password" in request.data and "signin_type" in  request.data) or ("phonenumber" in request.data and "password" in request.data and "signin_type" in request.data)):
            return Response({'error': "missing_params"}, status=status.HTTP_400_BAD_REQUEST)

        if request.data['signin_type'] == "email":
            emailinput = str(request.data['email'])
            passwordinput = str(request.data['password'])
            print emailinput, passwordinput
            valid_email = True
            try:
                validate_email(emailinput)
                valid_email = True
            except :
                valid_email = False
            if ((len(passwordinput) < 3) or not valid_email):
                return Response({"error":"Invalid_password_or_email"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                if User.objects.get(email=emailinput).check_password(passwordinput):
                    return Response({'status':"success" ,'userid':User.objects.get(email=emailinput).pk}, status=status.HTTP_200_OK)

                else:
            
                    return Response({'status':"password_incorrect"}, status=202)
            except User.DoesNotExist:
                return Response({"error":"user_does_not_exist"},status=403)
        if request.data['signin_type'] == "phone":
            phonenumber = str(request.data['phonenumber'])
            password = str(request.data['password'])
            if len(password) < 3 or len(phonenumber) < 8 or len (phonenumber)>13:
                return Response({"error":"invalid_params"},status=401)
            try:
                if User.objects.get(username=phonenumber).check_password(password):
                    return Response({'status':"success" ,'userid':User.objects.get(username=phonenumber).pk}, status=status.HTTP_200_OK)

                else:
                    return Response({'status':"password_incorrect"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error":"user_does_not_exist"},status=400)

class EverybodyCanAuthentication(SessionAuthentication):
    def authenticate(self, request):
        return None

class FacebookSignin(APIView):
    permission_classes = (AllowAny,)
    
    # this is a public api!!!
    authentication_classes = (EverybodyCanAuthentication,)
             
    def dispatch(self, *args, **kwargs):
        return super(FacebookSignin, self).dispatch(*args, **kwargs)
    
    def post(self, request):        
        #data = JSONParser().parse(request)
        access_token = request.data['access_token']  
        print "access token:", access_token
        try:
            app = SocialApp.objects.get(provider="facebook")
            token = SocialToken(app=app, token=access_token)
                            
            # check token against facebook                  
            login = fb_complete_login(request,app, token)
            login.token = token
            login.state = SocialLogin.state_from_request(request)
        
            # add or update the user into users table
            ret = complete_social_login(request, login)
            preferred_avatar_size_pixels=256
            picture_url = "http://graph.facebook.com/{0}/picture?width={1}&height={1}".format(sociallogin.account.uid, preferred_avatar_size_pixels)
 
            # if we get here we've succeeded
            return Response(status=200, data={
                'status': "success",
                'user_id': request.user.pk,
            })
            
        except Exception as e:
            print e
            return Response(status=401 ,data={
                'status': "fail",
                'error': "Bad_Access_Token",
            })

class LostPassword(APIView):
    def post(self, request, format=None):
        return
    
class NewPassword(APIView):
    def post(self, request, format=None):
        return
    
class UploadAvatar(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data["userid"]
            print "userid: ", userid
            given_file = request.FILES.get('file')
            #extension = given_file.name.split(".").lower()[-1]
            #print(settings.MEDIA_ROOT)
            print(given_file.name)
            user = UserProfile.objects.get(pk=userid)
            user.avatar.save(name = str(userid) + ".png", content = File(given_file))
            return Response(status=200,data={'status': "success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})
    
class UpdateProfile(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data["userid"]
            fullname = request.data["fullname"]
            gender = request.data["gender"]
            address = request.data["address"]
            birthday = request.data["birthday"]
            password = request.data["password"]
            print fullname
            if password != "":
                user = UserProfile.objects.get(pk=userid)
                user.fullname = fullname
                user.gender = gender
                user.address = address
                user.birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d")
                user.save()
                return Response(status=200,data={'status': "success"})
            else:
                user = UserProfile.objects.get(pk=userid)
                user.fullname = fullname
                user.gender = gender
                user.address = address
                user.birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d")
                password = password
                user.save()
                return Response(status=200,data={'status': "success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})
class GetUserProfile(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data["userid"]
            user = UserProfile.objects.get(pk=userid)
            return Response(status=200,data={'status':"success",'userid':userid,'fullname':user.fullname,'gender':user.gender,'address':user.address,'birthday':str(user.birthday)})
        except Exception as e: 
            print e
            return Response(status=400,data={'error': "fail"})

class GetAction(APIView):
    def post(self, request, format=None):
        try:
            actionid = request.data["actionid"]
            action = Action.objects.get(pk=actionid)
            return Response(status=200,data={'status':"success",'actionid':actionid,'title':action.title,'imageurl':action.firstPicture.url,'content':action.content})
        except Exception as e: 
            print e
            return Response(status=400,data={'error': "fail"})
    
class SetCalendarAction(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data["userid"]
            actionid = request.data["actionid"]
            starttime = request.data["datetime"]
            print userid, actionid
            CalendarAction.objects.create(userid=userid,actionid=actionid,startDate = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M"))
            #t = threading.Thread(target=updatenotification(userid=userid,actionid=actionid))
            #t.start()
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})
class GetCalendarAction(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data["userid"]
            print "userid: ",userid
            results = CalendarAction.objects.filter(userid=userid)
            results_json = []
            #t = threading.Thread(target=updatenotification(userid=userid,actionid=actionid))
            #t.start()
            for result in results:
                result_json={"actionid":result.actionid,"datetime":str(result.startDate),"title":Action.Objects.get(pk=result.actionid).title}
                results_json.append(result_json)
            return Response(status=200,data={'status': "success","calendaraction":results_json})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})

    
class ReportAction(APIView):
    def post(self, request, format=None):
        try:
            actionid = request.data["actionid"]
            userid = request.data["userid"]
            reporttype = request.data["reporttype"]
            Report.objects.create(actionid=actionid,userid=userid,report_type=reporttype)
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})
    
class CreateGroup(APIView):
    def post(self, request, format=None):
        try:
            actionid = request.data["actionid"]
            userid = request.data["userid"]
            members = request.data["friends"]
            print len(members)
            group = PrivateGroup.objects.create(actionid=actionid,userid=userid)
            group.members.add(UserProfile.objects.get(pk=userid))
            if len(members) > 0:
                for member in members:
                    group.members.add(UserProfile.objects.get(pk=member))         
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})
    
class RatingAction(APIView):
    def post(self, request, format=None):
        try:
            actionid = request.data["actionid"]
            userid = request.data["userid"]
            rating = request.data["rating"]
            Rating.objects.create(actionid=actionid,userid=userid,rating=rating)
            return Response(status=200,data={'status':"success"})
        except:
            return Response(status=400,data={'error': "fail"})
    
class NoteAction(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data["userid"]
            actionid = request.data["actionid"]
            content = request.data["content"]
            print userid, actionid
            Note.objects.create(userid=userid,actionid=actionid,content=content)
            #t = threading.Thread(target=updatenotification(userid=userid,actionid=actionid))
            #t.start()
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})
    
class GroupDetails(APIView):
    def post(self, request, format=None):
        return
    
class MyLikedActions(APIView):
    def post(self, request, format=None):
        return
    
class GetMyAction(APIView):
    def post(self, request, format=None):
        return

def updatenotification(userid,mapactionid):
    try:
        friends = UserProfile.objects.get(pk=userid).friends
        print "number of friend", friends.count()
        for friend in friends:
            print "creating notification"
            Notification.objects.create(userid=friend.friendid,notificationtype=Notification.FRIEND_CREATE_MAP_ACTION,friend_create_map_id=userid,actionmapid=mapactionid)
            print "success"
    except Exception as e:
        print e   
           
 
class CreateMapAction(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data['userid']
            title = request.data['title']
            content = request.data['content']
            long = request.data['long']
            lat = request.data['lat']
            point = geos.fromstr("POINT(%s %s)" % (long, lat))
            timefromuser = request.data['time']
            given_file = request.FILES.get('file')
            mapaction = MapAction(userid=userid,title=title,content=content,location=point,timefromuser=datetime.datetime.strptime(timefromuser, "%Y-%m-%d %H:%M"))
            mapaction.save()
            mapaction.firstPicture.save(name = str(mapactionid) + '.jpg', content = File(given_file))
            t = threading.Thread(target=updatenotification(userid=userid,mapactionid=mapaction.pk))
            t.start()
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=401 ,data={'status': "fail"})
        
class GetNearbyAction(APIView):
    def post(self, request, format=None):
        try:
            long = request.data['long']
            lat = request.data['lat']
            current_point = geos.fromstr("POINT(%s %s)" % (long, lat))
            distance_from_point = {'km': 10}
            mapactions = models.MapAction.gis.filter(location__distance_lte=(current_point, measure.D(**distance_from_point)))
            mapactions = mapactions.distance(current_point).order_by('distance')
            response_message = []
            sampleusers = random.sample(range(2,UserProfile.objects.count()),5)
            sampleuser_avatarurl = [UserProfile.objects.get(pk=t).avatar.url for t in sampleusers]
            for mapaction in mapactions:
                try:
                    Like.objects.get(actionid=action.pk,userid=userid)
                    response_json = {'Liked':True,'mapactionid':mapaction.pk,'title':mapaction.title,'content':mapaction.content,'imageurl':mapaction.firstPicture.url,'number_likes':Like.objects.filter(mapactionid=mapaction.pk).count(),'avatarurl':sampleuser_avatarurl,'number_more':random.randint(5,1000)}
                    response_message.append(response_json)
                except:
                    response_json = {'Liked':False,'mapactionid':mapaction.pk,'title':mapaction.title,'content':mapaction.content,'imageurl':mapaction.firstPicture.url,'number_likes':Like.objects.filter(mapactionid=mapaction.pk).count(),'avatarurl':sampleuser_avatarurl,'number_more':random.randint(5,1000)}
                    response_message.append(response_json)
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=401 ,data={'status': "fail"})
    
class SignOut(APIView):
    def post(self, request, format=None):
        return
    
class ListAction(APIView):
    def post(self, request, format=None):
        #actions = Action.objects.order_by('?')[:20]
        response_message = []
        result = []
        try:
            userid = request.data['userid']
            sample = random.sample(xrange(Action.objects.count()),3)
            result = [Action.objects.all()[i] for i in sample] 
            sampleusers = random.sample(range(2,UserProfile.objects.count()),5)
            sampleuser_avatarurl = [UserProfile.objects.get(pk=t).avatar.url for t in sampleusers]
            for j in range(0,3):
                action = result[j]
                #users_related = PrivateGroup.objects.filter(actionid=action.pk)                  
                try:               
                    Like.objects.get(actionid=action.pk,userid=userid)
                    resultjson = {'Liked':True,'title':action.title,'content':action.content, 'actionid':action.pk, 'actionimagerurl':action.firstPicture.url,'number_likes':Like.objects.filter(actionid=action.pk).count(),'avatarurl':sampleuser_avatarurl,'number_more':random.randint(5,1000)}
                    response_message.append(resultjson)
                except:
                    resultjson = {'Liked':False,'title':action.title,'content':action.content, 'actionid':action.pk, 'actionimagerurl':action.firstPicture.url,'number_likes':Like.objects.filter(actionid=action.pk).count(),'avatarurl':sampleuser_avatarurl,'number_more':random.randint(5,1000)}
                    response_message.append(resultjson)
            #return HttpResponse(serializers.serialize("json", actions))
            response_message_json = {'status':"success",'action':response_message}
            return Response(status=200 ,data=response_message_json)
        except Exception as e:
            print e
            return Response(status=401 ,data={'status': "fail"})

class GetNotifications(APIView):
    def post(self, request, format=None):
        userid = request.data['userid']
        try:
            notifications = Notification.objects.filter(userid=userid)
            result = []
            
            for notification in notifications:
                 notification_json = {'notification':notification} 
                 result.append(notification_json)
            return Response(status=200,data={'status':"success",'result':result})
        except:
            return Response(status=400 ,data={'status': "fail"})
    
def updatenotification_friend_request(userid,invitation):
    try:
       # friends = UserProfile.objects.get(pk=userid)
       # print "number of friend", friends.count()
       
        Notification.objects.create(userid=userid,notificationtype=Notification.FRIEND_REQUESTED,invitation=invitation)
        print "success"
    except Exception as e:
        print e   
        
class CreateFriend(APIView):
    def post(self, request, format=None):
        try:
            UserProfile.objects.get(pk=request.data['userid']).friends.add(User.objects.get(pk=request.data['friendid']))
            return Response({'status':"success"},status=200)
        except Exception as e:
            print e
            return Response({'status':"fail"},status=401)
        
class GetFriends(APIView):
    def post(self, request, format=None):
        try:
            UserProfile.objects.get(pk=request.data['userid']).friends.add(User.objects.get(pk=request.data['friendid']))
            return Response({'status':"success"},status=200)
        except Exception as e:
            print e
            return Response({'status':"fail"},status=401)

def updatenotification(userid,actionid):
    try:
        friends = UserProfile.objects.get(pk=userid).friends
        print "number of friend", friends.count()
        for friend in friends:
            print "creating notification"
            Notification.objects.create(userid=friend.friendid,notificationtype=Notification.LIKED,friend_like_id=userid,actionlikedid=actionid)
            print "success"
    except Exception as e:
        print e   
           
class LikeAction(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data["userid"]
            actionid = request.data["actionid"]
            print userid 
            Like.objects.create(userid=int(userid),actionid=int(actionid))
            t = threading.Thread(target=updatenotification(userid=userid,actionid=actionid))
            t.start()
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})

class GetLikesAction(APIView):
    def post(self, request, format=None):
        actionid = request.data["actionid"]
        try:
            result = Like.objects.filter(actionid=actionid)
            print result
            number_of_likes = result.count()
            print number_of_likes
            users_liked = []
            for i in range(0, number_of_likes):
                user_liked_id = result[i].userid
                try:
                    user_avatar = UserProfile.objects.get(pk=user_liked_id).avatar.url
                    user_liked_json={"userid":user_liked_id,"avatar":user_avatar}
                    users_liked.append(user_liked_json)
                except:
                    user_liked_json={"userid":user_liked_id}
                    users_liked.append(user_liked_json)
            
            return Response(status=200,data={'status':"success",'likes_number':number_of_likes,'users_liked':users_liked})
        except Exception as e:
            print e
            return Response(status=200 ,data={'status': "fail"})

class CommentGroup(APIView):
    def post(self, request, format=None):
        try:
            userid = request.data["userid"]
            actionid = request.data["actionid"]
            print userid 
            Like.objects.create(userid=int(userid),actionid=int(actionid))
            t = threading.Thread(target=updatenotification(userid=userid,actionid=actionid))
            t.start()
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})

def updatenotification_invitation(userid,invitation):
    try:
       # friends = UserProfile.objects.get(pk=userid)
       # print "number of friend", friends.count()
       
        Notification.objects.create(userid=userid,notificationtype=Notification.RECEIVED_INVITATION,invitation=invitation)
        print "success"
    except Exception as e:
        print e      
        
class SendInvitation(APIView):
    def post(self, request, format=None):
        try:
            fromuserid = request.data["fromuserid"]
            touserid = request.data["touserid"]
            actionid = request.data["actionid"]
            content = request.data["content"]
            invitation = Invitation.objects.create(fromuser=fromuserid,touser=touserid,actionid=actionid,content=content,isaccept=False)
            t = threading.Thread(target=updatenotification_invitation(touserid,invitation=invitation))
            t.start()
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})
class AcceptInvitation(APIView):
    def post(self, request, format=None):
        try:
            invitationid = request.data["invitationid"]
            invitation = Invitation.objects.get(pk=invitationid)
            invitation.isaccept = True
            invitation.save()
            return Response(status=200,data={'status':"success"})
        except Exception as e:
            print e
            return Response(status=400,data={'error': "fail"})
