from django.conf.urls import url
from django.contrib import admin
from lizard.views import TilesView, ClientView, PrivateGraphQLView

urlpatterns = [
    url(r'^vectortiles/(?P<organisation>[^/]+)/(?P<tileset_id>[^/]+)/(?P<z>[0-9]+)/(?P<x>[0-9]+)/(?P<y>[0-9]+)\.pbf', TilesView.as_view(), name="vector_tiles"),
    url(r'^admin/', admin.site.urls),
    url(r'^graphql', PrivateGraphQLView.as_view(graphiql=True)),
    url(r'^$', ClientView.as_view(), name='client_home')
]
