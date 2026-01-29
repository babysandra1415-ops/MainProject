from django.shortcuts import render,redirect
from College.models import *
from Admin.models import *
from Guest.models import *
from Faculty.models import *
from Student.models import *
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime

# Create your views here.
def HomePage(request):
    Faculty = tbl_faculty.objects.get(id=request.session['fid'])
    return render(request,'Faculty/HomePage.html',{'Faculty':Faculty})

def MyProfile(request):
    facultydata=tbl_faculty.objects.get(id=request.session["fid"])
    return render(request,'Faculty/MyProfile.html',{"facultydata": facultydata})

def EditProfile(request):
    facultydata=tbl_faculty.objects.get(id=request.session["fid"])
    if request.method == "POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        username=request.POST.get('txt_username')
        bio=request.POST.get('txt_biodata')
        
        facultydata.faculty_name=name
        facultydata.faculty_email=email
        facultydata.faculty_contact=contact
        facultydata.faculty_username=username
        facultydata.faculty_bio=bio
        facultydata.save()

        return render(request,'Faculty/EditProfile.html',{'msg':'updated'})
    else:
        return render(request,'Faculty/EditProfile.html',{"facultydata":facultydata})
def topublic(request,pid):
    Faculty=tbl_faculty.objects.get(id=pid)
    Faculty.faculty_accounttype=0
    Faculty.save()
    return render(request,'Faculty/MyProfile.html',{'msg':"Changed to Public","facultydata":Faculty})
def toprivate(request,prid):
    Faculty=tbl_faculty.objects.get(id=prid)
    Faculty.faculty_accounttype=1
    Faculty.save()
    return render(request,'Faculty/MyProfile.html',{'msg1':"Changed to Private","facultydata":Faculty})
def ChangePassword(request):
    facultydata=tbl_faculty.objects.get(id=request.session["fid"])
    facultypassword=facultydata.faculty_password

    if request.method == "POST":
        oldpassword=request.POST.get('txt_opassword')
        newpassword=request.POST.get('txt_npassword')
        retype=request.POST.get('txt_cpassword')
        if facultypassword==oldpassword:
            if newpassword==retype:
                facultydata.faculty_password=newpassword
                facultydata.save()
                return render(request,'Faculty/ChangePassword.html',{"msg":"Password Updated"})
            else:
                return render(request,'Faculty/ChangePassword.html',{"msg1":"Password Mismatch"})
        else:
            return render(request,'Faculty/ChangePassword.html',{"msg2":"Password Incorrect"})
    else:
        return render(request,'Faculty/ChangePassword.html')

def Notes(request):
    facultyid = tbl_faculty.objects.get(id=request.session['fid'])
    departmentid=facultyid.department.department.id
    course=tbl_collegecourse.objects.filter(college=request.session["cid"],course__department=departmentid)
    semester=tbl_semester.objects.all()
    subject=tbl_subject.objects.all()
    notes=tbl_notes.objects.filter(faculty=request.session['fid'])
    if request.method == "POST":
        Facultyid = tbl_faculty.objects.get(id=request.session['fid'])
        description=request.POST.get("txt_description")
        notes=request.FILES.get("file_notes")

        subject=tbl_subject.objects.get(id=request.POST.get("sel_subject"))
        tbl_notes.objects.create(notes_description=description,notes_file=notes,subject=subject,faculty=Facultyid)
        return render(request,'Faculty/Notes.html',{'msg':'data inserted'})
    else:
        return render(request,'Faculty/Notes.html',{'course':course,'semester':semester,'subject':subject,'notes':notes})
def delnotes(request,did):
    tbl_notes.objects.get(id=did).delete()
    return redirect("Faculty:Notes")
def AjaxCourse(request):
    departmentid = request.GET.get("did")
    facultyid = tbl_faculty.objects.get(id=request.session['fid'])
    course = tbl_collegecourse.objects.filter(college_id=college,course__department_id=departmentid)
    return render(request,"Faculty/AjaxCourse.html",{'course':course})
def AjaxSubject(request):
    courseid = request.GET.get("did")
    subject = tbl_subject.objects.filter(course=courseid)
    return render(request,"Faculty/AjaxSubject.html",{'subject':subject})
def Post(request):
    facultyid = tbl_faculty.objects.get(id=request.session['fid']) 
    post=tbl_post.objects.filter(faculty=facultyid)

    if request.method == "POST":
        photo=request.FILES.get("file_photo")
        description=request.POST.get("txt_description")
        posttype=request.POST.get("txt_post")
        tbl_post.objects.create(post_photo=photo,post_description=description,post_type=posttype,faculty=facultyid)
        
        return render(request,'Faculty/Post.html',{'msg':'data inserted','post':post})
    else:
        return render(request,'Faculty/Post.html',{'post':post})
