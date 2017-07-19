# coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from AiServer.models import HeartDisease,ChronicKidneyDisease,CheckInf
from DoctorAI.settings import BASE_DIR
# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
# Create your views here.
ADVICE = {"health":"结果显示您的身体状况良好，建议定期使用我们的系统检查，远离疾病~",
           "maybe":"结果显示您的健康数据显示有患病倾向，建议您去医院检查，并做好疾病的预防工作。",
           "danger":"结果显示您有很大概率患病，刻不容缓，请立即到医院就诊！",
           }
def get_device(req):
    try:
        if req.GET and req.GET['from'] == 'mobile':
            return "mobile"
        else:
            return "pc"
    except:
        return "pc"

def index(req):
    er_msg = ""
    if req.session.get('username', ''):
        return HttpResponseRedirect('/all-result/')
    if req.POST:
        post = req.POST
        type = req.POST['type']
        name = post['username']
        password = post['password']
        if type == '0': #register
            password2 = post['password2']
            if User.objects.filter(username=name):
                er_msg = "用户已存在！"
            elif password != password2:
                er_msg = "两次输入不一致！"
            else:
                new_User = User.objects.create_user(username=name, password=password)
                new_User.save()
            # 注册后自动登录
                user = auth.authenticate(username=name, password=password)
                if user is not None:
                    if user.is_active:
                        auth.login(req, user)
                        req.session['username'] = name
                return HttpResponseRedirect('/all-result/')
            return render_to_response('index.ejs',{'er_msg':er_msg})
        else: # logging
            if User.objects.filter(username=name):
                user = auth.authenticate(username=name, password=password)
                if user is not None:
                    if user.is_active:
                        auth.login(req, user)
                        req.session['username'] = name
                        return HttpResponseRedirect('/all-result/')
                    else:
                        er_msg = "用户状态未激活！"
                else:
                   er_msg = "密码错误！"
            else:
                er_msg = "该用户不存在!"
            return render_to_response('index.ejs', {'er_msg': er_msg})
    return render_to_response('index.ejs',{'er_msg':er_msg})

def logout(req):
    device = get_device(req)
    auth.logout(req)
    if device == 'mobile':
        return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/')

def post_checkinf(req,id):
    '''
    TODO 上传表单
    :param req:
    :return:
    '''
    context = {}
    device = get_device(req)

    if req.session.get('username', ''):
        username = req.session['username']
        try:
            user = User.objects.get(username=username)
        except:
            pass
    if device == 'pc':
        if id == '1':
            html_file = 'about-user.ejs'
        elif id == '2':
            html_file = 'about-user-1.ejs'
    else:
        if id == '1':
            html_file = 'heart.html'
        elif id == '2':
            html_file = 'kidney.html'
    if req.POST:
        post = req.POST
        type = post['type']
        device = post['device']
        new_check = CheckInf(user=user, use_agree=int(post['user_agree']))
        new_check.save()
        if type == '1':
            new_check.disease_id=1
            new_disease = HeartDisease(age=post['age'],
                                       sex=post['sex'],
                                       cp=post['cp'],
                                       tresbps=post['tresbps'],
                                       chol=post['chol'],
                                       fbs=post['fbs'],
                                       restecg=post['restecg'],
                                       thalach=post['thalach'],
                                       exang=post['exang'],
                                       oldpeak=post['oldpeak'],
                                       slope=post['slope'],
                                       ca=post['ca'],
                                       thal=post['thal'],
                                       check_inf=new_check,
                                       )
        else:
            new_check.disease_id=2
            new_disease = ChronicKidneyDisease(age=post['age'],
                                               bp=post['bp'],
                                               sg=post['sg'],
                                               al=post['al'],
                                               su=post['su'],
                                               rbc=post['rbc'],
                                               pc=post['pc'],
                                               pcc=post['pcc'],
                                               ba=post['ba'],
                                               bgr=post['bgr'],
                                               bu=post['bu'],
                                               sc=post['sc'],
                                               sod=post['sod'],
                                               pot=post['pot'],
                                               hemo=post['hemo'],
                                               pcv=post['pcv'],
                                               wc=post['wc'],
                                               rc=post['rc'],
                                               htn=post['htn'],
                                               dm=post['dm'],
                                               cad=post['cad'],
                                               appet=post['appet'],
                                               pe=post['pe'],
                                               ane=post['ane'],
                                               check_inf=new_check,
            )
        predict = predict_result(type,new_disease)
        new_check.result = predict
        new_disease.save()
        new_check.save()
        advice = ''
        if predict<0.25:
            advice = ADVICE['health']
        elif predict<0.5:
            advice = ADVICE['maybe']
        else:
            advice = ADVICE['danger']
        if device == 'mobile':
            file = 'result.html'
        else:
            file = 'result.ejs'
        return render_to_response(file,{'user':user,
                                        'type':type,
                                        'predict':predict,
                                        'advice':advice}) # 传输完跳转到结果展示页。
    return  render_to_response(html_file,{'user': user})


