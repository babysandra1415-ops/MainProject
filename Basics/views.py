from django.shortcuts import render

# Create your views here.
def Sum(request):
    if request.method=="POST":
        a=int(request.POST.get("txt_num1"))
        b=int(request.POST.get("txt_num2"))
        c=a+b
        return render(request,'Basics/Sum.html',{'Result':c})
    else:
        return render(request,'Basics/Sum.html')

def Calculator(request):
    if  request.method=="POST":
        a=int(request.POST.get("txt_num1"))
        b=int(request.POST.get("txt_num2"))
        btn=request.POST.get("btn_submit")
        if btn=="+":
            c=a+b
        elif btn=="-":
            c=a-b
        elif btn=="*":
            c=a*b
        elif btn=="/":
            c=a/b
        return render(request,'Basics/Calculator.html',{'Result':c})
    else:
         return render(request,'Basics/Calculator.html')

def Largest(request):
    if request.method=="POST":
        a=int(request.POST.get("txt_num1"))
        b=int(request.POST.get("txt_num2"))
        c=int(request.POST.get("txt_num3"))
        if a>=b:
            if a>=c:
                num=a
            else:
                num=c 
        else:
            if b>=c: 
                num=b
            else:
                num=c              
        return render(request,'Basics/Largest.html',{'Result':num})
    else:
        return render(request,'Basics/Largest.html')
