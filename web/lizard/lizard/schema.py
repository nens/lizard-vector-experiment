import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from lizard.models import Manhole, Organisation
from django.contrib.gis.db.models import PointField


@convert_django_field.register(PointField)
def convert_PointField(field, registry=None):
    return graphene.String()


class ManholeNode(DjangoObjectType):
    class Meta:
        model = Manhole
        filter_fields = ['code', 'surface_level', ]
        interfaces = (relay.Node, )

    def resolve_geometry(self, *_):
        return '{}'.format(str(self.geometry))

    @classmethod
    def get_node(cls, info, id):
        node = Manhole.object.get(pk=id)
        return node


class OrganisationType(DjangoObjectType):
    class Meta:
        model = Organisation


class Query(graphene.ObjectType):
    manhole = relay.Node.Field(ManholeNode)
    all_manholes = DjangoFilterConnectionField(ManholeNode)
    my_manholes = DjangoFilterConnectionField(ManholeNode)

    def resolve_my_manholes(self, info):
        if not info.context.user.is_authenticated():
            return Manhole.objects.none()
        else:
            return Manhole.objects.filter(surface_level='0.2')


schema = graphene.Schema(query=Query)
