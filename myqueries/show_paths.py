import json, sys

data = json.load(open(sys.argv[1]))
for run in data.get("runs", []):
    for r in run.get("results", []):
        print("=== " + r.get("message", {}).get("text", "") + " ===")
        flows = r.get("codeFlows", [])
        if not flows:
            loc = r["locations"][0]["physicalLocation"]
            print("  (sans chemin) " + loc["artifactLocation"]["uri"]
                  + ":" + str(loc["region"]["startLine"]))
            continue
        for cf in flows:
            for tf in cf.get("threadFlows", []):
                for step in tf.get("locations", []):
                    loc = step["location"]["physicalLocation"]
                    uri = loc["artifactLocation"]["uri"]
                    line = loc.get("region", {}).get("startLine", "?")
                    msg = step["location"].get("message", {}).get("text", "")
                    print(f"  {uri}:{line}   {msg}")
                print()
