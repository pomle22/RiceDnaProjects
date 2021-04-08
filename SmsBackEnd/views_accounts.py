from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from Users.models import UserSession, Profile
from django.shortcuts import get_object_or_404
from .helper import date_format, encode, decode, dictfetchall
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .forms import AdminSignUpForm
from django.db import connection
import time, datetime, json


manageAccountsPath = '/SmsBackEnd/manage_accounts/'


# function manage all  accounts in systems
@login_required()
def manage_accounts(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT au.id as user_id , au.username , au.first_name , au.last_name , au.email , ag.name as group_name , ur.* FROM auth_user au JOIN auth_user_groups aug ON au.id = aug.user_id JOIN auth_group ag ON ag.id = aug.group_id JOIN Users_role ur ON au.id = ur.user_id'
            )

            users_data = dictfetchall(cursor)
            # for i in users_data:
            #     encode_id = encode(i['user_id'])
            #     i['user_id'] = encode_id

            return render(request, 'accounts/manage_accounts.html',
                          {'users_data': users_data})
    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end render manage accounts ==')


# function view account active or not ative in systems
@login_required()
def active_accounts(request):
    try:
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            # user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=180))

            # users = (user for user in  user_status)
            # context = {"online_users"}
            cursor = connection.cursor()
            cursor.execute(
                'SELECT au.username , au.first_name , au.last_name , au.email , au.last_login , mu.session_id FROM auth_user au JOIN Users_usersession mu ON au.id = mu.user_id'
            )
            users_active = []
            for row in cursor.fetchall():
                users_active.append({
                    'username': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'last_login': row[4],
                    'session_id': row[5]
                })

            return render(request, 'accounts/active_accounts.html',
                          {'users_active': users_active})

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end render active accounts ==')

@login_required()
def edit_account(request, user_id):
    user_id = decode(user_id)
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = AdminSignUpForm(request.POST, request.FILES, instance=user)
        form.base_fields['avatar'].required = False
        if form.is_valid():
            user = form.update()
            # user = form.save()   <  have this probrem no upload image
            return redirect('/SmsBackEnd/manage_accounts/')
    else:
        form = AdminSignUpForm(instance=user)
    return render(request, 'accounts/edit_account.html', {'form': form})


# function view infomation of users
@user_passes_test(lambda u: u.is_superuser)

def view_account(request, user_id):
    try:
        user_id = decode(user_id)
        if request.method == "POST":
            return HttpResponseBadRequest()
        else:
            cursor = connection.cursor()
            cursor.execute(
                'SELECT au.username , au.first_name , au.last_name , au.email , ag.name as group_name, mp.location, mp.tel, mp.avatar FROM auth_user au JOIN auth_user_groups aug ON au.id = aug.user_id JOIN auth_group ag ON ag.id = aug.group_id JOIN ManageUsers_profile mp ON au.id = mp.user_id WHERE au.id = %s',
                [user_id])
            users_data = []
            for row in cursor.fetchall():
                users_data.append({
                    'username': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'group_name': row[4],
                    'location': row[5],
                    'tel': row[6],
                    'avatar': row[7]
                })
            return render(request, 'accounts/view_account.html',
                          {'users_data': users_data})

    except Exception as e:
        return HttpResponseServerError(e)
    finally:
        print('== end render view_accounts ==')


