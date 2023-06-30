import sqlalchemy as sql
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = sql.create_engine("mysql+pymysql://root:910506@localhost:3306/db?charset=utf8", echo=True)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
metadata = sql.MetaData()
meta = sql.schema.MetaData()


class Person():
    column_list = []
    def __init__(self, table_name):
        self.table_name = table_name
        
    def __repr__(self):
        return f"<Person(id={self.id}, name='{self.name}', age={self.age})>"
        
    
    def pk_columns(self, name, type):
        if type == 'int':
            cols = sql.Column(name, sql.Integer, primary_key=True)
        elif type == 'str':
            cols = sql.Column(name, sql.String(20), primary_key=True)
        Person.column_list.append(cols)
        
    def columns(self, name, type, pk:bool=False):
        if type == 'int':
            cols = sql.Column(name, sql.Integer)
        elif type == 'str':
            cols = sql.Column(name, sql.String(20))
        Person.column_list.append(cols)
            
    def create_table(self, name):
        table = sql.Table(name, metadata, *Person.column_list)
        table.create(bind=engine)
        return table

    def drop_table(self, name):
        table = sql.Table(name, metadata, *Person.column_list)
        table.drop(bind=engine)

        


if __name__ == "__main__":
    p1 = Person('test')
    # p1.pk_columns('id', 'int')
    # p1.columns('name', 'str')
    # tbl1 = p1.create_table('test4')
    
    
    p1.drop_table('test4')
    # users.create(bind=engine)
    # users.drop(engine)

    # person1 = Person(name='John', age=30)
    # person2 = Person(name='Jane', age=25)
    # session.add_all([person1, person2])
    # session.commit()
    # users.create(bind=engine)
    
    # # SELECT * FROM table
    # all_persons = session.query(Person).all()
    # print("All persons:")
    # for person in all_persons:
    #     print(person)

    # # SELECT * FROM table WHERE age > 28
    # filtered_persons = session.query(Person).filter(Person.age > 28).all()
    # print("Filtered persons (age > 28):")
    # for person in filtered_persons:
    #     print(person)
    
    # # MODIFY
    # person_to_modify = session.query(Person).filter_by(name='Jane').first()
    # person_to_modify.age = 26
    # session.commit()
    
    # #DELETE
    # person_to_delete = session.query(Person).filter_by(name='John').first()
    # session.delete(person_to_delete)
    # session.commit()