def delpost(request,did):
    tbl_post.objects.get(id=did).delete()
    return redirect("Faculty:Post")
def ViewPost(request):
    post=tbl_post.objects.all()
    return render(request,'Faculty/ViewPost.html',{'post':post})
# def likepost(request,pid):
#     faculty=tbl_faculty.objects.get(id=request.session["fid"])
#     postid=tbl_post.objects.get(id=pid)
#     tbl_like.objects.create(post=postid,faculty=faculty)
#     return redirect("Faculty:ViewPost")
def likepost(request):
    if request.method == "POST":
        faculty = tbl_faculty.objects.get(id=request.session["fid"])
        post_id = request.POST.get('post_id')
        post = tbl_post.objects.get(id=post_id)

        like_qs = tbl_like.objects.filter(post=post, faculty=faculty)
        if like_qs.exists():
            like_qs.delete() 
            liked = False
        else:
            tbl_like.objects.create(post=post, faculty=faculty)  
            liked = True

        return JsonResponse({'liked': liked})

    return JsonResponse({'error': 'Invalid request'})



def Comment(request, cid):
    post = tbl_post.objects.get(id=cid)
    faculty = tbl_faculty.objects.get(id=request.session["fid"])

    if request.method == "POST":

        form_type = request.POST.get("type")

        # ADD COMMENT
        if form_type == "comment":
            comment_text = request.POST.get("comment")

            if comment_text:  
                tbl_comment.objects.create(
                    post=post,
                    faculty=faculty,
                    comment_content=comment_text
                )
        elif form_type == "reply":
            reply_text = request.POST.get("reply")
            comment_id = request.POST.get("comment_id")

            if reply_text and comment_id:
                comment = tbl_comment.objects.get(id=comment_id)
                tbl_commentreply.objects.create(
                    comment=comment,
                    faculty=faculty,
                    commentreply_content=reply_text
                )

        return redirect("Faculty:Comment", cid=cid)

    comments = tbl_comment.objects.filter(post=post).order_by("-id")

    return render(request, "Faculty/Comment.html", {
        "comment": comments,
        "post": post
    })
def Follow(request, cid):
    faculty = tbl_faculty.objects.get(id=request.session["fid"])
    college = tbl_college.objects.get(id=cid)

    if not tbl_follow.objects.filter(fromfaculty=faculty,tocollege=college).exists():
        tbl_follow.objects.create(
            fromfaculty=faculty,
            tocollege=college,
            follow_status=1
        )
    return redirect("Faculty:ViewCollege")

def FollowU(request, uid):
    faculty = tbl_faculty.objects.get(id=request.session["fid"])
    target = tbl_student.objects.get(id=uid)

    status = 0 if target.student_accounttype == 1 else 1

    if not tbl_follow.objects.filter(fromfaculty=faculty, tostudent=target).exists():
        tbl_follow.objects.create(
            fromfaculty=faculty,
            tostudent=target,
            follow_status=status
        )
    return redirect("Faculty:UserList")
def FollowF(request, fid):
    faculty = tbl_faculty.objects.get(id=request.session["fid"])
    target = tbl_faculty.objects.get(id=fid)

    status = 0 if target.faculty_accounttype == 1 else 1

    if not tbl_follow.objects.filter(fromfaculty=faculty, tofaculty=target).exists():
        tbl_follow.objects.create(
            fromfaculty=faculty,
            tofaculty=target,
            follow_status=status
        )
    return redirect("Faculty:ViewFaculty")
def ViewFaculty(request):
    faculty = tbl_faculty.objects.get(id=request.session['fid'])
    facultys = tbl_faculty.objects.exclude(id=faculty.id)

    followed_ids = tbl_follow.objects.filter(
        fromfaculty=faculty,
        tofaculty__isnull=False
    ).values_list('tofaculty_id', flat=True)

    pending_ids = tbl_follow.objects.filter(
        fromfaculty=faculty,
        tofaculty__isnull=False,
        follow_status=0
    ).values_list('tofaculty_id', flat=True)

    return render(request,'Faculty/ViewFaculty.html',{
        'facultys': facultys,
        'followed_ids': followed_ids,
        'pending_ids': pending_ids
    })


