from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Sum, Avg
from datetime import datetime, timedelta
from django.views.generic import TemplateView

from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import ContactSubmission

from .models import *
from .forms import *


class HomeView(TemplateView):
    template_name = 'ehr/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context data you want to pass to the template
        return context

# Base permission mixins
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ['ADMIN', 'DOCTOR', 'NURSE', 'STAFF']

class DoctorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in ['ADMIN', 'DOCTOR']

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

# Patient Views
class PatientListView(StaffRequiredMixin, ListView):
    model = Patient
    template_name = 'ehr/patient/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(phone_number__icontains=search_query)
            )
        
        return queryset.order_by('last_name', 'first_name')

class PatientDetailView(StaffRequiredMixin, DetailView):
    model = Patient
    template_name = 'ehr/patient/patient_detail.html'
    context_object_name = 'patient'

class PatientCreateView(StaffRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'ehr/patient/patient_form.html'
    success_url = reverse_lazy('patient_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Patient record created successfully.')
        return super().form_valid(form)

class PatientUpdateView(StaffRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'ehr/patient/patient_form.html'
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Patient record updated successfully.')
        return super().form_valid(form)

class PatientDeleteView(AdminRequiredMixin, DeleteView):
    model = Patient
    template_name = 'ehr/patient/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Patient record deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Medical History Views
class MedicalHistoryCreateView(DoctorRequiredMixin, CreateView):
    model = MedicalHistory
    form_class = MedicalHistoryForm
    template_name = 'ehr/patient/medical_history_form.html'
    
    def get_initial(self):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return {'patient': patient}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Medical history added successfully.')
        return super().form_valid(form)

class MedicalHistoryUpdateView(DoctorRequiredMixin, UpdateView):
    model = MedicalHistory
    form_class = MedicalHistoryForm
    template_name = 'ehr/patient/medical_history_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Medical history updated successfully.')
        return super().form_valid(form)

class MedicalHistoryDeleteView(DoctorRequiredMixin, DeleteView):
    model = MedicalHistory
    template_name = 'ehr/patient/medical_history_confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Medical history deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Allergy Views
class AllergyCreateView(StaffRequiredMixin, CreateView):
    model = Allergy
    form_class = AllergyForm
    template_name = 'ehr/patient/allergy_form.html'
    
    def get_initial(self):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return {'patient': patient}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Allergy record added successfully.')
        return super().form_valid(form)

class AllergyUpdateView(StaffRequiredMixin, UpdateView):
    model = Allergy
    form_class = AllergyForm
    template_name = 'ehr/patient/allergy_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Allergy record updated successfully.')
        return super().form_valid(form)

class AllergyDeleteView(StaffRequiredMixin, DeleteView):
    model = Allergy
    template_name = 'ehr/patient/allergy_confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Allergy record deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Immunization Views
class ImmunizationCreateView(StaffRequiredMixin, CreateView):
    model = Immunization
    form_class = ImmunizationForm
    template_name = 'ehr/patient/immunization_form.html'
    
    def get_initial(self):
        patient = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return {'patient': patient, 'administered_by': self.request.user}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Immunization record added successfully.')
        return super().form_valid(form)

class ImmunizationUpdateView(StaffRequiredMixin, UpdateView):
    model = Immunization
    form_class = ImmunizationForm
    template_name = 'ehr/patient/immunization_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Immunization record updated successfully.')
        return super().form_valid(form)

class ImmunizationDeleteView(StaffRequiredMixin, DeleteView):
    model = Immunization
    template_name = 'ehr/patient/immunization_confirm_delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Immunization record deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Appointment Views
class AppointmentListView(StaffRequiredMixin, ListView):
    model = Appointment
    template_name = 'ehr/appointment/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by date if provided
        date_filter = self.request.GET.get('date')
        if date_filter:
            queryset = queryset.filter(date_time__date=date_filter)
        
        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by provider if not admin
        if self.request.user.role != 'ADMIN':
            queryset = queryset.filter(provider=self.request.user)
        
        return queryset.order_by('date_time')

class AppointmentDetailView(StaffRequiredMixin, DetailView):
    model = Appointment
    template_name = 'ehr/appointment/appointment_detail.html'
    context_object_name = 'appointment'

