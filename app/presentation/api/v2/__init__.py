from functools import lru_cache

import strawberry

from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"



@lru_cache
def get_graphql_route() -> GraphQLRouter:
    return GraphQLRouter(
        strawberry.Schema(Query)
    )
