#-*- coding:utf-8
from django.shortcuts import render_to_response

from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests,json,re,hashlib,MySQLdb,time
from public.hjlcSql import intelligence,intelligenceUpdateDate
from public.platformSql import message
from jhj_rePayMents.models import *
import logging
logger = logging.getLogger('django')
#获取pc登录验证码
# def pc_send():
#     url='http://123.56.13.177:9010/hjlc-web/user/verify_code/send'
#     data={
#         'mobile':'17000008888',
#         'template':'2'
#     }
#     res=requests.post(url=url,data=data)
#     url1='http://123.56.13.177:9010/hjlc-web/user/login'
#     code=message("select * from t_sms where Mobile='17000008888' order by Id DESC")
#     data1={
#         'mobile':"17000008888",
#         'password':"jhj123456",
#         'verifyCode':code
#     }
#     res=requests.post(url=url1,data=data1)
#     print res.cookies
#     return res.json()['data']['token']

    # token=pc_send()
    # accountId='426037901906673664'
    # page=1
    # limit=10
    # url='http://123.56.13.177:9010/hjlc-web/account/info?'+'accountId=%s&token=%s&'%(accountId,token)
    # res=requests.get(url)
    # amount=res.json()['data']['amount']
    # guarantee_balance_app_front=amount

def normal_repayment(request):

    jhj_balance_xw_front=""
    nm_balance_xw_front=""
    guarantee_balance_xw_front=""
    income_balance_xw_front=""
    jhj_balance_app_front=""
    nm_balance_app_front=""
    guarantee_balance_app_front=""
    income_balance_app_front=""
    Marketing_balance_app_front=""
    Marketing_balance_xw_front=""
    jhj_balance_app_behind=""
    jhj_balance_xw_behind=""
    nm_balance_app_behind=""
    nm_balance_xw_behind=""
    guarantee_balance_app_behind=""
    guarantee_balance_xw_behind=""
    income_balance_app_behind=""
    income_balance_xw_behind=""
    Marketing_balance_app_behind=""
    Marketing_balance_xw_behind=""
    jhj_balance_app_difference=""
    jhj_balance_xw_difference=""
    nm_balance_app_difference=""
    nm_balance_xw_difference=""
    guarantee_balance_app_difference=""
    guarantee_balance_xw_difference=""
    income_balance_app_difference=""
    income_balance_xw_difference=""
    Marketing_balance_app_difference=""
    Marketing_balance_xw_difference=""
    jhj_balance_app_calculation=""
    jhj_balance_xw_calculation=""
    nm_balance_app_calculation=""
    nm_balance_xw_calculation=""
    guarantee_balance_app_calculation=""
    guarantee_balance_xw_calculation=""
    income_balance_app_calculation=""
    income_balance_xw_calculation=""
    Marketing_balance_app_calculation=""
    Marketing_balance_xw_calculation=""

    return render(request,'index.html',locals())




