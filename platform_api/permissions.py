from keycloak_oidc.drf.permissions import InAuthGroup


class InStudentAuthGroup(InAuthGroup):
    """
    A permission to allow access if and only if a user is logged in,
    and is a member of the 'test' role inside keycloak.
    """
    allowed_group_names = ['student']


class InTeacherAuthGroup(InAuthGroup):
    """
    A permission to allow access if and only if a user is logged in,
    and is a member of the 'test' role inside keycloak.
    """
    allowed_group_names = ['teacher']


class InAdminAuthGroup(InAuthGroup):
    """
    A permission to allow access if and only if a user is logged in,
    and is a member of the 'test' role inside keycloak.
    """
    allowed_group_names = ['admin']

