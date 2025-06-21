from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)
    blood_type = models.CharField(max_length=5, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    condition = models.CharField(max_length=255)
    diagnosis_date = models.DateField()
    severity = models.CharField(max_length=100, blank=True)
    is_chronic = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient}'s {self.condition}"

class Allergy(models.Model):
    SEVERITY_CHOICES = [
        ('Mild', 'Mild'),
        ('Moderate', 'Moderate'),
        ('Severe', 'Severe'),
        ('Life-threatening', 'Life-threatening'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allergies')
    allergen = models.CharField(max_length=255)
    reaction = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    onset_date = models.DateField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient}'s allergy to {self.allergen}"

class Immunization(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='immunizations')
    vaccine = models.CharField(max_length=255)
    administration_date = models.DateField()
    next_dose_date = models.DateField(null=True, blank=True)
    administered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    lot_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient}'s {self.vaccine} immunization"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No-Show', 'No-Show'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_appointments')
    date_time = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.patient} with {self.provider} on {self.date_time}"

class Prescription(models.Model):
    FREQUENCY_CHOICES = [
        ('QD', 'Once daily'),
        ('BID', 'Twice daily'),
        ('TID', 'Three times daily'),
        ('QID', 'Four times daily'),
        ('QHS', 'At bedtime'),
        ('PRN', 'As needed'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    prescriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescribed_meds')
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    refills = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medication} for {self.patient}"

class LabTest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COLLECTED', 'Collected'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_tests')
    ordering_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_tests')
    test_name = models.CharField(max_length=255)
    test_date = models.DateTimeField()
    lab_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.test_name} for {self.patient}"

    def get_status_class(self):
        return self.status.lower()
    

class LabResult(models.Model):
    lab_test = models.OneToOneField(LabTest, on_delete=models.CASCADE, related_name='result')
    result_date = models.DateTimeField()
    result_value = models.CharField(max_length=100)
    reference_range = models.CharField(max_length=100)
    units = models.CharField(max_length=50)
    abnormal_flag = models.BooleanField(default=False)
    interpretation = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Results for {self.lab_test}"

class ImagingStudy(models.Model):
    STATUS_PENDING = 'Pending'
    STATUS_COMPLETED = 'Completed'
    STATUS_CANCELLED = 'Cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='imaging_studies')
    ordering_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordered_studies')
    study_type = models.CharField(max_length=255)
    study_date = models.DateTimeField()
    facility = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default=STATUS_PENDING
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.study_type} for {self.patient}"

class ImagingResult(models.Model):
    imaging_study = models.OneToOneField(ImagingStudy, on_delete=models.CASCADE, related_name='result')
    result_date = models.DateTimeField()
    findings = models.TextField()
    impression = models.TextField()
    radiologist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_results')
    reviewed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Results for {self.imaging_study}"

class BillingRecord(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Denied', 'Denied'),
        ('Appealed', 'Appealed'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='billing_records')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    service_date = models.DateField()
    service_description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    insurance_claim = models.BooleanField(default=False)
    claim_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Billing record #{self.id} for {self.patient}"

class InsurancePolicy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='insurance_policies')
    provider_name = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=100)
    group_number = models.CharField(max_length=100, blank=True)
    subscriber_name = models.CharField(max_length=255)
    relationship_to_patient = models.CharField(max_length=100)
    coverage_start_date = models.DateField()
    coverage_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider_name} policy for {self.patient}"

class TreatmentPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatment_plans')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_treatment_plans')
    diagnosis = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    goals = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Treatment plan for {self.patient}'s {self.diagnosis}"

class ProgressNote(models.Model):
    treatment_plan = models.ForeignKey(TreatmentPlan, on_delete=models.CASCADE, related_name='progress_notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_notes')
    note_date = models.DateTimeField()
    subjective = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    plan = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress note for {self.treatment_plan} on {self.note_date}"

class Alert(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_alerts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class UserAlert(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='user_alerts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('alert', 'user')

    def __str__(self):
        return f"{self.alert} for {self.user}"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TelehealthSession(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='telehealth_sessions')
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telehealth_sessions')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    session_date = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    join_url = models.URLField(blank=True)
    recording_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Telehealth session for {self.patient} with {self.provider}"

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('PATIENT_LIST', 'Patient List'),
        ('APPOINTMENT_STATS', 'Appointment Statistics'),
        ('BILLING_SUMMARY', 'Billing Summary'),
        ('PRESCRIPTION_ANALYSIS', 'Prescription Analysis'),
        ('CUSTOM', 'Custom Report')
    ]
    
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ReportParameter(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='parameters')
    name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=50)
    is_required = models.BooleanField(default=True)
    default_value = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} for {self.report}"

class ReportResult(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='results')
    parameters = models.JSONField()
    result_data = models.JSONField()
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_reports')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Results for {self.report} generated at {self.generated_at}"
    

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name}"