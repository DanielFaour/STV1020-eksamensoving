from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class IdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.scripts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "script" and values.get("src"):
            self.scripts.append(values["src"])


def main() -> None:
    data_text = (ROOT / "data.js").read_text(encoding="utf-8")
    match = re.fullmatch(r"window\.STV1020_DATA = (.*);\n?", data_text)
    assert match, "data.js has unexpected wrapper"
    data = json.loads(match.group(1))

    cards = data["flashcards"]
    questions = data["questions"]
    assert len(cards) >= 100
    assert len(questions) >= 251
    assert [question["id"] for question in questions] == list(range(1, len(questions) + 1))
    assert all(len(question["choices"]) == 5 for question in questions)
    assert all(len(set(question["choices"])) == 5 for question in questions)
    assert all(len(question["choiceExplanations"]) == 5 for question in questions)
    assert all(all(note for note in question["choiceExplanations"]) for question in questions)
    assert all(0 <= question["correctIndex"] <= 4 for question in questions)
    assert all(question["explanation"] for question in questions)
    assert len({card["id"] for card in cards}) == len(cards)
    assert len({card["term"] for card in cards}) == len(cards)
    assert len({question["question"] for question in questions}) == len(questions)

    parser = IdParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    assert len(parser.ids) == len(set(parser.ids)), "Duplicate HTML IDs found"
    assert parser.scripts == ["data.js", "app.js"], "Scripts must load data before app"

    app = (ROOT / "app.js").read_text(encoding="utf-8")
    referenced_ids = set(re.findall(r'\$\("#([^"]+)"\)', app))
    missing_ids = referenced_ids - set(parser.ids)
    assert not missing_ids, f"JavaScript references missing IDs: {sorted(missing_ids)}"
    for required in ("startExam", "submitExam", "gradeFor", "renderCard", "renderExamQuestion"):
        assert f"function {required}" in app

    print(
        f"Passed: {len(cards)} flashcards, {len(questions)} questions, "
        f"{len(parser.ids)} unique interface IDs."
    )


if __name__ == "__main__":
    main()
