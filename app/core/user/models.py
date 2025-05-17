
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

from crum import get_current_request

from config.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()

            if groups.exists():
                if 'group_id' not in request.session:
                    # django > version 5 no admite
                    # SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
                    # request.session['group'] = groups[0]
                    request.session['group_id'] = groups[0].id
                    request.session['group_name'] = groups[0].name

        except:
            pass
