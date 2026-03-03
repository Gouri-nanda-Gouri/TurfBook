from django.shortcuts import render, redirect
from TurfOwner.models import *
from Guest.models import *
from Administrator.models import *
from User.models import *


# SPORTS ADD (Owner can manage sports master)
def Sports(request):
    if request.method == "POST":
        name = request.POST.get('txt_sportsname')
        tbl_sports.objects.create(sports_name=name)
        return render(request, "TurfOwner/Sports.html")
    else:
        return render(request, "TurfOwner/Sports.html")


# OWNER PROFILE
def MyProfile(request):
    OwnerData = tbl_owner.objects.get(id=request.session['oid'])
    return render(request, "TurfOwner/MyProfile.html", {'OwnerData': OwnerData})


# EDIT OWNER PROFILE
def EditProfile(request):
    OwnerData = tbl_owner.objects.get(id=request.session['oid'])
    if request.method == "POST":
        name = request.POST.get('txt_name')
        email = request.POST.get('txt_email')
        contact = request.POST.get('txt_contact')

        OwnerData.owner_name = name
        OwnerData.owner_email = email
        OwnerData.owner_phone = contact
        OwnerData.save()

        return render(request, "TurfOwner/EditProfile.html", {'msg': 'Profile Updated'})
    
    return render(request, "TurfOwner/EditProfile.html", {'OwnerData': OwnerData})


# CHANGE OWNER PASSWORD
def ChangePassword(request):
    OwnerData = tbl_owner.objects.get(id=request.session['oid'])
    
    if request.method == "POST":
        oldpassword = request.POST.get('txt_old')
        newpassword = request.POST.get('txt_new')
        retypepassword = request.POST.get('txt_retype')

        if OwnerData.owner_password == oldpassword:
            if newpassword == retypepassword:
                OwnerData.owner_password = newpassword
                OwnerData.save()
                return render(request, "TurfOwner/ChangePassword.html", {'msg': 'Password Updated'})
            else:
                return render(request, "TurfOwner/ChangePassword.html", {'msg': 'New passwords do not match'})
        else:
            return render(request, "TurfOwner/ChangePassword.html", {'msg': 'Invalid Old Password'})

    return render(request, "TurfOwner/ChangePassword.html", {'OwnerData': OwnerData})


# OWNER HOMEPAGE
def HomePage(request):
    return render(request, "TurfOwner/HomePage.html")

def AddTurf(request):
    owner=tbl_owner.objects.get(id=request.session['oid'])
    disData=tbl_district.objects.all()

    if request.method=="POST":
        tbl_turf.objects.create(
            owner=owner,
            turf_name=request.POST.get('txt_name'),
            turf_description=request.POST.get('txt_desc'),
            turf_capacity=request.POST.get('txt_capacity'),
            turf_contact_number=request.POST.get('txt_contact'),
            turf_image=request.FILES.get('txt_photo'),
            place=tbl_place.objects.get(id=request.POST.get('sel_place'))
        )
        return render(request,"TurfOwner/AddTurf.html",{'msg':"Turf Added Successfully"})
    else:
        return render(request,"TurfOwner/AddTurf.html",{'disData':disData})
    


    

def MyTurf(request):
    owner=tbl_owner.objects.get(id=request.session['oid'])
    turfdata=tbl_turf.objects.filter(owner=owner)
    return render(request,"TurfOwner/MyTurf.html",{'turfdata':turfdata})

def DeleteTurf(request,did):
    tbl_turf.objects.get(id=did).delete()
    return render(request,"TurfOwner/MyTurf.html",{'msg':"Turf Deleted Successfully"})

def AddGallery(request,tid):
    turf=tbl_turf.objects.get(id=tid)
    gallery=tbl_turf_gallery.objects.filter(turf=turf)

    if request.method=="POST":
        tbl_turf_gallery.objects.create(
            turf=turf,
            gallery_image=request.FILES.get('txt_photo')
        )
        return render(request,"TurfOwner/AddGallery.html",{'gallery':gallery,'msg':"Image Added Successfully",'tid':tid})
    return render(request,"TurfOwner/AddGallery.html",{'gallery':gallery})

def AddTurfSports(request,tid):
    turf=tbl_turf.objects.get(id=tid)
    sports=tbl_sports.objects.all()
    assigned=tbl_turf_sports.objects.filter(turf=turf)

    if request.method=="POST":
        tbl_turf_sports.objects.create(
            turf=turf,
            sport=tbl_sports.objects.get(id=request.POST.get('sel_sport'))
        )
        return render(request,"TurfOwner/AddTurfSports.html",{'msg':"Sports Added Successfully",'tid':tid})
    return render(request,"TurfOwner/AddTurfSports.html",{
        'sports':sports,
        'assigned':assigned
    })

def AddSlot(request,tid):
    turf = tbl_turf.objects.get(id=tid)
    slots = tbl_slot.objects.filter(turf=turf)

    if request.method == "POST":
        tbl_slot.objects.create(
            turf=turf,
            slot_start_time=request.POST.get('txt_start'),
            slot_end_time=request.POST.get('txt_end'),
            slot_amount=request.POST.get('txt_amount')
        )
        return render(request,"TurfOwner/AddSlot.html",{
            'slots':slots,
            'msg':"Slot Added Successfully",
            'tid':tid
        })

    return render(request,"TurfOwner/AddSlot.html",{
        'slots':slots,
        'tid':tid
    })


def ViewBookings(request):
    owner = tbl_owner.objects.get(id=request.session['oid'])

    bookings = tbl_booking.objects.filter(
        slot__turf__owner=owner
    ).order_by('-booking_date')

    return render(request,"TurfOwner/ViewBookings.html",{
        'bookings':bookings
    })
    

def RejectBooking(request,bid):
    booking = tbl_booking.objects.get(id=bid)
    booking.booking_status = 3
    booking.save()

    request.session['owner_msg'] = "Booking rejected"
    return redirect("TurfOwner:ViewBookings")


def ApproveBooking(request,bid):
    booking = tbl_booking.objects.get(id=bid)

    # Approve selected booking
    booking.booking_status = 1
    booking.save()

    # Reject other bookings for same slot & same play date
    tbl_booking.objects.filter(
        slot=booking.slot,
        booking_todate=booking.booking_todate,
        booking_status=0   # only pending ones
    ).exclude(id=booking.id).update(booking_status=3)

    request.session['owner_msg'] = "Booking approved. Other pending bookings auto-rejected."
    return redirect("TurfOwner:ViewBookings")
