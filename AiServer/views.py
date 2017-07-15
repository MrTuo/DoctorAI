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
def index(req):
    er_message = ""
    if req.session.get('username', ''):
        return HttpResponseRedirect('/all-result/')
    if req.POST:
        post = req.POST
        type = req.POST['type']
        name = post['username']
        password = post['password']
        if type == '0': #register
            if User.objects.filter(username=name):
                return HttpResponseRedirect('exist')
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
        else: # logging
            if User.objects.filter(username=name):
                user = auth.authenticate(username=name, password=password)
                if user is not None:
                    if user.is_active:
                        auth.login(req, user)
                        req.session['username'] = name
                        return HttpResponseRedirect('/all-result/')
                    else:
                        return HttpResponse("not active")
                else:
                   return HttpResponse("psword error")
            else:
                return HttpResponse("not exist!")
        return HttpResponseRedirect('/all-result/')
    return render_to_response('index.ejs',{'er_message':er_message})


def post_checkinf(req,id):
    '''
    TODO 上传表单
    :param req:
    :return:
    '''
    context = {}
    if req.session.get('username', ''):
        username = req.session['username']
        try:
            user = User.objects.get(username=username)
        except:
            pass

    if id == '1':
        html_file = 'about-user.ejs'
    elif id == '2':
        html_file = 'about-user-1.ejs'
    if req.POST:
        post = req.POST
        type = post['type']
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
        new_check.result = predict_result(type,new_disease)
        new_disease.save()
        new_check.save()
        return HttpResponseRedirect('/all-result/') # 传输完跳转到结果展示页。
    return  render_to_response(html_file,context)

def get_all_feedbacks(req):
    '''
    TODO 展示所有feedback
    :param req:
    :return:
    '''

    return

def get_all_result(req):
    '''
    TODO 展示所有结果
    :param req:
    :return:
    '''
    if req.session.get('username', ''):
        username = req.session['username']
        try:
            user = User.objects.get(username=username)
            all_result = CheckInf.objects.filter(user=user)
        except:
            pass
        return render_to_response('follow-page.ejs',{'all_result':all_result})
    else:
        return HttpResponse('Please Login!')

def post_feedback(req,id):
    '''
    TODO 上传反馈
    :param req:
    :return:
    '''
    check = CheckInf.objects.filter(id = id)
    if req.POST:
        check.back_result = req.POST['back_result']
        check.save()
        return HttpResponseRedirect('all-result')
    return

def predict_result(disease_id,obj):
    '''
    TODO 从模型文件中加载参数，预测值并返回
    :param disease_id:疾病代码
    :param obj:输入对象
    :return:预测值
    '''
    if disease_id == '1':
        lg = joblib.load(BASE_DIR.replace('\\', '/')+'/AiServer/models/heart-disease/test.pkl')
        result = lg.predict([float(i) for i in [obj.age,obj.sex,obj.cp,obj.tresbps,obj.chol,obj.fbs,obj.restecg,obj.thalach,obj.exang,obj.oldpeak,obj.slope, obj.ca,obj.thal]])
    elif disease_id == '2':
        lg = joblib.load(BASE_DIR.replace('\\', '/')+'/AiServer/models/chronic-kidney-disease/test.pkl')
        result = lg.predict([float(i) for i in [obj.age,obj.bp,obj.sg,obj.al,obj.su,obj.rbc,obj.pc,obj.pcc,obj.ba,obj.bgr,obj.bu,obj.sc,obj.sod,obj.pot,obj.hemo,obj.pcv,obj.wc,obj.rc,obj.htn,obj.dm,obj.cad,obj.appet,obj.pe,obj.ane]])
    return result[0]

