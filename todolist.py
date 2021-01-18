from datetime import datetime, date, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class ToDoList(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

    @staticmethod
    def menu():
        while True:
            print('''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
            user_choice = int(input())
            if user_choice == 1:
                ToDoList.todays_tasks()
            elif user_choice == 2:
                ToDoList.week_task()
            elif user_choice == 3:
                print('All tasks:')
                ToDoList.all_tasks()
            elif user_choice == 4:
                ToDoList.missed_task()
            elif user_choice == 5:
                ToDoList.add_task()
            elif user_choice == 6:
                print('Choose the number of the task you want to delete:')
                ToDoList.all_tasks()
                ToDoList.delete_task()
            elif user_choice == 0:
                exit()

    @staticmethod
    def todays_tasks():
        today = datetime.today()
        print('Today', datetime.strftime(today, '%d %b'), ':')
        rows = session.query(ToDoList).filter(ToDoList.deadline == today.date()).all()
        if rows:
            for tasks in rows:
                print(tasks)
        else:
            print('Nothing to do!')

    @staticmethod
    def week_task():
        today = datetime.today()
        for k in range(7):
            day = today + timedelta(days=k)
            print(f"{datetime.strftime(day, '%A %d %b')}:")
            tasks = session.query(ToDoList).filter(ToDoList.deadline == day.date()).all()
            if tasks:
                for i in range(len(tasks)):
                    print(f'{i+1}. {tasks[i].task}\n')
            else:
                print('Nothing to do!\n')

    @staticmethod
    def all_tasks():
        rows = session.query(ToDoList).order_by(ToDoList.deadline).all()
        i = 1
        for tasks in rows:
            print(f'{i}. {tasks.task}. {tasks.deadline.day} {datetime.strftime(tasks.deadline, "%b")}')
            i += 1

    @staticmethod
    def add_task():
        new_row = ToDoList(task=input('Enter task> '),
                           deadline=datetime.strptime(str(input('Enter deadline > ')), '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print('The task has been added!')

    @staticmethod
    def missed_task():
        today = datetime.today().date()
        rows = session.query(ToDoList).filter(ToDoList.deadline < today).order_by(ToDoList.deadline).all()
        print('Missed tasks:')
        if rows:
            for i in range(len(rows)):
                print(f'{i+1}. {rows[i].task}. {rows[i].deadline.day} {datetime.strftime(rows[i].deadline, "%b")}')
        else:
            print('Nothing is missed!\n')

    @staticmethod
    def delete_task():
        rows = session.query(ToDoList).order_by(ToDoList.deadline).all()
        specific_row = rows[int(input())-1]  # in case rows is not empty
        session.delete(specific_row)
        session.commit()
        print('The task has been deleted!')


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

ToDoList.menu()
