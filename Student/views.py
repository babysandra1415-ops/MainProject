from django.shortcuts import render,redirect
from Guest.models import *
from College.models import *
from Faculty.models import *
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

