from django.shortcuts import render
from Admin.models import *
from Guest.models import *

# Create your views here.
def MyProfile(request):
    userdata=tbl_user.objects.get(id=request.session["uid"])
    return render(request,'User/MyProfile.html',{"userdata": userdata})
  
def EditProfile(request):
    userdata=tbl_user.objects.get(id=request.session["uid"])
    if request.method == "POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        address=request.POST.get('txt_address')
        userdata.user_name=name
        userdata.user_email=email
        userdata.user_contact=contact
        userdata.user_address=address
        userdata.save()

        return render(request,'User/EditProfile.html',{'msg':'updated'})
    else:
        return render(request,'User/EditProfile.html',{"userdata":userdata})

def ChangePassword(request):
    userdata=tbl_user.objects.get(id=request.session["uid"])
    userpassword=userdata.user_password

    if request.method == "POST":
        oldpassword=request.POST.get('txt_opassword')
        newpassword=request.POST.get('txt_npassword')
        retype=request.POST.get('txt_cpassword')
        if userpassword==oldpassword:
            if newpassword==retype:
                userdata.user_password=newpassword
                userdata.save()
                return render(request,'College/ChangePassword.html',{"msg":"Password Updated"})
            else:
                return render(request,'College/ChangePassword.html',{"msg1":"Password Mismatch"})
        else:
            return render(request,'College/ChangePassword.html',{"msg2":"Password Incorrect"})
    else:
        return render(request,'College/ChangePassword.html')

def HomePage(request):
    User = tbl_user.objects.get(id=request.session['uid'])
    return render(request,'User/HomePage.html')

def Complaint(request):
    return render(request,'User/Complaint.html')