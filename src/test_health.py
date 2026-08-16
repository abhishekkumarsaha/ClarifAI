from .health import backend_health


print()
print("========================================")
print("       CLARIFAI BACKEND HEALTH")
print("========================================")


result = backend_health()


print(
    "Status:",
    result["status"],
)


for key, value in result[
    "environment"
].items():

    print(
        f"{key}:",
        "OK" if value else "MISSING",
    )


print()
print("========================================")