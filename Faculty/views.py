from django.shortcuts import render,redirect
from College.models import *
from Admin.models import *
from Guest.models import *
from Faculty.models import *

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
def likepost(request,pid):
    faculty=tbl_faculty.objects.get(id=request.session["fid"])
    postid=tbl_post.objects.get(id=pid)
    tbl_like.objects.create(post=postid,faculty=faculty)
    return redirect("Faculty:ViewPost")


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
def Follow(request,cid):
    faculty=tbl_faculty.objects.get(id=request.session["fid"])
    collegeid=tbl_college.objects.get(id=cid)
    tbl_follow.objects.create(fromfaculty=faculty,tocollege=collegeid)
    return redirect("Faculty:ViewCollege")
def FollowU(request,uid):
    faculty=tbl_faculty.objects.get(id=request.session["fid"])
    studentid=tbl_student.objects.get(id=uid)
    tbl_follow.objects.create(fromfaculty=faculty,tostudent=studentid)
    return redirect("Faculty:UserList")

def FollowF(request,Fid):
    faculty=tbl_faculty.objects.get(id=request.session["fid"])
    facultyid=tbl_faculty.objects.get(id=Fid)
    tbl_follow.objects.create(fromfaculty=faculty,tofaculty=facultyid)
    return redirect("Faculty:ViewFaculty")
def ViewFaculty(request):
    faculty=tbl_faculty.objects.all()
    return render(request,'Faculty/ViewFaculty.html',{'faculty':faculty})

def ViewCollege(request):
    college=tbl_college.objects.filter(college_status=1)
    return render(request,'Faculty/ViewCollege.html',{'college':college})
def UserList(request):
    userdata=tbl_student.objects.all()
    return render(request,'Faculty/UserList.html',{"users":userdata})


