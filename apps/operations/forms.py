from django import forms

from apps.projects.models import Project, ProjectTask

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

        if started_at and due_at and due_at < started_at:
            self.add_error("due_at", "Due date cannot be before the start date.")

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
