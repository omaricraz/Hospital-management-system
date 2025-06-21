from django.contrib import admin
from .models import *

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ('gender',)

class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'condition', 'diagnosis_date', 'is_chronic')
    search_fields = ('patient__first_name', 'patient__last_name', 'condition')
    list_filter = ('is_chronic',)

class AllergyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'allergen', 'severity', 'is_active')
    search_fields = ('patient__first_name', 'patient__last_name', 'allergen')
    list_filter = ('severity', 'is_active')

class ImmunizationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'vaccine', 'administration_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'vaccine')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'date_time', 'status')
    search_fields = ('patient__first_name', 'patient__last_name', 'provider__first_name', 'provider__last_name')
    list_filter = ('status',)

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medication', 'prescriber', 'is_active')
    search_fields = ('patient__first_name', 'patient__last_name', 'medication')
    list_filter = ('is_active',)

class LabTestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test_name', 'test_date', 'status')
    search_fields = ('patient__first_name', 'patient__last_name', 'test_name')
    list_filter = ('status',)

class LabResultAdmin(admin.ModelAdmin):
    list_display = ('lab_test', 'result_date', 'abnormal_flag')
    search_fields = ('lab_test__patient__first_name', 'lab_test__patient__last_name', 'lab_test__test_name')

class ImagingStudyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'study_type', 'study_date', 'status')
    search_fields = ('patient__first_name', 'patient__last_name', 'study_type')
    list_filter = ('status',)

class ImagingResultAdmin(admin.ModelAdmin):
    list_display = ('imaging_study', 'result_date')
    search_fields = ('imaging_study__patient__first_name', 'imaging_study__patient__last_name', 'imaging_study__study_type')

class BillingRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'service_description', 'amount', 'status')
    search_fields = ('patient__first_name', 'patient__last_name', 'service_description')
    list_filter = ('status', 'insurance_claim')

class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider_name', 'policy_number', 'is_active')
    search_fields = ('patient__first_name', 'patient__last_name', 'provider_name')
    list_filter = ('is_active',)

class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnosis', 'is_active')
    search_fields = ('patient__first_name', 'patient__last_name', 'diagnosis')
    list_filter = ('is_active',)

class ProgressNoteAdmin(admin.ModelAdmin):
    list_display = ('treatment_plan', 'author', 'note_date')
    search_fields = ('treatment_plan__patient__first_name', 'treatment_plan__patient__last_name')

class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'is_active')
    search_fields = ('title', 'message')
    list_filter = ('priority', 'is_active')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'due_date', 'status')
    search_fields = ('title', 'assigned_to__first_name', 'assigned_to__last_name')
    list_filter = ('status', 'priority')

class TelehealthSessionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'session_date', 'status')
    search_fields = ('patient__first_name', 'patient__last_name', 'provider__first_name', 'provider__last_name')
    list_filter = ('status',)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type')
    search_fields = ('title', 'description')
    list_filter = ('report_type',)

class ReportParameterAdmin(admin.ModelAdmin):
    list_display = ('report', 'name', 'data_type', 'is_required')
    search_fields = ('report__title', 'name')

class ReportResultAdmin(admin.ModelAdmin):
    list_display = ('report', 'generated_by', 'generated_at')
    search_fields = ('report__title', 'generated_by__first_name', 'generated_by__last_name')

admin.site.register(Patient, PatientAdmin)
admin.site.register(MedicalHistory, MedicalHistoryAdmin)
admin.site.register(Allergy, AllergyAdmin)
admin.site.register(Immunization, ImmunizationAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(LabTest, LabTestAdmin)
admin.site.register(LabResult, LabResultAdmin)
admin.site.register(ImagingStudy, ImagingStudyAdmin)
admin.site.register(ImagingResult, ImagingResultAdmin)
admin.site.register(BillingRecord, BillingRecordAdmin)
admin.site.register(InsurancePolicy, InsurancePolicyAdmin)
admin.site.register(TreatmentPlan, TreatmentPlanAdmin)
admin.site.register(ProgressNote, ProgressNoteAdmin)
admin.site.register(Alert, AlertAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TelehealthSession, TelehealthSessionAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(ReportParameter, ReportParameterAdmin)
admin.site.register(ReportResult, ReportResultAdmin)