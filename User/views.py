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




def ConfirmBooking(request, sid):
    slot = tbl_slot.objects.get(id=sid)
    user = tbl_user.objects.get(id=request.session['uid'])

    if request.method == "POST":

        play_date = request.POST.get('txt_date')
        players = request.POST.get('txt_players')

        # Empty checks
        if not play_date:
            return render(request,"User/ConfirmBooking.html",{
                'slot':slot,
                'today':date.today(),
                'msg':'Please select play date'
            })

        if not players:
            return render(request,"User/ConfirmBooking.html",{
                'slot':slot,
                'today':date.today(),
                'msg':'Please enter number of players'
            })

        players = int(players)

        if players <= 0:
            return render(request,"User/ConfirmBooking.html",{
                'slot':slot,
                'today':date.today(),
                'msg':'Invalid player count'
            })

        # Convert to date object
        play_date_obj = date.fromisoformat(play_date)

        # Past date validation
        if play_date_obj < date.today():
            return render(request,"User/ConfirmBooking.html",{
                'slot':slot,
                'today':date.today(),
                'msg':'Cannot book past date'
            })

        # Capacity validation
        if players > slot.turf.turf_capacity:
            return render(request,"User/ConfirmBooking.html",{
                'slot':slot,
                'today':date.today(),
                'msg':'Player count exceeds turf capacity'
            })

        # Double booking validation
        if tbl_booking.objects.filter(
            slot=slot,
            booking_todate=play_date_obj
        ).exists():
            return render(request,"User/ConfirmBooking.html",{
                'slot':slot,
                'today':date.today(),
                'msg':'This slot is already booked for the selected date'
            })

        # Calculate total amount (per person pricing)
        total_amount = slot.slot_amount * players

        # Save booking
        tbl_booking.objects.create(
            user=user,
            slot=slot,
            booking_todate=play_date_obj,
            booking_players=players,
        )

        # Success message
        request.session['booking_msg'] = "Booking successful!"

        return redirect("User:MyBookings")

    return render(request,"User/ConfirmBooking.html",{
        'slot':slot,
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

from decimal import Decimal

def payment(request,bid):
    if 'uid' not in request.session:
        return redirect('Guest:login')

    booking = tbl_booking.objects.get(id=bid)

    # already paid
    if booking.booking_status == 4:
        return render(request,"User/Payment.html",{
            "msg":"Payment already completed"
        })

    # calculate total from players × slot amount
    total_amount = booking.booking_players * booking.slot.slot_amount

    # calculate 30% advance
    advance_amount = total_amount * Decimal('0.30')

    if request.method == "POST":

        # store only advance in booking_amount
        booking.booking_amount = advance_amount
        booking.booking_status = 4
        booking.save()

        return redirect("User:loader")

    return render(request,"User/Payment.html",{
        "booking":booking,
        "advance_amount":advance_amount,
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
