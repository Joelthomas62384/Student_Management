def UPDATE_STAFF(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        print(staff_id)
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        

        user = CustomUser.objects.get(id = staff_id)

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        staff = staff.objects.get(admin = staff_id)
        staff.address = address
        staff.gender = gender

        

        staff.save()
        messages.success(request,'Records Are Successfully Updated !')
        return redirect('view_staff')

    return render(request,'Hod/edit_staff.html')
