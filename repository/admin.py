# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from repository.models import *

admin.site.register(Article)
admin.site.register(User_Article)
admin.site.register(Classification)
admin.site.register(Tag)
admin.site.register(User)
admin.site.register(Baozhang)
admin.site.register(Blog)
admin.site.register(Comment)

# account:root
# pwd:root1234