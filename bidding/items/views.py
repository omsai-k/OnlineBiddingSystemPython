from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Item
from django.core.mail import send_mail
from datetime import datetime

@login_required(login_url='login')
def additem(request):
    if request.method == 'POST':
        iname = request.POST['iname']
        prof = request.FILES['img']
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        img3 = request.FILES.get('img3')
        img4 = request.FILES.get('img4')
        itag = request.POST['itag']
        sdisc = request.POST['sdis']
        ldisc = request.POST['ldis']
        price = request.POST['iprice']
        sdate = request.POST['s_date']
        end_time = request.POST['end_time'] 
        omail = request.user.email

        start_date = datetime.strptime(sdate, '%Y-%m-%d')
        end_datetime = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

        if end_datetime <= start_date:
            messages.error(request, "End time must be later than the start date.")
            return redirect('additem')

        item = Item(
            ownermail=omail,
            start_date=start_date,
            currentPrice=price,
            img1=img1,
            img2=img2,
            img3=img3,
            img4=img4,
            name=iname,
            profile=prof,
            tag=itag,
            short_description=sdisc,
            long_description=ldisc,
            basePrice=price,
            end_time=end_datetime
        )
        item.save()
        return redirect("home")
    else:
        return render(request, 'additem.html')


@login_required(login_url='login')
def biditem(request):
    id = request.GET['id']
    item = Item.objects.get(id=id)
    lstatus = "live"
    
    if item.status == lstatus and datetime.now() < item.end_time:
        return render(request, "biditem.html", {'item': item})
    else:
        if datetime.now() >= item.end_time and item.status == "live":
            item.status = "sold"
            item.save()
            winner = User.objects.get(id=item.highest_bidder)
            subject = f"Item Sold: {item.name}"
            msg = f"Congratulations! Your item {item.name} has been sold to {winner.username} at {item.currentPrice} INR."
            send_mail(subject, msg, "bidmafia007@gmail.com", [item.ownermail])
            return redirect("home")
        else:
            return redirect("home")


@login_required(login_url='login')
def validate(request):
    value = request.GET.get('bidrs')
    iid = request.GET.get('iid')
    bidder = request.user
    bidderEmail = bidder.email
    item_obj = Item.objects.get(id=iid)
    
    itemownerEmail = item_obj.ownermail
    
    if bidderEmail == itemownerEmail:
        return render(request, "notification.html")
    else:
        if datetime.now() < item_obj.end_time:
            mail = item_obj.ownermail
            subject = "Online Bidding"  
            msg = f"Congratulations! Your item is bidded by {bidder.email}, By INR rs = {value}. Contact your buyer by email. Thank you for using our app."
            to = mail  
            res = send_mail(subject, msg, "bidmafia007@gmail.com", [to])

            Item.objects.filter(id=iid).update(currentPrice=value)
            Item.objects.filter(id=iid).update(highest_bidder=bidder.id)
            return redirect("home")
        else:
            messages.error(request, "The auction has ended for this item.")
            return redirect("home")
