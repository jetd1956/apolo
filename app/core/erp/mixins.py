from django.contrib.auth.models import Group
from django.shortcuts import redirect
from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from crum import get_current_request

class IsSuperuserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_now'] = datetime.now()
        return context


class ValidatePermissionRequiredMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        # recibio los permisos desde la vista y en caso de ser mas de uno
        # me devuelve un array de permisos
        perms = []
        if isinstance(self.permission_required, str):
            perms.append(self.permission_required)
        else:
            perms = list(self.permission_required)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('erp:dashboard')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        request = get_current_request()

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)


        #for r in request.session.items():
        #    print(r)
        if 'group_id' in request.session:
            #grp_id = request.session['group_id']
            # variable de sesion del grupo
            #group = request.session['group']
            group = Group.objects.get(id=request.session['group_id'])

            perms = self.get_perms()
            # si viene mas de un permiso, este control es para que el usuario
            # deba tener todos los permisos y no algunos
            for p in perms:
                if not group.permissions.filter(codename=p).exists():
                    messages.error(request, 'No tiene permiso para ingresar a este módulo')
                    return HttpResponseRedirect(self.get_url_redirect())
            g = group.permissions.filter(codename=self.permission_required)
            #for q in g.items:
            print(self.permission_required)
            print(list(g))

            return super().dispatch(request, *args, **kwargs)

        messages.error(request, 'No tiene permiso para ingresar a este módulo')
        return HttpResponseRedirect(self.get_url_redirect())

#class ValidatePermissionRequiredMixin(object):
#    permission_required = ''
#    url_redirect = None
#
        #    def get_perms(self):
        #if isinstance(self.permission_required, str):
        #    perms = (self.permission_required,)
        #else:
        #    perms = self.permission_required
        #return perms
    #
    #def get_url_redirect(self):
        #    if self.url_redirect is None:
        #    return reverse_lazy('index')
        #return self.url_redirect
    ###
    #
    #def dispatch(self, request, *args, **kwargs):
        #    if request.user.has_perms(self.get_perms()):
        #    return super().dispatch(request, *args, **kwargs)
        #messages.error(request, 'No tiene permiso para ingresar a este módulo')
        #return HttpResponseRedirect(self.get_url_redirect())