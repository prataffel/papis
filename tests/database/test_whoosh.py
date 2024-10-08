import papis.config
import papis.database

import tests.database


class Test(tests.database.DatabaseTest):

    @classmethod
    def setUpClass(cls):
        papis.config.set("database-backend", "whoosh")
        tests.database.DatabaseTest.setUpClass()

    def test_backend_name(self):
        self.assertEqual(papis.config.get("database-backend"), "whoosh")

    def test_query(self):
        # The database is existing right now, which means that the
        # test library is in place and therefore we have some documents
        database = papis.database.get()
        docs = database.query("*")
        self.assertGreater(len(docs), 0)
