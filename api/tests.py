import unittest
import os
from api.eska import app, db, Artists, Hits


class ApiTests(unittest.TestCase):
    """Test hits and artists API"""

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(
            basedir, "test.db"
        )
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()
        a = Artists(first_name="test name", last_name="test lastname")
        a2 = Artists(first_name="second test name", last_name="second test lastname")
        h = Hits(title="test hit", artist=a)
        h2 = Hits(title="second test hit", artist=a2)
        db.session.add(h)
        db.session.add(a2)
        db.session.commit()

    def test_get_hits_list(self):
        """Test show list of hits"""
        res = self.app.get("/api/v1/hits")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(Hits.query.count(), len(res.get_json()["hits"]))

    def test_get_hit_details(self):
        """Test show hit details"""
        res = self.app.get("/api/v1/hits/1")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["hit"]["title"], "test hit")

    def test_create_new_hit(self):
        """Test create a new hit"""
        hits_before = Hits.query.count()
        res = self.app.post(
            "/api/v1/hits", json={"title": "new test hit", "artist_id": 1}
        )

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Hits.query.count(), hits_before + 1)
        self.assertEqual(res.get_json()["hit"]["title"], "new test hit")

    def test_update_hit(self):
        """Test change hit data"""
        res = self.app.put(
            "/api/v1/hits/1", json={"title": "updated test hit", "artist_id": 2}
        )

        updated = Hits.query.get(1)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["hit"]["title"], updated.title)
        self.assertEqual(
            res.get_json()["hit"]["artist"]["first_name"], updated.artist.first_name
        )  #

    def test_delete_hit(self):
        """Test remove hit from the database"""
        res = self.app.delete("/api/v1/hits/1")

        hits = Hits.query.count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(hits, 1)

    def test_no_hit_in_database(self):
        """Test requested hit does not exist in database"""
        res = self.app.get("/api/v1/hits/4")

        self.assertEqual(res.status_code, 404)

    def test_missing_data_in_create_hit(self):
        """Test missing data in post request"""
        res = self.app.post("/api/v1/hits", json={"hello": "new test hit"})

        self.assertEqual(res.status_code, 400)

    def test_wrong_data_type_in_create_hit(self):
        """Test wrong data type in post request"""
        res = self.app.post(
            "/api/v1/hits", json={"title": "new test hit", "artist_id": "hello"}
        )

        self.assertEqual(res.status_code, 400)

    def test_artist_not_in_database_when_create_hit(self):
        """Test artist assigned to created hit does not exist in database"""
        res = self.app.post(
            "/api/v1/hits", json={"title": "new test hit", "artist_id": 3}
        )

        self.assertEqual(res.status_code, 400)

    def test_wrong_format_send_in_create_hit(self):
        """Test request data is in wrong format"""
        res = self.app.post(
            "/api/v1/hits", data={"title": "new test hit", "artist_id": 1}
        )

        self.assertEqual(res.status_code, 400)

    def test_missing_data_in_update_hit(self):
        """Test missing data in put request"""
        res = self.app.put("/api/v1/hits/1", json={"hello": "new test hit"})

        self.assertEqual(res.status_code, 400)

    def test_wrong_data_type_in_update_hit(self):
        """Test wrong data type in put request"""
        res = self.app.put(
            "/api/v1/hits/1", json={"title": "new test hit", "artist_id": "hello"}
        )

        self.assertEqual(res.status_code, 400)

    def test_artist_not_in_database_when_update_hit(self):
        """Test artist assigned to updated hit does not exist in database"""
        res = self.app.put(
            "/api/v1/hits/2", json={"title": "new test hit", "artist_id": 4}
        )

        self.assertEqual(res.status_code, 400)

    def test_no_hit_to_update_in_database(self):
        """Test hit to update does not exist in database"""
        res = self.app.put(
            "/api/v1/hits/4", json={"title": "new test hit", "artist_id": 1}
        )

        self.assertEqual(res.status_code, 400)

    def test_no_hit_to_delete(self):
        """Test hit to delete does not exist in database"""
        res = self.app.delete("/api/v1/hits/5")

        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
