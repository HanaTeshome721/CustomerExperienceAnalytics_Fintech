import unittest
import oracledb

ADMIN_DSN = "localhost:1521/XEPDB1"
ADMIN_USER = "sys"
ADMIN_PASS = "2112"
TEST_USER = "Test_User"
TEST_PASS = "Friendly_786"

class TestOracleDBOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect as admin to setup user and grant privileges
        cls.admin_conn = oracledb.connect(
            user=ADMIN_USER,
            password=ADMIN_PASS,
            dsn=ADMIN_DSN,
            mode=oracledb.AUTH_MODE_SYSDBA
        )
        cls.admin_conn.autocommit = True
        cls.admin_cursor = cls.admin_conn.cursor()

        # Create user if not exists (ignore error if exists)
        try:
            cls.admin_cursor.execute(f"CREATE USER {TEST_USER} IDENTIFIED BY {TEST_PASS}")
        except oracledb.DatabaseError:
            pass  # User may already exist

        cls.admin_cursor.execute(
            f"GRANT CREATE SESSION, CREATE TABLE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE, UNLIMITED TABLESPACE TO {TEST_USER}"
        )

        # Connect as test user
        cls.user_conn = oracledb.connect(
            user=TEST_USER,
            password=TEST_PASS,
            dsn=ADMIN_DSN
        )
        cls.user_conn.autocommit = True
        cls.user_cursor = cls.user_conn.cursor()

    @classmethod
    def tearDownClass(cls):
        # Cleanup: Drop objects and user
        try:
            cls.user_cursor.execute("DROP PROCEDURE test_proc")
        except Exception:
            pass
        try:
            cls.user_cursor.execute("DROP SEQUENCE test_seq")
        except Exception:
            pass
        try:
            cls.user_cursor.execute("DROP VIEW test_view")
        except Exception:
            pass
        try:
            cls.user_cursor.execute("DROP TABLE test_table")
        except Exception:
            pass
        cls.user_cursor.close()
        cls.user_conn.close()

        cls.admin_cursor.execute(f"DROP USER {TEST_USER} CASCADE")
        cls.admin_cursor.close()
        cls.admin_conn.close()

    def test_create_table(self):
        self.user_cursor.execute("""
            CREATE TABLE test_table (
                id NUMBER PRIMARY KEY,
                name VARCHAR2(50)
            )
        """)
        self.user_cursor.execute("SELECT table_name FROM user_tables WHERE table_name = 'TEST_TABLE'")
        table = self.user_cursor.fetchone()
        self.assertIsNotNone(table, "Table was not created.")

    def test_create_view(self):
        # Make sure table exists first
        self.test_create_table()
        self.user_cursor.execute("CREATE OR REPLACE VIEW test_view AS SELECT id, name FROM test_table")
        self.user_cursor.execute("SELECT view_name FROM user_views WHERE view_name = 'TEST_VIEW'")
        view = self.user_cursor.fetchone()
        self.assertIsNotNone(view, "View was not created.")

    def test_create_sequence(self):
        self.user_cursor.execute("CREATE SEQUENCE test_seq START WITH 1 INCREMENT BY 1")
        self.user_cursor.execute("SELECT sequence_name FROM user_sequences WHERE sequence_name = 'TEST_SEQ'")
        seq = self.user_cursor.fetchone()
        self.assertIsNotNone(seq, "Sequence was not created.")

    def test_create_procedure(self):
        plsql = """
        CREATE OR REPLACE PROCEDURE test_proc IS
        BEGIN
          NULL;
        END;
        """
        self.user_cursor.execute(plsql)
        self.user_cursor.execute("SELECT object_name FROM user_procedures WHERE object_name = 'TEST_PROC'")
        proc = self.user_cursor.fetchone()
        self.assertIsNotNone(proc, "Procedure was not created.")

    def test_create_synonym(self):
        # Create a synonym pointing to the table
        self.test_create_table()  # Ensure table exists
        self.user_cursor.execute("CREATE SYNONYM test_syn FOR test_table")
        self.user_cursor.execute("SELECT synonym_name FROM user_synonyms WHERE synonym_name = 'TEST_SYN'")
        syn = self.user_cursor.fetchone()
        self.assertIsNotNone(syn, "Synonym was not created.")

if __name__ == '__main__':
    unittest.main()
