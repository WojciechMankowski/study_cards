from dataclasses import dataclass
from typing import List


# klasa fiszki
@dataclass
class Flashcard:
    notion: str
    definition: str
    name_image: str = ""
    categories: str = "uczę się"

    def change_of_category(self):
        if self.categories == "uczę się":
            self.categories = "powtarzam"
        elif self.categories == "powtarzam":
            self.categories = "znam"


# klasa zestawu fiszek
@dataclass
class SetOfFlashcards:
    name_user: str
    name_set: str
    set_flascards: List[Flashcard]

    def add_flashcard(self, flashcard):
        self.set_flascards.append(flashcard)

    def delete_flashcard(self, flashcard):
        self.set_flascards.remove(flashcard)

    def change_category(self, flashcard):
        flashcard.change_of_category()