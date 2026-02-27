import json

with open("/Users/medinameirambek/Desktop/meow/practice4/json/sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<52} {'Description':<22} {'Speed':<8} {'MTU'}")
print(f"{'-'*52} {'-'*22} {'-'*6} {'-'*6}")

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    dn    = attrs["dn"]
    desc  = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu   = attrs.get("mtu", "")
    print(f"{dn:<52} {desc:<22} {speed:<8} {mtu}")