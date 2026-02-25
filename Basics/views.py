from django.shortcuts import render

# Create your views here.

def Sum(request):
    if request.method=="POST":
        n1 = int(request.POST.get("txtno1"))
        n2 = int(request.POST.get("txtno2"))
        result = n1 + n2

        return render(request,"Basics/Sum.html",{'result':result})
    else:   
        return render(request,"Basics/Sum.html")
def Calculator(request):
    if request.method=="POST":
        n1 = int(request.POST.get("txtno1"))
        n2 = int(request.POST.get("txtno2"))
        op = request.POST.get("btn_submit")
        if op == '+':
            result = n1 + n2
        if op == '-':
            result = n1 - n2
        if op == '/':
            result = n1 / n2
        if op == '*':
            result = n1 * n2
        return render(request,"Basics/Calculator.html",{'result':result})
    else:
        return render(request,"Basics/Calculator.html")