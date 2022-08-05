import json
from uuid import uuid4
from pathlib import Path

from spydnote.api.settings import NOTES_DIR


def get_notes():
    list_notes = []
    fichiers = Path.glob(NOTES_DIR, "*.json")
    for fichier in fichiers:
        with open(fichier, "r", encoding='utf-8') as f:
            note_data = json.load(f)
            note_uuid = fichier.stem
            note_title = note_data.get("title")
            note_content = note_data.get("content")
            note = Note(uuid=note_uuid, title=note_title, content=note_content)
            list_notes.append(note)

    return list_notes


class Note:
    def __init__(self, title="", content="", uuid=None):
        self.uuid = uuid or str(uuid4())
        self.title = title
        self.content = content

    def __repr__(self):
        return f"{self.title} ({self.uuid})"

    def __str__(self):
        return self.title

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str):
            self._content = value
        else:
            raise TypeError("Valeur invalide, chaîne de caractères obligatoire.")

    def delete(self):
        self.path.unlink()
        return self.path.exists()

    @property
    def path(self):
        return NOTES_DIR / f"{self.uuid}.json"

    def save(self):
        NOTES_DIR.mkdir(exist_ok=True)

        data = {"title": self.title, "content": self.content}
        with open(self.path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)


if __name__ == '__main__':
    n = Note("Essai", "Une note")
    n.save()
    notes = get_notes()
    print(notes)
    n.content = "Changement de contenu"
    n.delete()
    notes = get_notes()
    print(notes)
