from fastapi import FastAPI
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from database import User, Flashcard, SetOfFlashcards

# stworzenie aplikacji FastAPI
app = FastAPI()

# creating connection to database and sessionmaker
engine = create_engine('sqlite:///flashcards.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

@app.get("/user/{user_name}")
async def get_user(user_name: str):
    user = session.query(User).filter(User.name == user_name).first()
    return user.dataToJSON()

@app.get("/{user_name}/sets")
async def get_sets_of_flashcards(user_name: str):
    sets_of_flashcards = session.query(SetOfFlashcards).filter(SetOfFlashcards.name_user == user_name).all()
    print(sets_of_flashcards)
    return {}

@app.post("/add_set/")
async def add_set_of_flashcards(user_name: str, name_set: str):
    set_of_flashcards = SetOfFlashcards(name_user=user_name, name_set=name_set)
    session.add(set_of_flashcards)
    session.commit()
    return {"message": "set of flashcards added"}

def add_flascard_to_set(name_set_of_flashcards, flashcard: Flashcard, user_name: str):
    set_of_flashcards = SetOfFlashcards(name_user=user_name,
                                        name_set=name_set_of_flashcards,
                                        set_flascards=flashcard.id)
    session.add(set_of_flashcards)
    session.commit()

@app.post("/flashcards")
async def add_flashcard(notion: str,
                        definition: str, name_image: str,
                        categories: str, name_set: str, nameuser: str):
    flashcard = Flashcard(notion=notion, definition=definition, name_image=name_image, categories=categories)
    session.add(flashcard)
    session.commit()
    add_flascard_to_set(name_set, flashcard, nameuser)
    return {"Karta została": "dodana"}

@app.post("/user_add/{user_name}/{password}/{email}")
async def add_user(user_name: str, password: str, email: str):
    user = User(name=user_name, password=password, email=email)
    session.add(user)
    session.commit()
    return {"message": "User added"}
# DELETE
#     usunięcie użytkownika
@app.delete("/user/{user_name}")
async def delete_user(user_name: str):
    user = session.query(User).filter(User.name == user_name).first()
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}

@app.delete("/set/{user_name}/{name_set}")
async def delete_set_of_flashcards(user_name: str, name_set: str):
    set_of_flashcards = session.query(SetOfFlashcards).filter(SetOfFlashcards.name_user == user_name).filter(SetOfFlashcards.name_set == name_set).first()
    session.delete(set_of_flashcards)
    session.commit()
    return {"message": "Set of flashcards deleted"}

@app.put("/update/flashcards/")
async def update_flashcard(notion: str, categories: str):
    flashcard = session.query(Flashcard).filter(Flashcard.notion == notion).first()
    flashcard.categories = categories
    session.commit()
    return {"message": "flashcard updated"}