from django.shortcuts import render,redirect
from Guest.models import *
from Administrator.models import *
from TurfOwner.models import *


# Create your views here.
def index(request):
    return render(request,"Guest/index.html")
    
def UserRegistration(request):
    disData=tbl_district.objects.all()
    
    if request.method=="POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        password=request.POST.get('txt_password')
        contact=request.POST.get('txt_contact')
        dob=request.POST.get('txt_dob')
        photo=request.FILES.get('txt_photo')
       
        place = tbl_place.objects.get(id=request.POST.get('sel_place'))
        
        
        #insert qry
        tbl_user.objects.create(user_name=name,user_email=email,user_password=password,user_contact=contact,user_dob=dob,user_photo=photo,place=place)
        return render(request,"Guest/UserRegistration.html",)
    else:   
        return render(request,"Guest/UserRegistration.html",{'disData':disData})

def Ajaxplace(request):
    place=tbl_place.objects.filter(district=request.GET.get('disid'))
    return render(request,"Guest/Ajaxplace.html",{'data':place})


def Login(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")

        admincount = tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        usercount = tbl_user.objects.filter(user_email=email,user_password=password).count()
        ownercount = tbl_owner.objects.filter(owner_email=email,owner_password=password).count()


        if admincount > 0:
            admindata = tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session['aid'] = admindata.id
            return redirect("Administrator:HomePage")
        
        elif usercount > 0:
            userdata = tbl_user.objects.get(user_email=email,user_password=password)
            request.session['uid'] = userdata.id
            return redirect("User:HomePage")
        elif ownercount > 0:
            ownerdata = tbl_owner.objects.get(owner_email=email,owner_password=password)
            if ownerdata.owner_status == "0":
                return render(request,"Guest/Login.html",{'msg':"Account verification is in progress. Please wait for approval."})
            elif ownerdata.owner_status == "2":
                return render(request,"Guest/Login.html",{'msg':"Your account has been rejected. Please contact support for more information."})
            else:
                request.session['oid'] = ownerdata.id
                return redirect("TurfOwner:HomePage")
        
        else:
            return render(request,"Guest/Login.html",{'msg':"Invalid Email Or Passsword"})

            
    else:
        return render(request,"Guest/Login.html")


def TurfRegistration(request):
    data=tbl_sports.objects.all()
    disData=tbl_district.objects.all()
    if request.method=="POST":
        name=request.POST.get('txt_turfname')
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        address=request.POST.get('txt_address')
        photo=request.FILES.get('txt_photo')
        proof=request.FILES.get('txt_proof')
        sport=request.POST.get('sel_sport')
        capacity=request.POST.get('txt_capacity')
        password=request.POST.get('txt_password')
        place = tbl_place.objects.get(id=request.POST.get('sel_place'))

        tbl_turf.objects.create(turf_name=name,turf_email=email,turf_contact=contact,turf_address=address,turf_photo=photo,turf_proof=proof,turf_capacity=capacity,turf_password=password,place=place)
        return render(request,"Guest/TurfRegistration.html",)
    else:   
        return render(request,"Guest/TurfRegistration.html",{'data':data,'disData':disData})
    
def owner_registration(request):
    districtData=tbl_district.objects.all()
    if request.method == "POST":
        tbl_owner.objects.create(
            owner_name=request.POST.get("txt_ownername"),
            owner_email=request.POST.get("txt_email"),
            owner_phone=request.POST.get("txt_phone"),
            owner_address=request.POST.get("txt_address"),
            owner_password=request.POST.get("txt_password"),
            place=tbl_place.objects.get(id=request.POST.get("sel_place")),
            owner_photo=request.FILES.get("txt_photo"),
            owner_proof=request.FILES.get("txt_proof"),
        )
        return render(request, "Guest/OwnerRegistration.html", {"msg": "Registration Successful"})
    
    return render(request, "Guest/OwnerRegistration.html",{'districtData': districtData})



def Contact(request):
    return render(request, "Guest/Contact.html")
                