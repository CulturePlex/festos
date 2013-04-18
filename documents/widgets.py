import os
from django import forms
from django.conf import settings
from django.forms.util import flatatt
from django.utils.safestring import mark_safe

class AnchorWidget(forms.Widget):
    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs, name=name)
        if hasattr(self, 'initial'):
            value = self.initial
        import ipdb; ipdb.set_trace()
        return mark_safe(
            "<p style='padding-top:4px'><a href='%s' %s>%s</a></p>" %
                (os.path.join(settings.MEDIA_URL,value.name),
                flatatt(final_attrs),
                value.name.split('/')[-1]))

    def _has_changed(self, initial, data):
        return False


class AnchorField(forms.FileField):
    widget = AnchorWidget
    def __init__(self, widget=None, label=None, initial=None, help_text=None):
        forms.Field.__init__(self, label=label, initial=initial,
            help_text=help_text, widget=widget)

    def clean(self, value, initial):
        self.widget.initial = initial
        return initial
