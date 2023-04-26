
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from app.models import Course,Session_Year
from app.models import *
from django.contrib import messages




@login_required(login_url='/')
def HOME(request):
    if request.user.user_type != "1":
        messages.error(request,"No Permission to go there")
        return redirect('logout')
        
    else:
        context = {
            'student':Student.objects.all().count(),
            'staff':Staff.objects.all().count(),
            'course':Course.objects.all().count(),
            'subject':Subject.objects.all().count(),
            'male_student':Student.objects.filter(gender="Male").count(),
            'Female_student':Student.objects.filter(gender="Female").count()
        }
        return render(request,'Hod/home.html',context) 
        

@login_required(login_url='/')
def ADD_STUDENT(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        course = Course.objects.all()
        session_year = Session_Year.objects.all()

        if request.method == "POST":
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_year_id')

            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request,'Email Is Already Taken')
                return redirect('add_student')
            if CustomUser.objects.filter(username=username).exists():
                messages.warning(request,'Username Is Already Taken')
                return redirect('add_student')
            else:
                user = CustomUser(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    profile_pic = profile_pic,
                    user_type = 3
                )
                user.set_password(password)
                user.save()

                course = Course.objects.get(id=course_id)
                session_year = Session_Year.objects.get(id=session_year_id)

                student = Student(
                    admin = user,
                    address = address,
                    session_year_id = session_year,
                    course_id = course,
                    gender = gender,
                )
                student.save()
                messages.success(request, user.first_name + "  " + user.last_name + " is Successfully Added !")
                return redirect('view_student')



        context = {
            'course':course,
            'session_year':session_year,
        }

        return render(request,'Hod/add_student.html',context)



