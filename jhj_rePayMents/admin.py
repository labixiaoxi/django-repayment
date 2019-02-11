from django.contrib import admin
from jhj_rePayMents.models import *

@admin.register(LoanInformation)
class LoanInformationAdmin(admin.ModelAdmin):
    list_display = ['id','loan','jhj_mobile','nm_mobile','period','loanType','rate']
    ordering = ['id']
    list_per_page = 30

@admin.register(RepaymentFront)
class RepaymentFrontAdmin(admin.ModelAdmin):
    # list_display = ['id','loan_id','repaymentType','jhj_xw_front','nm_xw_front','guarantee_xw_front','income_xw_front','jhj_app_front','nm_app_front','guarantee_app_front','income_app_front','jhj_app_behind','jhj_xw_behind','nm_app_behind','nm_xw_behind','guarantee_app_behind','guarantee_xw_behind','income_app_behind','income_xw_behind','loan_id_id']
    list_display = ['id','loan_id']
    ordering = ['id']
    list_per_page = 30