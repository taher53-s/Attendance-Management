from django import forms
from .models import Student, AttendanceRecord

class StudentEnrollmentForm(forms.ModelForm):
    YEAR_CHOICES = [(year, year) for year in range(2025, 2036)]
    year_of_passing = forms.ChoiceField(
        choices=YEAR_CHOICES,
        label="Year of Passing",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = ['name', 'app_id', 'year_of_passing', 'course']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'app_id': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_app_id(self):
        """Custom validation logic using model-level regex."""
        app_id = self.cleaned_data.get('app_id')
        if len(str(app_id)) != 7:
            raise forms.ValidationError("App ID must be exactly 7 digits.")
        return app_id

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['student', 'subject', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
