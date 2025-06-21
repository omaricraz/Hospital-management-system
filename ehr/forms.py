from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import *

User = get_user_model()

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = '__all__'
        widgets = {
            'diagnosis_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].disabled = True

class AllergyForm(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = '__all__'
        widgets = {
            'onset_date': forms.DateInput(attrs={'type': 'date'}),
            'reaction': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].disabled = True

class ImmunizationForm(forms.ModelForm):
    class Meta:
        model = Immunization
        fields = '__all__'
        widgets = {
            'administration_date': forms.DateInput(attrs={'type': 'date'}),
            'next_dose_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].disabled = True
        self.fields['administered_by'].disabled = True

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'patient' in self.initial:
            self.fields['patient'].disabled = True
        if 'provider' in self.initial:
            self.fields['provider'].disabled = True
    
    def clean_date_time(self):
        date_time = self.cleaned_data['date_time']
        if date_time < timezone.now():
            raise ValidationError("Appointment date/time cannot be in the past.")
        return date_time

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'patient' in self.initial:
            self.fields['patient'].disabled = True
        self.fields['prescriber'].disabled = True
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if end_date and start_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date.")
        
        return cleaned_data

class LabTestForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = '__all__'
        widgets = {
            'test_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'patient' in self.initial:
            self.fields['patient'].disabled = True
        self.fields['ordering_provider'].disabled = True

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = '__all__'
        widgets = {
            'result_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'interpretation': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lab_test'].disabled = True
        self.fields['reviewed_by'].disabled = True

class ImagingStudyForm(forms.ModelForm):
    class Meta:
        model = ImagingStudy
        fields = '__all__'
        widgets = {
            'study_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'patient' in self.initial:
            self.fields['patient'].disabled = True
        self.fields['ordering_provider'].disabled = True

class ImagingResultForm(forms.ModelForm):
    class Meta:
        model = ImagingResult
        fields = '__all__'
        widgets = {
            'result_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'findings': forms.Textarea(attrs={'rows': 5}),
            'impression': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imaging_study'].disabled = True
        self.fields['radiologist'].disabled = True
        self.fields['reviewed_by'].disabled = True

class BillingRecordForm(forms.ModelForm):
    class Meta:
        model = BillingRecord
        fields = '__all__'
        widgets = {
            'service_date': forms.DateInput(attrs={'type': 'date'}),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'patient' in self.initial:
            self.fields['patient'].disabled = True
        if 'appointment' in self.initial:
            self.fields['appointment'].disabled = True

class InsurancePolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = '__all__'
        widgets = {
            'coverage_start_date': forms.DateInput(attrs={'type': 'date'}),
            'coverage_end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'patient' in self.initial:
            self.fields['patient'].disabled = True
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('coverage_start_date')
        end_date = cleaned_data.get('coverage_end_date')
        
        if end_date and start_date and end_date < start_date:
            raise ValidationError("Coverage end date cannot be before start date.")
        
        return cleaned_data

class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TreatmentPlan
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'goals': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'patient' in self.initial:
            self.fields['patient'].disabled = True
        self.fields['provider'].disabled = True
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if end_date and start_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date.")
        
        return cleaned_data

class ProgressNoteForm(forms.ModelForm):
    class Meta:
        model = ProgressNote
        fields = '__all__'
        widgets = {
            'note_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'subjective': forms.Textarea(attrs={'rows': 3}),
            'objective': forms.Textarea(attrs={'rows': 3}),
            'assessment': forms.Textarea(attrs={'rows': 3}),
            'plan': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['treatment_plan'].disabled = True
        self.fields['author'].disabled = True

class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = '__all__'
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].disabled = True
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if end_date and start_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date.")
        
        return cleaned_data

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['created_by'].disabled = True
    
    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date < timezone.now():
            raise ValidationError("Due date cannot be in the past.")
        return due_date

class TelehealthSessionForm(forms.ModelForm):
    class Meta:
        model = TelehealthSession
        fields = '__all__'
        widgets = {
            'session_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'patient' in self.initial:
            self.fields['patient'].disabled = True
        if 'appointment' in self.initial:
            self.fields['appointment'].disabled = True
        if 'provider' in self.initial:
            self.fields['provider'].disabled = True
    
    def clean_session_date(self):
        session_date = self.cleaned_data['session_date']
        if session_date < timezone.now():
            raise ValidationError("Session date/time cannot be in the past.")
        return session_date

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'report_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if Report.objects.filter(title=title).exists():
            raise forms.ValidationError("A report with this title already exists.")
        return title

class ReportParameterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.report = kwargs.pop('report')
        super().__init__(*args, **kwargs)
        
        # Add date fields with proper validation
        self.fields['from_date'] = forms.DateField(
            label='From Date',
            required=False,
            widget=forms.DateInput(attrs={'type': 'date'})
        )
        self.fields['to_date'] = forms.DateField(
            label='To Date',
            required=False,
            widget=forms.DateInput(attrs={'type': 'date'}),
            validators=[self.validate_date_range]
        )
    
    def validate_date_range(self, value):
        """Ensure to_date is after from_date if both exist"""
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        
        if from_date and to_date and to_date < from_date:
            raise forms.ValidationError("To date must be after from date")
        return value
    

from django import forms
from .models import ContactSubmission  # Make sure to import the model

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email',
                'class': 'form-control'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject',
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Your Message', 
                'rows': 5,
                'class': 'form-control'
            }),
        }