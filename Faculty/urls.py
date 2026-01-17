from django.urls import path,include
from Faculty import views
app_name="Faculty"

urlpatterns = [
  path('HomePage/',views.HomePage,name="HomePage"),  
  path('MyProfile/',views.MyProfile,name="MyProfile"),  
  path("EditProfile/",views.EditProfile,name="EditProfile"),
  path('topublic/<int:pid>',views.topublic,name="topublic"),
  path('toprivate/<int:prid>',views.toprivate,name="toprivate"),
  path("ChangePassword/",views.ChangePassword,name="ChangePassword"),
  path("Notes/",views.Notes,name="Notes"),
  path("AjaxCourse/",views.AjaxCourse,name="AjaxCourse"),
  path("AjaxSubject/",views.AjaxSubject,name="AjaxSubject"),
  path('delnotes/<int:did>',views.delnotes,name="delnotes"),
  path('Post/',views.Post,name="Post"), 
  path('delpost/<int:did>',views.delpost,name="delpost"),
  path('ViewPost/',views.ViewPost,name="ViewPost"), 
  path('likepost/<int:pid>',views.likepost,name="likepost"), 
  path('Comment/<int:cid>',views.Comment,name="Comment"),
  path('Follow/<int:cid>',views.Follow,name="Follow"),
  path('FollowU/<int:uid>',views.FollowU,name="FollowU"),
  path('FollowF/<int:fid>',views.FollowF,name="FollowF"),
  path('UserList/',views.UserList,name="UserList"), 
  path('ViewCollege/',views.ViewCollege,name="ViewCollege"),
  path('ViewFaculty/',views.ViewFaculty,name="ViewFaculty"),
  path('Followers/',views.Followers,name="Followers"),
  path('acceptrequest/<int:aid>',views.acceptrequest,name="acceptrequest"),
  path('rejectrequest/<int:rid>',views.rejectrequest,name="rejectrequest"),
]
