from django import forms

from apps.core.configuration import get_enabled_plans, get_enabled_services


class ForaFormMixin:
    text_input_class = (
        "w-full rounded-fora-sm border border-fora-border "
        "bg-fora-surface px-4 py-3 text-fora-text outline-none "
        "transition focus:border-fora-border-strong"
    )

    textarea_class = (
        "w-full min-h-40 resize-y rounded-fora-sm border border-fora-border "
        "bg-fora-surface px-4 py-3 text-fora-text outline-none "
        "transition focus:border-fora-border-strong"
    )

    select_class = (
        "w-full rounded-fora-sm border border-fora-border "
        "bg-fora-surface px-4 py-3 text-fora-text outline-none "
        "transition focus:border-fora-border-strong"
    )

    def style_fields(self):
        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, forms.Textarea):
                widget.attrs["class"] = self.textarea_class
            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = self.select_class
            else:
                widget.attrs["class"] = self.text_input_class


class ContactForm(ForaFormMixin, forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    company = forms.CharField(max_length=160, required=False)
    website = forms.URLField(required=False, assume_scheme="https")
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style_fields()


class ProjectInquiryForm(ForaFormMixin, forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    company = forms.CharField(max_length=160, required=False)
    website = forms.URLField(required=False, assume_scheme="https")

    service_interest_id = forms.ChoiceField(
        label="Service",
        choices=(),
        required=False,
    )

    plan_interest_id = forms.ChoiceField(
        label="Engagement",
        choices=(),
        required=False,
    )

    message = forms.CharField(
        label="What are you trying to improve?",
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        services = get_enabled_services()
        plans = get_enabled_plans()

        self.fields["service_interest_id"].choices = [
            ("", "Not sure yet"),
            *[(service.id, service.name) for service in services],
        ]

        self.fields["plan_interest_id"].choices = [
            ("", "Not sure yet"),
            *[(plan.id, f"{plan.name} — ${plan.price}") for plan in plans],
        ]

        self.style_fields()
