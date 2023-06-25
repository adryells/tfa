from graphene import ObjectType, String


class Teste(ObjectType):
    oi = String()

    def resolve_oi(self, _):
        return "oiiiii"
