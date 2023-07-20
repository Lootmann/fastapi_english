from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from tests.factory import ExampleFactory, WordFactory


class TestRouterWordsGET:
    def test_get_all_examples(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hello", meaning="こんにちは")

        ExampleFactory.create_example(
            session, sentence="hello world", translation="こんにちは、せかい。", word_id=word.id
        )

        ExampleFactory.create_example(
            session, sentence="hello, goodbye", translation="こんにちは、さようなら。", word_id=word.id
        )

        resp = client.get("/examples")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert len(data) == 2

    def test_get_one_example(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hello", meaning="こんにちは")

        example = ExampleFactory.create_example(
            session, sentence="hello world", translation="こんにちは、せかい。", word_id=word.id
        )

        resp = client.get(f"/examples/{example.id}")
        data = resp.json()

        assert resp.status_code == status.HTTP_200_OK
        assert data["id"] == example.id
        assert data["word_id"] == word.id
        assert data["sentence"] == example.sentence
        assert data["translation"] == example.translation

    def test_get_one_example_with_wrong_example_id(self, client: TestClient, session: Session):
        word = WordFactory.create_word(session, spell="hello", meaning="こんにちは")

        example = ExampleFactory.create_example(
            session, sentence="hello world", translation="こんにちは、せかい。", word_id=word.id
        )

        resp = client.get(f"/examples/{example.id + 100}")
        data = resp.json()

        assert resp.status_code == status.HTTP_404_NOT_FOUND
        assert data["detail"] == f"Example {example.id + 100} Not Found"
