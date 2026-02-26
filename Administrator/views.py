from django.shortcuts import render,redirect
from Administrator.models import *
from Guest.models import *
from TurfOwner.models import *
from User.models import *

# Create your views here.

def District(request):
    data=tbl_district.objects.all()
    if request.method=="POST":
        name=request.POST.get('txt_Dis')
        
        #insert qry
        tbl_district.objects.create(district_name=name)
        return render(request,"Administrator/District.html",{'dis':data})
    else:   
        return render(request,"Administrator/District.html",{'dis':data})
    

def DeleteDistrict(request,did):
    tbl_district.objects.get(id=did).delete()
    return redirect("Administrator:District")

def UpdateDistrict(request,did):
    districtOne=tbl_district.objects.get(id=did)
    if request.method=="POST":
        districtOne.district_name=request.POST.get("txt_Dis")
        districtOne.save()
        return redirect("Administrator:District")
    else:
        return render(request,"Administrator/District.html",{"districtOne":districtOne})
        

def AdminRegistration(request):
    data=tbl_admin.objects.all()
    if request.method=="POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        password=request.POST.get('txt_pass')
        tbl_admin.objects.create(admin_name=name,admin_email=email,admin_password=password)
        return render(request,"Administrator/AdminRegistration.html",{'adm':data})
    else:   
        return render(request,"Administrator/AdminRegistration.html",{'adm':data})
    
def DeleteAdminRegistration(request,aid):
    tbl_admin.objects.get(id=aid).delete()
    return redirect("Administrator:AdminRegistration")   

def UpdateAdminRegistration(request,aid):
    AdminRegistrationOne=tbl_admin.objects.get(id=aid)
    if request.method=="POST":
        AdminRegistrationOne.admin_name=request.POST.get("txt_name")
        AdminRegistrationOne.admin_email=request.POST.get("txt_email")
        AdminRegistrationOne.admin_password=request.POST.get("txt_pass")
        AdminRegistrationOne.save()
        return redirect("Administrator:AdminRegistration")
    else:
        return render(request,"Administrator/AdminRegistration.html",{"AdminRegistrationOne":AdminRegistrationOne})  
    
def Category(request):
    data=tbl_category.objects.all()
    if request.method=="POST":
        name=request.POST.get('txt_cat')
        
        tbl_category.objects.create(category_name=name)
        return render(request,"Administrator/Category.html",{'cat':data})
    else:   
        return render(request,"Administrator/Category.html",{'cat':data})

def DeleteCategory(request,cid):
    tbl_category.objects.get(id=cid).delete()
    return redirect("Administrator:Category")  

def UpdateCategory(request,cid):
    categoryOne=tbl_category.objects.get(id=cid)
    if request.method=="POST":
        categoryOne.category_name=request.POST.get("txt_cat")
        categoryOne.save()
        return redirect("Administrator:Category")
    else:
        return render(request,"Administrator/Category.html",{"categoryOne":categoryOne})  
    


def Place(request):
    disData=tbl_district.objects.all()
    data=tbl_place.objects.all()

    if request.method=="POST":
        placeName=request.POST.get('txt_place')
        district = tbl_district.objects.get(id=request.POST.get('sel_district'))
        
        #insert qry
        tbl_place.objects.create(place_name=placeName,district=district)
        return render(request,"Administrator/Place.html",{'disData':disData,"placeData":data})
    else:   
        return render(request,"Administrator/Place.html",{'disData':disData,"placeData":data})  
    
def DeletePlace(request,pid):
    tbl_place.objects.get(id=pid).delete()
    return redirect("Administrator:Place")  
    
def editplace(request,eid):
    disData=tbl_district.objects.all()

    editdata=tbl_place.objects.get(id=eid)
    if request.method=="POST":
        placeName=request.POST.get('txt_place')
        district = tbl_district.objects.get(id=request.POST.get('sel_district'))
        editdata.place_name=placeName
        editdata.district=district
        editdata.save()
        return render(request,"Administrator/Place.html",{'msg':"Inserted"})
    else:
        return render(request,'Administrator/Place.html',{'editdata':editdata,'disData':disData})
    
