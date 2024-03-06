
from django.contrib import admin
from django.urls import path  ,include
from django.conf.urls.static import static
from django.conf import settings

### API
from .router import router
from rest_framework.authtoken import views


from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls' , namespace='accounts')),
    path('blog/', include('blog.urls' , namespace='blog')),
    path('auth/', include('social_django.urls', namespace='social')),
    path( 'swagger/', schema_view),


    ### API
    path('api/' , include(router.urls)),
    path('api-token-auth/' , views.obtain_auth_token , name='api-token-auth'),


]
if settings.DEBUG is True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

