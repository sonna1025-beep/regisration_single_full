import unittest
import sqlite3
import gc
import app as app_module
from app import app, init_db

TEST_DB = "test_register.db"


class RegisterTestCase(unittest.TestCase):

    def setUp(self):
        app_module.DB_NAME = TEST_DB
        app.config["TESTING"] = True
        init_db()
        # Clear table before each test
        conn = sqlite3.connect(TEST_DB)
        conn.execute("DELETE FROM users")
        conn.commit()
        conn.close()
        self.client = app.test_client()

    def tearDown(self):
        gc.collect()  # release SQLite file handles on Windows
        app_module.DB_NAME = "register.db"

    def _register(self, ovog="Bat", ner="Bold", utas="99001122", email="bat@gmail.com"):
        return self.client.post("/register", data={
            "ovog": ovog,
            "ner": ner,
            "utas": utas,
            "email": email,
        }, follow_redirects=True)

    def _get_users(self):
        conn = sqlite3.connect(TEST_DB)
        c = conn.cursor()
        c.execute("SELECT ovog, ner, utas, email FROM users")
        rows = c.fetchall()
        conn.close()
        return rows

    # --- Happy path ---

    def test_successful_registration(self):
        resp = self._register()
        self.assertIn("Бүртгэл амжилттай", resp.data.decode())

    def test_user_saved_to_db(self):
        self._register()
        users = self._get_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0], ("Bat", "Bold", "99001122", "bat@gmail.com"))

    # --- Email validation ---

    def test_invalid_email_no_at(self):
        resp = self._register(email="batgmail.com")
        self.assertIn("Имэйл буруу", resp.data.decode())

    def test_invalid_email_no_domain(self):
        resp = self._register(email="bat@")
        self.assertIn("Имэйл буруу", resp.data.decode())

    def test_invalid_email_not_saved(self):
        self._register(email="notanemail")
        self.assertEqual(len(self._get_users()), 0)

    # --- Duplicate email ---

    def test_duplicate_email_rejected(self):
        self._register()
        resp = self._register()
        self.assertIn("давхардсан", resp.data.decode())

    def test_duplicate_email_not_saved_twice(self):
        self._register()
        self._register()
        self.assertEqual(len(self._get_users()), 1)

    # --- Multiple unique users ---

    def test_two_different_users(self):
        self._register(email="bat@gmail.com")
        self._register(ovog="Tur", ner="Bold", utas="88001122", email="tur@gmail.com")
        self.assertEqual(len(self._get_users()), 2)


if __name__ == "__main__":
    unittest.main()
