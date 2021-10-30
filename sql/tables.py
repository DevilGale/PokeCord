from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Trainer(Base):
    __tablename__ = 'trainer'
    id = Column(String, primary_key=True) # Discord ID of User
    pokemon = relationship('PokemonMapping', back_populates='pokemon')

class Moves(Base):
    __tablename__ = 'moves'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(int, primary_key=True)
    pokemon = Column(String(length=32))
    type = Column(String)
    type2 = Column(String, default=None)
    image_path = Column(String) # Path to image

    def fromJson(self, requestJson):
        pokeObj = Pokemon(
            id=requestJson['id'],
            pokemon=requestJson['name'],
            type=requestJson['types'][0]['type']['name'],
            type2=requestJson['types'][1]['type']['name'] if len(requestJson['types'])==2 else None,
            image_path=None
        )
        session.add(pokeObj)
        session.commit()

class PokeCord(Base):
    __tablename__ = 'pokecord'
    discord_server = Column(String, primary_key=True) 
    channel_bind = Column(String)                     # Channel to post in
    message_id = Column(String)                       # Message with the wild pokemon
    wild_pokemon = Column(id, ForeignKey(Pokemon.id)) # Pokemon that appeared
    appear_time = Column(DateTime)                    # Time to appear

class PokemonMapping(Base):
    __tablename__ = 'pokemon_mapping'
    id = Column(int, primary_key=True, autoincrement=True)
    obtained = Column(DateTime, default=datetime.today())
    trainer = Column(String, ForeignKey(Trainer.id))
    pokemon = Column(Integer, ForeignKey(Pokemon.id))
    level = Column(Integer, default=5)
    exp = Column(Integer, default=0)
    nickname = Column(String, default=None)
    move1 = Column(Integer, ForeignKey(Moves.id))
    move2 = Column(Integer, ForeignKey(Moves.id))
    move3 = Column(Integer, ForeignKey(Moves.id))
    move4 = Column(Integer, ForeignKey(Moves.id))

class ItemMapping(Base):
    __tablename__ = 'item_mapping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trainer = Column(String, ForeignKey(Trainer.id))
    item = Column(String)

engine = create_engine('sqlite:///test.db')
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()