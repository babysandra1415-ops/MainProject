from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from College.models import *

# Create your views here.
def AdminRegistration(request):
    data=tbl_admin.objects.all()
    if request.method=="POST":
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password")
        tbl_admin.objects.create(admin_name=name,admin_email=email,admin_password=password)
        return render(request,'Admin/AdminRegistration.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/AdminRegistration.html',{'admin':data})
def deladmin(request,did):
    tbl_admin.objects.get(id=did).delete()
    return redirect("Admin:AdminRegistration")
def editadmin(request,eid):
     editdata=tbl_admin.objects.get(id=eid)
     data=tbl_admin.objects.all()
     if request.method=="POST":
        name=request.POST.get("txt_name")
        editdata.admin_name=name
        email=request.POST.get("txt_email")
        editdata.admin_email=email
        password=request.POST.get("txt_password")
        editdata.admin_password=password
        editdata.save()
        return redirect("Admin:AdminRegistration")
     else:
        return render(request,'Admin/AdminRegistration.html',{'editdata':editdata,'admin':data})
def District(request):
    data=tbl_district.objects.all()
    if request.method=="POST":
        district=request.POST.get("txt_district")
        tbl_district.objects.create(district_name=district)
        return render(request,'Admin/District.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/District.html',{'district':data})
def deldistrict(request,id):
    tbl_district.objects.get(id=id).delete()
    return redirect("Admin:District")
def editdistrict(request,eid):
     editdata=tbl_district.objects.get(id=eid)
     data=tbl_district.objects.all()
     if request.method=="POST":
        district=request.POST.get("txt_district")
        editdata.district_name=district
        editdata.save()
        return redirect("Admin:District")
     else:
        return render(request,'Admin/District.html',{'editdata':editdata,'district':data})
def Category(request):
    data=tbl_category.objects.all()
    if request.method=="POST":
        category=request.POST.get("txt_category")
        tbl_category.objects.create(category_name=category)
        return render(request,'Admin/Category.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Category.html',{'category':data})
def delcategory(request,did):
    tbl_category.objects.get(id=did).delete()
    return redirect("Admin:Category")
def editcategory(request,eid):
    editdata=tbl_category.objects.get(id=eid)
    data=tbl_category.objects.all()
    if request.method=="POST":
        category=request.POST.get("txt_category")
        editdata.category_name=category
        editdata.save()
        return redirect('Admin:Category')
    else:
        return render(request,'Admin/Category.html',{'editdata':editdata,'category':data})
def Place(request):
    ddata=tbl_district.objects.all()
    pdata=tbl_place.objects.all()
    if request.method=="POST":
        place=request.POST.get("txt_place")
        district=tbl_district.objects.get(id=request.POST.get("sel_district"))
        tbl_place.objects.create(place_name=place, district=district)
        return render(request,'Admin/Place.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Place.html',{"district":ddata,'place':pdata})
def delplace(request,id):
    tbl_place.objects.get(id=id).delete()
    return redirect("Admin:Place")
def editplace(request,id):
    district=tbl_district.objects.all()
    place=tbl_place.objects.all()
    editdata=tbl_place.objects.get(id=id)
    if request.method=="POST":
        Place=request.POST.get("txt_place")
        editdata.district=tbl_district.objects.get(id=request.POST.get("sel_district"))
        editdata.place_name=Place
        editdata.save()
        return redirect("Admin:Place")
    else:
        return render(request,'Admin/Place.html',{'editdata':editdata,'district':district,'place':place})
def Subcategory(request):
    cdata=tbl_category.objects.all()
    sdata=tbl_subcategory.objects.all()
    if request.method=="POST":
        subcategory=request.POST.get("txt_subcategory")
        category=tbl_category.objects.get(id=request.POST.get("sel_category"))
        tbl_subcategory.objects.create(subcategory_name=subcategory, category=category)
        return render(request,'Admin/Subcategory.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Subcategory.html',{"category":cdata,'subcategory':sdata})
def delsub(request,id):
    tbl_subcategory.objects.get(id=id).delete()
    return redirect("Admin:Subcategory")
def editsub(request,id):
    category=tbl_category.objects.all()
    subcategory=tbl_subcategory.objects.all()
    editdata=tbl_subcategory.objects.get(id=id)
    if request.method=="POST":
        Subcategory=request.POST.get("txt_subcategory")
        editdata.category=tbl_category.objects.get(id=request.POST.get("sel_category"))
        editdata.subcategory_name=Subcategory
        editdata.save()
        return redirect("Admin:Subcategory")
    else:
        return render(request,'Admin/Subcategory.html',{'editdata':editdata,'category':category,'subcategory':subcategory})
def UserList(request):
    userdata=tbl_student.objects.all()
    return render(request,'Admin/UserList.html',{"users":userdata})
def CollegeList(request):
    collegedata=tbl_college.objects.all()
    return render(request,'Admin/CollegeList.html',{"colleges":collegedata})
def HomePage(request):
    Admin = tbl_admin.objects.get(id=request.session['aid'])
    return render(request,'Admin/HomePage.html')
def acceptcollege(request,aid):
    College=tbl_college.objects.get(id=aid)
    College.college_status=1
    College.save()
    return render(request,'Admin/CollegeList.html',{'msg':"Accepted"})
def rejectcollege(request,rid):
    College=tbl_college.objects.get(id=rid)
    College.college_status=2
    College.save()
    return render(request,'Admin/CollegeList.html',{'msg':"Rejected"})