def detail(req,id):
    '''
    TODO 展示所有feedback
    :param req:
    :return:
    '''
    device = get_device(req)

    if req.session.get('username', ''):
        username = req.session['username']
        try:
            user = User.objects.get(username=username)
        except:
            pass
        check = CheckInf.objects.get(id=id)
        if device == 'mobile':
            return render_to_response('detail.html',{'check':check})
        return render_to_response('datail.ejs',{'check':check})
    if device == 'mobile':
        return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/')

def get_all_result(req):
    '''
    TODO 展示所有结果
    :param req:
    :return:
    '''
    device = get_device(req)

    if req.session.get('username', ''):
        username = req.session['username']
        try:
            user = User.objects.get(username=username)
            all_result = CheckInf.objects.filter(user=user)
        except:
            pass
        if device == 'mobile':
            return render_to_response('main.html',{'all_result':all_result,'user': user})
        return render_to_response('follow-page.ejs',{'all_result':all_result,'user': user})
    else:
        if device == 'mobile':
            return HttpResponseRedirect('login')
        return HttpResponseRedirect('/')

def post_feedback(req,id):
    '''
    TODO 上传反馈
    :param req:
    :return:
    '''
    device = get_device(req)
    if req.session.get('username', ''):
        username = req.session['username']
        try:
            user = User.objects.get(username=username)
            all_result = CheckInf.objects.filter(user=user)
        except:
            pass
        check = CheckInf.objects.get(id=id)
        if req.POST:
            check.back_result = req.POST['back_result']
            check.back_content = req.POST['back_content']
            device = req.POST['device']
            check.save()
            if device == 'mobile':
                return HttpResponseRedirect('/all-result/?from=mobile')
            else:
                return HttpResponseRedirect('/all-result/')
        if device == 'mobile':
            return render_to_response('feedback.html',{'user':user})
        return render_to_response('feed-back.ejs', {'user': user})
    else:
        if device == 'mobile':
            return HttpResponseRedirect('/login/')
        return HttpResponse('Please Login!')


def predict_result(disease_id,obj):
    '''
    TODO 从模型文件中加载参数，预测值并返回
    :param disease_id:疾病代码
    :param obj:输入对象
    :return:预测值
    '''
    if disease_id == '1':
        lg = joblib.load(BASE_DIR.replace('\\', '/')+'/AiServer/models/heart-disease/test.pkl')
        result = lg.predict_proba([float(i) for i in [obj.age,obj.sex,obj.cp,obj.tresbps,obj.chol,obj.fbs,obj.restecg,obj.thalach,obj.exang,obj.oldpeak,obj.slope, obj.ca,obj.thal]])
    elif disease_id == '2':
        lg = joblib.load(BASE_DIR.replace('\\', '/')+'/AiServer/models/chronic-kidney-disease/test.pkl')
        result = lg.predict_proba([float(i) for i in [obj.age,obj.bp,obj.sg,obj.al,obj.su,obj.rbc,obj.pc,obj.pcc,obj.ba,obj.bgr,obj.bu,obj.sc,obj.sod,obj.pot,obj.hemo,obj.pcv,obj.wc,obj.rc,obj.htn,obj.dm,obj.cad,obj.appet,obj.pe,obj.ane]])
    return 1-result[0][0]

### mobile request
def login(req):
    if req.POST:
        post = req.POST
        name = post['username']
        password = post['password']
        if User.objects.filter(username=name):
            user = auth.authenticate(username=name, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(req, user)
                    req.session['username'] = name
                    return HttpResponseRedirect('/all-result/?from=mobile')
                else:
                    er_msg = "用户状态未激活！"
            else:
                er_msg = "密码错误！"
        else:
            er_msg = "该用户不存在!"
        return render_to_response('login.html', {'er_msg': er_msg})
    return render_to_response('login.html')

def register(req):
    if req.POST:
        post = req.POST
        name = post['username']
        password = post['password']
        password2 = post['password2']
        if User.objects.filter(username=name):
            er_msg = "用户已存在！"
        elif password != password2:
            er_msg = "两次输入不一致！"
        else:
            new_User = User.objects.create_user(username=name, password=password)
            new_User.save()
            # 注册后自动登录
            user = auth.authenticate(username=name, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(req, user)
                    req.session['username'] = name
            return HttpResponseRedirect('/all-result/?from=mobile')
        return render_to_response('signup.html', {'er_msg': er_msg})
    return render_to_response('signup.html')
