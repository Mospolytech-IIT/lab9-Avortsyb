from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


def db_manip():
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/9_back"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # Создание модели данных
    class Base(DeclarativeBase):
        pass

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, autoincrement=True)
        username = Column(String, unique=True, nullable=False)
        email = Column(String, unique=True, nullable=False)
        password = Column(String, nullable=False)

        posts = relationship("Post", back_populates="user")

    class Post(Base):
        __tablename__ = 'posts'

        id = Column(Integer, primary_key=True, autoincrement=True)
        title = Column(String, nullable=False)
        content = Column(Text, nullable=False)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

        user = relationship("User", back_populates="posts")

    # Создание таблиц
    Base.metadata.create_all(bind=engine)

    # Заполнение бд данными
    Session = sessionmaker(bind=engine)
    session = Session()

    user1 = User(username="Violetta", email="Vilollett@bk.ru", password="12345")
    user2 = User(username="Alexey", email="Alexn@mail.com", password="54321")
    user3 = User(username="Ivan", email="I@yandex.ru", password="67890")
    user4 = User(username="Daria", email="Dar@gmail.ru", password="09876")
    user5 = User(username="Regina", email="Reg@outlook.com", password="1234567890")

    session.add_all([user1, user2, user3, user4, user5])
    session.commit()

    post1 = Post(title="First Post", content="Hello, Word!", user_id=user1.id)
    post2 = Post(title="Random Post", content="text text text", user_id=user1.id)
    post3 = Post(title="Meow", content="Meow, meow, meow", user_id=user2.id)
    post4 = Post(title="Numbers", content="1, 2, 3, 4, 5, 6, 7, 8, 9, 10", user_id=user3.id)
    post5 = Post(title="Text", content="Random text", user_id=user5.id)

    session.add_all([post1, post2, post3, post4, post5])
    session.commit()

    # Считывание данных
    users = session.query(User).all()
    for user in users:
        print(f"id: {user.id}\n, username: {user.username}\n, email: {user.email}\n, password: {user.password}")
    print()

    posts = session.query(Post).join(User).all()
    for post in posts:
        print(f"id: {post.id},"
              f" title: {post.title}\n, content: {post.content}\n, user_id: {post.user_id}\n"
              f"author - id: {post.user.id}\n, username: {post.user.username}\n, email: {post.user.email}\n, password: "
              f"{post.user.password}")
    print()

    user_posts = session.query(Post).filter(Post.user_id == user1.id).all()
    for post in user_posts:
        print(f"title: {post.title}\n, content: {post.content}")
    print()

    # Обновление данных
    user_to_update = session.query(User).filter(User.id == user4.id).first()
    print(f"id: {user_to_update.id}\n, username: {user_to_update.username}\n, email: {user_to_update.email}\n, password: "
          f"{user_to_update.password}")
    if user_to_update:
        user_to_update.email = "Violetta@bk.ru"
        session.commit()
    session.refresh(user_to_update)
    print(f"id: {user_to_update.id}\n, username: {user_to_update.username}\n, email: {user_to_update.email}\n, password: "
          f"{user_to_update.password}")
    print()

    post_to_update = session.query(Post).filter(Post.id == post1.id).first()
    print(f"id: {post_to_update.id}\n, title: {post_to_update.title}\n, content: {post_to_update.content}\n, user_id: "
          f"{post_to_update.user_id}")
    if post_to_update:
        post_to_update.content += " new text"
        session.commit()
    session.refresh(post_to_update)
    print(f"id: {post_to_update.id}, title: {post_to_update.title}, content: {post_to_update.content}, user_id: "
          f"{post_to_update.user_id}")
    print()

    # Удаление данных
    posts = session.query(Post).join(User).all()
    for post in posts:
        print(f"id: {post.id}, title: {post.title}, content: {post.content}, user_id: {post.user_id}\n"
              f"author - id: {post.user.id}, username: {post.user.username}, email: {post.user.email}, password: "
              f"{post.user.password}")
    print()
    post_to_delete = session.query(Post).filter(Post.id == post3.id).first()
    if post_to_delete:
        session.delete(post_to_delete)
        session.commit()
    posts = session.query(Post).join(User).all()
    for post in posts:
        print(f"id: {post.id}, title: {post.title}, content: {post.content}, user_id: {post.user_id}\n"
              f"author - id: {post.user.id}, username: {post.user.username}, email: {post.user.email}, password: "
              f"{post.user.password}")
    print()

    users = session.query(User).all()
    for user in users:
        print(f"id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}")
    user_posts = session.query(Post).filter(Post.user_id == user1.id).all()
    for post in user_posts:
        print(f"title: {post.title}, content: {post.content}")
    print()
    user_to_delete = session.query(User).filter(User.id == user1.id).first()
    if user_to_delete:
        session.query(Post).filter(Post.user_id == user_to_delete.id).delete()
        session.delete(user_to_delete)
        session.commit()
    users = session.query(User).all()
    for user in users:
        print(f"id: {user.id}, username: {user.username}, email: {user.email}, password: {user.password}")
    user_posts = session.query(Post).filter(Post.user_id == user1.id).all()
    for post in user_posts:
        print(f"title: {post.title}, content: {post.content}")
    print()


if __name__ == '__main__':
    db_manip()
