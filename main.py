from sqlalchemy import create_engine, ForeignKey, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#inherat class
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    ID = Column("ID", Integer, primary_key=True)
    firstname = Column("firstname", String)
    question = Column("question", String)
    response = Column("response", String)


    def __init__(self, ID, firstname, question, response):
        self.ID = ID
        self.firstname = firstname
        self.question = question
        self.response = response

    def __repr__(self):
        return f"({self.ID}) {self.firstname}  {self.question}  {self.response}"


engine = create_engine("sqlite:///")
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

u1 = Users(123,"BAR","HEY","hello")
session.add(u1)
session.commit()



#printing all database
results = session.query(Users).all()
print(results)

#printing by id
results = session.query(Users).filter(Users.ID == 123)
for r in results:
    print(r)

