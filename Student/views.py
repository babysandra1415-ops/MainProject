from django.shortcuts import render,redirect
from Guest.models import *
from College.models import *
from Student.models import *
from Faculty.models import *
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from datetime import datetime
# Create your views here.
def HomePage(request):
    if "sid" not in request.session:
        return redirect("Guest/Login.html")
    else:
        Student = tbl_student.objects.get(id=request.session['sid'])
        return render(request,'Student/HomePage.html',{'Student':Student})
def MyProfile(request):
    if "sid" not in request.session:
        return redirect("Guest/Login.html")
    else:
        studentdata=tbl_student.objects.get(id=request.session["sid"])
        return render(request,'Student/MyProfile.html',{"studentdata": studentdata})
def EditProfile(request):
    if "sid" not in request.session:
        return redirect("Guest/Login.html")
    else:
        studentdata=tbl_student.objects.get(id=request.session["sid"])
        if request.method == "POST":
            name=request.POST.get('txt_name')
            email=request.POST.get('txt_email')
            contact=request.POST.get('txt_contact')
            username=request.POST.get('txt_username')
            bio=request.POST.get('txt_biodata')
        
            studentdata.student_name=name
            studentdata.student_email=email
            studentdata.student_contact=contact
            studentdata.student_username=username
            studentdata.student_bio=bio
            studentdata.save()

            return render(request,'Student/EditProfile.html',{'msg':'updated'})
        else:
            return render(request,'Student/EditProfile.html',{"studentdata":studentdata})
def topublic(request,pid):
    Student=tbl_student.objects.get(id=pid)
    Student.student_accounttype=0
    Student.save()
    return render(request,'Student/MyProfile.html',{'msg':"Changed to Public","studentdata":Student})
def toprivate(request,prid):
    Student=tbl_student.objects.get(id=prid)
    Student.student_accounttype=1
    Student.save()
    return render(request,'Student/MyProfile.html',{'msg1':"Changed to Private","studentdata":Student})
def ChangePassword(request):
    studentdata=tbl_student.objects.get(id=request.session["sid"])
    studentpassword=studentdata.student_password

    if request.method == "POST":
        oldpassword=request.POST.get('txt_opassword')
        newpassword=request.POST.get('txt_npassword')
        retype=request.POST.get('txt_cpassword')
        if studentpassword==oldpassword:
            if newpassword==retype:
                studentdata.student_password=newpassword
                studentdata.save()
                return render(request,'Student/ChangePassword.html',{"msg":"Password Updated"})
            else:
                return render(request,'Student/ChangePassword.html',{"msg1":"Password Mismatch"})
        else:
            return render(request,'Student/ChangePassword.html',{"msg2":"Password Incorrect"})
    else:
        return render(request,'Student/ChangePassword.html')



def ViewNotes(request):
    if "sid" not in request.session:
        return redirect("Guest/Login.html")

    department = tbl_department.objects.all()
    semester = tbl_semester.objects.all()

    # initial load → show all notes
    notes = tbl_notes.objects.all()

    return render(request, 'Student/ViewNotes.html', {
        "department": department,
        "semester": semester,
        "notes": notes
    })


def AjaxCourse(request):
    departmentid = request.GET.get("did")
    course = tbl_course.objects.filter(department=departmentid)
    return render(request,"Student/AjaxCourse.html",{'course':course})

def AjaxCompresult(request):
    did = request.GET.get('did')
    cid = request.GET.get('cid')
    sem = request.GET.get('sem')
    sub = request.GET.get('sub')

    data = tbl_notes.objects.select_related(
        "subject",
        "subject__course",
        "subject__semester"
    )

    if did and did != "Department":
        data = data.filter(subject__course__department_id=did)

    if cid:
        data = data.filter(subject__course_id=cid)

    if sem and sem != "Semester":
        data = data.filter(subject__semester_id=sem)

    if sub:
        data = data.filter(subject_id=sub)

    return render(request, "Student/Ajaxnotes.html", {"data": data})



