from django.shortcuts import render,redirect
from Guest.models import *
from College.models import *
from Faculty.models import *
from django.db.models import Q
# Create your views here.
def HomePage(request):
    Student = tbl_student.objects.get(id=request.session['sid'])
    return render(request,'Student/HomePage.html',{'Student':Student})
def MyProfile(request):
    studentdata=tbl_student.objects.get(id=request.session["sid"])
    return render(request,'Student/MyProfile.html',{"studentdata": studentdata})
def EditProfile(request):
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
    student=tbl_student.objects.get(id=request.session["sid"])
    department=tbl_department.objects.all()
   
    semester=tbl_semester.objects.all()
    if request.method == "POST":
        subject=tbl_subject.objects.get(id=request.POST.get("sel_subject"))
        notes=tbl_notes.objects.filter(subject=subject)
        return render(request,'Student/ViewNotes.html',{"department": department,'semester':semester,'notes':notes})
    else:
        return render(request,'Student/ViewNotes.html',{"department": department,'semester':semester})
def AjaxCourse(request):
    departmentid = request.GET.get("did")
    course = tbl_course.objects.filter(department=departmentid)
    return render(request,"Student/AjaxCourse.html",{'course':course})
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
    post=tbl_post.objects.all()
    return render(request,'Student/ViewPost.html',{'post':post})
def likepost(request,pid):
    student=tbl_student.objects.get(id=request.session["sid"])
    postid=tbl_post.objects.get(id=pid)
    tbl_like.objects.create(post=postid,student=student)
    return redirect("Student:ViewPost")
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
def FollowU(request, uid):
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

def ViewCollegeProfile(request):
    student=tbl_student.objects.get(id=request.session["sid"])
    collegedata=tbl_follow.objects.filter(tostudent=student)
    collegeid=tbl_follow.objects.get(fromstudent=student)
    post=tbl_post.objects.filter(college_id=collegeid)
    return render(request,'Student/ViewCollegeProfile.html',{"collegedata": collegedata,"post":post})




