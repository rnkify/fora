from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from apps.core.configuration import get_enabled_plans, get_enabled_services
from apps.leads.models import Lead, LeadActivity
from apps.projects.models import Project, ProjectActivity, ProjectTask

INPUT_CLASS = (
    "w-full rounded-fora-sm border border-fora-border "
    "bg-fora-surface px-4 py-3 text-fora-text outline-none "
    "transition focus:border-fora-border-strong"
)


class ProjectDeliveryForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            "status",
            "started_at",
            "due_at",
            "delivered_at",
            "revision_count",
            "notes",
        )
        widgets = {
            "started_at": forms.DateInput(attrs={"type": "date"}),
            "due_at": forms.DateInput(attrs={"type": "date"}),
            "delivered_at": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs["class"] = INPUT_CLASS
            if self.is_bound and name in self.errors:
                field.widget.attrs["aria-invalid"] = "true"
                field.widget.attrs["aria-describedby"] = f"id_{name}_error"

    def clean(self):
        cleaned_data = super().clean()
        started_at = cleaned_data.get("started_at")
        due_at = cleaned_data.get("due_at")
        delivered_at = cleaned_data.get("delivered_at")

        if started_at and due_at and due_at < started_at:
            self.add_error("due_at", "Due date cannot be before the start date.")

        if started_at and delivered_at and delivered_at < started_at:
            self.add_error(
                "delivered_at",
                "Delivery date cannot be before the start date.",
            )

        return cleaned_data


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = ("title", "due_at")
        widgets = {
            "due_at": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs["class"] = INPUT_CLASS
            if self.is_bound and name in self.errors:
                field.widget.attrs["aria-invalid"] = "true"
                field.widget.attrs["aria-describedby"] = f"id_{name}_error"


class TaskStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=ProjectTask.Status.choices,
    )


class ProjectActivityForm(forms.ModelForm):
    class Meta:
        model = ProjectActivity
        fields = ("description",)
        labels = {"description": "Note"}
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["class"] = INPUT_CLASS
        if self.is_bound and "description" in self.errors:
            self.fields["description"].widget.attrs.update({
                "aria-invalid": "true",
                "aria-describedby": "id_description_error",
            })


class StaffAuthenticationForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        "not_staff": "This account does not have access to Fora operations.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASS

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise ValidationError(
                self.error_messages["not_staff"],
                code="not_staff",
            )


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "status",
            "score",
            "estimated_value",
            "service_interest_id",
            "plan_interest_id",
            "next_action_at",
            "notes",
        )
        widgets = {
            "next_action_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 7}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service_interest_id"] = forms.ChoiceField(
            label="Service interest",
            required=False,
            choices=[
                ("", "Not selected"),
                *[(item.id, item.name) for item in get_enabled_services()],
            ],
        )
        self.fields["plan_interest_id"] = forms.ChoiceField(
            label="Plan interest",
            required=False,
            choices=[
                ("", "Not selected"),
                *[(item.id, item.name) for item in get_enabled_plans()],
            ],
        )
        self.fields["score"].help_text = (
            "0–39 Low fit · 40–59 Possible fit · "
            "60–79 Good fit · 80–100 Strong fit"
        )
        self.fields["score"].widget.attrs.update({"min": "0", "max": "100"})
        for name, field in self.fields.items():
            field.widget.attrs["class"] = INPUT_CLASS
            descriptions = []
            if field.help_text:
                descriptions.append(f"id_{name}_helptext")
            if self.is_bound and name in self.errors:
                field.widget.attrs["aria-invalid"] = "true"
                descriptions.append(f"id_{name}_error")
            if descriptions:
                field.widget.attrs["aria-describedby"] = " ".join(descriptions)

    def clean_score(self):
        score = self.cleaned_data["score"]
        if score > 100:
            raise forms.ValidationError("Score must be between 0 and 100.")
        return score


class LeadActivityForm(forms.ModelForm):
    class Meta:
        model = LeadActivity
        fields = ("type", "note")
        widgets = {"note": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = INPUT_CLASS
            if self.is_bound and name in self.errors:
                field.widget.attrs["aria-invalid"] = "true"
                field.widget.attrs["aria-describedby"] = f"id_{name}_error"
