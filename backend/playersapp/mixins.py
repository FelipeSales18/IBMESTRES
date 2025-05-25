from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Funcionario

class ColaboradorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        funcionario = Funcionario.objects.filter(user=self.request.user).first()
        return funcionario is not None and not funcionario.is_leader

class LiderRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        funcionario = Funcionario.objects.filter(user=self.request.user).first()
        return funcionario is not None and funcionario.is_leader