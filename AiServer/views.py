# coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from AiServer.models import HeartDisease,ChronicKidneyDisease,CheckInf

# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
# Create your views here.
def index(req):
    er_message = ""
    if req.POST:
        post = req.POST
        type = req.POST['type']
        new_name = post['name']
        new_email = post['email']
        new_password = post['password']
        if type == '0': #register
            if User.objects.filter(username=new_name):
                er_message = 'exist'
            else:
                new_User = User.objects.create_user(username=new_name, password=new_password)
                new_User.save()
                return HttpResponseRedirect('/')
        else: # logging
            if req.session.get('username', ''):
                return HttpResponseRedirect('/')
            if req.POST:
                post = req.POST
                logname = post["name"]
                logpassword = post["password"]
                if User.objects.filter(username=logname):
                    user = auth.authenticate(username=logname, password=logpassword)
                    if user is not None:
                        if user.is_active:
                            auth.login(req, user)
                            req.session['username'] = logname
                            return HttpResponseRedirect('/')
                        else:
                            er_message = "not active"
                    else:
                        er_message = "psword error"
                else:
                    er_message = "not exist!"
                return render_to_response('select-disease.ejs')
    return render_to_response('index.ejs',{'er_message':er_message})


def choose_disease(req):
    '''
    TODO 选择疾病,貌似不需要
    :param req:
    :return:
    '''
    post = req.POST
    choose_disease_id = post['disease_id']


    return

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
        pass # TODO 保存对象，计算结果并保存
        post = req.POST
        type = post['type']
        new_check = CheckInf(user=user, use_agree=post['user_agree'])
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
            )
        new_check.result = predict_result()
        new_check.save()
        new_disease.save()
        return render_to_response("",context) # 传输完跳转到结果展示页。
    return  render_to_response(html_file,context)

def get_result(req):
    '''
    TODO 获取结果  貌似不用
    :param req:
    :return:
    '''

    return

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
    all_result = CheckInf.objects.get
    return

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
    if disease_id == 1:
        obj=HeartDisease()
        lg = joblib.load('/models/heart-disease/test.pkl')
        result = lg.predict([int(i) for i in [obj.age,obj.sex,obj.cp,obj.tresbps,obj.chol,obj.fbs,obj.restecg,obj.thalach,obj.oldpeak,obj.slope, obj.ca,obj.thal]])
    elif disease_id == 2:
        lg = joblib.load('/models/chronic-kidney-disease/test.pkl')
        result = lg.predict([int(i) for i in []])
    return result[0]