def Post(request):
    studentid = tbl_student.objects.get(id=request.session['sid']) 
    post=tbl_post.objects.filter(student=studentid)

    if request.method == "POST":
        photo=request.FILES.get("file_photo")
        description=request.POST.get("txt_description")
        posttype=request.POST.get("txt_post")
        tbl_post.objects.create(post_photo=photo,post_description=description,post_type=posttype,student=studentid)
        
        return render(request,'Student/Post.html',{'msg':'data inserted','post':post})
    else:
        return render(request,'Student/Post.html',{'post':post})
def delpost(request,did):
    tbl_post.objects.get(id=did).delete()
    return redirect("Student:Post")
def ViewPost(request):
    student = tbl_student.objects.get(id=request.session["sid"])
    post=tbl_post.objects.all()
    liked_posts = tbl_like.objects.filter(student=student).values_list('post_id', flat=True)
    return render(request,'Student/ViewPost.html',{'post':post,'liked_posts': liked_posts})
# def likepost(request,pid):
#     student=tbl_student.objects.get(id=request.session["sid"])
#     postid=tbl_post.objects.get(id=pid)
#     tbl_like.objects.create(post=postid,student=student)
#     return redirect("Student:ViewPost")

def likepost(request):
    if request.method == "POST":
        student = tbl_student.objects.get(id=request.session["sid"])
        post_id = request.POST.get('post_id')
        post = tbl_post.objects.get(id=post_id)

        like_qs = tbl_like.objects.filter(post=post, student=student)
        if like_qs.exists():
            like_qs.delete() 
            liked = False
        else:
            tbl_like.objects.create(post=post, student=student)  
            liked = True

        return JsonResponse({'liked': liked})

    return JsonResponse({'error': 'Invalid request'})


def Comment(request, cid):
    post = tbl_post.objects.get(id=cid)
    student = tbl_student.objects.get(id=request.session["sid"])

    if request.method == "POST":

        form_type = request.POST.get("type")

        # ADD COMMENT
        if form_type == "comment":
            comment_text = request.POST.get("comment")

            if comment_text:  
                tbl_comment.objects.create(
                    post=post,
                    student=student,
                    comment_content=comment_text
                )
        elif form_type == "reply":
            reply_text = request.POST.get("reply")
            comment_id = request.POST.get("comment_id")

            if reply_text and comment_id:
                comment = tbl_comment.objects.get(id=comment_id)
                tbl_commentreply.objects.create(
                    comment=comment,
                    student=student,
                    commentreply_content=reply_text
                )

        return redirect("Student:Comment", cid=cid)

    comments = tbl_comment.objects.filter(post=post).order_by("-id")

    return render(request, "Student/Comment.html", {
        "comment": comments,
        "post": post
    })

def ViewCollege(request):
    student = tbl_student.objects.get(id=request.session['sid'])
    college = tbl_college.objects.filter(college_status=1)

    followed_ids = tbl_follow.objects.filter(
        fromstudent=student,
        tocollege__isnull=False
    ).values_list('tocollege_id', flat=True)

    return render(request,'Student/ViewCollege.html',{
        'college': college,
        'followed_ids': followed_ids
    })

def ViewFaculty(request):
    student = tbl_student.objects.get(id=request.session['sid'])
    faculty = tbl_faculty.objects.all()

    followed_ids = tbl_follow.objects.filter(
        fromstudent=student,
        tofaculty__isnull=False
    ).values_list('tofaculty_id', flat=True)

    pending_ids = tbl_follow.objects.filter(
        fromstudent=student,
        tofaculty__isnull=False,
        follow_status=0
    ).values_list('tofaculty_id', flat=True)

    return render(request,'Student/ViewFaculty.html',{
        'faculty': faculty,
        'followed_ids': followed_ids,
        'pending_ids': pending_ids
    })

def StudentList(request):
    student = tbl_student.objects.get(id=request.session['sid'])
    users = tbl_student.objects.exclude(id=student.id)

    followed_ids = tbl_follow.objects.filter(
        fromstudent=student,
        tostudent__isnull=False
    ).values_list('tostudent_id', flat=True)

    pending_ids = tbl_follow.objects.filter(
        fromstudent=student,
        tostudent__isnull=False,
        follow_status=0
    ).values_list('tostudent_id', flat=True)

    return render(request,'Student/StudentList.html',{
        'users': users,
        'followed_ids': followed_ids,
        'pending_ids': pending_ids
    })


