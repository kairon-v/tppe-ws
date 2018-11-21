
from django.db.utils import IntegrityError
from django.db.models import Q

from spyne.error import ResourceNotFoundError, ResourceAlreadyExistsError
from spyne.model.primitive import Unicode, Integer
from spyne.model.complex import Iterable
from spyne.service import ServiceBase
from spyne.protocol.soap import Soap11
from spyne.application import Application
from spyne.decorator import rpc
from spyne.util.django import DjangoComplexModel

from .models import Book as BookModel, User as UserModel, BookLoan as BookLoanModel


class User(DjangoComplexModel):
    class Attributes(DjangoComplexModel.Attributes):
        django_model = UserModel

class Book(DjangoComplexModel):
    class Attributes(DjangoComplexModel.Attributes):
        django_model = BookModel

class BookLoan(DjangoComplexModel):
    class Attributes(DjangoComplexModel.Attributes):
        django_model = BookLoanModel

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

class BookService(ServiceBase):
    @rpc(_returns=Iterable(Book))
    def book_listing(ctx):
        try:
            return BookModel.objects.all()
        except BookModel.DoesNotExist:
            raise ResourceNotFoundError('Book')

    @rpc(Unicode, Unicode, _returns=Book)
    def get_book(ctx, title = None, isbn = None):
        try:
            return BookModel.objects.filter(Q(title=title) | Q(isbn=isbn)).first()
        except BookModel.DoesNotExist:
            raise ResourceNotFoundError('Book')

    @rpc(Unicode, Integer, _returns=Book)
    def update_book_copies(ctx, isbn, copies):
        try:
            book = BookModel.objects.filter(isbn=isbn).first()
            book.copies += copies
            book.save()
        except BookModel.DoesNotExist:
            raise ResourceNotFoundError('Book')

    @rpc(Book, _returns=Book)
    def create_book(ctx, book):
        try:
            return BookModel.objects.create(**book.as_dict())
        except IntegrityError:
            raise ResourceAlreadyExistsError('Book')


class BookLoanService(ServiceBase):
    @rpc(_returns=Iterable(BookLoan))
    def book_loan_listing(ctx):
        try:
            return BookModel.objects.all()
        except BookModel.DoesNotExist:
            raise ResourceNotFoundError('Book')
    
    @rpc(Unicode, Unicode, Integer, _returns=BookLoan)
    def create_book_loan(ctx, user_email, isbn, days):
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise ResourceNotFoundError('User')
        
        try:
            book = BookModel.objects.filter(isbn=isbn).first()
        except BookModel.DoesNotExist:
            raise ResourceNotFoundError('Book')
        
        rented = BookLoanModel.objects.filter(
            user=user,
            book=book,
            return_date=None
        )

        if rented is not None:
            raise ResourceAlreadyExistsError('BookLoan')

        return BookLoanModel.objects.create(
            user=user,
            book=book,
            days=days
        )

app = Application([UserService, BookService, BookLoanService],
    'library.views',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)
