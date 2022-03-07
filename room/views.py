from contextlib import ContextDecorator
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import rooms
# Create your views here.


def home(request):
    return render(request, 'index.html')
@csrf_exempt
def clear_db(request):
    if request.method=='POST':
            rooms.objects.all().delete()
    return JsonResponse({"data":"database cleared"})

@csrf_exempt
def vacancy(request):
    if request.method == "POST":
        data = request.POST.get('send').split("*")
        
            # return JsonResponse({"data":"please enter time"})
        d1=data[0].split(":")
        d2=data[1].split(":")

        db=rooms.objects.all()

        arr=['C-Contact','S-Sharing','T-Team']
        for i in db.iterator():
            time=i.time.split("-")
            b1=time[0].split(":")
            b2=time[1].split(":")

            Sbasehh = int(b1[0])
            Sbasemm = int(b1[1])
            Ebasehh = int(b2[0])
            Ebasemm = int(b2[1])

            Scurrhh = int(d1[0])
            Scurrmm = int(d1[1])
            Ecurrhh = int(d2[0])
            Ecurrmm = int(d2[1])

            if Ebasehh > Scurrhh and Ebasehh <Ecurrhh:
                arr.remove(i.room)
            elif Ebasehh==Ebasehh:
                arr.remove(i.room)
         
    return JsonResponse({'data': arr})


@csrf_exempt
def book(request):
    if request.method == "POST":
        data = request.POST.get('send')

        timeDB = data.split("*")
        # edge case
        # if timeDB[0].split(":").isdigit()==False:
        #     return JsonResponse({"data":"please enter time"})

        if int(timeDB[2]) > 20:
            return JsonResponse({"data": "NO_VACANT_ROOM"})

        b1 = timeDB[0].split(":")
        b2 = timeDB[1].split(":")
        if int(b1[0]) > int(b2[0]):
            return JsonResponse({"data": "time is incorrect"})
        if int(b1[0]) == int(b2[0]) and int(b1[1]) > int(b2[1]):
            return JsonResponse({"data": "time is incorrect"})

            # modulo by 15
        part = timeDB[0].split(":")
        if int(part[1]) % 15 != 0:
            return JsonResponse({"data": "Time is Incorrect m"})
        part = timeDB[1].split(":")
        if int(part[1]) % 15 != 0:
            return JsonResponse({"data": "Time is Incorrect mo"})

        # buffer time
        if int(b1[0]) < 9:
            if int(b2[0]) >= 9 and int(b2[1]) >= 15:
                return JsonResponse({"data": "NO_VACANT_ROOM"})
        elif int(b1[0]) == 9 and int(b1[1]) < 15:
            if int(b2[0]) >= 9 and int(b2[1]) >= 15:
                return JsonResponse({"data": "NO_VACANT_ROOM"})

        if int(b1[0]) < 13:
            if int(b2[0]) >= 13 and int(b2[1]) >= 15:
                return JsonResponse({"data": "NO_VACANT_ROOM"})
        elif int(b1[0]) == 13:
            if int(b2[0]) >= 13 and int(b2[1]) >= 45:
                return JsonResponse({"data": "NO_VACANT_ROOM"})

        if int(b1[0]) < 18:
            if int(b2[0]) >= 19:
                return JsonResponse({"data": "NO_VACANT_ROOM"})
        elif int(b1[0]) == 18:
            if int(b2[0]) >= 19:
                return JsonResponse({"data": "NO_VACANT_ROOM"})

        # check in database
        room_name = ""
        if int(timeDB[2]) <= 3:
            room_name = "C-Contact"
        elif int(timeDB[2]) <= 7:
            room_name = "S-Sharing"
        elif int(timeDB[2]) <= 20:
            room_name = "T-Team"

        db = rooms.objects.filter(room=room_name)
        if len(db)==0:
            user = rooms.objects.create(time=b1[0]+":"+b1[1]+"-"+b2[0]+":"+b2[1], room=room_name)
            user.save()
            return JsonResponse({"data": 'Slot Booked'})

        
        for t in db.iterator():
            time = t.time.split("-")
            # print(time)
            d1 = time[0].split(":")
            d2 = time[1].split(":")
            Sbasehh = int(b1[0])
            Sbasemm = int(b1[1])
            Ebasehh = int(b2[0])
            Ebasemm = int(b2[1])

            Scurrhh = int(d1[0])
            Scurrmm = int(d1[1])
            Ecurrhh = int(d2[0])
            Ecurrmm = int(d2[1])
            if Sbasehh > Ecurrhh or Ebasehh < Scurrhh:
                user = rooms.objects.create(time=Scurrhh+":"+Scurrmm+"-"+Ecurrhh+":"+Ecurrmm, room=room_name)
                user.save()
                return JsonResponse({"data": 'Slot Booked'})
            elif Sbasehh == Ecurrhh:
                if Sbasemm >= Ecurrmm:
                    user = rooms.objects.create(time=Scurrhh+":"+Scurrmm+"-"+Ecurrhh+":"+Ecurrmm, room=room_name)
                    user.save()
                    return JsonResponse({"data": 'saved'})
            elif Ebasehh == Scurrhh:
                if Ebasemm <= Scurrmm:
                    user = rooms.objects.create(time=Scurrhh+":"+Scurrmm+"-"+Ecurrhh+":"+Ecurrmm, room=room_name)
                    user.save()
                    return JsonResponse({"data": 'saved'})
            else:
                return JsonResponse({"data": "NO_VACANT_ROOM"})

    return JsonResponse({'data': "s"})
