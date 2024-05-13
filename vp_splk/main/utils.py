from django.contrib.auth.mixins import LoginRequiredMixin


class DataMixin(LoginRequiredMixin):
    # fields = '__all__'
    # form_class = None
    title = None
    extra_context = {}

    def __init__(self):
        if self.title:
            self.extra_context['title'] = self.title


    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context

