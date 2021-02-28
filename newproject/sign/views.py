from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import RegisterUser
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class NewsRegisterView(CreateView):
    model = User
    form_class = RegisterUser
    success_url = '/sign/login'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
