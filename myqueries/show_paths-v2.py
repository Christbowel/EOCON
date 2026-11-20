import json, sys

data = json.load(open(sys.argv[1]))
for run in data.get("runs", []):
    for r in run.get("results", []):
        print("\n=== " + r.get("message", {}).get("text", "") + " ===")
        cf = r.get("codeFlows", [])
        if not cf:
            continue
        # on ne garde que le 1er chemin (le plus court suffit pour montrer)
        steps = cf[0]["threadFlows"][0]["locations"]
        seen = []
        for s in steps:
            loc = s["location"]["physicalLocation"]
            uri = loc["artifactLocation"]["uri"]
            line = loc.get("region", {}).get("startLine", "?")
            msg = s["location"].get("message", {}).get("text", "")
            var = msg.replace("ControlFlowNode for ", "")
            if var == "ImportMember":
                continue
            key = (uri, line, var)
            if key in seen:
                continue
            seen.append(key)
            seen_list = [k for k in seen]
            pos = len(seen_list)
        # 2e passe pour marquer source/sink proprement
        clean = []
        for s in steps:
            loc = s["location"]["physicalLocation"]
            uri = loc["artifactLocation"]["uri"]
            line = loc.get("region", {}).get("startLine", "?")
            var = s["location"].get("message", {}).get("text", "").replace("ControlFlowNode for ", "")
            if var == "ImportMember":
                continue
            if clean and clean[-1] == (uri, line, var):
                continue
            clean.append((uri, line, var))
        for i, (uri, line, var) in enumerate(clean):
            tag = "[SOURCE]" if i == 0 else "[SINK]  " if i == len(clean)-1 else "        "
            print(f"  {tag} {uri}:{line}   {var}")
