from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///flashcards.sqlite', echo=True)
base = declarative_base()


class User(base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', email='%s')>" % (self.name, self.email)

    def dataToJSON(self):
        return {'name': self.name, 'email': self.email, "password": self.password}

class Flashcard(base):
    __tablename__ = 'flashcards'
    id = Column(Integer, primary_key=True)
    notion = Column(String)
    definition = Column(String)
    name_image = Column(String)
    categories = Column(String)

    def __repr__(self):
        return "<Flashcard(name='%s', definition='%s')>" % (self.notion, self.definition)


class SetOfFlashcards(base):
    __tablename__ = 'sets_of_flashcards'
    id = Column(Integer, primary_key=True)
    name_user = Column(String)
    name_set = Column(String)
    set_flascards = Column(Integer, ForeignKey(Flashcard.id))

    def __repr__(self):
        return "<SetOfFlashcards(name_user='%s', name_set='%s', set_flascards='%s')>" % \
               (self.name_user, self.name_set, self.set_flascards)


if __name__ == '__main__':
    # base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    user_name = "wojtek"
    name_set = "Animals"
    set_of_flashcards = session.query(SetOfFlashcards).filter(SetOfFlashcards.name_user == user_name,
    SetOfFlashcards.name_set == name_set).all()
    print(set_of_flashcards)
    flashcard = []
    for i in set_of_flashcards:
        print("i"*5)
        flashcard.append(session.query(Flashcard).filter(Flashcard.id == i.set_flascards).all()[0])
    # flashcard = session.query(Flashcard).filter(Flashcard.id == set_of_flashcards.set_flascards).all()
    print(flashcard)
