from django.contrib import admin

# Register your models here.
from .models import Login
from .models import Fact
from .models import Daily
from .models import Feedback
admin.site.register(Login)
admin.site.register(Fact)
admin.site.register(Daily)
admin.site.register(Feedback)