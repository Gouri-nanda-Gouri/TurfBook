from django.shortcuts import render,redirect
from Guest.models import *
from TurfOwner.models import *
from User.models import *
from datetime import date

# Create your views here.

def HomePage(request):
    
    return render(request,"User/HomePage.html",)

def MyProfile(request):
    UserData=tbl_user.objects.get(id=request.session['uid'] )
    return render(request,"User/MyProfile.html",{'UserData':UserData})

def EditProfile(request):
    UserData=tbl_user.objects.get(id=request.session['uid'] )
    if request.method=="POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_email')
        contact=request.POST.get('txt_contact')
        UserData.userregistration_name=name
        UserData.userregistration_email=email
        UserData.userregistration_contact=contact
        UserData.save()
        return render(request,"User/EditProfile.html",{'msg':'updated'}) 
    return render(request,"User/EditProfile.html",{'UserData':UserData})

def ChangePassword(request):

    UserData=tbl_user.objects.get(id=request.session['uid'] )
    if request.method=="POST":
        oldpassword=request.POST.get('txt_old') 
        newpassword=request.POST.get('txt_new')
        retypepassword=request.POST.get('txt_retype')
        if UserData.userregistration_password == oldpassword:
            if newpassword == retypepassword:
                UserData.userregistration_password=newpassword
                UserData.save()
                return render(request,"User/ChangePassword.html",{'msg':'updated'}) 
            else:
                return render(request,"User/ChangePassword.html",{'msg':'New Password and Retype Password are not matching'})
        else:
            return render(request,"User/ChangePassword.html",{'msg':'Invalid Old Password'})
    return render(request,"User/ChangePassword.html",{'UserData':UserData})





def ViewTurf(request):
    district=tbl_district.objects.all() 
    trufData=tbl_turf.objects.filter(turf_status=1)
    return render(request,"User/ViewTurf.html",{'district':district,'turfs':trufData})

def ViewSlot(request,tid):
    turf = tbl_turf.objects.get(id=tid, turf_status=1)
    slots = tbl_slot.objects.filter(turf=turf)

    return render(request,"User/ViewSlot.html",{
        'turf': turf,
        'slots': slots
    })


def Ajaxturf(request):
    placeid = request.GET.get('placeid')
    turf = tbl_turf.objects.filter(
        place=placeid,
        turf_status=1
    )

    return render(request,"User/Ajaxturf.html",{'data':turf})

# def BookSlot(request,sid):
#     slot = tbl_slot.objects.get(id=sid)
#     user = tbl_user.objects.get(id=request.session['uid'])

#     if request.method == "POST":
#         play_date = request.POST.get('txt_date')

#         # empty check
#         if not play_date:
#             return render(request,"User/ConfirmBooking.html",{
#                 'slot':slot,
#                 'today':date.today(),
#                 'msg':'Please select play date'
#             })

#         # past date check
#         if play_date < str(date.today()):
#             return render(request,"User/ConfirmBooking.html",{
#                 'slot':slot,
#                 'today':date.today(),
#                 'msg':'Cannot book past date'
#             })

#         # double booking check
#         if tbl_booking.objects.filter(
#             slot=slot,
#             booking_todate=play_date,
#             booking_status=1
#         ).exists():
#             return render(request,"User/ConfirmBooking.html",{
#                 'slot':slot,
#                 'today':date.today(),
#                 'msg':'This slot is already booked for the selected date'
#             })

#         # save booking
#         tbl_booking.objects.create(
#             user=user,
#             slot=slot,
#             booking_todate=play_date,
#             booking_amount=slot.slot_amount
#         )

#         return render(request,"User/ConfirmBooking.html",{
#             'slot':slot,
#             'today':date.today(),
#             'msg':'Booking successful!'
#         })

#     return render(request,"User/ConfirmBooking.html",{
#         'slot':slot,
#         'today':date.today()
#     })



from datetime import date
from decimal import Decimal
from datetime import date
from decimal import Decimal

