from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin

from .models import Student, SymptomReport, PredictionRecord

# Register the Token model from rest_framework.authtoken
# with the custom name "Auth Tokens" for better display in admin
TokenAdmin.raw_id_fields = ['user']
admin.site.register(Token, TokenAdmin)
admin.site.site_header = 'CPSU Student Health Administration'
admin.site.site_title = 'CPSU Health Admin'
admin.site.index_title = 'Clinic Administration'

# Customized Student Admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'school_id', 'share_data_consent')
    list_filter = ('share_data_consent',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'school_id')
    readonly_fields = ('date_of_birth',)
    fieldsets = (
        ('Student Information', {
            'fields': ('user', 'school_id')
        }),
        ('Health Privacy', {
            'fields': ('share_data_consent',)
        }),
    )

# Customized SymptomReport Admin
class SymptomReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'symptoms_list', 'input_method', 'created_at')
    list_filter = ('input_method', 'created_at')
    search_fields = ('student__user__username', 'student__user__first_name', 'student__user__last_name')
    readonly_fields = ('created_at',)
    
    def symptoms_list(self, obj):
        return ', '.join(obj.symptoms)
    symptoms_list.short_description = 'Symptoms'

# Customized PredictionRecord Admin
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'symptom_report', 'disease', 'confidence_percent', 'severity', 'created_at')
    list_filter = ('severity', 'disease', 'created_at')
    search_fields = ('disease', 'symptom_report__student__user__username')
    readonly_fields = ('created_at',)
    
    def confidence_percent(self, obj):
        return f"{obj.confidence_score * 100:.1f}%"
    confidence_percent.short_description = 'Confidence'

# Register the models with their custom admin classes
admin.site.register(Student, StudentAdmin)
admin.site.register(SymptomReport, SymptomReportAdmin)
admin.site.register(PredictionRecord, PredictionRecordAdmin)