class AppointmentCreateView(StaffRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'ehr/appointment/appointment_form.html'
    success_url = reverse_lazy('appointment_list')
    
    def get_initial(self):
        initial = super().get_initial()
        if 'patient_id' in self.kwargs:
            initial['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        if self.request.user.role in ['DOCTOR', 'NURSE']:
            initial['provider'] = self.request.user
        return initial
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Appointment created successfully.')
        return super().form_valid(form)

class AppointmentUpdateView(StaffRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'ehr/appointment/appointment_form.html'
    
    def get_success_url(self):
        return reverse_lazy('appointment_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Appointment updated successfully.')
        return super().form_valid(form)

class AppointmentDeleteView(StaffRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'ehr/appointment/appointment_confirm_delete.html'
    success_url = reverse_lazy('appointment_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Appointment deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Prescription Views
class PrescriptionListView(StaffRequiredMixin, ListView):
    model = Prescription
    template_name = 'ehr/prescription/prescription_list.html'
    context_object_name = 'prescriptions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by patient if provided
        patient_id = self.request.GET.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Filter by prescriber if not admin
        if self.request.user.role != 'ADMIN':
            queryset = queryset.filter(prescriber=self.request.user)
        
        return queryset.order_by('-start_date')

class PrescriptionDetailView(StaffRequiredMixin, DetailView):
    model = Prescription
    template_name = 'ehr/prescription/prescription_detail.html'
    context_object_name = 'prescription'

class PrescriptionCreateView(DoctorRequiredMixin, CreateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'ehr/prescription/prescription_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        if 'patient_id' in self.kwargs:
            patient = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
            initial['patient'] = patient
        initial['prescriber'] = self.request.user
        return initial
    
    def get_success_url(self):
        return reverse_lazy('prescription_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Prescription created successfully.')
        return super().form_valid(form)

class PrescriptionUpdateView(DoctorRequiredMixin, UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'ehr/prescription/prescription_form.html'
    
    def get_success_url(self):
        return reverse_lazy('prescription_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Prescription updated successfully.')
        return super().form_valid(form)

class PrescriptionDeleteView(DoctorRequiredMixin, DeleteView):
    model = Prescription
    template_name = 'ehr/prescription/prescription_confirm_delete.html'
    success_url = reverse_lazy('prescription_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Prescription deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Lab Test Views
class LabTestListView(StaffRequiredMixin, ListView):
    model = LabTest
    template_name = 'ehr/lab_test/lab_test_list.html'
    context_object_name = 'lab_tests'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by patient if provided
        patient_id = self.request.GET.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by ordering provider if not admin
        if self.request.user.role != 'ADMIN':
            queryset = queryset.filter(ordering_provider=self.request.user)
        
        return queryset.order_by('-test_date')

class LabTestDetailView(StaffRequiredMixin, DetailView):
    model = LabTest
    template_name = 'ehr/lab_test/lab_test_detail.html'
    context_object_name = 'lab_test'

class LabTestCreateView(DoctorRequiredMixin, CreateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'ehr/lab_test/lab_test_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        if 'patient_id' in self.kwargs:
            initial['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        initial['ordering_provider'] = self.request.user
        return initial
    
    def get_success_url(self):
        return reverse_lazy('lab_test_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Lab test ordered successfully.')
        return super().form_valid(form)

class LabTestUpdateView(DoctorRequiredMixin, UpdateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'ehr/lab_test/lab_test_form.html'
    
    def get_success_url(self):
        return reverse_lazy('lab_test_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Lab test updated successfully.')
        return super().form_valid(form)

class LabTestDeleteView(DoctorRequiredMixin, DeleteView):
    model = LabTest
    template_name = 'ehr/lab_test/lab_test_confirm_delete.html'
    success_url = reverse_lazy('lab_test_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Lab test deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Lab Result Views
class LabResultCreateView(StaffRequiredMixin, CreateView):
    model = LabResult
    form_class = LabResultForm
    template_name = 'ehr/lab_test/lab_result_form.html'
    
    def get_initial(self):
        lab_test = get_object_or_404(LabTest, pk=self.kwargs['lab_test_id'])
        return {
            'lab_test': lab_test,
            'reviewed_by': self.request.user
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab_test'] = get_object_or_404(LabTest, pk=self.kwargs['lab_test_id'])
        return context
    
    def get_success_url(self):
        return reverse('lab_test_detail', kwargs={'pk': self.object.lab_test.pk})
    
    def form_valid(self, form):
        form.instance.lab_test.status = 'Completed'
        form.instance.lab_test.save()
        messages.success(self.request, 'Lab results added successfully.')
        return super().form_valid(form)
    
class LabResultUpdateView(StaffRequiredMixin, UpdateView):
    model = LabResult
    form_class = LabResultForm
    template_name = 'ehr/lab_test/lab_result_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lab_test'] = self.object.lab_test  # Add the lab_test to context
        return context

    def get_success_url(self):
        return reverse('lab_test_detail', kwargs={'pk': self.object.lab_test.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Lab results updated successfully.')
        return super().form_valid(form)

class LabResultUpdateView(StaffRequiredMixin, UpdateView):
    model = LabResult
    form_class = LabResultForm
    template_name = 'ehr/lab_test/lab_result_form.html'
    
    def get_success_url(self):
        return reverse_lazy('lab_test_detail', kwargs={'pk': self.object.lab_test.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Lab results updated successfully.')
        return super().form_valid(form)

class LabResultDeleteView(StaffRequiredMixin, DeleteView):
    model = LabResult
    template_name = 'ehr/lab_test/lab_result_confirm_delete.html'
    
    def get_success_url(self):
        lab_test = self.object.lab_test
        lab_test.status = 'Pending'
        lab_test.save()
        return reverse_lazy('lab_test_detail', kwargs={'pk': lab_test.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Lab results deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Imaging Study Views
class ImagingStudyListView(StaffRequiredMixin, ListView):
    model = ImagingStudy
    template_name = 'ehr/imaging/imaging_study_list.html'
    context_object_name = 'imaging_studies'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('patient', 'ordering_provider')
        
        # Filter by patient if provided
        patient_id = self.request.GET.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by ordering provider if not admin
        if self.request.user.role != 'ADMIN':
            queryset = queryset.filter(ordering_provider=self.request.user)
        
        return queryset.order_by('-study_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the status choices to context
        context['status_choices'] = [
            ('', 'All Statuses'),
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled'),
        ]
        return context

class ImagingStudyDetailView(StaffRequiredMixin, DetailView):
    model = ImagingStudy
    template_name = 'ehr/imaging/imaging_study_detail.html'
    context_object_name = 'imaging_study'
    
    def get_queryset(self):
        return super().get_queryset().select_related('patient', 'ordering_provider')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = (
            self.request.user.role in ['ADMIN', 'DOCTOR'] and 
            self.object.status != 'COMPLETED'
        )
        return context

class ImagingStudyCreateView(DoctorRequiredMixin, CreateView):
    model = ImagingStudy
    form_class = ImagingStudyForm
    template_name = 'ehr/imaging/imaging_study_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        if 'patient_id' in self.kwargs:
            initial['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        initial['ordering_provider'] = self.request.user
        initial['status'] = 'PENDING'
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['providers'] = User.objects.filter(role__in=['DOCTOR', 'ADMIN'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('imaging_study_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.ordering_provider = self.request.user
        messages.success(self.request, 'Imaging study ordered successfully.')
        return super().form_valid(form)

class ImagingStudyUpdateView(DoctorRequiredMixin, UpdateView):
    model = ImagingStudy
    form_class = ImagingStudyForm
    template_name = 'ehr/imaging/imaging_study_form.html'
    
    def get_queryset(self):
        return super().get_queryset().filter(
            ordering_provider=self.request.user
        ) if self.request.user.role != 'ADMIN' else super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['providers'] = User.objects.filter(role__in=['DOCTOR', 'ADMIN'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('imaging_study_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Imaging study updated successfully.')
        return super().form_valid(form)

class ImagingStudyDeleteView(DoctorRequiredMixin, DeleteView):
    model = ImagingStudy
    template_name = 'ehr/imaging/imaging_study_confirm_delete.html'
    success_url = reverse_lazy('imaging_study_list')
    
    def get_queryset(self):
        return super().get_queryset().filter(
            ordering_provider=self.request.user,
            status='PENDING'
        ) if self.request.user.role != 'ADMIN' else super().get_queryset()
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Imaging study deleted successfully.')
        return response

# Imaging Result Views

class ImagingResultCreateView(CreateView):
    model = ImagingResult
    form_class = ImagingResultForm
    template_name = 'ehr/imaging/imaging_result_form.html'

    def get_initial(self):
        initial = super().get_initial()
        imaging_study_pk = self.kwargs.get('imaging_study_pk')
        if imaging_study_pk:
            imaging_study = get_object_or_404(ImagingStudy, pk=imaging_study_pk)
            initial.update({
                'imaging_study': imaging_study,
                'radiologist': self.request.user,
                'reviewed_by': self.request.user,
            })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imaging_study_pk = self.kwargs.get('imaging_study_pk')
        if imaging_study_pk:
            context['imaging_study'] = get_object_or_404(ImagingStudy, pk=imaging_study_pk)
        return context

    def form_valid(self, form):
        form.instance.imaging_study = get_object_or_404(
            ImagingStudy, 
            pk=self.kwargs.get('imaging_study_pk')
        )
        form.instance.radiologist = self.request.user
        form.instance.reviewed_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('imaging_study_detail', kwargs={'pk': self.kwargs.get('imaging_study_pk')})

class ImagingResultUpdateView(LoginRequiredMixin, UpdateView):
    model = ImagingResult
    form_class = ImagingResultForm
    template_name = 'ehr/imaging/imaging_result_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imaging_study'] = self.object.imaging_study
        return context
    
    def get_success_url(self):
        return reverse('imaging_study_detail', kwargs={'pk': self.object.imaging_study.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Imaging results updated successfully.')
        return super().form_valid(form)

class ImagingResultDeleteView(LoginRequiredMixin, DeleteView):
    model = ImagingResult
    template_name = 'ehr/imaging/imaging_result_confirm_delete.html'
    
    def get_success_url(self):
        imaging_study = self.object.imaging_study
        imaging_study.status = 'Pending'
        imaging_study.save()
        return reverse('imaging_study_detail', kwargs={'pk': imaging_study.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Imaging results deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Billing Views
class BillingRecordListView(StaffRequiredMixin, ListView):
    model = BillingRecord
    template_name = 'ehr/billing/billing_record_list.html'
    context_object_name = 'billing_records'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by patient if provided
        patient_id = self.request.GET.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-service_date')

class BillingRecordDetailView(StaffRequiredMixin, DetailView):
    model = BillingRecord
    template_name = 'ehr/billing/billing_record_detail.html'
    context_object_name = 'billing_record'

class BillingRecordCreateView(StaffRequiredMixin, CreateView):
    model = BillingRecord
    form_class = BillingRecordForm
    template_name = 'ehr/billing/billing_record_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        if 'patient_id' in self.kwargs:
            initial['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        if 'appointment_id' in self.kwargs:
            initial['appointment'] = get_object_or_404(Appointment, pk=self.kwargs['appointment_id'])
        return initial
    
    def get_success_url(self):
        return reverse_lazy('billing_record_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Billing record created successfully.')
        return super().form_valid(form)

class BillingRecordUpdateView(StaffRequiredMixin, UpdateView):
    model = BillingRecord
    form_class = BillingRecordForm
    template_name = 'ehr/billing/billing_record_form.html'
    
    def get_success_url(self):
        return reverse_lazy('billing_record_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Billing record updated successfully.')
        return super().form_valid(form)

class BillingRecordDeleteView(StaffRequiredMixin, DeleteView):
    model = BillingRecord
    template_name = 'ehr/billing/billing_record_confirm_delete.html'
    success_url = reverse_lazy('billing_record_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Billing record deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Insurance Policy Views
class InsurancePolicyListView(StaffRequiredMixin, ListView):
    model = InsurancePolicy
    template_name = 'ehr/insurance/insurance_policy_list.html'
    context_object_name = 'insurance_policies'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by patient if provided
        patient_id = self.request.GET.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        return queryset.order_by('-coverage_start_date')

class InsurancePolicyDetailView(StaffRequiredMixin, DetailView):
    model = InsurancePolicy
    template_name = 'ehr/insurance/insurance_policy_detail.html'
    context_object_name = 'insurance_policy'

class InsurancePolicyCreateView(StaffRequiredMixin, CreateView):
    model = InsurancePolicy
    form_class = InsurancePolicyForm
    template_name = 'ehr/insurance/insurance_policy_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        if 'patient_id' in self.kwargs:
            initial['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        return initial
    
    def get_success_url(self):
        return reverse_lazy('insurance_policy_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Insurance policy added successfully.')
        return super().form_valid(form)

class InsurancePolicyUpdateView(StaffRequiredMixin, UpdateView):
    model = InsurancePolicy
    form_class = InsurancePolicyForm
    template_name = 'ehr/insurance/insurance_policy_form.html'
    
    def get_success_url(self):
        return reverse_lazy('insurance_policy_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Insurance policy updated successfully.')
        return super().form_valid(form)

class InsurancePolicyDeleteView(StaffRequiredMixin, DeleteView):
    model = InsurancePolicy
    template_name = 'ehr/insurance/insurance_policy_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('insurance_policy_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Insurance policy deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Treatment Plan Views
class TreatmentPlanListView(StaffRequiredMixin, ListView):
    model = TreatmentPlan
    template_name = 'ehr/treatment/treatment_plan_list.html'
    context_object_name = 'treatment_plans'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by patient if provided
        patient_id = self.request.GET.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Filter by provider if not admin
        if self.request.user.role != 'ADMIN':
            queryset = queryset.filter(provider=self.request.user)
        
        return queryset.order_by('-start_date')

class TreatmentPlanDetailView(StaffRequiredMixin, DetailView):
    model = TreatmentPlan
    template_name = 'ehr/treatment/treatment_plan_detail.html'
    context_object_name = 'treatment_plan'

class TreatmentPlanCreateView(DoctorRequiredMixin, CreateView):
    model = TreatmentPlan
    form_class = TreatmentPlanForm
    template_name = 'ehr/treatment/treatment_plan_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        if 'patient_id' in self.kwargs:
            initial['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        initial['provider'] = self.request.user
        return initial
    
    def get_success_url(self):
        return reverse_lazy('treatment_plan_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Treatment plan created successfully.')
        return super().form_valid(form)

class TreatmentPlanUpdateView(DoctorRequiredMixin, UpdateView):
    model = TreatmentPlan
    form_class = TreatmentPlanForm
    template_name = 'ehr/treatment/treatment_plan_form.html'
    
    def get_success_url(self):
        return reverse_lazy('treatment_plan_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Treatment plan updated successfully.')
        return super().form_valid(form)

class TreatmentPlanDeleteView(DoctorRequiredMixin, DeleteView):
    model = TreatmentPlan
    template_name = 'ehr/treatment/treatment_plan_confirm_delete.html'
    success_url = reverse_lazy('treatment_plan_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Treatment plan deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Progress Note Views
class ProgressNoteCreateView(StaffRequiredMixin, CreateView):
    model = ProgressNote
    form_class = ProgressNoteForm
    template_name = 'ehr/treatment/progress_note_form.html'
    
    def get_initial(self):
        treatment_plan = get_object_or_404(TreatmentPlan, pk=self.kwargs['treatment_plan_id'])
        return {
            'treatment_plan': treatment_plan,
            'author': self.request.user
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['treatment_plan_id'] = self.kwargs['treatment_plan_id']
        return context
    
    def get_success_url(self):
        return reverse_lazy('treatment_plan_detail', kwargs={'pk': self.object.treatment_plan.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Progress note added successfully.')
        return super().form_valid(form)

class ProgressNoteUpdateView(StaffRequiredMixin, UpdateView):
    model = ProgressNote
    form_class = ProgressNoteForm
    template_name = 'ehr/treatment/progress_note_form.html'
    
    def get_success_url(self):
        return reverse_lazy('treatment_plan_detail', kwargs={'pk': self.object.treatment_plan.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Progress note updated successfully.')
        return super().form_valid(form)

class ProgressNoteDeleteView(StaffRequiredMixin, DeleteView):
    model = ProgressNote
    template_name = 'ehr/treatment/progress_note_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('treatment_plan_detail', kwargs={'pk': self.object.treatment_plan.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Progress note deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Alert Views
class AlertListView(StaffRequiredMixin, ListView):
    model = Alert
    template_name = 'ehr/alert/alert_list.html'
    context_object_name = 'alerts'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        # Filter by priority if provided
        priority_filter = self.request.GET.get('priority')
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        return queryset.order_by('-start_date')

class AlertDetailView(StaffRequiredMixin, DetailView):
    model = Alert
    template_name = 'ehr/alert/alert_detail.html'
    context_object_name = 'alert'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alert = self.object
        context['total_recipients'] = alert.user_alerts.count()
        context['read_count'] = alert.user_alerts.filter(is_read=True).count()
        context['unread_count'] = alert.user_alerts.filter(is_read=False).count()
        return context

class AlertCreateView(StaffRequiredMixin, CreateView):
    model = Alert
    form_class = AlertForm
    template_name = 'ehr/alert/alert_form.html'
    success_url = reverse_lazy('alert_list')
    
    def get_initial(self):
        return {'created_by': self.request.user}
    
    def form_valid(self, form):
        messages.success(self.request, 'Alert created successfully.')
        return super().form_valid(form)

class AlertUpdateView(StaffRequiredMixin, UpdateView):
    model = Alert
    form_class = AlertForm
    template_name = 'ehr/alert/alert_form.html'
    success_url = reverse_lazy('alert_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Alert updated successfully.')
        return super().form_valid(form)

class AlertDeleteView(StaffRequiredMixin, DeleteView):
    model = Alert
    template_name = 'ehr/alert/alert_confirm_delete.html'
    success_url = reverse_lazy('alert_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Alert deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Task Views
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'ehr/task/task_list.html'
    context_object_name = 'task_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # For debugging, temporarily remove all filters
        print("Raw queryset count:", queryset.count())  # Debug line
        
        return queryset.order_by('due_date')

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'ehr/task/task_detail.html'
    context_object_name = 'task'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Users can only see their own tasks unless they're admin
        if self.request.user.role != 'ADMIN':
            queryset = queryset.filter(assigned_to=self.request.user)
        return queryset

class TaskCreateView(StaffRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'ehr/task/task_form.html'
    success_url = reverse_lazy('task_list')
    
    def get_initial(self):
        return {'created_by': self.request.user}
    
    def form_valid(self, form):
        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'ehr/task/task_form.html'
    
    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Users can only update their own tasks unless they're admin
        if self.request.user.role != 'ADMIN':
            queryset = queryset.filter(assigned_to=self.request.user)
        return queryset
    
    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully.')
        return super().form_valid(form)
    
def task_update_status(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk)
        if request.user == task.assigned_to or request.user.is_staff:
            new_status = request.POST.get('status')
            task.status = new_status
            task.save()
            messages.success(request, 'Task status updated successfully!')
        else:
            messages.error(request, 'You are not authorized to update this task.')
    return redirect('task_detail', pk=pk)

class TaskDeleteView(StaffRequiredMixin, DeleteView):
    model = Task
    template_name = 'ehr/task/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Task deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Telehealth Views
class TelehealthSessionListView(StaffRequiredMixin, ListView):
    model = TelehealthSession
    template_name = 'ehr/telehealth/telehealth_session_list.html'
    context_object_name = 'telehealth_sessions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by provider if not admin
        if self.request.user.role != 'ADMIN':
            queryset = queryset.filter(provider=self.request.user)
        
        return queryset.order_by('-session_date')

class TelehealthSessionDetailView(StaffRequiredMixin, DetailView):
    model = TelehealthSession
    template_name = 'ehr/telehealth/telehealth_session_detail.html'
    context_object_name = 'telehealth_session'

class TelehealthSessionCreateView(StaffRequiredMixin, CreateView):
    model = TelehealthSession
    form_class = TelehealthSessionForm
    template_name = 'ehr/telehealth/telehealth_session_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        if 'patient_id' in self.kwargs:
            initial['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_id'])
        if 'appointment_id' in self.kwargs:
            initial['appointment'] = get_object_or_404(Appointment, pk=self.kwargs['appointment_id'])
        if self.request.user.role in ['DOCTOR', 'NURSE']:
            initial['provider'] = self.request.user
        return initial
    
    def get_success_url(self):
        return reverse_lazy('telehealth_session_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Telehealth session scheduled successfully.')
        return super().form_valid(form)

class TelehealthSessionUpdateView(StaffRequiredMixin, UpdateView):
    model = TelehealthSession
    form_class = TelehealthSessionForm
    template_name = 'ehr/telehealth/telehealth_session_form.html'
    
    def get_success_url(self):
        return reverse_lazy('telehealth_session_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Telehealth session updated successfully.')
        return super().form_valid(form)

class TelehealthSessionDeleteView(StaffRequiredMixin, DeleteView):
    model = TelehealthSession
    template_name = 'ehr/telehealth/telehealth_session_confirm_delete.html'
    
    def get_success_url(self):
        # Redirect to the list view after deletion
        return reverse_lazy('telehealth_session_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Telehealth session deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Report Views
class ReportListView(StaffRequiredMixin, ListView):
    model = Report
    template_name = 'ehr/report/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by type if provided
        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(report_type=type_filter)
        
        return queryset.order_by('title')

class ReportDetailView(StaffRequiredMixin, DetailView):
    model = Report
    template_name = 'ehr/report/report_detail.html'
    context_object_name = 'report'

class ReportCreateView(AdminRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'ehr/report/report_form.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Report created successfully!')
        return reverse_lazy('report_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ReportUpdateView(AdminRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'ehr/report/report_form.html'
    success_url = reverse_lazy('report_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Report template updated successfully.')
        return super().form_valid(form)

class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'ehr/report/report_confirm_delete.html'
    success_url = reverse_lazy('report_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Report template deleted successfully.')
        return super().delete(request, *args, **kwargs)

class ReportGenerateView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        report = get_object_or_404(Report, pk=self.kwargs['pk'])
        form = ReportParameterForm(report=report)
        return render(request, 'ehr/report/report_generate.html', {'report': report, 'form': form})
    
    def post(self, request, *args, **kwargs):
        report = get_object_or_404(Report, pk=self.kwargs['pk'])
        form = ReportParameterForm(report=report, data=request.POST)
        
        if form.is_valid():
            # Process the report with the given parameters
            parameters = form.cleaned_data
            result_data = self.generate_report(report, parameters)
            
            # Save the report result
            report_result = ReportResult.objects.create(
                report=report,
                parameters=parameters,
                result_data=result_data,
                generated_by=request.user
            )
            
            return render(request, 'ehr/report/report_result.html', {
                'report': report,
                'result': report_result,
                'data': result_data
            })
        
        return render(request, 'ehr/report/report_generate.html', {'report': report, 'form': form})
    
    def generate_report(self, report, parameters):
        # This is a placeholder for actual report generation logic
        # In a real implementation, this would query the database based on parameters
        # and format the results appropriately
        
        report_data = {
            'title': report.title,
            'type': report.report_type,
            'parameters': parameters,
            'generated_at': timezone.now().isoformat(),
            'data': {
                'sample_data': [1, 2, 3, 4, 5],
                'description': 'This is a sample report. Actual implementation would generate real data based on parameters.'
            }
        }
        
        return report_data

class ReportResultView(StaffRequiredMixin, DetailView):
    model = ReportResult
    template_name = 'ehr/report/report_result.html'
    context_object_name = 'result'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.object.result_data
        context['report'] = self.object.report
        return context
    
class ReportGenerateView(StaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        report = get_object_or_404(Report, pk=self.kwargs['pk'])
        form = ReportParameterForm(report=report)
        return render(request, 'ehr/report/report_generate.html', 
                    {'report': report, 'form': form})
    
    def post(self, request, *args, **kwargs):
        report = get_object_or_404(Report, pk=self.kwargs['pk'])
        form = ReportParameterForm(report=report, data=request.POST)
        
        if form.is_valid():
            parameters = form.cleaned_data
            result_data = self.generate_report_data(report, parameters)
            
            # Save the report result
            report_result = ReportResult.objects.create(
                report=report,
                parameters=parameters,
                result_data=result_data,
                generated_by=request.user
            )
            
            return redirect('report_result', pk=report_result.pk)
        
        return render(request, 'ehr/report/report_generate.html', 
                    {'report': report, 'form': form})

    def generate_report_data(self, report, parameters):
        """Generate actual report data based on report type"""
        if report.report_type == 'PATIENT_LIST':
            return self.generate_patient_list(parameters)
        elif report.report_type == 'APPOINTMENT_STATS':
            return self.generate_appointment_stats(parameters)
        elif report.report_type == 'BILLING_SUMMARY':
            return self.generate_billing_summary(parameters)
        elif report.report_type == 'PRESCRIPTION_ANALYSIS':
            return self.generate_prescription_analysis(parameters)
        else:
            return {'error': 'Unsupported report type'}

    def generate_patient_list(self, parameters):
        """Generate patient list report"""
        queryset = Patient.objects.all()
        
        # Apply filters from parameters
        if parameters.get('gender'):
            queryset = queryset.filter(gender=parameters['gender'])
        if parameters.get('min_age'):
            min_dob = datetime.now() - timedelta(days=365*int(parameters['min_age']))
            queryset = queryset.filter(date_of_birth__lte=min_dob)
        if parameters.get('max_age'):
            max_dob = datetime.now() - timedelta(days=365*int(parameters['max_age']))
            queryset = queryset.filter(date_of_birth__gte=max_dob)
        
        patients = list(queryset.values(
            'first_name', 'last_name', 'gender', 'date_of_birth', 'phone_number'
        )[:1000])  # Limit to 1000 records
        
        return {
            'report_type': 'patient_list',
            'generated_at': datetime.now().isoformat(),
            'total_patients': queryset.count(),
            'patients': patients,
            'filters': {
                'gender': parameters.get('gender', 'All'),
                'age_range': f"{parameters.get('min_age', '0')}-{parameters.get('max_age', '100+')}"
            }
        }

    def generate_appointment_stats(self, parameters):
        """Generate appointment statistics report"""
        from_date = parameters.get('from_date', datetime.now() - timedelta(days=30))
        to_date = parameters.get('to_date', datetime.now())
        
        stats = Appointment.objects.filter(
            date_time__gte=from_date,
            date_time__lte=to_date
        ).values('status').annotate(
            count=Count('id'),
            duration_avg=Avg('duration')
        )
        
        return {
            'report_type': 'appointment_stats',
            'generated_at': datetime.now().isoformat(),
            'date_range': {
                'from': from_date.isoformat(),
                'to': to_date.isoformat()
            },
            'stats': list(stats),
            'total_appointments': sum(item['count'] for item in stats)
        }

def generate_billing_summary(self, parameters):
    """Generate billing summary report with proper None handling"""
    # Initialize query filters
    filters = {}
    
    # Handle date parameters safely
    if parameters.get('from_date'):
        filters['service_date__gte'] = parameters['from_date']
    if parameters.get('to_date'):
        filters['service_date__lte'] = parameters['to_date']
    
    # Only apply the filter if we have valid conditions
    queryset = BillingRecord.objects.all()
    if filters:
        queryset = queryset.filter(**filters)
    
    # Get the summary data
    summary = queryset.aggregate(
        total_amount=Sum('amount'),
        total_paid=Sum('payment_amount'),
        total_records=Count('id')
    )
    
    # Handle None values in the summary
    for key in ['total_amount', 'total_paid']:
        summary[key] = summary[key] or 0  # Convert None to 0
    
    return {
        'report_type': 'billing_summary',
        'generated_at': timezone.now().isoformat(),
        'date_range': {
            'from': parameters.get('from_date'),
            'to': parameters.get('to_date')
        },
        'summary': summary
    }

from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .models import Appointment, Prescription, UserAlert, Patient, Task

class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        
        if request.user.role == 'PATIENT':
            # Patient dashboard
            try:
                patient = request.user.patient_profile
                context['patient'] = patient
                context['upcoming_appointments'] = Appointment.objects.filter(
                    patient=patient,
                    date_time__gte=timezone.now(),
                    status='Scheduled'
                ).order_by('date_time')[:5]
                context['active_prescriptions'] = Prescription.objects.filter(
                    patient=patient,
                    is_active=True
                ).order_by('-start_date')[:5]
                context['unread_alerts'] = UserAlert.objects.filter(
                    user=request.user,
                    is_read=False
                ).select_related('alert').order_by('-alert__start_date')[:5]
            except Patient.DoesNotExist:
                context['error'] = "Patient profile not found."
        else:
            # Staff dashboard
            context['recent_patients'] = Patient.objects.order_by('-created_at')[:5]
            
            if request.user.role != 'ADMIN':
                context['upcoming_appointments'] = Appointment.objects.filter(
                    provider=request.user,
                    date_time__gte=timezone.now(),
                    status='Scheduled'
                ).order_by('date_time')[:5]
                context['pending_tasks'] = Task.objects.filter(
                    assigned_to=request.user,
                    status__in=['Pending', 'In Progress']
                ).order_by('due_date')[:5]
            
            context['unread_alerts'] = UserAlert.objects.filter(
                user=request.user,
                is_read=False
            ).select_related('alert').order_by('-alert__start_date')[:5]
        
        return render(request, 'ehr/dashboard.html', context)

    

# contact submission
from django.views.decorators.http import require_POST
@require_POST
def contact_view(request):
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'No Subject')
        message = request.POST.get('message')
        
        if not all([name, email, message]):
            return JsonResponse({
                'error': 'Please fill in all required fields'
            }, status=400)
        
        # Send email
        full_message = f"""
        Name: {name}
        Email: {email}
        
        Message:
        {message}
        """
        
        send_mail(
            subject=f"New Contact: {subject}",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
        )
        
        return JsonResponse({
            'message': 'Your message has been sent successfully!'
        })
        
    except Exception as e:
        return JsonResponse({
            'error': 'An error occurred while sending your message. Please try again later.'
        }, status=500)
    
    return render(request, 'ehr/home.html')