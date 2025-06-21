from django.urls import path
from . import views

urlpatterns = [
    
    #Home
    path('', views.HomeView.as_view(), name='home'),

    
    # Dashboard
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),

    path('contact/', views.contact_view, name='contact'),
    
    
    # Patient URLs
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('patients/add/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient_update'),
    path('patients/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    
    # Medical History URLs
    path('patients/<int:patient_id>/medical-history/add/', views.MedicalHistoryCreateView.as_view(), name='medical_history_create'),
    path('medical-history/<int:pk>/edit/', views.MedicalHistoryUpdateView.as_view(), name='medical_history_update'),
    path('medical-history/<int:pk>/delete/', views.MedicalHistoryDeleteView.as_view(), name='medical_history_delete'),
    
    # Allergy URLs
    path('patients/<int:patient_id>/allergies/add/', views.AllergyCreateView.as_view(), name='allergy_create'),
    path('allergies/<int:pk>/edit/', views.AllergyUpdateView.as_view(), name='allergy_update'),
    path('allergies/<int:pk>/delete/', views.AllergyDeleteView.as_view(), name='allergy_delete'),
    
    # Immunization URLs
    path('patients/<int:patient_id>/immunizations/add/', views.ImmunizationCreateView.as_view(), name='immunization_create'),
    path('immunizations/<int:pk>/edit/', views.ImmunizationUpdateView.as_view(), name='immunization_update'),
    path('immunizations/<int:pk>/delete/', views.ImmunizationDeleteView.as_view(), name='immunization_delete'),
    
    # Appointment URLs
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointments/add/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/patient/<int:patient_id>/add/', views.AppointmentCreateView.as_view(), name='appointment_create_for_patient'),
    path('appointments/<int:pk>/edit/', views.AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
    
    # Prescription URLs
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription_detail'),
    path('prescriptions/add/', views.PrescriptionCreateView.as_view(), name='prescription_create'),
    path('prescriptions/patient/<int:patient_id>/add/', views.PrescriptionCreateView.as_view(), name='prescription_create_for_patient'),
    path('prescriptions/<int:pk>/edit/', views.PrescriptionUpdateView.as_view(), name='prescription_update'),
    path('prescriptions/<int:pk>/delete/', views.PrescriptionDeleteView.as_view(), name='prescription_delete'),
    
    # Lab Test URLs
    path('lab-tests/', views.LabTestListView.as_view(), name='lab_test_list'),
    path('lab-tests/<int:pk>/', views.LabTestDetailView.as_view(), name='lab_test_detail'),
    path('lab-tests/add/', views.LabTestCreateView.as_view(), name='lab_test_create'),  
    path('lab-tests/patient/<int:patient_id>/add/', views.LabTestCreateView.as_view(), name='lab_test_create_for_patient'),
    path('lab-tests/<int:pk>/edit/', views.LabTestUpdateView.as_view(), name='lab_test_update'),
    path('lab-tests/<int:pk>/delete/', views.LabTestDeleteView.as_view(), name='lab_test_delete'),
    
    # Lab Result URLs
    path('lab-tests/<int:lab_test_id>/results/add/', views.LabResultCreateView.as_view(), name='lab_result_create'),
    path('lab-results/<int:pk>/edit/', views.LabResultUpdateView.as_view(), name='lab_result_update'),
    path('lab-results/<int:pk>/delete/', views.LabResultDeleteView.as_view(), name='lab_result_delete'),
    
    # Imaging Study URLs
    path('imaging-studies/', views.ImagingStudyListView.as_view(), name='imaging_study_list'),
    path('imaging-studies/<int:pk>/', views.ImagingStudyDetailView.as_view(), name='imaging_study_detail'),
    path('imaging-studies/add/', views.ImagingStudyCreateView.as_view(), name='imaging_study_create'), 
    path('imaging-studies/patient/<int:patient_id>/add/', views.ImagingStudyCreateView.as_view(), name='imaging_study_create_for_patient'),
    path('imaging-studies/<int:pk>/edit/', views.ImagingStudyUpdateView.as_view(), name='imaging_study_update'),
    path('imaging-studies/<int:pk>/delete/', views.ImagingStudyDeleteView.as_view(), name='imaging_study_delete'),
    
    # Imaging Result URLs
    path('imaging-studies/<int:imaging_study_pk>/results/create/',views.ImagingResultCreateView.as_view(),name='imaging_result_create'),
    path('imaging-results/<int:pk>/update/', views.ImagingResultUpdateView.as_view(), name='imaging_result_update'),
    path('imaging-results/<int:pk>/delete/', views.ImagingResultDeleteView.as_view(), name='imaging_result_delete'),
    
    # Billing Record URLs
    path('billing/', views.BillingRecordListView.as_view(), name='billing_record_list'),
    path('billing/add/', views.BillingRecordCreateView.as_view(), name='billing_record_create'),
    path('billing/patient/<int:patient_id>/add/', views.BillingRecordCreateView.as_view(), name='billing_record_create_for_patient'),
    path('billing/appointment/<int:appointment_id>/add/', views.BillingRecordCreateView.as_view(), name='billing_record_create_for_appointment'),
    path('billing/<int:pk>/', views.BillingRecordDetailView.as_view(), name='billing_record_detail'),
    path('billing/<int:pk>/edit/', views.BillingRecordUpdateView.as_view(), name='billing_record_update'),
    path('billing/<int:pk>/delete/', views.BillingRecordDeleteView.as_view(), name='billing_record_delete'),
    
    # Insurance Policy URLs
    path('insurance/', views.InsurancePolicyListView.as_view(), name='insurance_policy_list'),
    path('insurance/add/', views.InsurancePolicyCreateView.as_view(), name='insurance_policy_create'),
    path('insurance/patient/<int:patient_id>/add/', views.InsurancePolicyCreateView.as_view(), name='insurance_policy_create_for_patient'),
    path('insurance/<int:pk>/', views.InsurancePolicyDetailView.as_view(), name='insurance_policy_detail'),
    path('insurance/<int:pk>/edit/', views.InsurancePolicyUpdateView.as_view(), name='insurance_policy_update'),
    path('insurance/<int:pk>/delete/', views.InsurancePolicyDeleteView.as_view(), name='insurance_policy_delete'),
    
    # Treatment Plan URLs
    path('treatment-plans/', views.TreatmentPlanListView.as_view(), name='treatment_plan_list'),    
    path('treatment-plans/<int:pk>/', views.TreatmentPlanDetailView.as_view(), name='treatment_plan_detail'),
    path('treatment-plans/add/', views.TreatmentPlanCreateView.as_view(), name='treatment_plan_create'),
    path('treatment-plans/patient/<int:patient_id>/add/', views.TreatmentPlanCreateView.as_view(), name='treatment_plan_create_for_patient'),
    path('treatment-plans/<int:pk>/edit/', views.TreatmentPlanUpdateView.as_view(), name='treatment_plan_update'),
    path('treatment-plans/<int:pk>/delete/', views.TreatmentPlanDeleteView.as_view(), name='treatment_plan_delete'),
    
    # Progress Note URLs
    path('treatment-plans/<int:treatment_plan_id>/notes/add/', views.ProgressNoteCreateView.as_view(), name='progress_note_create'),
    path('progress-notes/<int:pk>/edit/', views.ProgressNoteUpdateView.as_view(), name='progress_note_update'),
    path('progress-notes/<int:pk>/delete/', views.ProgressNoteDeleteView.as_view(), name='progress_note_delete'),
    
    # Alert URLs
    path('alerts/', views.AlertListView.as_view(), name='alert_list'),
    path('alerts/<int:pk>/', views.AlertDetailView.as_view(), name='alert_detail'),
    path('alerts/add/', views.AlertCreateView.as_view(), name='alert_create'),
    path('alerts/<int:pk>/edit/', views.AlertUpdateView.as_view(), name='alert_update'),
    path('alerts/<int:pk>/delete/', views.AlertDeleteView.as_view(), name='alert_delete'),
    
    # Task URLs
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/add/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('tasks/<int:pk>/update-status/', views.task_update_status, name='task_update_status'),
    
    # Telehealth URLs
    path('telehealth/', views.TelehealthSessionListView.as_view(), name='telehealth_session_list'),
    path('telehealth/<int:pk>/', views.TelehealthSessionDetailView.as_view(), name='telehealth_session_detail'),
    path('telehealth/<int:pk>/delete/', views.TelehealthSessionDeleteView.as_view(), name='telehealth_session_delete'),
    path('telehealth/add/', views.TelehealthSessionCreateView.as_view(), name='telehealth_session_create'),
    path('telehealth/patient/<int:patient_id>/add/', views.TelehealthSessionCreateView.as_view(), name='telehealth_session_create_for_patient'),
    path('telehealth/<int:pk>/edit/', views.TelehealthSessionUpdateView.as_view(), name='telehealth_session_update'),
    
    # Report URLs
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/add/', views.ReportCreateView.as_view(), name='report_create'),
    path('reports/<int:pk>/edit/', views.ReportUpdateView.as_view(), name='report_update'),
    path('reports/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report_delete'),
    path('reports/<int:pk>/generate/', views.ReportGenerateView.as_view(), name='report_generate'),
    path('report-results/<int:pk>/', views.ReportResultView.as_view(), name='report_result'),
]