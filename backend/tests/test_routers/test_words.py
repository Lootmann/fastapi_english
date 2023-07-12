from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.factory import WordFactory


class TestGETWords:
    def test_get_all_user(self, client: TestClient, session: Session):
        WordFactory.create_word(session, spell="hoge", meaning="てすと")

        resp = client.get("/words")
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert len(data) == 1
