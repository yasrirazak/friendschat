from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from usermgr.models import *

import datetime
import json

def index(request):
    # if user has login, go to home page
    if request.session.get('has_login', False):
        return HttpResponseRedirect(('/usermgr/home'))
    return HttpResponseRedirect(('/usermgr/home'))
    
def signup(request):
    # if user has login, go to home page
    if request.session.get('has_login', False):
        return HttpResponseRedirect(('/usermgr/home'))
    return render(request,'usermgr/signup.html')
    
def regist(request):
    context={}
    if request.method == "POST":
        # check userfield and password field, if empty go to login page
        try:
            userfield=str(request.POST['usernamevar'])
            passwordfield=str(request.POST['passwordvar'])
            get_user_all = User.objects.all()
        except:
            return render(request,'usermgr/index.html')

        # check user data, if username and password matched, user can get data from database
        # if can't go to login page

        check=int(0)

        for account in get_user_all:
            usernamecheck=account.username
            if(userfield==usernamecheck):
                check=1
        if(check==1):
            context['warn']=str(userfield+" has been registered")
            return render(request,'usermgr/signup.html',context)
        else:
            obj=User(username=userfield,password=passwordfield)
            obj.save()
            return HttpResponseRedirect('/usermgr/')
    else:
        return HttpResponse('ooops sorry')
    	

# views for home page

def home(request):
    context={}
    if request.method == "POST":
        # check userfield and password field, if empty go to login page
        try:
            userfield=str(request.POST['usernamevar'])
            passwordfield=str(request.POST['passwordvar'])
            get_user_all = User.objects.all()
        except:
            return render(request,'usermgr/index.html')

        # check user data, if username and password matched, user can get data from database
        # if can't go to login page

        check=int(0)

        for account in get_user_all:
            usernamecheck=account.username
            passwordcheck=account.password
            if((userfield==usernamecheck)and(passwordfield==passwordcheck)):
                check=1
        if(check==1):
            request.session['has_login'] = userfield
            return HttpResponseRedirect('/usermgr/home/')
        else:
            context['warn']="username not found"
    # if user has login, getting data user such as status and redirect go to home page
    if request.session.get('has_login', False):
        session_user = request.session.get('has_login')
        try:
            get_id=User.objects.get(username=session_user)
        except:
            raise Http404("Not Found")

        get_user_all = User.objects.all()
        get_account_id =get_id.id
        statussort = Status.objects.order_by('-pub_date')
        mystatus = statussort.filter(account_id=get_account_id)
        friendssort = Friends.objects.all()
        all_my_friend = friendssort.filter(account=get_account_id)
        messagesort = Messages.objects.order_by('-pub_date')

        #declaration empty variable
        list_friend=[]
        list_friend_withmyid=[get_account_id]
        list_myid=[get_account_id]

        #listing friends id
        for x in all_my_friend:
                list_friend_withmyid.append(int(x.friend_id))
                list_friend.append(int(x.friend_id))

        #listing status by my account id and my friends id
        mystatussort=[]
        for status in statussort:
            if status.account_id in list_friend_withmyid:
                mystatussort.append(status)


        context['list_friends_box']=list_friend,
        context['list_myid_box']=list_myid
        context['session_user']=session_user
        context['status_friends_box']=mystatussort

        return render(request,'usermgr/home.html',context)


    return render(request,'usermgr/index.html',context)
def message(request):

    if request.session.get('has_login', False):
        session_user=request.session.get('has_login')
        try:
            get_id=User.objects.get(username=session_user)
        except:
            raise Http404("Not Found")
        get_account_id=get_id.id
        friendssort = Friends.objects.all()
        all_my_friend=friendssort.filter(account=get_account_id)
        messagesort=Messages.objects.order_by('pub_date')

        #declaration empty variable
        list_friend=[]
        list_friend_name=[]
        list_myid=[]

        #listing friends id
        for x in all_my_friend:
            list_friend.append(int(x.friend_id))
            friend_obj=User.objects.get(id=int(x.friend_id))
            list_friend_name.append(str(friend_obj.username))

        temp=''
        temp_date=''
        list_message=[]
        list_date=[]

        for y in list_friend:
            for msg in messagesort:
                if (msg.account_id==y)and(msg.friend_id==get_account_id):
                    temp=msg.message
                    temp_date=msg.pub_date
                if (msg.friend_id==y)and(msg.account_id==get_account_id):
                    temp=msg.message
                    temp_date=msg.pub_date

            list_message.append(temp)
            list_date.append(temp_date)
            temp=''
            temp_date=''

        list_myid.append(get_account_id)
        context={}
        context['msg']=zip(list_friend_name,list_message,list_date,list_friend)

        return render (request,'usermgr/message.html',context)
    else:
        return HttpResponse('ooops sorry')
