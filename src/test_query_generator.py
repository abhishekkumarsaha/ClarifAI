from .news_search import build_search_queries


print()
print("========================================")
print("       CLARIFAI QUERY GENERATOR")
print("========================================")


claim = input(
    "\nEnter a news claim: "
).strip()


queries = build_search_queries(claim)


print()
print("Generated queries:")

if not queries:
    print("No queries generated.")

else:
    for index, query in enumerate(
        queries,
        start=1,
    ):
        print(
            f"{index}. {query}"
        )


print()
print("========================================")
print("       QUERY TEST COMPLETE")
print("========================================")