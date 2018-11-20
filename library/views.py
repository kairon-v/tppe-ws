
from django.db.utils import IntegrityError

from spyne.error import ResourceNotFoundError, ResourceAlreadyExistsError
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.application import Application
from spyne.decorator import rpc
from spyne.util.django import DjangoComplexModel

from .models import User as UserModel


class User(DjangoComplexModel):
    class Attributes(DjangoComplexModel.Attributes):
        django_model = UserModel


class UserService(ServiceBase):
    @rpc(_returns=Iterable(User))
    def user_listing(ctx):
        try:
            return UserModel.objects.all()
        except UserModel.DoesNotExist:
            raise ResourceNotFoundError('User')

    @rpc(Unicode, _returns=User)
    def get_user(ctx, email):
        try:
            return UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise ResourceNotFoundError('User')

    @rpc(User, _returns=User)
    def create_user(ctx, user):
        try:
            return UserModel.objects.create(**user.as_dict())
        except IntegrityError:
            raise ResourceAlreadyExistsError('User')


app = Application([UserService],
    'library.views',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)