def Follow(request, cid):
    student = tbl_student.objects.get(id=request.session["sid"])
    college = tbl_college.objects.get(id=cid)

    if not tbl_follow.objects.filter(fromstudent=student, tocollege=college).exists():
        tbl_follow.objects.create(
            fromstudent=student,
            tocollege=college,
            follow_status=1
        )
    return redirect("Student:ViewCollege")
def FollowF(request, Fid):
    student = tbl_student.objects.get(id=request.session["sid"])
    faculty = tbl_faculty.objects.get(id=Fid)

    status = 0 if faculty.faculty_accounttype == 1 else 1

    if not tbl_follow.objects.filter(fromstudent=student, tofaculty=faculty).exists():
        tbl_follow.objects.create(
            fromstudent=student,
            tofaculty=faculty,
            follow_status=status
        )
    return redirect("Student:ViewFaculty")
def FollowU(request,uid):
    student = tbl_student.objects.get(id=request.session["sid"])
    target = tbl_student.objects.get(id=uid)

    status = 0 if target.student_accounttype == 1 else 1

    if not tbl_follow.objects.filter(fromstudent=student, tostudent=target).exists():
        tbl_follow.objects.create(
            fromstudent=student,
            tostudent=target,
            follow_status=status
        )
    return redirect("Student:StudentList")


def FollowRequest(request):
    student=tbl_student.objects.get(id=request.session["sid"])
    request=tbl_follow.objects.filter(tostudent=student)
    return render(request,'Student/FollowRequest.html',{"request":request})