def repayments(request):
    print u"***********************************还款后的金额*******************************************************"
    jhj_balance_app_calculation=""
    jhj_balance_xw_calculation=""
    nm_balance_app_calculation=""
    nm_balance_xw_calculation=""
    guarantee_balance_app_calculation=""
    guarantee_balance_xw_calculation=""
    income_balance_app_calculation=""
    income_balance_xw_calculation=""
    Marketing_balance_app_calculation=""
    Marketing_balance_xw_calculation=""
    #获取贷款信息
    user_id = request.POST['user_id']   #投资人手机号
    userId = request.POST['userId']     #借款人手机号
    loan_id = request.POST['loan_id']   #贷款id
    period = request.POST['period']    #还款期数
    repaymentType = request.POST['repaymentType'] #还款类型
    interestRate = request.POST['interestRate']  #产品中利率

    #获取投资人的account
    user_ids = intelligence("select id FROM user where mobile=en_aes(%s)"%user_id)
    account_user_ids=intelligence("select id from account where user_id='%s'"%user_ids[0])
    #获取借款人的account
    userIds = intelligence("select id FROM user where mobile=en_aes(%s)"%userId)
    account_userIds=intelligence("select id from account where user_id='%s'"%userIds[0])
    #新网前的金额
    result1=str(account_user_ids[0])   #投资人acount_id
    result2=str(account_userIds[0])
    result3="426037901906673664"
    result4="SYS_GENERATE_004"
    result5="SYS_GENERATE_002"

    id=[result1,result2,result3,result4,result5]
    xw_front_list=['jhj_balance_xw_front','nm_balance_xw_front','guarantee_balance_xw_front','income_balance_xw_front','Marketing_balance_xw_front']

    """4个新网还款前的值"""
    for i in range(5):
        url='http://123.56.13.177:9090/query/direct/userInfoQuery'
        data={
                'param':json.dumps({"platformUserNo":id[i]})
                }
        res=requests.post(url,data=data)
        xw_front_list[i] = res.json()['balance']
    jhj_balance_xw_front=xw_front_list[0]
    nm_balance_xw_front=xw_front_list[1]
    guarantee_balance_xw_front=xw_front_list[2]
    income_balance_xw_front=xw_front_list[3]
    Marketing_balance_xw_front=xw_front_list[4]

    """4个前端还款前的值"""
    #投资人还款前的金额
    url='http://123.56.13.177:9090/hjlc-api/user/accountStat?userId=%s&token=&role=2'%(user_ids)
    res=requests.get(url=url)
    app_amount=res.json()['data']['amount']
    jhj_balance_app_front=app_amount

    #南门还款前的金额
    user_Id='511301393391423488'
    url='http://123.56.13.177:9090/hjlc-api/user/accountStat?'+'userId=%s&token=&role=3'%(userIds)
    res=requests.get(url=url)
    nm_balance_app_front=res.json()['data']['amount']

    #担保还款前的金额
    sql_result = intelligence("select * from account where user_id=426037901839564800")
    guarantee_balance_app_front=float(sql_result[7])

    #收入账户还款前的金额
    #md5加密
    result=hashlib.md5()
    result.update("jhj123456")
    result_code=result.hexdigest()
    s=requests.session()
    url='http://123.56.13.24:6856/adminUser/loginValidate'
    data={
            'name':'admin',
            'pass':result_code,
            'code':1
    }
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    res=s.post(url=url,data=data,headers=headers)
    url1='http://123.56.13.24:6856/account/list'
    res1=s.get(url=url1)
    result_004=re.compile("SYS_GENERATE_004</td>.*?<td>(.*?)</td>",re.S)
    items_004=re.findall(result_004,res1.text)
    income_balance_app_front=items_004[0]

    result_002=re.compile("SYS_GENERATE_002</td>.*?<td>(.*?)</td>",re.S)
    items_002=re.findall(result_002,res1.text)
    Marketing_balance_app_front=items_002[0]



    """修改时间,发起还款"""
    end_date=time.strftime("%Y-%m-%d",time.localtime())
    sql="update loan_repayment_plan set end_date='%s' where loan_id='%s' and period='%s'"%(end_date,loan_id,period)
    print sql
    intelligenceUpdateDate(sql)


    """发起还款"""
    #返回的uncode类型需要转换成int,
    types=int(request.POST['select_test'].encode('utf-8'))
    print types
    # 发起还款
    if types==0:
        print "未选择类型"
    elif types== 1 :
        sql_third_party_id=intelligence("select * from loan_repayment_plan where loan_id='%s' and period=%s"%(loan_id,period))
        print sql_third_party_id
        repaymentPhaseId=int(sql_third_party_id[4].encode('utf-8'))
        print repaymentPhaseId
        url='http://test.loan.huijiahuzhu.com/api/loan/cutPayment?repaymentPhaseId=%s&type=%s'%(repaymentPhaseId,types)
        requests.get(url=url)
    elif types== 2 :
        sql_third_party_id=intelligence("select * from loan_repayment_plan where loan_id='%s' and period=%s"%(loan_id,period))
        repaymentPhaseId=int(sql_third_party_id[4].encode('utf-8'))
        print repaymentPhaseId
        url='http://test.loan.huijiahuzhu.com/api/loan/cutPayment?repaymentPhaseId=%s&type=%s'%(repaymentPhaseId,types)
        requests.get(url=url)
    elif types== 3 :
        sql_third_party_id=intelligence("select * from loan_repayment_plan where loan_id='%s' and period=%s"%(loan_id,period))
        repaymentPhaseId=int(sql_third_party_id[4].encode('utf-8'))
        print repaymentPhaseId
        url='http://test.loan.huijiahuzhu.com/api/loan/cutPayment?repaymentPhaseId=%s&type=%s'%(repaymentPhaseId,types)
        requests.get(url=url)
    elif types==4:
        pass
    #查看还款表的状态
    sql_result="select * from loan_repayment_plan where loan_id=%s and period=%s"%(loan_id,period)
    while True:
        if types==1:
            if int(intelligence(sql_result)[22].encode('utf-8'))==4:
                break
        elif types==2:
            if int(intelligence(sql_result)[22].encode('utf-8'))==9:
                break
        elif types==3:
            if int(intelligence(sql_result)[22].encode('utf-8'))==11:
                break

    print u"***********************************还款后的金额*******************************************************"

    """还款后的金额"""
    """4个新网还款前的值"""
    xw_behind_list=["jhj_balance_xw_behind","nm_balance_xw_behind","guarantee_balance_xw_behind","income_balance_xw_behind","Marketing_balance_xw_behind"]
    for i in range(5):
        url='http://123.56.13.177:9090/query/direct/userInfoQuery'
        data={
                'param':json.dumps({"platformUserNo":id[i]})
                }
        res=requests.post(url,data=data)
        xw_behind_list[i] = res.json()['balance']
    jhj_balance_xw_behind=xw_behind_list[0]
    nm_balance_xw_behind=xw_behind_list[1]
    guarantee_balance_xw_behind=xw_behind_list[2]
    income_balance_xw_behind=xw_behind_list[3]
    Marketing_balance_xw_behind=xw_behind_list[4]

    """4个前端还款后的值"""
    #投资人还款前的金额
    url='http://123.56.13.177:9090/hjlc-api/user/accountStat?userId=%s&token=&role=2'%(user_ids)
    res=requests.get(url=url)
    app_amount=res.json()['data']['amount']
    jhj_balance_app_behind=app_amount

    #南门还款后的金额
    user_Id='511301393391423488'
    url='http://123.56.13.177:9090/hjlc-api/user/accountStat?'+'userId=%s&token=&role=3'%(userIds)
    res=requests.get(url=url)
    nm_balance_app_behind=res.json()['data']['amount']

    #担保还款后的金额
    sql_result = intelligence("select * from account where user_id=426037901839564800")
    guarantee_balance_app_behind=float(sql_result[7])

    #收入账户还款后的金额
    #md5加密
    result=hashlib.md5()
    result.update("jhj123456")
    result_code=result.hexdigest()
    s=requests.session()
    url='http://123.56.13.24:6856/adminUser/loginValidate'
    data={
            'name':'admin',
            'pass':result_code,
            'code':1
    }
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    res=s.post(url=url,data=data,headers=headers)
    url1='http://123.56.13.24:6856/account/list'
    res=s.get(url=url1)
    result_004=re.compile("SYS_GENERATE_004</td>.*?<td>(.*?)</td>",re.S)
    items_004=re.findall(result_004,res.text)
    income_balance_app_behind=items_004[0]
    result_002=re.compile("SYS_GENERATE_002</td>.*?<td>(.*?)</td>",re.S)
    items_002=re.findall(result_002,res.text)
    Marketing_balance_app_behind=items_002[0]

    print u"***********************************写入数据库*******************************************************"
    LoanInformation.objects.create(
        loan=loan_id,
        jhj_mobile=user_id,
        nm_mobile=userId,
        period=period,
        loanType=repaymentType,
        rate=interestRate
    )
    RepaymentFront.objects.create(
        jhj_xw_front=jhj_balance_xw_front,
        nm_xw_front=nm_balance_xw_front,
        guarantee_xw_front=guarantee_balance_xw_front,
        income_xw_front=income_balance_xw_front,
        jhj_app_front=jhj_balance_app_front,
        nm_app_front=nm_balance_app_front,
        guarantee_app_front=guarantee_balance_app_front,
        income_app_front=income_balance_app_front,
        jhj_app_behind=jhj_balance_app_behind,
        jhj_xw_behind=jhj_balance_xw_behind,
        nm_app_behind=nm_balance_app_behind,
        nm_xw_behind=nm_balance_xw_behind,
        guarantee_app_behind=guarantee_balance_app_behind,
        guarantee_xw_behind=guarantee_balance_xw_behind,
        income_app_behind=income_balance_app_behind,
        income_xw_behind=income_balance_xw_behind,
        loan_id_id = loan_id,
        repaymentType =repaymentType,
    )

    print u"***********************************计算差值*******************************************************"

    jhj_balance_app_difference=round((float(jhj_balance_app_behind) - float(jhj_balance_app_front)),2)
    jhj_balance_xw_difference=round((float(jhj_balance_xw_behind) - float(jhj_balance_xw_front)),2)
    nm_balance_app_difference=float(nm_balance_app_behind) - float(nm_balance_app_front)
    nm_balance_xw_difference=float(nm_balance_xw_behind) - float(nm_balance_xw_front)
    guarantee_balance_app_difference=float(guarantee_balance_app_behind) - float(guarantee_balance_app_front)
    guarantee_balance_xw_difference=float(guarantee_balance_xw_behind) - float(guarantee_balance_xw_front)
    income_balance_app_difference=round((float(income_balance_app_behind) - float(income_balance_app_front)),2)
    income_balance_xw_difference=round((float(income_balance_xw_behind) - float(income_balance_xw_front)),2)
    Marketing_balance_app_difference=round(float(Marketing_balance_app_behind)-float(Marketing_balance_app_front),2)
    Marketing_balance_xw_difference = round(float(Marketing_balance_xw_behind)-float(Marketing_balance_xw_front),2)

    print u"***********************************自己计算差值*******************************************************"

    value = request.POST['select_test']
    values =int(value.encode('utf-8'))
    repaymentTypes=int(repaymentType.encode('utf-8'))
    #repaymentTye(1是智慧投,2是直投)
    if repaymentTypes==1:
        sql="select * from loan_repayment_plan where loan_id='%s' and period='%s'"%(loan_id,period)
        results = intelligence(sql)
        amount_result = float(results[10])    #借款人扣的钱
        principai_result = float(results[11])+float(results[13]) #投资人应该得的钱
        jhj_balance_app_calculation=0
        jhj_balance_xw_calculation=principai_result
        if values == 1: #正常还款
            jhj_balance_xw_calculation=principai_result
            nm_balance_app_calculation = amount_result
            nm_balance_xw_calculation = amount_result
            income_balance_app_calculation = float(results[15])  #手续费
            income_balance_xw_calculation = float(results[15])   #手续费
            guarantee_balance_app_calculation = 0
            guarantee_balance_xw_calculation = 0
        elif values == 2: #担保代偿
            jhj_balance_xw_calculation=principai_result
            nm_balance_app_calculation = 0
            nm_balance_xw_calculation = 0
            income_balance_app_calculation = float(results[15])  #手续费
            income_balance_xw_calculation = float(results[15])   #手续费
            guarantee_balance_app_calculation = amount_result
            guarantee_balance_xw_calculation = amount_result
        elif values == 3: #逾期还款
            jhj_balance_xw_calculation = 0
            nm_balance_app_calculation = amount_result
            nm_balance_xw_calculation = amount_result
            income_balance_app_calculation = 0  #手续费
            income_balance_xw_calculation = 0   #手续费
            guarantee_balance_app_calculation = amount_result
            guarantee_balance_xw_calculation = amount_result

    elif repaymentTypes == 2: #直投
        #获取订单金额
        sql = "select * from orders where loan_id=%s"%loan_id
        results=intelligence(sql)
        amount_result=float(results[10])
        print u"订单金额:"+str(amount_result)
        #当期剩余本金
        sql="select SUM(principal) from loan_repayment_plan   where loan_id=%s and period<%s"%(loan_id,period)
        principal_result = intelligence(sql)
        sum_principal = float(principal_result[0])
        print u"当期剩余本金:"+str(sum_principal)
        #当期6%利息
        sql = "select * from loan_repayment_plan where loan_id=%s and period=%s"%(loan_id,period)
        sql_result = intelligence(sql)
        period_principal = float(sql_result[11])
        print u"当期6%利息:"+str(period_principal)
        #总利息(基本利息+产品加息)
        # sql = "select sum(period) from loan_repayment_plan where loan_id=%s"%(loan_id)
        # sql_result = intelligence(sql)
        # sum_period = int(sql_result[0])
        sum_interest = sum_principal*float(interestRate)/100.00/12.00
        print u"当前总利率:"+str(sum_interest)
        #营销补息
        interest_supplement = sum_interest-period_principal
        print u"营销补息:"+str(interest_supplement)
        #当期本金
        sql="select * from loan_repayment_plan   where loan_id=%s and period=%s"%(loan_id,period)
        principal_result = intelligence(sql)
        sum_principal = float(principal_result[11])
        print u"当期本金:"+str(sum_principal)
        #借款人还款金额
        sql="select * from loan_repayment_plan   where loan_id=%s and period=%s"%(loan_id,period)
        amount_result = intelligence(sql)
        sum_amount = float(amount_result[10])
        print u"借款人还款:"+str(sum_amount)
        #收入金额
        sql="select * from loan_repayment_plan   where loan_id=%s and period=%s"%(loan_id,period)
        amount_result = intelligence(sql)
        procedure_fee = float(amount_result[15])
        print u"收入金额:"+str(procedure_fee)

        if values == 1:#正常还款
            #借款人还款金额
            jhj_balance_app_calculation = sum_principal+sum_interest
            jhj_balance_xw_calculation = sum_principal+sum_interest
            nm_balance_app_calculation = sum_amount
            nm_balance_xw_calculation = sum_amount
            guarantee_balance_app_calculation = 0
            guarantee_balance_xw_calculation = 0
            income_balance_app_calculation = procedure_fee
            income_balance_xw_calculation =procedure_fee
            Marketing_balance_app_calculation =   interest_supplement
            Marketing_balance_xw_calculation = interest_supplement

        elif values ==2:#担保代偿
            jhj_balance_app_calculation = sum_principal+sum_interest
            jhj_balance_xw_calculation = sum_principal+sum_interest
            nm_balance_app_calculation = 0
            nm_balance_xw_calculation = 0
            guarantee_balance_app_calculation = sum_amount
            guarantee_balance_xw_calculation = sum_amount
            income_balance_app_calculation = procedure_fee
            income_balance_xw_calculation =procedure_fee
            Marketing_balance_app_calculation =   interest_supplement
            Marketing_balance_xw_calculation = interest_supplement

        elif values ==3:#逾期还款
            jhj_balance_app_calculation = 0
            jhj_balance_xw_calculation = 0
            nm_balance_app_calculation = sum_amount
            nm_balance_xw_calculation = sum_amount
            guarantee_balance_app_calculation = -sum_amount
            guarantee_balance_xw_calculation = -sum_amount
            income_balance_app_calculation = 0
            income_balance_xw_calculation =0
            Marketing_balance_app_calculation =   0
            Marketing_balance_xw_calculation = 0

    # context={
    #     "jhj_balance_xw_front":jhj_balance_xw_front,
    #     "nm_balance_xw_front":nm_balance_xw_front,
    #     "guarantee_balance_xw_front":guarantee_balance_xw_front,
    #     "income_balance_xw_front":income_balance_xw_front,
    #     "jhj_balance_app_front":jhj_balance_app_front,
    #     "nm_balance_app_front":nm_balance_app_front,
    #     "guarantee_balance_app_front":guarantee_balance_app_front,
    #     "income_balance_app_front":income_balance_app_front,
    #     "Marketing_balance_app_front":Marketing_balance_app_front,
    #     "Marketing_balance_xw_front":Marketing_balance_xw_front,
    #     "jhj_balance_xw_behind":jhj_balance_xw_behind,
    #     "nm_balance_xw_behind":nm_balance_xw_behind,
    #     "guarantee_balance_xw_behind":guarantee_balance_xw_behind,
    #     "income_balance_xw_behind":income_balance_xw_behind,
    #     "jhj_balance_app_behind":jhj_balance_app_behind,
    #     "nm_balance_app_behind":nm_balance_app_behind,
    #     "guarantee_balance_app_behind":guarantee_balance_app_behind,
    #     "income_balance_app_behind":income_balance_app_behind,
    #     "Marketing_balance_app_behind":Marketing_balance_app_behind,
    #     "Marketing_balance_xw_behind":Marketing_balance_xw_behind,
    #     "jhj_balance_app_difference":jhj_balance_app_difference,
    #     "jhj_balance_xw_difference":jhj_balance_xw_difference,
    #     "nm_balance_app_difference":nm_balance_app_difference,
    #     "nm_balance_xw_difference":nm_balance_xw_difference,
    #     "guarantee_balance_app_difference":guarantee_balance_app_difference,
    #     "guarantee_balance_xw_difference":guarantee_balance_xw_difference,
    #     "income_balance_app_difference":income_balance_app_difference,
    #     "income_balance_xw_difference":income_balance_xw_difference,
    #     "Marketing_balance_app_difference":Marketing_balance_app_difference,
    #     "Marketing_balance_xw_difference":Marketing_balance_xw_difference,
    #     "jhj_balance_app_calculation":jhj_balance_app_calculation,
    #     "jhj_balance_xw_calculation":jhj_balance_xw_calculation,
    #     "nm_balance_app_calculation":nm_balance_app_calculation,
    #     "nm_balance_xw_calculation":nm_balance_xw_calculation,
    #     "guarantee_balance_app_calculation":guarantee_balance_app_calculation,
    #     "guarantee_balance_xw_calculation":guarantee_balance_xw_calculation,
    #     "income_balance_app_calculation":income_balance_app_calculation,
    #     "income_balance_xw_calculation":income_balance_xw_calculation,
    #     "Marketing_balance_app_calculation":Marketing_balance_app_calculation,
    #     "Marketing_balance_xw_calculation":Marketing_balance_app_calculation,
    # }
    # return render(request,"index.html",context)

    return render(request,"index.html",locals())

def test(request):
    return HttpResponse("测试")




