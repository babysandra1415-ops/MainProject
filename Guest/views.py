from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from College.models import *
from Faculty.models import *

# Create your views here.
def UserRegistration(request):
    district=tbl_district.objects.all()
    place=tbl_place.objects.all()
    if request.method == "POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        contact=request.POST.get("txt_contact")
        address=request.POST.get("txt_address")
        password=request.POST.get("txt_password")
        photo=request.FILES.get("file_photo")
        place=tbl_place.objects.get(id=request.POST.get("sel_place"))
        tbl_user.objects.create(user_name=name,user_email=email,user_contact=contact,user_address=address,
        user_password=password,user_photo=photo,place=place)
        return render(request,'Guest/UserRegistration.html',{'msg':'data inserted'})
    else:
        return render(request,'Guest/UserRegistration.html',{'district':district,'place':place})

def CollegeRegistration(request):
    district=tbl_district.objects.all()
    place=tbl_place.objects.all()
    if request.method == "POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        contact=request.POST.get("txt_contact")
        address=request.POST.get("txt_address")
        password=request.POST.get("txt_password")
        photo=request.FILES.get("file_photo")
        logo=request.FILES.get("file_logo")
        proof=request.FILES.get("file_proof")
        place=tbl_place.objects.get(id=request.POST.get("sel_place"))
        tbl_college.objects.create(college_name=name,college_email=email,college_contact=contact,college_address=address,
        college_password=password,college_photo=photo,college_logo=logo,college_proof=proof,place=place)
        return render(request,'Guest/CollegeRegistration.html',{'msg':'data inserted'})
    else:
        return render(request,'Guest/CollegeRegistration.html',{'district':district,'place':place})

def AjaxPlace(request):
    district=tbl_district.objects.get(id=request.GET.get("did"))
    place=tbl_place.objects.filter(district=district)
    return render(request,'Guest/AjaxPlace.html',{"place":place})

def StudentRegistration(request):
    college=tbl_college.objects.all()
    department=tbl_collegedepartment.objects.all()
    course=tbl_collegecourse.objects.all()
    year=tbl_academicyear.objects.all()
    if request.method == "POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        contact=request.POST.get("txt_contact")
        username=request.POST.get("txt_username")
        password=request.POST.get("txt_password")
        photo=request.FILES.get("file_photo")
        bio=request.POST.get("txt_bio")
        accounttype=request.POST.get("txt_account")
        college=tbl_college.objects.get(id=request.POST.get("sel_college"))
        year=tbl_academicyear.objects.get(id=request.POST.get("sel_year"))
        course=tbl_collegecourse.objects.get(id=request.POST.get("sel_course"))
        tbl_student.objects.create(student_name=name,student_email=email,student_contact=contact,student_username=username,
        student_password=password,student_photo=photo,student_bio=bio,student_accounttype=accounttype,college=college,course=course,academicyear=year)
        return render(request,'Guest/StudentRegistration.html',{'msg':'data inserted'})
    else:
        return render(request,'Guest/StudentRegistration.html',{'college':college,'department':department,'course':course,'year':year})
def AjaxCourse(request):
    departmentid = request.GET.get("did")
    collegeid = request.GET.get("college")
    course = tbl_collegecourse.objects.filter(course__department=departmentid,college=collegeid)
    return render(request,"Guest/AjaxCourse.html",{'course':course})
def AjaxDepartment(request):
    collegeid = request.GET.get("did")
    department = tbl_collegedepartment.objects.filter(college=collegeid)
    return render(request,"Guest/AjaxDepartment.html",{'department':department})
def Login(request):
    if request.method == "POST":
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password")

        admincount=tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        usercount=tbl_user.objects.filter(user_email=email,user_password=password).count()
        collegecount=tbl_college.objects.filter(college_email=email,college_password=password,college_status=1).count()
        facultycount=tbl_faculty.objects.filter(faculty_email=email,faculty_password=password).count()
        studentcount=tbl_student.objects.filter(student_email=email,student_password=password).count()
        
        if admincount>0:
            admindata=tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session["aid"]=admindata.id
            return redirect("Admin:HomePage")
        elif usercount>0:
            userdata=tbl_user.objects.get(user_email=email,user_password=password)
            request.session["uid"]=userdata.id
            return redirect("User:HomePage")
        elif collegecount>0:
            collegedata=tbl_college.objects.get(college_email=email,college_password=password)
            request.session["cid"]=collegedata.id
            return redirect("College:HomePage")   
        elif facultycount>0:
            facultydata=tbl_faculty.objects.get(faculty_email=email,faculty_password=password)
            request.session["fid"]=facultydata.id
            return redirect("Faculty:HomePage")  
        elif studentcount>0:
            studentdata=tbl_student.objects.get(student_email=email,student_password=password)
            request.session["sid"]=studentdata.id
            return redirect("Student:HomePage")  
        else:
            return render(request,'Guest/Login.html',{'msg':' Invalid Email or Password '})
    else:
        return render(request,'Guest/Login.html')
def index(request):
    student_count = tbl_student.objects.count()
    college_count = tbl_college.objects.count()
    faculty_count = tbl_faculty.objects.count()
    post_count = tbl_post.objects.count()

    context = {
        "student_count": student_count,
        "college_count": college_count,
        "faculty_count": faculty_count,
        "post_count": post_count,
    }
    return render(request,"Guest/index.html", context)
    