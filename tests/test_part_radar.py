import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("part_radar", ROOT / "tools" / "part_radar.py")
radar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(radar)
DEMO = json.loads((ROOT / "examples" / "pi-zero-camera-research.json").read_text())


class PartRadarTests(unittest.TestCase):
    def test_adaptable_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = radar.write_artifacts(copy.deepcopy(DEMO), Path(temp))
            self.assertIn('status: "ADAPTABLE"', (directory / "research.yaml").read_text())
            event = json.loads((directory / "design-required.json").read_text())
            self.assertEqual(event["event"], "DesignRequired")
            self.assertEqual(event["reason"], "EXISTING_DESIGN_REQUIRES_MODIFICATION")
            order = json.loads((directory / "engineering-order.json").read_text())
            self.assertEqual(order["type"], "EngineeringWorkOrder")
            self.assertEqual(order["status"], "OPEN")
            self.assertEqual(order["team"], "engineering")
            self.assertEqual(order["requested_action"], "REVIEW_ADAPTATION")
            self.assertIn("optocamzero", order["closest_candidate"]["url"])
            self.assertEqual(order["closest_candidate"]["license"]["name"], "CC-BY-SA-4.0")
            self.assertNotIn("discord.txt", [p.name for p in directory.iterdir()])

    def test_found_has_no_engineering_order(self):
        data = copy.deepcopy(DEMO)
        data["status"] = "FOUND"
        data["evaluation"]["mismatches"] = []
        data["evaluation"]["unknowns"] = []
        with tempfile.TemporaryDirectory() as temp:
            directory = radar.write_artifacts(data, Path(temp))
            self.assertEqual(sorted(p.name for p in directory.iterdir()), ["research.yaml"])

    def test_not_found_event(self):
        data = copy.deepcopy(DEMO)
        data["status"] = "NOT_FOUND"
        data["selected_candidate_id"] = None
        data["evaluation"]["reason"] = "No suitable confirmed open design survived evaluation."
        event = radar.design_required(radar.validate(data))
        self.assertEqual(event["reason"], "NO_SUITABLE_OPEN_SOURCE_DESIGN")
        order = radar.engineering_order(data)
        self.assertEqual(order["status"], "OPEN")
        self.assertEqual(order["requested_action"], "EVALUATE_NEW_DESIGN")
        self.assertIsNone(order["closest_candidate"])

    def test_license_classification_is_conservative(self):
        self.assertEqual(radar.license_classification(None, None), "NO_LICENSE_FOUND")
        self.assertEqual(radar.license_classification("MIT", None), "OPEN_SOURCE_UNCLEAR")
        self.assertEqual(radar.license_classification("CC-BY-NC-4.0", "https://example.com/license"), "RESTRICTED")
        self.assertEqual(radar.license_classification("CC-BY-SA-4.0", "https://example.com/license"), "OPEN_SOURCE_CONFIRMED")

    def test_rejects_unlicensed_found_and_uncertain_found(self):
        data = copy.deepcopy(DEMO)
        data["status"] = "FOUND"
        data["evaluation"]["mismatches"] = []
        with self.assertRaisesRegex(ValueError, "unknowns"):
            radar.validate(data)
        data["evaluation"]["unknowns"] = []
        data["candidates"][0]["license"] = {"name": None, "url": None, "classification": "NO_LICENSE_FOUND"}
        with self.assertRaisesRegex(ValueError, "confirmed open-source"):
            radar.validate(data)

    def test_boundary_and_packaging(self):
        dockerfile = (ROOT / "Dockerfile").read_text()
        self.assertIn("@sha256:f1e7c421", dockerfile)
        self.assertIn("/opt/plow/prompt/AGENTS.md", dockerfile)
        self.assertIn("/opt/plow/skills/", dockerfile)
        self.assertTrue((ROOT / "skills" / "engineering-work-order" / "SKILL.md").is_file())
        self.assertNotIn("ENTRYPOINT", dockerfile)
        self.assertNotIn("CMD ", dockerfile)
        self.assertNotIn("agent-index-client.py", dockerfile)
        prompt = (ROOT / "prompt" / "AGENTS.md").read_text()
        for forbidden in ("Never generate or modify CAD", "Never call Onshape", "simulation tools"):
            self.assertIn(forbidden, prompt)
        compose = (ROOT / "compose.yml").read_text()
        self.assertIn("AGENT_ID: ${AGENT_ID:-}", compose)
        self.assertIn("state:/var/lib/plow", compose)
        self.assertIn("127.0.0.1:3001:3001", compose)
        self.assertIn("dev-dashboard:", compose)
        self.assertIn("network_mode: service:agent", compose)
        self.assertIn("./dev/Caddyfile:/etc/caddy/Caddyfile:ro", compose)
        self.assertNotIn("3000:3000", compose)
        caddyfile = (ROOT / "dev" / "Caddyfile").read_text()
        self.assertIn("respond @foreign_origin 403", caddyfile)
        self.assertIn("reverse_proxy 127.0.0.1:3000", caddyfile)
        self.assertIn("request_header -X-Plow-*", caddyfile)


if __name__ == "__main__":
    unittest.main()
