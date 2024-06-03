from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView


class CreateStampedView(LoginRequiredMixin, CreateView):
    """A view that creates a StampedModel instance."""

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class UpdateStampedView(LoginRequiredMixin, UpdateView):
    """A view that updates a StampedModel instance."""

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)
