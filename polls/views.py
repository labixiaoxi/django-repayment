# -*-coding:utf-8
from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from jhj_rePayMents.public.hjlcSql import *
import re,json,requests


def index(request):
    # num = ""
    return render(request,'add.html')

def add(request):
    print u"**********************进件**************************************************"
    id_list = []
    # num = request.POST['test']
    # for i in range(int(num)):
    sql="select apply_id from loan_project order by apply_id desc Limit 1"
    sql_id=intelligence(sql)[0]
    result_num = sql_id[7:]
    applyId ="applyId"+str(int(result_num)+1)
    print  applyId
    url='http://123.56.13.177:9090/hjlc-api/api/eloan/submit'
    test_data={	"applyId": applyId,
        "sourceId":"FL",
        "borrowerInfo": {
        "age": "99",
        "corpName": "金惠家",
        "corpPhone": "028-88888888",
        "corpPlaceAddr": "蜀西路42号",
        "corpPlaceCity": "成都市",
        "corpPlaceCounty": "金牛区",
        "corpPlacePovice": "四川省",
        "corpPost": "其他",
        "corpType": "其他",
        "education": "本科",
        "gender": "男",
        "idNo": "230805198901039999",
        "industry": "其他",
        "marital": "未婚",
        "mateIdNo": "230805198901038888",
        "mobile": "17099999999",
        "name": "auto5825",
        "name1": "auto15825",
        "name2": "auto25825",
        "nation": "汉",
        "permanentAddressCity": "台北市",
        "permanentAddressCounty": "台台区",
        "permanentAddressDetail": "蜀东路42号",
        "permanentAddressPovice": "台湾省",
        "personalIncome": "0-3000",
        "phoneNum1": "17099999998",
        "phoneNum2": "17099999997",
        "receiverAddressCity": "成都市",
        "receiverAddressCounty": "郫都区",
        "receiverAddressDetail": "金粮路556号",
        "receiverAddressPovice": "四川省",
        "relation1": "父亲",
        "relation2": "母亲",
        "sourceOfRepayment": "其他收入",
        "termOfValidity": "2020-01-01",
        "workingLife": "5年"
    },
    "creditInfo": {
        "creditAccount": "zhanghao3821",
        "creditPasswd": "pwd3821",
        "debtAmount": 0.00,
        "historyOverdueNum": 0,
        "insuranceAccount": "baodan3821",
        "insurancePassWord": "bdpwd3821",
        "insuranceType": "车险",
        "isExceed": "0",
        "isOverdue": "0",
        "settleAccountNum": 0,
        "threeMonthInquiries": 3,
        "vCode": "code3821"
    },
    "loanInfo": {
        "applyLoanAmount": 1000000.00,
        "category": "100",
        "channel": "1003",
        "channelLoanAmount": 100000.00,
        "firstLoanAmount": 1000000.00,
        "firstLoanBalance": 50000.00,
        "guaranteeType": "其他",
        "initialValue": 1200000.00,
        "loanUse": "其他",
        "mortgageStatus": "1",
        "rateCode": "482",
    },
    "mortgageInfo": {
        "coOwners": [{
            "ownerCorpAddressCity": "佳木斯市",
            "ownerCorpAddressCounty": "向阳区",
            "ownerCorpAddressDetail": "永安街100号",
            "ownerCorpAddressPovice": "黑龙江省",
            "ownerCorpName": "金惠家门店",
            "ownerCorpPost": "其他",
            "ownerIdNo": "230805198901038888",
            "ownerMobile": "17088889999",
            "ownerName": "owner8532"
        }, {
            "ownerCorpAddressCity": "佳木斯市",
            "ownerCorpAddressCounty": "向阳区",
            "ownerCorpAddressDetail": "永安街100号",
            "ownerCorpAddressPovice": "黑龙江省",
            "ownerCorpName": "金惠家门店",
            "ownerCorpPost": "其他",
            "ownerIdNo": "230805198901038888",
            "ownerMobile": "17088889999",
            "ownerName": "owner4219"
        }],
        "estateAreaCity": "成都市",
        "estateAreaCounty": "郫都区",
        "estateAreaDetail": "金粮路900号",
        "estateAreaPovice": "四川省",
        "floor": 5,
        "mortgageType": "1",
        "totalFloor": 20,
        "useStatus": "在住",
        "warrants": "chanquan7386"
        }
    }
    data={
    "requestData":json.dumps(test_data),"skip*!^^fh.h23123k$d":"1",
    }
    res=requests.post(url=url,data=data)
    id_list.append(str(res.json()['data']))
    with open('id_list.txt','w') as f:
        f.write(','.join(id_list))

    print u"**********************影像**************************************************"

    with open('id_list.txt','r') as f:
        requestsIds = f.readlines()
    for requestId in requestsIds:
        print requestId
        url='http://123.56.13.177:9090/JHJTestMock/fenling/submitImg?requestId=%s&num=1'%requestId
        res =requests.get(url=url)
        print res.content
    print u"**********************pc**************************************************"
    url='http://123.56.13.24:6856/adminUser/loginValidate'
    data={
            'name':'admin',
            'pass':'1cfb50ece6c08b7fa074742ab1d668ef',
    }
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    res=requests.post(url=url,data=data,headers=headers)
    result= res.cookies.get_dict()
    pc_cookies=""
    for values in result.values():
        pc_cookies = values

    print u"**********************一审**************************************************"

    url='http://123.56.13.24:6856/loan/project/audit'
    with open('id_list.txt','r') as f:
        requestIds = f.readlines()
    for requestId in range(len(requestIds)):
        data={
            "loanProjectId":str(requestIds[requestId]),
            "limitAmount":100000.00,
            "loanRateId":2,
            "guaranteeId":"426037901839564800",
            "fundChannel":"p2p",
            "auditResult":1,
            "rejectReason":""
            }
        cookie={
        "JSESSIONID":pc_cookies
        }
        res = requests.post(url=url,data=data,cookies=cookie)
        print res.content

    print u"**********************分单**************************************************"

    url='http://123.56.13.177:9090/hjlc-api/api/eloan/submitOrder?'
    with open('id_list.txt','r') as f:
        requestIds = f.readlines()
    money = request.POST['money']
    for i in range(len(requestIds)):
        loanAmount=money
        data={
        "orders":[
            {
                "currentMobile":"15882255633",
                "idNo":"449137910529130496",
                "isActualBorrower":"Y",
                "userName":"孔勇",
                "loanAmount":loanAmount,
                "orderId":"1530939575790",
                "userType":"P"
                }
            ],
            "requestId":requestIds[i],
            "totalCount":1
        }
        data={
            "requestData":json.dumps(data),"skip*!^^fh.h23123k$d":"1",
        }
        res = requests.post(url=url,data=data)
        print res.content

    print u"**********************二审**************************************************"
    # url = "http://123.56.13.24:6856/loan/project/audit"
    # with open('id_list.txt','r') as f:
    #     requestIds = f.readlines()
    # for requestId in range(len(requestIds)):
    #     data={
    #         "loanProjectId":str(requestIds[requestId]),
    #         "limitAmount":100000,
    #         "loanRateId":
    #         "guaranteeId":
    #         "fundChannel":"p2p",
    #         "auditResult":1,
    #         "rejectReason":"",
    #         "marketType":2,
    #     }
    #     cookie={
    #     "JSESSIONID":pc_cookies
    #     }


    # return render(request,'add.html',locals())
    return HttpResponse(u"进件成功")

