"""Preserve the non-secret architecture verdict and fail closed."""
import json
import os
from pathlib import Path

response = json.loads((Path(os.environ["RUNNER_TEMP"]) / "dcode-response.json").read_text())
gate = response.get("architecture_gate", {})
result = {"commit": os.environ["GITHUB_SHA"], "architecture_gate": gate}
Path("dcode-result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
mode = os.environ.get("DCODE_ENFORCE_ARCH", "")
if mode == "false":
    print("BOOTSTRAP ONLY; excluded from the final experiment results.")
elif mode != "true":
    raise SystemExit("Set enforcement explicitly: true, or false for bootstrap only.")
elif gate.get("is_active") is not True:
    raise SystemExit("No active architecture gate; cannot claim validation.")
elif gate.get("result") != "PASSED":
    raise SystemExit("Architecture gate did not pass: " + str(gate.get("result")))