def insert_status(request):
    try:
        session_user=request.session.get('has_login')
        get_id=User.objects.get(username=session_user)
    except:
            raise Http404("Not Found")
    # inserting status from statusfield to database
    try:
     statusfield=str(request.POST['statusvar'])
     current_date = timezone.now()

     obj=User.objects.get(username=session_user)
     obj.status_set.create(status=statusfield,pub_date=current_date)
    except:
     return render(request,'usermgr/home.html')
    return HttpResponseRedirect(reverse('usermgr:home'))

def insert_message(request):
    try:
     session_user=request.session.get('has_login')
     get_id=User.objects.get(username=session_user)
    except:
     raise Http404("Not Found")
    # inserting message from messagefield to database
    try:
     idfriendfield=int(request.POST['idfriendvar'])
     msgfield=str(request.POST['msgvar'])
     current_date = timezone.now()

     get_id.messages_set.create(message=msgfield,pub_date=current_date,friend_id=idfriendfield)
     url='/usermgr/chat/'+str(idfriendfield)
    except Exception as e:
     return HttpResponse(e)
    return HttpResponseRedirect(url)

def friends(request):
    session_user=request.session.get('has_login')
    try:
        get_id=User.objects.get(username=session_user)
    except:
        raise Http404("Not Found")
    # if user has login, get data user friends name

    if request.session.get('has_login', False):
        get_user_all = User.objects.all()
        get_account_id=get_id.id
        friendssort = Friends.objects.all()
        all_friend=friendssort.order_by('account')
        friendssort_by_my_id=all_friend.filter(account=get_account_id)
        listfriends=[]
        listboxfriends=[]
        for x in friendssort_by_my_id:
            listfriends.append(int(x.friend_id))
        for y in listfriends:
            y=int(y)
            getaccount_name=User.objects.get(pk=y)
            listboxfriends.append((getaccount_name))

        context={}
        #wait confirmation request add friend
        listwaitconfirm_adding=[]
        listwaitconfirm_user=[]
        listwaitconfirm_request=[]
        for z in friendssort:
            if z.friend_id == get_account_id:
                listwaitconfirm_adding.append(z.account_id)

        context['list_wait_conf']=listwaitconfirm_adding

        for zz in listwaitconfirm_adding:
            if zz in listfriends:
                pass
            else:
                listwaitconfirm_request.append(zz)

        for zzz in listwaitconfirm_request:
            get_user=User.objects.get(id=int(zzz))
            listwaitconfirm_user.append(get_user)
        context['list_wait_conf']=listwaitconfirm_user
        context['friends_box']=listboxfriends
        context['session_user']=session_user
        context['userall']=get_user_all
        return render(request,'usermgr/friends.html',context)

def detail(request,status_id):
    if request.method == "GET":
        try:
            session_user=request.session.get('has_login')
            if session_user is None:
                return HttpResponse('ooops sorry')
            obj=Status.objects.get(pk=status_id)
            context={'obj':obj,'idstatus':obj.id,'session_user':session_user}
            return render(request,'usermgr/detail.html',context)
        except:
            raise Http404

def edit_status(request):
    if request.method == "POST":
        try:
            session_user=request.session.get('has_login')
            if session_user is None:
                return HttpResponse('ooops sorry')
            else:
                idstatusfield = int(request.POST['idstatusvar'])
                statusfield = str(request.POST['statusvar'])
                obj=Status.objects.get(pk=idstatusfield)
                obj.status = statusfield
                obj.save()
                return HttpResponseRedirect('/usermgr/home')
        except Exception as e:
            return HttpResponse(str(e))
    else:
        raise Http404('Not Allowed')


