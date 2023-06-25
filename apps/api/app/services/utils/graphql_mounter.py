from graphene import ObjectType, Mutation, Field


def mount_object(object_type: type[Mutation] | type[ObjectType]):
    is_mutation = issubclass(object_type, Mutation)

    relation_name = object_type.__name__

    object_properties = {
        f'{relation_name}': object_type.Field() if is_mutation else Field(object_type),
        f'resolve_{relation_name}': lambda _, __: object_type,
    }

    return type(f'{relation_name}Mount', tuple(), object_properties)
