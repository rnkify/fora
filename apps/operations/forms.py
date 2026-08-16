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

        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASS


class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = ("title", "due_at")
        widgets = {
            "due_at": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASS


class TaskStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=ProjectTask.Status.choices,
    )
