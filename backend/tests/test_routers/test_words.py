from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.factory import WordFactory


class TestRouterWordsGET:
    def test_get_all_user(self, client: TestClient, session: Session):
        WordFactory.create_word(session, spell="hoge", meaning="てすと")

        resp = client.get("/words")
        assert resp.status_code == status.HTTP_200_OK

        data = resp.json()
        assert len(data) == 1

    def test_get_one_word(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hoge", meaning="てすと")

        resp = client.get(f"/words/{word.id}")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["id"] == word.id
        assert data["spell"] == word.spell
        assert data["meaning"] == word.meaning

    def test_get_one_word_with_wrongid(self, client: TestClient):
        resp = client.get("/words/99999")
        data = resp.json()

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data == {"detail": "Word 99999: Not Found"}

    def test_search_words(self, client: TestClient, session: Session):
        WordFactory.create_word(session, spell="hoge", meaning="てすと")
        WordFactory.create_word(session, spell="hage", meaning="てすと")
        WordFactory.create_word(session, spell="hige", meaning="てすと")

        resp = client.get("/words?spell=h")
        data = resp.json()
        assert len(data) == 3

        resp = client.get("/words?spell=H")
        data = resp.json()
        assert len(data) == 3

        resp = client.get("/words?spell=age")
        data = resp.json()
        assert len(data) == 1

        resp = client.get("/words?spell=zyx")
        data = resp.json()
        assert len(data) == 0


class TestRouterWordsPOST:
    def test_create_word(self, client: TestClient, session: Session):
        resp = client.get("/words")
        data = resp.json()
        assert len(data) == 0

        resp = client.post("/words", json={"spell": "hoge", "meaning": "ほげ"})
        data = resp.json()
        assert resp.status_code == status.HTTP_201_CREATED
        assert data["spell"] == "hoge"
        assert data["meaning"] == "ほげ"

        resp = client.get("/words")
        data = resp.json()
        assert len(data) == 1

    def test_create_dup_word(self, client: TestClient, session: Session):
        resp = client.post("/words", json={"spell": "hoge", "meaning": "ほげ"})
        resp = client.post("/words", json={"spell": "hoge", "meaning": "ひげ"})
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        data = resp.json()
        assert data["detail"] == "Word hoge is duplicated"


class TestRouterWordsPATCH:
    def test_udpate_word_when_both_empty(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hoge", meaning="てすと")

        resp = client.patch(f"/words/{word.id}", json={})
        data = resp.json()

        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert data["detail"] == "Word Empty"

    def test_update_word_when_spell_is_empty(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hoge", meaning="てすと")

        resp = client.patch(f"/words/{word.id}", json={"meaning": "ほげげ"})
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["spell"] == "hoge"
        assert data["meaning"] == "ほげげ"

    def test_update_word_when_meaning_is_empty(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hoge", meaning="てすと")

        resp = client.patch(f"/words/{word.id}", json={"spell": "hige"})
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["spell"] == "hige"
        assert data["meaning"] == "てすと"

    def test_update_word_when_word_id_is_wrong(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hoge", meaning="てすと")

        resp = client.patch(f"/words/{word.id + 100}", json={"spell": "hige", "meaning": "ててて"})
        data = resp.json()

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data["detail"] == f"Word {word.id + 100} Not Found"

    def test_update_word_when_word_is_duplicated(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hoge", meaning="てすと")

        resp = client.patch(f"/words/{word.id}", json={"spell": "hoge", "meaning": "すてて"})
        data = resp.json()

        assert resp.status_code == status.HTTP_409_CONFLICT
        assert data["detail"] == "Word hoge is duplicated"


class TestRouterWordsDELETE:
    def test_delete_word(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hoge", meaning="てすと")

        resp = client.get("/words")
        data = resp.json()
        assert len(data) == 1

        resp = client.delete(f"/words/{word.id}")
        data = resp.json()
        assert resp.status_code == status.HTTP_200_OK
        assert data == None

    def test_delete_word_when_word_id_is_wrong(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hoge", meaning="てすと")

        resp = client.delete(f"/words/{word.id + 100}")
        data = resp.json()
        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data["detail"] == f"Word {word.id + 100} Not Found"
