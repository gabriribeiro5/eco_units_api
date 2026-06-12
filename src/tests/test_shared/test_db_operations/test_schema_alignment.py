import sys
import types
import unittest
from unittest.mock import MagicMock

sys.modules.setdefault("pymysql", types.SimpleNamespace(err=types.SimpleNamespace(OperationalError=Exception)))

from use_cases.agent_login.agentLogin import AgentLoginHandler


class TestSchemaAlignedAgentLogin(unittest.TestCase):
    def test_authenticate_agent_uses_agent_id_from_backoffice_admin_row(self):
        handler = AgentLoginHandler.__new__(AgentLoginHandler)
        handler.db = MagicMock()
        handler.script_select_backoffice_admin_by_email = "SELECT 1"
        handler.db.run_query.return_value = [
            {
                "agent_id": 7,
                "backoffice_admin_secret": "secret",
            }
        ]
        handler.insert_session = MagicMock()

        token = handler.authenticate_agent("admin@example.com", "secret", "admin")

        self.assertEqual(token, "session$hash_type!admin_id!7")


if __name__ == "__main__":
    unittest.main()
