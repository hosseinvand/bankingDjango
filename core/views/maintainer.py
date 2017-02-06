from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic import TemplateView

from core.forms.maintainer import SetGreenbackForATMForm
from core.mixin import MaintainerRequired


class SetGreenbackForATMView(MaintainerRequired, FormView):
    template_name = 'core/simple_from_with_single_button.html'
    success_url = reverse_lazy('core:main_panel')
    form_class = SetGreenbackForATMForm

    def get_form_kwargs(self):
        kwargs = super(FormView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(SetGreenbackForATMView, self).form_valid(form)
