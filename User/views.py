from django.shortcuts import render,redirect
from Guest.models import *
from TurfOwner.models import *
from User.models import *
from datetime import date
from django.http import JsonResponse

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
    ar=[1,2,3,4,5]
    parry=[]
    avg=0

    district = tbl_district.objects.all()   # FIX 1

    Us=tbl_turf.objects.filter(turf_status=1)  # FIX 2

    for i in Us:
        tot=0
        ratecount=tbl_rating.objects.filter(truf=i.id).count()
        if ratecount>0:
            ratedata=tbl_rating.objects.filter(truf=i.id)
            for j in ratedata:
                tot=tot+j.rating_data
                avg=tot//ratecount
            parry.append(avg)
        else:
            parry.append(0)

    datas=zip(Us,parry)

    return render(request,'User/ViewTurf.html',{
        "turfs":datas,
        "ar":ar,
        "district":district   # FIX 1
    })

def ViewSlot(request,tid):
    turf = tbl_turf.objects.get(id=tid, turf_status=1)
    slots = tbl_slot.objects.filter(turf=turf)

    return render(request,"User/ViewSlot.html",{
        'turf': turf,
        'slots': slots
    })


def Ajaxturf(request):
    ar=[1,2,3,4,5]
    parry=[]
    avg=0

    placeid = request.GET.get('placeid')

    turf = tbl_turf.objects.filter(
        place=placeid,
        turf_status=1
    )

    for i in turf:
        tot=0
        ratecount=tbl_rating.objects.filter(truf=i.id).count()
        if ratecount>0:
            ratedata=tbl_rating.objects.filter(truf=i.id)
            for j in ratedata:
                tot=tot+j.rating_data
                avg=tot//ratecount
            parry.append(avg)
        else:
            parry.append(0)

    datas=zip(turf,parry)

    return render(request,"User/Ajaxturf.html",{
        'data':datas,
        'ar':ar
    })

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



def rating(request,mid):
    parray=[1,2,3,4,5]
    mid=mid
    # wdata=tbl_booking.objects.get(id=mid)
    
    counts=0
    counts=stardata=tbl_rating.objects.filter(truf=mid).count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.filter(truf=mid).order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        # print(avg)
        return render(request,"User/Rating.html",{'mid':mid,'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"User/Rating.html",{'mid':mid})

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    user_review=request.GET.get('user_review')
    pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(user=tbl_user.objects.get(id=request.session["uid"]),user_review=user_review,rating_data=rating_data,truf=tbl_turf.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(truf=pid).order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(truf=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(truf=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)



def Complaint(request):
    user=tbl_user.objects.get(id=request.session['uid'])
    if request.method=="POST":
        title=request.POST.get('txt_title')
        content=request.POST.get('txt_content')
        tbl_complaint.objects.create(user=user,complaint_title=title,complaint_content=content)
        return render(request,"User/Complaint.html",{'msg':'Complaint submitted successfully'})
    else:
        return render(request,"User/Complaint.html")
    

def Feedback(request):
    user=tbl_user.objects.get(id=request.session['uid'])
    if request.method=="POST":
        content=request.POST.get('txt_content')
        tbl_feedback.objects.create(user=user,feedback_content=content)
        return render(request,"User/Feedback.html",{'msg':'Feedback submitted successfully'})
    else:
        return render(request,"User/Feedback.html")