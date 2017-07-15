# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CheckInf(models.Model):
    user = models.ForeignKey(User)
    disease_id = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField(default=-1)# 不同病结果不同，但是都是数字表示
    use_agree = models.BooleanField(default=0)
    back_result = models.IntegerField(default=-1,  null=True)# 反馈结果，要求同result

    def __unicode__(self):
        return self.user.username

class HeartDisease(models.Model):
    check_inf = models.OneToOneField(CheckInf)
    name = models.CharField(max_length=50, default = "心脏病")
    # 13 features
    age = models.IntegerField()
    sex = models.BooleanField() #男：0， 女：1
    cp = models.IntegerField() # 胸部疼痛的类型.1：典型心绞痛；2：非典型心绞痛，3：非心绞痛；4：无临床症状
    tresbps = models.FloatField()# 安静血压 （mmHg）
    chol = models.FloatField()# 血清类固醇含量 mg/dl
    fbs = models.FloatField()# 空腹时的血糖:
    restecg = models.IntegerField()# 静息心电图结果.0:正常；1：拥有ST-T畸形波；2：显示可能或明确的左心室肥厚
    thalach = models.IntegerField()# 达到最大心率
    exang = models.BooleanField()# 是否为运动诱发的心绞痛，0是，1否
    oldpeak = models.FloatField()# 运动相对于休息引起的ST抑郁症：0.0~9.0
    slope = models.IntegerField()# 峰值运动ST段的斜率：1：上涨；2：瓶；3：下坡
    ca = models.IntegerField()# 主要血管数量（0-3），用荧光镜检查
    thal = models.IntegerField()# thal：3 =正常; 6 =固定缺陷; 7 =可逆缺陷（先写thal吧，后面在确认一下是什么）

    def __unicode__(self):
        return self.check_inf.user.username


class ChronicKidneyDisease(models.Model):
    check_inf = models.OneToOneField(CheckInf)
    name = models.CharField(max_length=50, default="肾炎")

    age = models.IntegerField()# 年龄（数值）
    bp = models.BooleanField()# 血压（数值）：mmHg：浮点值
    sg = models.FloatField()# 比重（标称）：（1.005, 1.010, 1.015, 1.020, 1.025）选一个（注释：人体密度与水密度值比，选接近值）
    al = models.IntegerField()# 白蛋白（标称）：（0, 1, 2, 3, 4, 5）
    su = models.IntegerField()# 血糖（标称）：（0, 1, 2, 3, 4, 5）
    rbc = models.BooleanField()# 红细胞含量（标称）：（正常0，异常1）
    pc = models.BooleanField()# 脓细胞（标称）：（正常0，异常1）
    pc = models.BooleanField()# 脓细胞（标称）：（正常0，异常1）
    pcc = models.BooleanField()# 脓细胞团块（标称）：（可见0，不可见1）
    ba = models.BooleanField()# 细菌(标称)：（可见，不可见）
    bgr = models.FloatField()# 随机血糖值（数值）：mgs / dl
    bu = models.FloatField()# 血尿素（数值）：mgs / dl
    sc = models.FloatField()# 血清肌酸酐（数值）：mgs / dl
    sod = models.FloatField()# 钠含量（数值）：mEq / L
    pot = models.FloatField()# 钾含量（数值）：mEq / L
    hemo = models.FloatField()# 血红蛋白（数值）：gms
    pcv = models.IntegerField()# 红细胞压积（比值）：
    wc = models.IntegerField()# 白血球数（数值）：cells / cumm
    rc = models.BooleanField()# 红血细胞数（数值）：millions / cmm
    htn = models.BooleanField()# 高血压（标称）：（是0，否1）
    dm = models.BooleanField()# 糖尿病（标称）：（是0，否1）
    cad = models.BooleanField()# 冠状动脉疾病（标称）：（是0，否1）
    appet = models.BooleanField()# 胃口(标称)：（好0，差1）
    pe = models.BooleanField()# 足部水肿（标称）：（是0，否1）
    ane = models.BooleanField()# 贫血症（标称）：（是0，否1）

    def __unicode__(self):
        return self.check_inf.user.username