def ViewCollege(request):
    faculty = tbl_faculty.objects.get(id=request.session['fid'])
    college = tbl_college.objects.filter(college_status=1)

    followed_ids = tbl_follow.objects.filter(
        fromfaculty=faculty,
        tocollege__isnull=False
    ).values_list('tocollege_id', flat=True)

    return render(request,'Faculty/ViewCollege.html',{
        'college': college,
        'followed_ids': followed_ids
    })

def UserList(request):
    faculty = tbl_faculty.objects.get(id=request.session['fid'])
    users = tbl_student.objects.all()

    followed_ids = tbl_follow.objects.filter(
        fromfaculty=faculty,
        tostudent__isnull=False
    ).values_list('tostudent_id', flat=True)

    pending_ids = tbl_follow.objects.filter(
        fromfaculty=faculty,
        tostudent__isnull=False,
        follow_status=0
    ).values_list('tostudent_id', flat=True)

    return render(request,'Faculty/UserList.html',{
        'users': users,
        'followed_ids': followed_ids,
        'pending_ids': pending_ids
    })
def Followers(request):
    faculty = tbl_faculty.objects.get(id=request.session["fid"])

    following = tbl_follow.objects.filter(
        fromfaculty=faculty
    )

    followers = tbl_follow.objects.filter(
        tofaculty=faculty,
        follow_status=1
    )
    requests = tbl_follow.objects.filter(
        tofaculty=faculty,
        follow_status=0
    )

    return render(
        request,
        "Faculty/Followers.html",
        {
            "following": following,
            "followers": followers,
            "requests": requests
        }
    )
def acceptrequest(request,aid):
    Follow=tbl_follow.objects.get(id=aid)
    Follow.follow_status=1
    Follow.save()
    return redirect("Faculty:Followers")

def rejectrequest(request,rid):
    tbl_follow.objects.get(id=rid).delete()
    return redirect("Faculty:Followers")
def Complaint(request):
    faculty=tbl_faculty.objects.get(id=request.session["fid"])
    complaint=tbl_complaint.objects.filter(faculty_id=faculty)
    if request.method == "POST":
        
        title=request.POST.get("txt_title")
        content=request.POST.get("txt_content")
        tbl_complaint.objects.create(complaint_title=title,complaint_content=content,faculty=faculty)
        
        return render(request,'Faculty/Complaint.html',{'complaint':complaint})
    else:
        return render(request,'Faculty/Complaint.html',{'complaint':complaint})
def deletecomplaint(request,did):
    tbl_complaint.objects.get(id=did).delete()
    return redirect("Faculty:Complaint")

def chatpage(request,id):
    faculty  = tbl_faculty.objects.get(id=id)
    return render(request,"Faculty/Chat.html",{"faculty":faculty})

def ajaxchat(request):
    from_faculty = tbl_faculty.objects.get(id=request.session["fid"])
    to_faculty = tbl_faculty.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),faculty_from=from_faculty,faculty_to=to_faculty,chat_file=request.FILES.get("file"))
    return render(request,"Faculty/Chat.html")

def ajaxchatview(request):
    tid = request.GET.get("tid")
    user = tbl_faculty.objects.get(id=request.session["fid"])
    chat_data = tbl_chat.objects.filter((Q(faculty_from=user) | Q(faculty_to=user)) & (Q(faculty_from=tid) | Q(faculty_to=tid))).order_by('chat_time')
    return render(request,"Faculty/ChatView.html",{"data":chat_data,"tid":int(tid)})

def clearchat(request):
    tbl_chat.objects.filter(Q(faculty_from=request.session["fid"]) & Q(faculty_to=request.GET.get("tid")) | (Q(faculty_from=request.GET.get("tid")) & Q(faculty_to=request.session["sid"]))).delete()
    return render(request,"Faculty/ClearChat.html",{"msg":"Chat Deleted Sucessfully...."})

def schatpage(request,id):
    student  = tbl_student.objects.get(id=id)
    return render(request,"Faculty/SChat.html",{"student":student})

def sajaxchat(request):
    from_faculty = tbl_faculty.objects.get(id=request.session["fid"])
    to_student = tbl_student.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),faculty_from=from_faculty,student_to=to_student,chat_file=request.FILES.get("file"))
    return render(request,"Faculty/SChat.html")

def sajaxchatview(request):
    tid = request.GET.get("tid")
    user = tbl_faculty.objects.get(id=request.session["fid"])
    chat_data = tbl_chat.objects.filter((Q(faculty_from=user) | Q(faculty_to=user)) & (Q(student_from=tid) | Q(student_to=tid))).order_by('chat_time')
    return render(request,"Faculty/SChatView.html",{"data":chat_data,"tid":int(tid)})

