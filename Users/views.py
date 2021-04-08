from django.contrib.auth import login as dj_login, logout as dj_logout
from .models import UserSession
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from SmsBackEnd.helper import date_format, encode, decode, dictfetchall
from django.core.mail import EmailMessage
import os.path
import datetime
from django.utils.translation import ugettext_lazy as _
from .forms import LoginForm, PasswordResetRequestForm, ResetChangePasswordForm, ChangePasswordForm , SignUpForm


from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework import status
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice

userPath = '/Users'
homePath = '/'
appPath = '/SmsBaseApp/home/'
adminPath = '/SmsBackEnd/smsbackend_admin/'
curatorPath = '/SmsBackEnd/smsbackend_curator/'
workerPath = '/SmsBackEnd/smsbackend_collector/'
loginPath = '/Users/login/'


# Login function
def login(request):
    user_session = ''
    args = {}
    form = LoginForm(request.POST or None)
    # check if post button login check user pass
    if request.method == 'POST':
        if 'loginBtn' in request.POST and form.is_valid():
            user = form.login(request)
            request.session['user_id'] = user.id
            # check new user create storage folder
            check_create_storage(request)
            if user is not None:
                dj_login(request, user)
                # user_logged_in_handler('joe',request,user)
                # if 'next' in request.POST:
                #     return redirect(request.POST.get('next'))
                if is_admin(request, user):
                    return redirect(adminPath)
                elif is_curator(request, user):
                    return redirect(curatorPath)
                elif is_worker(request, user):
                    return redirect(workerPath)
                elif is_user(request, user):
                    return redirect(appPath)
                return redirect(homePath)
        elif 'test' in request.POST:
            message_header = _('Register successfully.')
            message_detail = _('Please confirm your email.')
            message_header_json = str(message_header)
            message_detail_json = str(message_detail)
            request.session['sm_value'] = {'message_header': message_header_json,
                                           'message_detail': message_detail_json,
                                           'type': 'success',
                                           'displaytime': '5'}
            return redirect(userPath + '/status_message/')
    args['form'] = form
    return render(request, 'login.html', args)

