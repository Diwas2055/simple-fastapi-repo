import json


def json_to_env(json_data, indent=""):
    env_lines = []

    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, dict):
                env_lines.append(f"{indent}{key.upper()}=")
                env_lines.extend(json_to_env(value, indent + "  "))
            else:
                env_lines.append(f"{indent}{key.upper()}={value}")
    elif isinstance(json_data, list):
        for index, item in enumerate(json_data):
            env_lines.append(f"{indent}{index + 1}=")
            env_lines.extend(json_to_env(item, indent + "  "))

    return env_lines


def write_env_file(json_data, file_path=".env"):
    env_lines = json_to_env(json_data)

    with open(file_path, "w") as env_file:
        env_file.write("\n".join(env_lines))


# Example usage:
json_data = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "username": "user",
        "password": "pass",
        "database_name": "mydb",
    },
    "api_key": "abc123",
    "debug_mode": True,
    "features": ["feature1", "feature2", "feature3"],
}

write_env_file(json_data)
