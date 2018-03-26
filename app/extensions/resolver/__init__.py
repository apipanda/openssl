import re

from connexion.resolver import Resolver


class InformResolver(Resolver):

    def __init__(self, default_module_name, collection_endpoint_name='search'):

        Resolver.__init__(self)
        self.default_module_name = default_module_name
        self.collection_endpoint_name = collection_endpoint_name

    def resolve_operation_id(self, operation):

        if operation.operation.get('operationId'):
            return Resolver.resolve_operation_id(self, operation)

        return self.resolve_operation_id_using_rest_semantics(operation)

    def resolve_operation_id_using_rest_semantics(self, operation):

        path_match = re.search(
            '^/?(?P<resource_name>([\w\-](?<!/))*)'
            '(?P<trailing_slash>/*)(?P<extended_path>.*)$',
            operation.path
        )

        def get_controller_name():
            x_router_controller = operation.operation.get(
                'x-swagger-router-controller')

            name = self.default_module_name
            resource_name = path_match.group('resource_name')

            if x_router_controller:
                name = x_router_controller

            elif resource_name:
                resource_controller_name = resource_name.replace('-', '_')
                name += '.' + resource_controller_name

            return name

        def get_function_name():
            method = operation.method

            is_collection_endpoint = \
                method.lower() == 'get' \
                and path_match.group('resource_name') \
                and not path_match.group('extended_path')

            return (self.collection_endpoint_name if
                    is_collection_endpoint else method.lower())

        return '{}.{}'.format(get_controller_name(), get_function_name())