@login_required(login_url='/')
def VIEW_STUDENT(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        students = Student.objects.all()
        context = {
            "students" : students
        }
        return render(request,'Hod/view_student.html',context)

@login_required(login_url='/')
def EDIT_STUDENT(request,id):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        student = Student.objects.filter(id = id)
        course = Course.objects.all()
        session_year = Session_Year.objects.all()

        context = {
            'student':student,
            'course':course,
            'session_year':session_year,
        }
        return render(request,'Hod/edit_student.html',context)


@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        if request.method == "POST":
            student_id = request.POST.get('student_id')
            print(student_id)
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            course_id = request.POST.get('course_id')
            session_year_id = request.POST.get('session_year_id')

            user = CustomUser.objects.get(id = student_id)

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username

            if password != None and password != "":
                user.set_password(password)
            if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic
            user.save()

            student = Student.objects.get(admin = student_id)
            student.address = address
            student.gender = gender

            course = Course.objects.get(id = course_id)
            student.course_id = course

            session_year = Session_Year.objects.get(id = session_year_id)
            student.session_year_id = session_year

            student.save()
            messages.success(request,'Record Are Successfully Updated !')
            return redirect('view_student')

        return render(request,'Hod/edit_student.html')

@login_required(login_url='/')
def DELETE_STUDENT(request,admin):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        student = CustomUser.objects.get(id = admin)
        student.delete()
        messages.error(request,'Deleted Successfully !')
        return redirect('view_student')
	
@login_required(login_url='/')
def ADD_COURSE(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        if request.method == "POST":
            course_name = request.POST.get('course_name')

            course = Course(
                name = course_name,
            )
            course.save()
            messages.success(request,'Course Added Successfully')

            return redirect('view_course')

        return render(request,'Hod/add_course.html')


@login_required(login_url='/')
def VIEW_COURSE(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        course = Course.objects.all()
        context = {
            'course':course,
        }
        return render(request,'Hod/view_course.html',context)

@login_required(login_url='/')
def EDIT_COURSE(request,id):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        course = Course.objects.filter(id = id)
        context = {
            'course':course
        }
        return render(request,'Hod/edit_course.html',context)

@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        if request.method == "POST":
            name = request.POST.get('name')
            course_id = request.POST.get('course_id')

            course = Course.objects.get(id=course_id)
            course.name = name
            course.save()

            messages.success(request, "The Course has been updated successfully")

            return redirect('view_course')
        return render(request, 'Hod/edit_course.html')
@login_required(login_url='/')
def DELETE_COURSE(request,id):
    
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        course = Course.objects.get(id = id)
        course.delete()
        messages.error(request,"The Course has been deleted")
        return redirect('view_course')


@login_required(login_url='/')
def ADD_STAFF(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        if request.method == "POST":
            profile_pic = request.FILES.get('profile_pic')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            address = request.POST.get('address')
            gender = request.POST.get('gender')

            if CustomUser.objects.filter(email=email).exists():
                messages.warning(request, "This Email has been taken Already")
                return redirect('add_staff')
            elif CustomUser.objects.filter(username=username).exists():
                messages.warning(request, "This Username has been taken Already")
                return redirect('add_staff')
            else:
                user = CustomUser(first_name=first_name, last_name=last_name, email=email, username=username, profile_pic=profile_pic, user_type=2)
                user.set_password(password)
                user.save()

                staff = Staff(admin=user, address=address, gender=gender)
                staff.save()
                messages.success(request, 'Staff has been added successfully')
                return redirect('view_staff')
        return render(request, 'Hod/add_staff.html')

@login_required(login_url='/')
def VIEW_STAFF(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")

        return redirect("logout")
    else:
        context = {
            'staff':Staff.objects.all()
        }
        return render(request,'Hod/view_staff.html',context)


@login_required(login_url='/')
def EDIT_STAFF(request,id):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")

        return redirect("logout")
    else:
        staff = Staff.objects.filter(id=id)
        context = {
            'staff': staff
        }
        return render(request,'Hod/edit_staff.html',context)


@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
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

            staff = Staff.objects.get(admin = staff_id)
            staff.address = address
            staff.gender = gender

            

            staff.save()
            messages.success(request,'Records Are Successfully Updated !')
            return redirect('view_staff')

        return render(request,'Hod/edit_staff.html')


@login_required(login_url='/')
def DELETE_STAFF(request,admin):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        print(admin)
        staff = CustomUser.objects.get(id=admin)
        staff.delete()
        messages.success(request,'Staff has been removed successfully')
        return redirect('view_staff')


@login_required(login_url='/')
def ADD_SUBJECT(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        if request.method =="POST":
            name = request.POST.get('name')
            course = request.POST.get('course_id')
            staff = request.POST.get('staff_id')

            course = Course.objects.get(id=course)
            staff = Staff.objects.get(id=staff)

            subject = Subject(
                name = name,
                course = course,
                staff = staff
                
            )
            subject.save()
            messages.success(request,"The Subject is added")
            redirect('view_subject')


        context = {
            'course':Course.objects.all(),
            'staff':Staff.objects.all()
        }
        return render(request,'Hod/add_subject.html',context)

@login_required(login_url='/')
def VIEW_SUBJECT(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        subject = Subject.objects.all()
        context = {
            'subject':subject
        }
        return render(request,'Hod/view_subject.html',context)

@login_required(login_url='/')
def EDIT_SUBJECT(request,id):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        subject = Subject.objects.filter(id=id)
        course = Course.objects.all()
        staff = Staff.objects.all()

        context = {
            'subject':subject,
            'course':course,
            'staff':staff
        }
        
        print(staff)
        

        return render(request,'Hod/edit_subject.html',context)

@login_required(login_url='/')
def UPDATE_SUBJECT(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        if request.method == "POST":
            id = request.POST.get('id')
            name = request.POST.get('name')
            course = request.POST.get('course_id')
            staff = request.POST.get('staff_id')
            course_id = Course.objects.get(id=course)
            staff_id = Staff.objects.get(id=staff)

            Subject.objects.filter(id=id).update(
                name=name,
                course=course_id,
                staff=staff_id
            )
            messages.success(request, 'The Subject is Updated Successfully')
            return redirect('view_subject')

@login_required(login_url='/')

def DELETE_SUBJECT(request,id):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        subject = Subject.objects.get(id = id)
        subject.delete()
        messages.success(request,"The Subject has been deleted successfully")
        return redirect('view_subject')



@login_required(login_url='/')

def ADD_SESSION(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        if request.method =="POST":
            session_year_start = request.POST.get('session_year_start')
            session_year_end = request.POST.get('session_year_end')

            session = Session_Year(
                session_start =session_year_start,
                session_end = session_year_end

            )
            session.save()
            messages.success(request,"The Session has been added successfully")
            return redirect('view_session')


        return render(request,'Hod/add_session.html')

@login_required(login_url='/')

def VIEW_SESSION(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        context = {
            'session':Session_Year.objects.all()
        }
        return render(request,'Hod/view_session.html',context)

@login_required(login_url='/')

def EDIT_SESSION(request,id):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        context = {
            'session':Session_Year.objects.filter(id=id)
        }
        return render(request,'Hod/edit_session.html',context)
@login_required(login_url='/')

def UPDATE_SESSION(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        if request.method == "POST":
            session_year_start = request.POST.get('session_year_start')
            session_year_end = request.POST.get('session_year_end')
            session_id = request.POST.get('id')

            Session_Year.objects.filter(id=session_id).update(
                session_start=session_year_start,
                session_end=session_year_end
            )
            return redirect('view_session')
        
@login_required(login_url='/')

def DELETE_SESSION(request,id):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        session = Session_Year.objects.get(id=id)
        session.delete()
        messages.success(request,"Session has been deleted successfully")
        return redirect('view_session')

@login_required(login_url='/')

def STAFF_SEND_NOTIFICATION(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        staff = Staff.objects.all()
        see_notification = Staff_Notification.objects.all().order_by("-id")[:5]
        context = {
            'staff':staff,
            'see_notification':see_notification
        }
        return render(request,'Hod/staff_notification.html',context)

@login_required(login_url='/')

def SAVE_STAFF_NOTIFICATION(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        if request.method == "POST":
            staff_id = request.POST.get('id')
            sender = request.user.id
            message = request.POST.get('message')
            staff = Staff.objects.get(admin=staff_id)
            # print(staff)
            send = CustomUser.objects.get(id=sender)
            notification = Staff_Notification(staff_id=staff,message=message,sender=send)
            notification.save()
            messages.success(request,"The message has been send Successfully")
            return redirect('staff_send_notification')
@login_required(login_url='/')

def staff_notification_all(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:

        all_ids = Staff.objects.values_list('admin', flat=True)
        if request.method == "POST":
            message = request.POST.get('message')
            sender = request.user.id

            send = CustomUser.objects.get(id=sender)

            for i in range(len(list(all_ids))):
                staff = Staff.objects.get(admin=str(all_ids[i]))
                notification = Staff_Notification(staff_id=staff,message=message,sender=send)
                notification.save()
                
            messages.success(request,"Notification Send to all")
            return redirect('staff_send_notification')

@login_required(login_url='/')
def STAFF_LEAVE(request):
    leave = Staff_leave.objects.filter(status=0).order_by('-id')
    context = {
        'leave':leave
    }
    return render(request,'Hod/staff_leave.html',context)

@login_required(login_url='/')

def STAFF_LEAVE_APPROVE(request , id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    messages.success(request,"The Leave has been approved")
    return redirect('staff_leave')

@login_required(login_url='/')

def STAFF_LEAVE_Dis(request,id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = -1
    leave.save()
    messages.success(request,"The Leave has been Rejected")
    return redirect('staff_leave')



@login_required(login_url='/')
def STUDENT_SEND_NOTIFICATION(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        student = Student.objects.all()
        see_notification = Student_Notification.objects.all().order_by("-id")
        context = {
            'student':student,
            'see_notification':see_notification
        }
    return render(request,'Hod/send_student_notification.html',context)



@login_required(login_url='/')
def student_notification_all(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:

        all_ids = Student.objects.values_list('admin', flat=True)
        if request.method == "POST":
            message = request.POST.get('message')
            sender = request.user.id

            send = CustomUser.objects.get(id=sender)

            for i in range(len(list(all_ids))):
                student = Student.objects.get(admin=str(all_ids[i]))
                notification = Student_Notification(student_id=student,message=message,sender=send)
                notification.save()
                
            messages.success(request,"Notification Send to all")
            return redirect('student_send_notification')
    return redirect('student_send_notification')




@login_required(login_url='/')
def SAVE_STUDENT_NOTIFICATION(request):
    if request.user.user_type!='1':
        messages.error(request,"No Permission to go there")
        return redirect("logout")
    else:
        if request.method == "POST":
            student_id = request.POST.get('id')
            sender = request.user.id
            message = request.POST.get('message')
            student = Student.objects.get(admin=student_id)
            # print(staff)
            send = CustomUser.objects.get(id=sender)
            # print(send,sender,message,student)
            notification = Student_Notification(student_id=student,message=message,sender=send)
            notification.save()
            messages.success(request,"The message has been send Successfully")
            return redirect('student_send_notification')
        



def STUDENT_LEAVE(request):
    leave = Student_leave.objects.filter(status=0).order_by('-id')
    context = {
        'leave':leave
    }
    return render(request,'Hod/Student_leave.html',context)




def STUDENT_LEAVE_APPROVE(request,id):
    leave = Student_leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    messages.success(request,"The Leave has been approved")
    return redirect('Student_leave')




def STUDENT_LEAVE_Dis(request,id):
    leave = Student_leave.objects.get(id=id)
    leave.status = -1
    leave.save()
    messages.success(request,"The Leave has been Rejected")
    return redirect('Student_leave')