# Admin Signup
@login_required()
def create_accounts(request):
    try:
        args = {}
        if request.method == 'POST':
            form = AdminSignUpForm(request.POST, request.FILES)
            # Check register button
            if 'registerbtn' in request.POST:
                if form.is_valid():
                    user = form.save()
                    user = User.objects.filter(
                        username=form.cleaned_data.get('username')).first()
                    group_admin = Group.objects.get(
                        name=form.cleaned_data['user_group'])
                    user.groups.add(group_admin)
                    role = Role.objects.create(user_id=user.id)
                    # email confirmation
                    current_site = get_current_site(request)
                    subject = _('Confirm registration from SmsBaseApp')
                    message = render_to_string(
                        'acc_active_email.html', {
                            'user': user,
                            'domain': current_site,
                            'uid': urlsafe_base64_encode(force_bytes(
                                user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                    email = EmailMessage(
                        subject, message, to=['nationalbiobank@gmail.com'])
                    email.send()
                    message_header = _('Register successfully.')
                    message_detail = _('Please confirm your email.')
                    message_header_json = str(message_header)
                    message_detail_json = str(message_detail)
                    request.session['sm_value'] = {
                        'message_header': message_header_json,
                        'message_detail': message_detail_json,
                        'type': 'success',
                        'displaytime': '5'
                    }
                    # request.session['goto'] = manageAccountsPath
                    return redirect('/SmsBackEnd/manage_accounts/')
                    # return redirect(projectPath+'/status_message/')
                else:
                    print(form.errors.as_data())
        else:
            # if not post show form signup
            form = AdminSignUpForm()

        args['form'] = form
        return render(request, 'accounts/create_accounts.html', args)
    except Exception as e:
        return e
    finally:
        print('== end function create account ==')


@user_passes_test(lambda u: u.is_superuser)
def del_user(request, username):
    try:
        u = User.objects.get(username=username)
        u.delete()
        messages.success(request, "The user is deleted")

    except User.DoesNotExist:
        messages.error(request, "User doesnot exist")
        return render(request, 'front.html')

    except Exception as e:
        return render(request, 'front.html', {'err': e.message})

    return redirect('/SmsBackEnd/manage_accounts/')


@csrf_exempt
def change_form_permission(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        # user_id = decode(user_id)

        form_name = request.POST.get('form_name')
        check = request.POST.get('check')
        # form_two = request.POST.get('form_two')
        # form_three = request.POST.get('form_three')
        # form_four = request.POST.get('form_four')
        # form_five = request.POST.get('form_five')
        # form_six = request.POST.get('form_six')

        response_data = {}
        response_data['result'] = 'Create post successful!'
        if form_name == "form_one":
            if check == "true":
                Role.objects.filter(user_id=user_id).update(form_one=1)
            else:
                Role.objects.filter(user_id=user_id).update(form_one=0)
        elif form_name == "form_two":
            if check == "true":
                Role.objects.filter(user_id=user_id).update(form_two=1)
            else:
                Role.objects.filter(user_id=user_id).update(form_two=0)
        elif form_name == "form_three":
            if check == "true":
                Role.objects.filter(user_id=user_id).update(form_three=1)
            else:
                Role.objects.filter(user_id=user_id).update(form_three=0)
        elif form_name == "form_four":
            if check == "true":
                Role.objects.filter(user_id=user_id).update(form_four=1)
            else:
                Role.objects.filter(user_id=user_id).update(form_four=0)
        elif form_name == "form_five":
            if check == "true":
                Role.objects.filter(user_id=user_id).update(form_five=1)
            else:
                Role.objects.filter(user_id=user_id).update(form_five=0)
        elif form_name == "form_six":
            if check == "true":
                Role.objects.filter(user_id=user_id).update(form_six=1)
            else:
                Role.objects.filter(user_id=user_id).update(form_six=0)
        else:
            pass


        return HttpResponse(JsonResponse({'results': ''}),
                            content_type='application/json')
    else:
        return HttpResponse(
        json.dumps({"nothing to see": "this isn't happening"}),
        content_type="application/json"
    )


@user_passes_test(lambda u: u.is_superuser)
def delete_user_sessions(request, username):
    user = User.objects.get(username=username)
    user_sessions = UserSession.objects.filter(user=user)
    for user_session in user_sessions:
        user_session.session.delete()

    return redirect('/SmsBackEnd/active_accounts/')


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # dj_login(request, user)
        message_header = _('Confirm email successfully.')
        message_detail = _('Enjoy using our system.')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {
            'message_header': message_header_json,
            'message_detail': message_detail_json,
            'type': 'success',
            'displaytime': '10'
        }
        request.session['goto'] = loginPath

        return redirect('/SmsBackEnd/status_message/')
    else:
        message_header = _('Confirm email failed.')
        message_detail = _('Please contact officer.')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {
            'message_header': message_header_json,
            'message_detail': message_detail_json,
            'type': 'error',
            'displaytime': '10'
        }

        request.session['goto'] = '/SmsBackEnd/smsbackend_admin/'

        return redirect('/SmsBackEnd/status_message/')


def status_message(request):
    args = {}

    try:
        args['goto'] = request.session['goto']
        sm_value = request.session['sm_value']
        args['type'] = sm_value['type']
        args['message_header'] = sm_value['message_header']
        args['message_detail'] = sm_value['message_detail']
        args['displaytime'] = sm_value['displaytime']

        del request.session['goto']
        del request.session['sm_value']

        return render(request, 'status_message.html', args)

    except KeyError:
        return redirect('/SmsBackEnd/smsbackend_admin/')


def password_reset_request(request):
    args = {}
    form = PasswordResetRequestForm(request.POST or None)
    if request.method == 'POST':
        if 'resetBtn' in request.POST and form.is_valid():
            user = User.objects.filter(
                email=form.cleaned_data.get('email')).first()

            # email confirmation
            current_site = get_current_site(request)
            subject = _('Confirm password change from SmsBaseApp')
            message = render_to_string(
                'acc_reset_password_email.html', {
                    'user':
                        user,
                    'domain':
                        current_site,
                    'uid':
                        urlsafe_base64_encode(force_bytes(user.pk)).decode,
                    'token':
                        account_activation_token.make_token(user),
                    'date':
                        urlsafe_base64_encode(
                            force_bytes(datetime.now().strftime('%y%m%d'))).decode,
                    'time':
                        urlsafe_base64_encode(
                            force_bytes(datetime.now().strftime('%H%M'))).decode,
                })
            user.email_user(subject, message)
            message_header = _('Request a Password Change')
            message_detail = _('Please confirm the password at your email')
            message_header_json = str(message_header)
            message_detail_json = str(message_detail)

            request.session['sm_value'] = {
                'message_header': message_header_json,
                'message_detail': message_detail_json,
                'type': 'info',
                'displaytime': '10'
            }
            request.session['goto'] = '/SmsBackEnd/smsbackend_admin/'

            return redirect(projectPath + '/status_message/')

    args['form'] = form
    return render(request, 'password_reset_request.html', args)


def activate_password_reset(request, uidb64, token, date, time):
    email_expired = 30

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        date = force_text(urlsafe_base64_decode(date))
        time = force_text(urlsafe_base64_decode(time))
        dt = datetime.strptime(date + time, '%y%m%d%H%M')
        diff_dt = datetime.now() - dt
        # diff_dt_minute = divmod(diff_dt.days * 86400 + diff_dt.seconds, 60)
        diff_dt_minute = (diff_dt.days * 86400 + diff_dt.seconds) / 60
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # request correct
    if user is not None and account_activation_token.check_token(
            user, token) and diff_dt_minute <= email_expired:
        request.session['reset_password'] = {
            'user': uid,
            'dt': datetime.now().strftime('%y%m%d%H%M')
        }
        # dj_login(request, user)
        return redirect('SmsBackEnd/user/reset/password/change/')

    # request expired
    elif user is not None and account_activation_token.check_token(
            user, token) and diff_dt_minute > email_expired:
        message_header = _('Reset password failed.')
        message_detail = _(
            'Reset Passwords request expired. Please login again')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {
            'message_header': message_header_json,
            'message_detail': message_detail_json,
            'type': 'error',
            'displaytime': '10'
        }
        request.session['goto'] = '/SmsBackEnd/smsbackend_admin/'

        return redirect('SmsBackEnd/status_message/')

    else:
        message_header = _('Reset password failed.')
        message_detail = _('Please contact officer.')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {
            'message_header': message_header_json,
            'message_detail': message_detail_json,
            'type': 'error',
            'displaytime': '10'
        }
        request.session['goto'] = '/SmsBackEnd/smsbackend_admin/'

        return redirect('SmsBackEnd/status_message/')


def reset_change_password_request(request):
    args = {}
    form = ResetChangePasswordForm(request.POST or None)

    # if not request.user.is_authenticated():
    #     return redirect('/SmsBackEnd/smsbackend_admin/')

    if request.method == 'POST':
        if 'resetBtn' in request.POST and form.is_valid():
            try:
                user = User.objects.get(pk=request.session['reset_user'])
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                del request.session['reset_user']
                message_header = _('Reset password successfully')
                message_detail = _('New password is saved successfully')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {
                    'message_header': message_header_json,
                    'message_detail': message_detail_json,
                    'type': 'success',
                    'displaytime': '10'
                }
                request.session['goto'] = '/SmsBackEnd/smsbackend_admin/'

                return redirect('SmsBackEnd/status_message/')

            except KeyError:
                message_header = _('Reset password failed.')
                message_detail = _('Please a new request.')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {
                    'message_header': message_header_json,
                    'message_detail': message_detail_json,
                    'type': 'error',
                    'displaytime': '10'
                }
                request.session['goto'] = '/SmsBackEnd/smsbackend_admin/'

                return redirect('SmsBackEnd/status_message/')

    else:
        try:
            rs_value = request.session['reset_password']
            user = User.objects.get(pk=rs_value['user'])
            dt = datetime.strptime(rs_value['dt'], '%y%m%d%H%M')
            diff_dt = datetime.now() - dt
            diff_dt_minute = (diff_dt.days * 86400 + diff_dt.seconds) / 60
            del request.session['reset_password']

            request.session['reset_user'] = rs_value['user']

        except KeyError:
            message_header = _('Reset password failed.')
            message_detail = _('Please a new request.')
            message_header_json = str(message_header)
            message_detail_json = str(message_detail)
            request.session['sm_value'] = {
                'message_header': message_header_json,
                'message_detail': message_detail_json,
                'type': 'error',
                'displaytime': '10'
            }
            request.session['goto'] = '/SmsBackEnd/smsbackend_admin/'

            return redirect('SmsBackEnd/status_message/')

    args['form'] = form
    return render(request, 'reset_change_password.html', args)


def change_password(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
    else:
        return redirect('/SmsBackEnd/smsbackend_admin/')

    args = {}
    form = ChangePasswordForm(request.POST or None)

    if request.method == 'POST':
        if 'cpBtn' in request.POST and form.is_valid():
            chk_old_pass_flag = user.check_password(
                form.cleaned_data.get('password0'))

            if chk_old_pass_flag:
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                message_header = _('Reset password successfully')
                message_detail = _(
                    'New password is saved successfully. Please login again')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {
                    'message_header': message_header_json,
                    'message_detail': message_detail_json,
                    'type': 'success',
                    'displaytime': '10'
                }
                request.session['goto'] = '/SmsBackEnd/smsbackend_admin/'

                return redirect(projectPath + '/status_message/')
            else:
                message_header = _('Reset password failed.')
                message_detail = _(
                    'The old password incorrect. Please login again')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {
                    'message_header': message_header_json,
                    'message_detail': message_detail_json,
                    'type': 'error',
                    'displaytime': '3'
                }
                request.session['goto'] = 'SmsBackEnd/user/change_password/'

                return redirect('SmsBackEnd/status_message/')

    args['form'] = form
    return render(request, 'change_password.html', args)


# function show message when create account
def status_message(request):
    args = {}
    try:
        sm_value = request.session['sm_value']
        args['type'] = sm_value['type']
        args['message_header'] = sm_value['message_header']
        args['message_detail'] = sm_value['message_detail']
        args['displaytime'] = sm_value['displaytime']
        del request.session['sm_value']

        return render(request, 'accounts/status_message.html', args)

    except KeyError:
        return redirect('/SmsBackEnd/ibiobank/')
    finally:
        print(' == end function show message == ')


def django_image_and_file_upload_ajax(request):
    if request.method == 'POST':
        form = ImageFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'error': False,
                'message': 'Uploaded Successfully'
            })
        else:
            return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = ImageFileUploadForm()
        return render(request, 'django_image_upload_ajax.html', {'form': form})
