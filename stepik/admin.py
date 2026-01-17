from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Task)
admin.site.register(Example)
admin.site.register(Try)