def Followers(request):
    student = tbl_student.objects.get(id=request.session["sid"])

    following = tbl_follow.objects.filter(
        fromstudent=student
    )

    followers = tbl_follow.objects.filter(
        tostudent=student,
        follow_status=1
    )
    requests = tbl_follow.objects.filter(
        tostudent=student,
        follow_status=0
    )

    return render(
        request,
        "Student/Followers.html",
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
    return redirect("Student:Followers")

def rejectrequest(request,rid):
    tbl_follow.objects.get(id=rid).delete()
    return redirect("Student:Followers")

def ViewCollegeProfile(request,pid):
    
    college=tbl_college.objects.get(id=pid)
    
    post=tbl_post.objects.filter(college=college)
    return render(request,'Student/ViewCollegeProfile.html',{"college": college,"post":post})
def ViewFacultyProfile(request,fid):
    
    faculty=tbl_faculty.objects.get(id=fid)
    
    post=tbl_post.objects.filter(faculty=faculty)
    return render(request,'Student/ViewFacultyProfile.html',{"faculty": faculty,"post":post})
def ViewStudentProfile(request,sid):
    
    student=tbl_student.objects.get(id=sid)
    
    post=tbl_post.objects.filter(student=student)
    return render(request,'Student/ViewStudentProfile.html',{"student": student,"post":post})

def Complaint(request):
    student=tbl_student.objects.get(id=request.session["sid"])
    complaint=tbl_complaint.objects.filter(student_id=student)
    if request.method == "POST":
        
        title=request.POST.get("txt_title")
        content=request.POST.get("txt_content")
        tbl_complaint.objects.create(complaint_title=title,complaint_content=content,student=student)
        
        return render(request,'Student/Complaint.html',{'complaint':complaint})
    else:
        return render(request,'Student/Complaint.html',{'complaint':complaint})
def deletecomplaint(request,did):
    tbl_complaint.objects.get(id=did).delete()
    return redirect("Student:Complaint")



def ChatList(request):
    """Instagram-style unified chat list: only followed people, with seen/unseen counts."""
    if "sid" not in request.session:
        return redirect("Guest:Login")
    student = tbl_student.objects.get(id=request.session["sid"])
    conversations = []
    # People student follows (accepted)
    following = tbl_follow.objects.filter(fromstudent=student, follow_status=1)
    for f in following:
        if f.tostudent:
            other_id, other_type = f.tostudent_id, "student"
            name = f.tostudent.student_name
            photo = f.tostudent.student_photo
            chat_filter = (Q(student_from=student) | Q(student_to=student)) & (Q(student_from=f.tostudent) | Q(student_to=f.tostudent))
        elif f.tofaculty:
            other_id, other_type = f.tofaculty_id, "faculty"
            name = f.tofaculty.faculty_name
            photo = f.tofaculty.faculty_photo
            chat_filter = (Q(student_from=student) | Q(student_to=student)) & (Q(faculty_from=f.tofaculty) | Q(faculty_to=f.tofaculty))
        elif f.tocollege:
            other_id, other_type = f.tocollege_id, "college"
            name = f.tocollege.college_name
            photo = f.tocollege.college_photo
            chat_filter = (Q(student_from=student) | Q(student_to=student)) & (Q(college_from=f.tocollege) | Q(college_to=f.tocollege))
        else:
            continue
        last_chat = tbl_chat.objects.filter(chat_filter).order_by('-chat_time').first()
        unseen = tbl_chat.objects.filter(chat_filter, chat_seen=False)
        unseen = unseen.filter(student_to=student)
        unseen_count = unseen.count()
        conversations.append({
            "other_id": other_id, "other_type": other_type, "name": name, "photo": photo,
            "last_chat": last_chat, "unseen_count": unseen_count
        })
    def sort_key(c):
        if c["last_chat"]:
            return (1, c["last_chat"].chat_time)
        return (0, datetime(1970, 1, 1))
    conversations.sort(key=sort_key, reverse=True)
    return render(request, "Student/ChatList.html", {"conversations": conversations, "Student": student})

def ajaxchatseen(request):
    """Mark messages as seen when opening chat."""
    tid = request.GET.get("tid")
    utype = request.GET.get("utype", "student")
    user = tbl_student.objects.get(id=request.session["sid"])
    if utype == "student":
        tbl_chat.objects.filter(student_from_id=tid, student_to=user, chat_seen=False).update(chat_seen=True)
    elif utype == "faculty":
        tbl_chat.objects.filter(faculty_from_id=tid, student_to=user, chat_seen=False).update(chat_seen=True)
    elif utype == "college":
        tbl_chat.objects.filter(college_from_id=tid, student_to=user, chat_seen=False).update(chat_seen=True)
    return JsonResponse({"ok": True})

def chatpage(request,id):
    student  = tbl_student.objects.get(id=id)
    tbl_chat.objects.filter(student_from_id=id, student_to=request.session["sid"], chat_seen=False).update(chat_seen=True)
    return render(request,"Student/Chat.html",{"student":student})

def ajaxchat(request):
    from_student = tbl_student.objects.get(id=request.session["sid"])
    to_student = tbl_student.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),student_from=from_student,student_to=to_student,chat_file=request.FILES.get("file"))
    return render(request,"Student/Chat.html")

def ajaxchatview(request):
    tid = request.GET.get("tid")
    user = tbl_student.objects.get(id=request.session["sid"])
    chat_data = tbl_chat.objects.filter((Q(student_from=user) | Q(student_to=user)) & (Q(student_from=tid) | Q(student_to=tid))).order_by('chat_time')
    return render(request,"Student/ChatView.html",{"data":chat_data,"tid":int(tid)})

def clearchat(request):
    tbl_chat.objects.filter(Q(student_from=request.session["sid"]) & Q(student_to=request.GET.get("tid")) | (Q(student_from=request.GET.get("tid")) & Q(student_to=request.session["sid"]))).delete()
    return render(request,"Student/ClearChat.html",{"msg":"Chat Deleted Sucessfully...."})



def fchatpage(request,id):
    faculty  = tbl_faculty.objects.get(id=id)
    tbl_chat.objects.filter(faculty_from_id=id, student_to=request.session["sid"], chat_seen=False).update(chat_seen=True)
    return render(request,"Student/FChat.html",{"faculty":faculty})

