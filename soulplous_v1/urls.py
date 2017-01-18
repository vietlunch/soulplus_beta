from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
import apps.core.api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('apps.core.urls', namespace='core')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/signup/', apps.core.api.AccountSignup.as_view()),
    url(r'^api/v1/signin/', apps.core.api.AccountSignin.as_view()),
    url(r'^api/v1/facebooksignin/', csrf_exempt(apps.core.api.FacebookSignin.as_view())),
    url(r'^api/v1/lostpassword/', apps.core.api.LostPassword.as_view()),
    url(r'^api/v1/newpassword/', apps.core.api.NewPassword.as_view()),
    url(r'^api/v1/uploadavatar/', apps.core.api.UploadAvatar.as_view()),
    url(r'^api/v1/updateprofile/', apps.core.api.UpdateProfile.as_view()),
    url(r'^api/v1/userprofile/', apps.core.api.GetUserProfile.as_view()),
    url(r'^api/v1/homeactionlist/', apps.core.api.ListAction.as_view()),
    url(r'^api/v1/notifications/', apps.core.api.GetNotifications.as_view()),
    url(r'^api/v1/getmyaction/', apps.core.api.GetMyAction.as_view()),
    url(r'^api/v1/likeaction/', apps.core.api.LikeAction.as_view()),
    url(r'^api/v1/reportaction/', apps.core.api.ReportAction.as_view()),
    url(r'^api/v1/calendaraction/', apps.core.api.SetCalendarAction.as_view()),
    url(r'^api/v1/getcalendaraction/', apps.core.api.GetCalendarAction.as_view()),
    url(r'^api/v1/noteaction/', apps.core.api.NoteAction.as_view()),
    url(r'^api/v1/ratingaction/', apps.core.api.RatingAction.as_view()),
    url(r'^api/v1/getaction/', apps.core.api.GetAction.as_view()),
    url(r'^api/v1/creategroup/', apps.core.api.CreateGroup.as_view()),
    url(r'^api/v1/createaction/', apps.core.api.CreateAction.as_view()),
    url(r'^api/v1/getmylikedactions/', apps.core.api.MyLikedActions.as_view()),
    url(r'^api/v1/getlikesaction/', apps.core.api.GetLikesAction.as_view()),
    url(r'^api/v1/comment/', apps.core.api.CommentGroup.as_view()),
    url(r'^api/v1/sendinvitation/', apps.core.api.SendInvitation.as_view()),
    url(r'^api/v1/acceptinvitation/', apps.core.api.AcceptInvitation.as_view()),
    url(r'^api/v1/createfriend/', apps.core.api.CreateFriend.as_view()),
    url(r'^api/v1/getfriends/', apps.core.api.GetFriends.as_view()),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

