from django.shortcuts import render,redirect
from Guest.models import *
from Admin.models import *
from College.models import *
from Faculty.models import *


# Create your views here.
def HomePage(request):
    College = tbl_college.objects.get(id=request.session['cid'])
    return render(request,'College/HomePage.html',{'College':College})

def CollegeProfile(request):
    collegedata=tbl_college.objects.get(id=request.session["cid"])
    return render(request,'College/CollegeProfile.html',{"collegedata": collegedata})
def EditProfile(request):
    collegedata=tbl_college.objects.get(id=request.session["cid"])
    if request.method == "POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        address=request.POST.get('txt_address')
        collegedata.college_name=name
        collegedata.college_email=email
        collegedata.college_contact=contact
        collegedata.college_address=address
        collegedata.save()

        return render(request,'College/EditProfile.html',{'msg':'updated'})
    else:
        return render(request,'College/EditProfile.html',{"collegedata":collegedata})
def ChangePassword(request):
    collegedata=tbl_college.objects.get(id=request.session["cid"])
    collegepassword=collegedata.college_password

    if request.method == "POST":
        oldpassword=request.POST.get('txt_opassword')
        newpassword=request.POST.get('txt_npassword')
        retype=request.POST.get('txt_cpassword')
        if collegepassword==oldpassword:
            if newpassword==retype:
                collegedata.college_password=newpassword
                collegedata.save()
                return render(request,'College/ChangePassword.html',{"msg":"Password Updated"})
            else:
                return render(request,'College/ChangePassword.html',{"msg1":"Password Mismatch"})
        else:
            return render(request,'College/ChangePassword.html',{"msg2":"Password Incorrect"})
    else:
        return render(request,'College/ChangePassword.html')

def FacultyRegistration(request):
    faculty=tbl_faculty.objects.filter(college=request.session['cid'])
    department=tbl_collegedepartment.objects.filter(college=request.session["cid"])
    if request.method == "POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        contact=request.POST.get("txt_contact")
        username=request.POST.get("txt_username")
        password=request.POST.get("txt_password")
        photo=request.FILES.get("file_photo")
        bio=request.POST.get("txt_biodata")
        accounttype=request.POST.get("txt_account")
        college=tbl_college.objects.get(id=request.session['cid'])
        departmentid=tbl_collegedepartment.objects.get(id=request.POST.get("sel_department"))
       
        tbl_faculty.objects.create(faculty_name=name,faculty_email=email,faculty_contact=contact,faculty_username=username,
        faculty_password=password,faculty_photo=photo,faculty_bio=bio,faculty_accounttype=accounttype,college=college,department=departmentid)
        return render(request,'College/FacultyRegistration.html',{'msg':'data inserted'})
    else:
        return render(request,'College/FacultyRegistration.html',{'faculty':faculty,'department':department})



def AssignSubject(request,fid):
    faculty=tbl_faculty.objects.get(id=fid)
    departmentid=faculty.department.department.id
    course=tbl_collegecourse.objects.filter(college=request.session["cid"],course__department=departmentid)
    semester=tbl_semester.objects.all()
    assignsubject=tbl_assignsubject.objects.filter(faculty=fid)
    if request.method == "POST":
       
        subject=tbl_subject.objects.get(id=request.POST.get("sel_subject"))

        tbl_assignsubject.objects.create(subject=subject,faculty=faculty)
        return render(request,'College/AssignSubject.html',{'msg':'data inserted'})
    else:
        return render(request,'College/AssignSubject.html',{'course':course,'faculty':faculty,'semester':semester,'assignsubject':assignsubject})
def delfaculty(request,did):
    tbl_faculty.objects.get(id=did).delete()
    return redirect("College:FacultyRegistration")
def CollegeDepartment(request):
    ddata=tbl_department.objects.all()
    cdata=tbl_collegedepartment.objects.filter(college=request.session["cid"])
    if request.method=="POST":
        department=tbl_department.objects.get(id=request.POST.get("sel_department"))
        college=tbl_college.objects.get(id=request.session["cid"])
        tbl_collegedepartment.objects.create(department=department,college=college)
        cdata = tbl_collegedepartment.objects.filter(college=request.session["cid"])
        return render(request,'College/CollegeDepartment.html',{'msg':'data inserted',"collegedepartment":cdata,"department":ddata})
    else:
        return render(request,'College/CollegeDepartment.html',{"collegedepartment":cdata,"department":ddata})
def deldepartment(request,did):
    tbl_collegedepartment.objects.get(id=did).delete()
    return redirect("College:CollegeDepartment")