def fajaxchat(request):
    from_student = tbl_student.objects.get(id=request.session["sid"])
    to_faculty = tbl_faculty.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),student_from=from_student,faculty_to=to_faculty,chat_file=request.FILES.get("file"))
    return render(request,"Student/FChat.html")

def fajaxchatview(request):
    tid = request.GET.get("tid")
    user = tbl_student.objects.get(id=request.session["sid"])
    chat_data = tbl_chat.objects.filter((Q(student_from=user) | Q(student_to=user)) & (Q(faculty_from=tid) | Q(faculty_to=tid))).order_by('chat_time')
    return render(request,"Student/FChatView.html",{"data":chat_data,"tid":int(tid)})

def fclearchat(request):
    tbl_chat.objects.filter(Q(student_from=request.session["sid"]) & Q(faculty_to=request.GET.get("tid")) | (Q(faculty_from=request.GET.get("tid")) & Q(student_to=request.session["sid"]))).delete()
    return render(request,"Student/FClearChat.html",{"msg":"Chat Deleted Sucessfully...."})

def cchatpage(request,id):
    college  = tbl_college.objects.get(id=id)
    tbl_chat.objects.filter(college_from_id=id, student_to=request.session["sid"], chat_seen=False).update(chat_seen=True)
    return render(request,"Student/CChat.html",{"college":college})

def cajaxchat(request):
    from_student = tbl_student.objects.get(id=request.session["sid"])
    to_college = tbl_college.objects.get(id=request.POST.get("tid"))
    tbl_chat.objects.create(chat_content=request.POST.get("msg"),chat_time=datetime.now(),student_from=from_student,college_to=to_college,chat_file=request.FILES.get("file"))
    return render(request,"Student/CChat.html")

def cajaxchatview(request):
    tid = request.GET.get("tid")
    user = tbl_student.objects.get(id=request.session["sid"])
    chat_data = tbl_chat.objects.filter((Q(student_from=user) | Q(student_to=user)) & (Q(college_from=tid) | Q(college_to=tid))).order_by('chat_time')
    return render(request,"Student/CChatView.html",{"data":chat_data,"tid":int(tid)})

def cclearchat(request):
    tbl_chat.objects.filter(Q(student_from=request.session["sid"]) & Q(college_to=request.GET.get("tid")) | (Q(college_from=request.GET.get("tid")) & Q(student_to=request.session["sid"]))).delete()
    return render(request,"Student/ClearChat.html",{"msg":"Chat Deleted Sucessfully...."})

def Search(request):
    # student=tbl_student.objects.all().exclude(id=request.session['sid'])
    # faculty= tbl_faculty.objects.all()
    # college = tbl_college.objects.all()
    if request.method == "POST":
        student=tbl_student.objects.all().exclude(id=request.session['sid'])
        faculty= tbl_faculty.objects.all()
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
        return render(request,"Student/Search.html",{'student':student,'college':college,'faculty':faculty})
    else:
        return render(request,"Student/Search.html")

def Notification(request):
    student = tbl_student.objects.get(id=request.session["sid"])

    likes = tbl_like.objects.filter(
        post__student=student
    ).exclude(student=student)
    comments = tbl_comment.objects.filter(
        post__student=student
    ).exclude(student=student)

    replies = tbl_commentreply.objects.filter(
        comment__student=student
    ).exclude(student=student)
    follows = tbl_follow.objects.filter(
        tostudent=student,
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
    return render(request, "Student/Notification.html", context)

    
def rating(request):
    parray=[1,2,3,4,5]
    # wdata=tbl_booking.objects.get(id=mid)
    
    counts=0
    counts=stardata=tbl_rating.objects.all().count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.all().order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        # print(avg)
        return render(request,"Student/Rating.html",{'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"Student/Rating.html")

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    
    user_review=request.GET.get('user_review')
    # pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(student=tbl_student.objects.get(id=request.session['sid']),user_review=user_review,rating_data=rating_data)
    stardata=tbl_rating.objects.all().order_by('-datetime')
    return render(request,"Student/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.all()
    ratecount = tbl_rating.objects.all().count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)
def Logout(request):
    del request.session["sid"]       
    return redirect("Guest:Login")