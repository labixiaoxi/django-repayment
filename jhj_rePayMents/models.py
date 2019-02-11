#-*- coding:utf-8
from __future__ import unicode_literals
from django.db import models

class LoanInformation(models.Model):
    id = models.IntegerField("序号",primary_key=True)
    loan = models.CharField('贷款id',max_length=200)
    jhj_mobile = models.CharField('投资人手机号',max_length=11)
    nm_mobile = models.CharField('借款人手机号',max_length=11)
    period = models.IntegerField('还款期数',max_length=2)
    loanType = models.IntegerField('还款类型,1是智慧投,2是直投',max_length=1)
    rate = models.CharField('直投的总利率',max_length=200)




class RepaymentFront(models.Model):
    repaymentType = models.CharField('还款类型,1正常还款,2担保代偿,3逾期还款',max_length=200)
    jhj_xw_front = models.CharField('jhj新网金额',max_length=200)
    nm_xw_front = models.CharField('南门新网金额',max_length=200)
    guarantee_xw_front = models.CharField('担保新网金额',max_length=200)
    income_xw_front = models.CharField('收入新网金额',max_length=200)
    jhj_app_front = models.CharField('jhj金额',max_length=200)
    nm_app_front = models.CharField('南门金额',max_length=200)
    guarantee_app_front = models.CharField('担保金额',max_length=200)
    income_app_front = models.CharField('收入金额',max_length=200)
    jhj_app_behind = models.CharField('jhj金额',max_length=200)
    jhj_xw_behind = models.CharField('jhj新网金额',max_length=200)
    nm_app_behind = models.CharField('南门金额',max_length=200)
    nm_xw_behind = models.CharField('南门新网金额',max_length=200)
    guarantee_app_behind = models.CharField('担保金额',max_length=200)
    guarantee_xw_behind = models.CharField('担保新网金额',max_length=200)
    income_app_behind = models.CharField('收入金额',max_length=200)
    income_xw_behind = models.CharField('收入新网金额',max_length=200)
    loan_id = models.ForeignKey(LoanInformation)