def CollegeCourse(request):
    college = tbl_college.objects.get(id=request.session["cid"])
    ddata=tbl_collegedepartment.objects.filter(college=college)
    ccdata=tbl_collegecourse.objects.filter(college=college)
    if request.method=="POST":
        department=tbl_department.objects.get(id=request.POST.get("sel_department"))
        course=tbl_course.objects.get(id=request.POST.get("sel_course"))
        college=tbl_college.objects.get(id=request.session["cid"])
        tbl_collegecourse.objects.create(course=course,college=college)
        ddata = tbl_collegedepartment.objects.filter(college=request.session["cid"])
        
        return render(request,'College/CollegeCourse.html',{'msg':'data inserted',"collegedepartment":ddata,"course":ccdata})
    else:
        return render(request,'College/CollegeCourse.html',{"collegedepartment":ddata,"course":ccdata})
def delcourse(request,did):
    tbl_collegecourse.objects.get(id=did).delete()
    return redirect("College:CollegeCourse")
def AjaxCollegeCourse(request):
    departmentid = request.GET.get("did")
    course = tbl_course.objects.filter(department=departmentid)
    return render(request,"College/AjaxCollegeCourse.html",{'course':course})
def AjaxDepartment(request):
    collegeid = request.GET.get("did")
    department = tbl_collegedepartment.objects.filter(college=collegeid)
    return render(request,"College/AjaxDepartment.html",{'department':department})
def AjaxSubject(request):
    courseid = request.GET.get("course")
    semid = request.GET.get("semid")
    subject = tbl_subject.objects.filter(course=courseid,semester=semid)
    return render(request,"College/AjaxSubject.html",{'subject':subject})
def delsubject(request,did):
    tbl_assignsubject.objects.get(id=did).delete()
    return redirect("College:FacultyRegistration")
def Post(request):
    collegeid = tbl_college.objects.get(id=request.session['cid']) 
    post=tbl_post.objects.filter(college=collegeid)

    if request.method == "POST":
        photo=request.FILES.get("file_photo")
        description=request.POST.get("txt_description")
        posttype=request.POST.get("txt_post")
        tbl_post.objects.create(post_photo=photo,post_description=description,post_type=posttype,college=collegeid)
        
        return render(request,'College/Post.html',{'msg':'data inserted','post':post})
    else:
        return render(request,'College/Post.html',{'post':post})
def delpost(request,did):
    tbl_post.objects.get(id=did).delete()
    return redirect("College:Post")
def ViewPost(request):
    post=tbl_post.objects.all()
    return render(request,'College/ViewPost.html',{'post':post})
def likepost(request,pid):
    college=tbl_college.objects.get(id=request.session["cid"])
    postid=tbl_post.objects.get(id=pid)
    tbl_like.objects.create(post=postid,college=college)
    return redirect("College:ViewPost")
def Comment(request, cid):
    post = tbl_post.objects.get(id=cid)
    college = tbl_college.objects.get(id=request.session["cid"])

    if request.method == "POST":

        form_type = request.POST.get("type")

        # ADD COMMENT
        if form_type == "comment":
            comment_text = request.POST.get("comment")

            if comment_text:  
                tbl_comment.objects.create(
                    post=post,
                    college=college,
                    comment_content=comment_text
                )
        elif form_type == "reply":
            reply_text = request.POST.get("reply")
            comment_id = request.POST.get("comment_id")

            if reply_text and comment_id:
                comment = tbl_comment.objects.get(id=comment_id)
                tbl_commentreply.objects.create(
                    comment=comment,
                    college=college,
                    commentreply_content=reply_text
                )

        return redirect("College:Comment", cid=cid)

    comments = tbl_comment.objects.filter(post=post).order_by("-id")

    return render(request, "College/Comment.html", {
        "comment": comments,
        "post": post
    })
def FollowF(request,fid):
    college=tbl_college.objects.get(id=request.session["cid"])
    facultyid=tbl_faculty.objects.get(id=fid)
    tbl_follow.objects.create(fromcollege=college,tofaculty=facultyid)
    return redirect("College:FacultyList")
def FollowC(request,Cid):
    college=tbl_college.objects.get(id=request.session["cid"])
    collegeid=tbl_college.objects.get(id=Cid)
    tbl_follow.objects.create(fromcollege=college,tocollege=collegeid)
    return redirect("College:CollegeList")
def FollowS(request,Sid):
    college=tbl_college.objects.get(id=request.session["cid"])
    studentid=tbl_student.objects.get(id=Sid)
    tbl_follow.objects.create(fromcollege=college,tostudent=studentid)
    return redirect("College:StudentList")
def FacultyList(request):
    faculty=tbl_faculty.objects.all()
    return render(request,'College/FacultyList.html',{'faculty':faculty})
def CollegeList(request):
    college=tbl_college.objects.all()
    return render(request,'College/CollegeList.html',{'college':college})
def StudentList(request):
    student=tbl_student.objects.all()
    return render(request,'College/StudentList.html',{'users':student})