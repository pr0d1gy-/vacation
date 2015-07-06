from rest_framework.response import Response
from rest_framework import status

from vacation_app.models import Employee

def is_self(func):
    def func_inside(self, request, *args, **kwargs):
        if str(request.user.id) == kwargs['pk']:
            result = func(self, request, *args, **kwargs)
            return result
        else:
            return Response({'error': 'Only for self'}, status=status.HTTP_401_UNAUTHORIZED)
    return func_inside


# def is_user(func):
#     def func_inside(self, request, *args, **kwargs):
#         if request.user.group_code == Employee.GUSER:
#             return Response({'error': 'Your user'}, status=status.HTTP_401_UNAUTHORIZED)
#         return
#     return func_inside


def is_admin(func):
    def func_inside(self, request, *args, **kwargs):
        if request.user.group_code == Employee.GADMIN:
            result = func(self, request, *args, **kwargs)
            return result
        else:
            return Response({'error': 'Not admin'}, status=status.HTTP_401_UNAUTHORIZED)
    return func_inside


def is_manager_or_admin(func):
    def func_inside(self, request, *args, **kwargs):
        if request.user.group_code == Employee.GMGER or request.user.group_code == Employee.GADMIN:
            result = func(self, request, *args, **kwargs)
            return result
        else:
            return Response({'error': 'Not manager not admin'}, status=status.HTTP_401_UNAUTHORIZED)
    return func_inside


def get_for_user(func):
    def func_inside(self, request, *args, **kwargs):
        if request.user.group_code == Employee.GADMIN or request.user.group_code == Employee.GMGER:
            result = func(self, request, *args, **kwargs)
            return result
        else:
            self.queryset = self.queryset.filter(user=request.user.id)
            result = func(self, request, *args, **kwargs)
            return result
    return func_inside