def sclearchat(request):
    tbl_chat.objects.filter(Q(faculty_from=request.session["fid"]) & Q(student_to=request.GET.get("tid")) | (Q(student_from=request.GET.get("tid")) & Q(faculty_to=request.session["fid"]))).delete()
    return render(request,"Faculty/ClearChat.html",{"msg":"Chat Deleted Sucessfully...."})

def cchatpage(request,id):
    college  = tbl_college.objects.get(id=id)
    return render(request,"Faculty/CChat.html",{"college":college})

def cajaxchat(request):
    from_faculty = tbl_faculty.objects.get(id=request.session["fid"])
    to_college = tbl_college.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),faculty_from=from_faculty,college_to=to_college,chat_file=request.FILES.get("file"))
    return render(request,"Faculty/CChat.html")

def cajaxchatview(request):
    tid = request.GET.get("tid")
    user = tbl_faculty.objects.get(id=request.session["fid"])
    chat_data = tbl_chat.objects.filter((Q(faculty_from=user) | Q(faculty_to=user)) & (Q(college_from=tid) | Q(college_to=tid))).order_by('chat_time')
    return render(request,"Faculty/CChatView.html",{"data":chat_data,"tid":int(tid)})

def cclearchat(request):
    tbl_chat.objects.filter(Q(faculty_from=request.session["fid"]) & Q(college_to=request.GET.get("tid")) | (Q(college_from=request.GET.get("tid")) & Q(faculty_to=request.session["fid"]))).delete()
    return render(request,"Faculty/ClearChat.html",{"msg":"Chat Deleted Sucessfully...."})


def ViewCollegeProfile(request,pid):
    
    college=tbl_college.objects.get(id=pid)
    
    post=tbl_post.objects.filter(college=college)
    return render(request,'Faculty/ViewCollegeProfile.html',{"college": college,"post":post})
def ViewFacultyProfile(request,fid):
    
    faculty=tbl_faculty.objects.get(id=fid)
    
    post=tbl_post.objects.filter(faculty=faculty)
    return render(request,'Faculty/ViewFacultyProfile.html',{"faculty": faculty,"post":post})
def ViewStudentProfile(request,sid):
    
    student=tbl_student.objects.get(id=sid)
    
    post=tbl_post.objects.filter(student=student)
    return render(request,'Faculty/ViewStudentProfile.html',{"student": student,"post":post})

def Search(request):
    # student=tbl_student.objects.all().exclude(id=request.session['sid'])
    # faculty= tbl_faculty.objects.all()
    # college = tbl_college.objects.all()
    if request.method == "POST":
        student=tbl_student.objects.all()
        faculty= tbl_faculty.objects.all().exclude(id=request.session['fid'])
        college = tbl_college.objects.all()
        search = request.POST.get("txt_search")
        usertype = request.POST.get("sel_user")
       
        # If search text exists
        if search:
            student = student.filter(
                Q(student_name__icontains=search) |
                Q(student_username__icontains=search)
            )

            faculty = faculty.filter(
                Q(faculty_name__icontains=search) |
                Q(faculty_username__icontains=search)
            )

            college = college.filter(
                Q(college_name__icontains=search) |
                Q(college_email__icontains=search)
            )

        # If filter selected
        if usertype == "Student":
            faculty = tbl_faculty.objects.none()
            college = tbl_college.objects.none()

        elif usertype == "Faculty":
            student = tbl_student.objects.none()
            college = tbl_college.objects.none()

        elif usertype == "College":
            student = tbl_student.objects.none()
            faculty = tbl_faculty.objects.none()
        return render(request,"Faculty/Search.html",{'student':student,'college':college,'faculty':faculty})
    else:
        return render(request,"Faculty/Search.html")

def Notification(request):
    faculty = tbl_faculty.objects.get(id=request.session["fid"])

    likes = tbl_like.objects.filter(
        post__faculty=faculty
    ).exclude(faculty=faculty)
    comments = tbl_comment.objects.filter(
        post__faculty=faculty
    ).exclude(faculty=faculty)

    replies = tbl_commentreply.objects.filter(
        comment__faculty=faculty
    ).exclude(faculty=faculty)
    follows = tbl_follow.objects.filter(
        tofaculty=faculty,
        follow_status=1
    )
    news = tbl_news.objects.filter(news_status=1)

    context = {
        "likes": likes,
        "comments": comments,
        "replies": replies,
        "follows": follows,
        "news": news
    }
    return render(request, "Faculty/Notification.html", context)

