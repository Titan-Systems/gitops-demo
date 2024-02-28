import os
import yaml

from titan.gitops import collect_resources_from_config


def crawl(path: str):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                yield os.path.join(root, file)


def collect_resources(path: str):
    resources = []

    for file in crawl(path):
        with open(file, "r") as f:
            print(f"Reading config file: {file}")
            config = yaml.safe_load(f)
            resources.extend(collect_resources_from_config(config))

    return resources


def str_to_bool(s: str) -> bool:
    s = s.lower()
    if s not in {"true", "false"}:
        raise ValueError(f"Invalid value for boolean: {s}")
    return s == "true"


def main():
    # Bootstrap environment
    try:
        workspace = os.environ["GITHUB_WORKSPACE"]

        # Inputs
        policy_name = str_to_bool(os.environ["INPUT_POLICY-NAME"])
        resource_path = os.environ["INPUT_RESOURCE-PATH"]
    except KeyError as e:
        raise ValueError(f"Missing environment variable: {e}") from e

    print("Config\n------")
    print(f"\t policy_name: {policy_name}")
    print(f"\t resource_path: {resource_path}")
    print(f"\t workspace: {workspace}")

    resources = collect_resources(os.path.join(workspace, resource_path))
    print(f"Resources Found: {len(resources)}")
    if policy_name == "team-restricted-roles-policy":
        raise Exception(
            "Role assignment private_equity_analyst to user j.simmons (team=hedge fund) violates policy team-restricted-roles-policy"
        )


if __name__ == "__main__":
    main()