def Department(request):
    data=tbl_department.objects.all()
    if request.method=="POST":
        department=request.POST.get("txt_department")
        tbl_department.objects.create(department_name=department)
        return render(request,'Admin/Department.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Department.html',{'department':data})
def deldepartment(request,did):
    tbl_department.objects.get(id=did).delete()
    return render(request,'Admin/Department.html',{'msg1':'deleted'})
def editdepartment(request,eid):
    department=tbl_department.objects.all()
    editdata=tbl_department.objects.get(id=eid)
    if request.method=="POST":
        Dname=request.POST.get("txt_department")
        editdata.department_name=Dname
        editdata.save()
        return render(request,'Admin/Department.html',{'msg2':'edited'})
    else:
        return render(request,'Admin/Department.html',{'editdata':editdata,'department':department})
def Semester(request):
    data=tbl_semester.objects.all()
    if request.method=="POST":
        semester=request.POST.get("txt_semester")
        tbl_semester.objects.create(semester_name=semester)
        return render(request,'Admin/Semester.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Semester.html',{'semester':data})
def delsemester(request,did):
    tbl_semester.objects.get(id=did).delete()
    return render(request,'Admin/Semester.html',{'msg1':'deleted'})
def editsemester(request,eid):
    semester=tbl_semester.objects.all()
    editdata=tbl_semester.objects.get(id=eid)
    if request.method=="POST":
        Sname=request.POST.get("txt_semester")
        editdata.semester_name=Sname
        editdata.save()
        return render(request,'Admin/Semester.html',{'msg2':'edited'})
    else:
        return render(request,'Admin/Semester.html',{'editdata':editdata,'semester':semester})
def Academicyear(request):
    data=tbl_academicyear.objects.all()
    if request.method=="POST":
        year=request.POST.get("txt_academicyear")
        tbl_academicyear.objects.create(academicyear_year=year)
        return render(request,'Admin/Academicyear.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Academicyear.html',{'year':data})
def delacademicyear(request,did):
    tbl_academicyear.objects.get(id=did).delete()
    return render(request,'Admin/Academicyear.html',{'msg1':'deleted'})
def editacademicyear(request,eid):
    year=tbl_academicyear.objects.all()
    editdata=tbl_academicyear.objects.get(id=eid)
    if request.method=="POST":
        Yname=request.POST.get("txt_academicyear")
        editdata.academicyear_year=Yname
        editdata.save()
        return render(request,'Admin/Academicyear.html',{'msg2':'edited'})
    else:
        return render(request,'Admin/Academicyear.html',{'editdata':editdata,'year':year})
def Course(request):
    ddata=tbl_department.objects.all()
    cdata=tbl_course.objects.all()
    if request.method=="POST":
        course=request.POST.get("txt_course")
        department=tbl_department.objects.get(id=request.POST.get("sel_department"))
        tbl_course.objects.create(course_name=course, department=department)
        return render(request,'Admin/Course.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Course.html',{"department":ddata,'course':cdata})
def delcourse(request,did):
    tbl_course.objects.get(id=did).delete()
    return render(request,'Admin/Course.html',{'msg':'data deleted'})
def editcourse(request,eid):
    department=tbl_department.objects.all()
    course=tbl_course.objects.all()
    editdata=tbl_course.objects.get(id=eid)
    if request.method=="POST":
        Course=request.POST.get("txt_course")
        editdata.department=tbl_department.objects.get(id=request.POST.get("sel_department"))
        editdata.course_name=Course
        editdata.save()
        return render(request,'Admin/Course.html',{'msg2':'edited'})
    else:
        return render(request,'Admin/Course.html',{'editdata':editdata,'department':department,'course':course})
def Subject(request):
    ddata=tbl_department.objects.all()
    cdata=tbl_course.objects.all()
    sdata=tbl_semester.objects.all()
    subdata=tbl_subject.objects.all()
    if request.method=="POST":
        subject=request.POST.get("txt_subject")
        course=tbl_course.objects.get(id=request.POST.get("sel_course"))
        semester=tbl_semester.objects.get(id=request.POST.get("sel_semester"))
        tbl_subject.objects.create(subject_name=subject,semester=semester,course=course)
        return render(request,'Admin/Subject.html',{'msg':'inserted'})
    else:
        return render(request,'Admin/Subject.html',{'department':ddata,'course':cdata,'semester':sdata,'subject':subdata})
def delsubject(request,did):
    tbl_subject.objects.get(id=did).delete()
    return render(request,'Admin/Subject.html',{'msg':'data deleted'})
def editsubject(request,eid):
    department=tbl_department.objects.all()
    course=tbl_course.objects.all()
    semester=tbl_semester.objects.all()
    subject=tbl_subject.objects.all()
    editdata=tbl_subject.objects.get(id=eid)
    if request.method=="POST":
        Subject=request.POST.get("txt_subject")
        editdata.department=tbl_department.objects.get(id=request.POST.get("sel_department"))
        editdata.course=tbl_course.objects.get(id=request.POST.get("sel_course"))
        editdata.semester=tbl_semester.objects.get(id=request.POST.get("sel_semester"))
        editdata.subject_name=Subject
        editdata.save()
        return render(request,'Admin/Subject.html',{'msg2':'edited'})
    else:
        return render(request,'Admin/Subject.html',{'editdata':editdata,'department':department,'course':course,'semester':semester,'subject':subject})
def AjaxCourse(request):
    departmentid = request.GET.get("did")
    course = tbl_course.objects.filter(department=departmentid)
    return render(request,"Admin/AjaxCourse.html",{'course':course})
