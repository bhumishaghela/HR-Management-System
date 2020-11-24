from django.contrib import admin

# Register your models here.
from .models import Login
from .models import Fact
from .models import Daily
from .models import Feedback
from .models import Notification
from .models import Achievement
from .models import Teach

admin.site.register(Login)
admin.site.register(Fact)
admin.site.register(Daily)
admin.site.register(Feedback)
admin.site.register(Notification)
admin.site.register(Achievement)
admin.site.register(Teach)