#  Signup  
def signup(request):
    try:
        args = {}
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            # Check register button
            if 'registerbtn' in request.POST:
                if form.is_valid():
                    user = form.save()
                    user = User.objects.filter(
                        username=form.cleaned_data.get('username')).first()
                    print("ok")
                    my_group = Group.objects.get(name='User')
                    user.groups.add(my_group)
                    print("ok1")
                    user_email = form.cleaned_data['email']
                    # email confirmation
                    print("ok2")
                    current_site = get_current_site(request)
                    print("ok3")
                    subject = _('Confirm registration from BaseProject')
                    message = render_to_string(
                        'acc_active_email.html', {
                            'user': user,
                            'domain': current_site,
                            'uid': urlsafe_base64_encode(force_bytes(
                                user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                    print("ok4")
                    email = EmailMessage(
                        subject, message, to=[user_email])
                    print("ok5")
                    email.send()
                    print("ok6")
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
                    request.session['goto'] = homePath
                    return redirect(userPath + '/status_message/')
                    # return redirect(projectPath+'/status_message/')
                else:
                    print(form.errors.as_data())
        else:
            # if not post show form signup
            form = SignUpForm()

        args['form'] = form
        return render(request, 'signup.html', args)
    except Exception as e:
        return e
    finally:
        print('== end function signup ==')

def is_admin(request, user):
    request.session.modified = True
    request.session['user_session'] = "SuperAdmin"
    if user.groups.filter(name='SuperAdmin').exists():
        return True
    else:
        return False

def is_curator(request, user):
    request.session.modified = True
    request.session['user_session'] = "Curator"
    if user.groups.filter(name='Curator').exists():
        return True
    else:
        return False

def is_worker(request, user):
    request.session.modified = True
    request.session['user_session'] = "Worker"
    if user.groups.filter(name='Worker').exists():
        return True
    else:
        return False

def is_user(request, user):
    request.session.modified = True
    request.session['user_session'] = "User"
    if user.groups.filter(name='User').exists():
        return True
    else:
        return False

def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        dj_login(request, user)
        message_header = _('Confirm email successfully.')
        message_detail = _('Enjoy using our system.')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {'message_header': message_header_json,
                                       'message_detail': message_detail_json,
                                       'type': 'success',
                                       'displaytime': '5'}
        request.session['goto'] = loginPath
        return redirect(userPath+'/status_message/')
    else:
        message_header = _('Confirm email failed.')
        message_detail = _('Please contact officer.')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {'message_header': message_header_json,
                                       'message_detail': message_detail_json,
                                       'type': 'error',
                                       'displaytime': '5'}
        request.session['goto'] = homePath
        return redirect(userPath+'/status_message/')

# Check and Create folder
def check_create_storage(request):
    try:
        user_id = request.session.get('user_id')
        path = str(user_id)
        default_path = os.path.abspath(settings.MEDIA_ROOT+"/storage/"+path)
        if not os.path.exists(settings.MEDIA_ROOT+"/storage/"+path):
            os.makedirs(default_path)
    except OSError as e:
        if e.errno == 17:
            return False

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
        return redirect(homePath)

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
            message = render_to_string('acc_reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'date': urlsafe_base64_encode(force_bytes(datetime.datetime.now().strftime('%y%m%d'))),
                'time': urlsafe_base64_encode(force_bytes(datetime.datetime.now().strftime('%H%M'))),
            })
            user.email_user(subject, message)
            message_header = _('Request a Password Change')
            message_detail = _('Please confirm the password at your email')
            message_header_json = str(message_header)
            message_detail_json = str(message_detail)
            request.session['sm_value'] = {'message_header': message_header_json,
                                           'message_detail': message_detail_json,
                                           'type': 'info',
                                           'displaytime': '5'}
            request.session['goto'] = homePath
            return redirect(userPath+'/status_message/')
    args['form'] = form
    return render(request, 'password_reset_request.html', args)

def activate_password_reset(request, uidb64, token, date, time):
    email_expired = 30
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        date = force_text(urlsafe_base64_decode(date))
        time = force_text(urlsafe_base64_decode(time))
        dt = datetime.datetime.strptime(date + time, '%y%m%d%H%M')
        diff_dt = datetime.datetime.now() - dt
        diff_dt_minute = (diff_dt.days * 86400 + diff_dt.seconds)/60
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # request correct
    if user is not None and account_activation_token.check_token(user, token) and diff_dt_minute <= email_expired:
        request.session['reset_password'] = {'user': uid,
                                             'dt': datetime.datetime.now().strftime('%y%m%d%H%M')}
        # dj_login(request, user)
        return redirect(userPath+'/user/reset/password/change/')
    # request expired
    elif user is not None and account_activation_token.check_token(user, token) and diff_dt_minute > email_expired:
        message_header = _('Reset password failed.')
        message_detail = _(
            'Reset Passwords request expired. Please login again')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {'message_header': message_header_json,
                                       'message_detail': message_detail_json,
                                       'type': 'error',
                                       'displaytime': '5'}
        request.session['goto'] = homePath
        return redirect(userPath + '/status_message/')
    else:
        message_header = _('Reset password failed.')
        message_detail = _('Please contact officer.')
        message_header_json = str(message_header)
        message_detail_json = str(message_detail)
        request.session['sm_value'] = {'message_header': message_header_json,
                                       'message_detail': message_detail_json,
                                       'type': 'error',
                                       'displaytime': '5'}
        request.session['goto'] = homePath
        return redirect(userPath+'/status_message/')

def reset_change_password_request(request):
    args = {}
    form = ResetChangePasswordForm(request.POST or None)
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
                request.session['sm_value'] = {'message_header': message_header_json,
                                               'message_detail': message_detail_json,
                                               'type': 'success',
                                               'displaytime': '5'}
                request.session['goto'] = homePath
                return redirect(userPath + '/status_message/')
            except KeyError:
                message_header = _('Reset password failed.')
                message_detail = _('Please a new request.')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {'message_header': message_header_json,
                                               'message_detail': message_detail_json,
                                               'type': 'error',
                                               'displaytime': '5'}
                request.session['goto'] = homePath
                return redirect(userPath + '/status_message/')
    else:
        try:
            rs_value = request.session['reset_password']
            user = User.objects.get(pk=rs_value['user'])
            dt = datetime.datetime.strptime(rs_value['dt'], '%y%m%d%H%M')
            diff_dt = datetime.datetime.now() - dt
            diff_dt_minute = (diff_dt.days * 86400 + diff_dt.seconds) / 60
            del request.session['reset_password']
            request.session['reset_user'] = rs_value['user']
        except KeyError:
            message_header = _('Reset password failed.')
            message_detail = _('Please a new request.')
            message_header_json = str(message_header)
            message_detail_json = str(message_detail)
            request.session['sm_value'] = {'message_header': message_header_json,
                                           'message_detail': message_detail_json,
                                           'type': 'error',
                                           'displaytime': '5'}
            request.session['goto'] = homePath
            return redirect(userPath + '/status_message/')
    args['form'] = form
    return render(request, 'reset_change_password.html', args)

def change_password(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
    else:
        return redirect(homePath)
    args = {}
    form = ChangePasswordForm(request.POST or None)
    if request.method == 'POST':
        if 'cpBtn' in request.POST and form.is_valid():
            chk_old_pass_flag = user.check_password(
                form.cleaned_data.get('password0'))
            if chk_old_pass_flag:
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                message_header = _('Change password successfully')
                message_detail = _(
                    'New password is saved successfully. Please login again')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {'message_header': message_header_json,
                                               'message_detail': message_detail_json,
                                               'type': 'success',
                                               'displaytime': '5'}
                request.session['goto'] = homePath

                return redirect(userPath + '/status_message/')
            else:
                message_header = _('Change password failed.')
                message_detail = _(
                    'The old password incorrect. Please login again')
                message_header_json = str(message_header)
                message_detail_json = str(message_detail)
                request.session['sm_value'] = {'message_header': message_header_json,
                                               'message_detail': message_detail_json,
                                               'type': 'error',
                                               'displaytime': '5'}
                request.session['goto'] = userPath + \
                    '/user/change_password/'
                return redirect(userPath + '/status_message/')
    args['form'] = form
    return render(request, 'change_password.html', args)

def logout(request):
    try:
        dj_logout(request)
        return redirect(loginPath)
    except KeyError:
        pass
        return redirect(request, loginPath)


def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
class TOTPCreateView(views.APIView):
    """
    Use this endpoint to set up a new TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)
class TOTPVerifyView(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, token, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device == None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            return Response(True, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)