def ConfirmBooking(request, sid):
    slot = tbl_slot.objects.get(id=sid)
    user = tbl_user.objects.get(id=request.session['uid'])
    sports = tbl_sports.objects.all()

    if request.method == "POST":

        play_date = request.POST.get('txt_date')
        sport_id = request.POST.get('sel_sport')

        # validations
        if not play_date:
            return render(request,"User/ConfirmBooking.html",{
                'slot':slot,'sports':sports,'today':date.today(),
                'msg':'Please select play date'
            })

        if not sport_id:
            return render(request,"User/ConfirmBooking.html",{
                'slot':slot,'sports':sports,'today':date.today(),
                'msg':'Please select sport'
            })

        play_date_obj = date.fromisoformat(play_date)

        if play_date_obj < date.today():
            return render(request,"User/ConfirmBooking.html",{
                'slot':slot,'sports':sports,'today':date.today(),
                'msg':'Cannot book past date'
            })

        # prevent duplicate booking
        if tbl_booking.objects.filter(
            slot=slot,
            booking_todate=play_date_obj
        ).exists():
            return render(request,"User/ConfirmBooking.html",{
                'slot':slot,'sports':sports,'today':date.today(),
                'msg':'This slot is already booked for the selected date'
            })

        sport = tbl_sports.objects.get(id=sport_id)

        # slot amount = total amount
        total_amount = slot.slot_amount

        # save booking
        tbl_booking.objects.create(
            user=user,
            slot=slot,
            sport=sport,
            booking_todate=play_date_obj,
            total_amount=total_amount,
            booking_amount=total_amount
        )

        request.session['booking_msg'] = "Booking successful!"

        return redirect("User:MyBookings")

    return render(request,"User/ConfirmBooking.html",{
        'slot':slot,
        'sports':sports,
        'today':date.today()
    })

def MyBookings(request):
    user = tbl_user.objects.get(id=request.session['uid'])
    bookings = tbl_booking.objects.filter(user=user).order_by('-booking_date')

    msg = request.session.pop('booking_msg', None)

    return render(request,"User/MyBookings.html",{
        'bookings':bookings,
        'msg':msg
    })


def CancelBooking(request,bid):
    booking = tbl_booking.objects.get(id=bid)
    booking.booking_status = 2
    booking.save()

    # store alert in session
    request.session['booking_msg'] = "Booking cancelled successfully"

    return redirect("User:MyBookings")
from django.db.models import Sum
from decimal import Decimal

def payment(request,bid):
    if 'uid' not in request.session:
        return redirect('Guest:login')

    booking = tbl_booking.objects.get(id=bid)

    if booking.booking_status == 4:
        return render(request,"User/Payment.html",{
            "msg":"Payment already completed"
        })

    # calculate using required players
    total_amount = booking.slot.slot_amount * booking.sport.required_players

    if request.method == "POST":

        booking.booking_amount = total_amount
        booking.total_amount = total_amount
        booking.booking_status = 4
        booking.save()

        return redirect("User:loader")

    return render(request,"User/Payment.html",{
        "booking":booking,
        "total_amount":total_amount
    })

def loader(request):
    if 'uid' not in request.session:
        return redirect('Guest:login')
    return render(request,"User/Loader.html")

def paymentsuc(request):
    if 'uid' not in request.session:
        return redirect('Guest:login')
    return render(request,"User/Paymentsuc.html")

def AddRequest(request, bid):
    booking = tbl_booking.objects.get(id=bid)

    if request.method == "POST":
        players = request.POST.get("players")
        description = request.POST.get("description")

        tbl_request.objects.create(
            booking=booking,
            user=tbl_user.objects.get(id=request.session['uid']),
            slot=booking.slot,
            sport=booking.sport,
            request_players=players,
            request_description=description,
        )
        return redirect("User:ViewRequest")

    return render(request, "User/AddRequest.html", {"booking": booking})

def ViewRequest(request):
    requests = tbl_request.objects.all().order_by('-created_date')
    return render(request, "User/ViewRequest.html", {"requests": requests})


def JoinRequest(request, rid):
    req = tbl_request.objects.get(id=rid)
    user = tbl_user.objects.get(id=request.session['uid'])

    # prevent duplicate join
    if tbl_request_join.objects.filter(request=req, user=user).exists():
        return redirect("User:ViewRequest")

    # increase joined count
    req.joined_players += 1

    # close if full
    if req.joined_players >= req.request_players:
        req.request_status = 1

    req.save()

    # store join record
    tbl_request_join.objects.create(
        request=req,
        user=user
    )

    return redirect("User:ViewRequest")