def search(request):
    try:
            session_user=request.session.get('has_login')
            get_id=User.objects.get(username=session_user)
    except:
            raise Http404("Not Found")
    if request.method == "POST":
        try:
            if session_user is None:
                return HttpResponse('ooops sorry')
            user_list=[]
            if session_user is None:
                return HttpResponse('ooops sorry')
            else:
                keyword = str(request.POST['varkeyword'])
                get_user_all = User.objects.all().order_by('username')

                for user in get_user_all:
                    if  keyword in str(user.username):
                        user_list.append(user)
                context={}
                context['find_list']=user_list
                return render(request, 'usermgr/search.html',context)
        except Exception as e:
            return HttpResponse(str(e))
    else:
        session_user=request.session.get('has_login')
        if session_user is None:
            return HttpResponse('ooops sorry')
    return render(request, 'usermgr/search.html')

def add(request,friend_id):

    friend_id=int(friend_id)
    session_user=request.session.get('has_login')
    if session_user is None:
        return HttpResponse('ooops sorry')
    context={}
    try:
        friend=User.objects.get(id=friend_id)
        my_user=User.objects.get(username=session_user)
        if friend.id==my_user.id:
            return HttpResponse('ooops sorry')
        friendssort = Friends.objects.all().filter(account_id=my_user.id)
        check=int(0)
        for my_friend in friendssort:
            if my_friend.friend_id==friend_id:
                check=1
        if check==0:
            my_user.friends_set.create(friend_id=friend_id)

    except:
        context['warn']=str('oops sorry')

    return HttpResponseRedirect('/usermgr/profile/'+str(friend_id))

def profile(request,user_id):
    user_id=int(user_id)
    session_user=request.session.get('has_login')
    if session_user is None:
        return HttpResponse('ooops sorry')
    context={}
    try:
        user=User.objects.get(id=user_id)
        my_user=User.objects.get(username=session_user)

        friendssort = Friends.objects.all()
        friend_list=friendssort.filter(account=my_user.id)
        status = False
        for friend in friend_list:
            if friend.friend_id == user_id:
                status  = True
        if user_id==my_user.id:
            status = True
        context['profile']=user
        context['status']=status
    except:
        context['warn']=str('not found')

    return render(request, 'usermgr/profile.html',context)

def chat(request,friend_id):
    try:
        session_user=request.session.get('has_login')
        if session_user is None:
            return HttpResponse('ooops sorry')
        get_id=User.objects.get(username=session_user)
        get_account_id=get_id.id
        friendssort=Friends.objects.all()
        friendssort=friendssort.filter(account=get_account_id)
        cek=int(0)
        id_friend=int(friend_id)
        temp=int(0)
        for i in friendssort:
            temp=int(i.friend_id)
            if temp==id_friend:
                cek=int(1)

        if cek==0:
            raise Http404("NOT ALLOWED")
        list_friend_id=int(friend_id)
        list_friend_id_and_my_id=[int(friend_id),get_account_id]
        list_myid=[get_account_id]
        messagesort=Messages.objects.order_by('-pub_date')

        my_messages_sort=[]
        for msg in messagesort:
            if msg.friend_id in list_friend_id_and_my_id:
                if msg.account_id in list_friend_id_and_my_id:
                    my_messages_sort.append(msg)
        context={}
        context['list_friend_id_box']=list_friend_id
        context['list_myid_box']=list_myid
        context['list_friend_id_and_my_id']=list_friend_id_and_my_id
        context['session_user']=session_user
        context['message_box']=my_messages_sort
        return render(request,'usermgr/chat.html',context)
    except:
        raise Http404("ERROR")

def delete(request,status_id):
    try:
        session_user=request.session.get('has_login')
        if session_user is None:
            return HttpResponse('ooops sorry')
        obj=Status.objects.get(pk=status_id)
        obj.delete()
        return HttpResponseRedirect('/usermgr/home')
    except:
        raise Http404

def logout(request):
 # deleting session from session store
 try:
     del request.session['has_login']
 except:
     return render(request,'usermgr/index.html')
 return render(request, 'usermgr/index.html')
