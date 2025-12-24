import os
import json
import requests

lists_hagezi = [
    ["hagezi-light", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/light-onlydomains.txt"],
    ["hagezi-normal", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/multi-onlydomains.txt"],
    ["hagezi-pro", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro-onlydomains.txt"],
    ["hagezi-proplus", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro.plus-onlydomains.txt"],
    ["hagezi-ultimate", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/ultimate-onlydomains.txt"],
    ["hagezi-tif", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/tif-onlydomains.txt"]
]

output_dir = "./rule-set"


def convert_domains(list_info: list) -> str:
    r = requests.get(list_info[1])
    domain_list = []
    if r.status_code == 200:
        lines = r.text.splitlines()
        for line in lines:
            if not line.startswith("#") and line.strip():
                domain_list.append(line)
    result = {
        "version": 3,
        "rules": [
            {
                "domain_suffix": domain_list
            }
        ]
    }
    filepath = os.path.join(output_dir, list_info[0] + ".json")
    with open(filepath, "w") as f:
        f.write(json.dumps(result, indent=2))
    return filepath


def main():
    files = []
    os.makedirs(output_dir, exist_ok=True)
    for ls in lists_hagezi:
        filepath = convert_domains(ls)
        files.append(filepath)
    print("rule-set source generated:")
    for filepath in files:
        print(filepath)
    for filepath in files:
        srs_path = filepath.replace(".json", ".srs")
        os.system("sing-box rule-set compile --output " + srs_path + " " + filepath)


if __name__ == "__main__":
    main()