def UserRegistration(request):
     return render(request,"Administrator/UserRegistration.html"),

def HomePage(request):
    return render(request,"Administrator/HomePage.html",)

def UserList(request):
    data=tbl_user.objects.all()
    return render(request,"Administrator/UserList.html",{'UserData':data})

def UserAccept(request,uid):
    user=tbl_user.objects.get(id=uid)
    user.userregistration_status=1
    user.save()
    return redirect("Administrator:UserList")

def UserReject(request,uid):
    user=tbl_user.objects.get(id=uid)
    user.userregistration_status=2
    user.save()
    return redirect("Administrator:UserList")


def OwnerVerification(request):
    pendingOwners=tbl_owner.objects.filter(owner_status=0)
    approvedOwners=tbl_owner.objects.filter(owner_status=1)
    rejectedOwners=tbl_owner.objects.filter(owner_status=2)

    return render(request,"Administrator/OwnerVerification.html",{
        'pendingOwners':pendingOwners,
        'approvedOwners':approvedOwners,
        'rejectedOwners':rejectedOwners,
    })

def ApproveOwner(request,aid):
    owner=tbl_owner.objects.get(id=aid)
    owner.owner_status=1
    owner.save()
    return redirect("Administrator:OwnerVerification")

def RejectOwner(request,rid):
    owner=tbl_owner.objects.get(id=rid)
    owner.owner_status=2
    owner.save()
    return redirect("Administrator:OwnerVerification")

def TurfVerification(request):
    pendingTurf=tbl_turf.objects.filter(turf_status=0)
    approvedTurf=tbl_turf.objects.filter(turf_status=1)
    rejectedTurf=tbl_turf.objects.filter(turf_status=2)

    return render(request,"Administrator/TurfVerification.html",{
        'pendingTurf':pendingTurf,
        'approvedTurf':approvedTurf,
        'rejectedTurf':rejectedTurf
    })


def ApproveTurf(request,aid):
    turf=tbl_turf.objects.get(id=aid)
    turf.turf_status=1
    turf.save()
    return redirect("Administrator:TurfVerification")



def RejectTurf(request,rid):
    turf=tbl_turf.objects.get(id=rid)
    turf.turf_status=2
    turf.save()
    return redirect("Administrator:TurfVerification")


def Sports(request):
    sports=tbl_sports.objects.all()
    if request.method=="POST":
        sportName=request.POST.get('txt_sport')
        required_players = request.POST.get('txt_players')
        tbl_sports.objects.create(sports_name=sportName, required_players=required_players)
        return render(request,"Administrator/Sports.html",{'sports':sports,'msg':"Sport Added Successfully"})
    return render(request,"Administrator/Sports.html",{'sports':sports})

def DeleteSports(request,sid):
    tbl_sports.objects.get(id=sid).delete()
    return render(request,"Administrator/Sports.html",{'msg':"Sport Deleted Successfully"})

def UpdateSports(request,uid):
    sportsOne=tbl_sports.objects.get(id=uid)
    if request.method=="POST":
        sportsOne.sports_name=request.POST.get("txt_sport")
        sportsOne.required_players = request.POST.get("txt_players")
        sportsOne.save()
        return render(request,"Administrator/Sports.html",{'msg':"Sport Updated Successfully"})

    else:
        return render(request,"Administrator/Sports.html",{"sportsOne":sportsOne})
    

def ViewRequests(request):
    requests = tbl_request.objects.all().order_by('-created_date')
    return render(request, "Administrator/ViewRequests.html", {"requests": requests})


def ViewBookings(request):
    bookings = tbl_booking.objects.all().order_by('-booking_date')
    return render(request, "Administrator/ViewBookings.html", {"bookings": bookings})