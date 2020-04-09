import json

from django.utils.datastructures import MultiValueDictKeyError
from graphene_django.views import GraphQLView


def place_files_in_operation(operation, files_map, files):
    """Injects files request.FILES into the appropriate keys
    in the operation's variables"""

    try:
        if len(files_map) == 1:
            key, value = files_map.popitem()
            # value should match the pattern ["variables.name"]
            name = value[0].split(".")[-1]
            operation["variables"][name] = files[key]

        else:
            for key, value in files_map.items():
                # value should match the pattern ["variables.name.index"]
                name = value[0].split(".")[-2]
                index = int(value[0].split(".")[-1])
                operation["variables"][name][index] = files[key]

    except MultiValueDictKeyError:
        # Catch the exception when a file is missing in the attachments
        # Do nothing and let graphene complain about the missing file
        pass

    return operation


class BaseGraphqlView(GraphQLView):
    """Provides support for File upload with multipart/form-data
    https://github.com/jaydenseric/graphql-multipart-request-spec"""

    def parse_body(self, request):
        """Handles multipart request spec for multipart/form-data,
        Returns super class output otherwise"""

        content_type = self.get_content_type(request)
        if content_type == "multipart/form-data":
            operation = json.loads(request.POST.get("operations", "{}"))
            file_map = json.loads(request.POST.get("map", "{}"))

            return place_files_in_operation(operation, file_map, request.FILES)
        return super(BaseGraphqlView, self).parse_body(request)
