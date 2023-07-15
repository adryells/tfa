from app.database.session import main_session
from app.database.utils import restart_db

if __name__ == "__main__":
    db_session = main_session()

    drop_tables = int(input("Wanna drop tables? [0] - No [1] - Yes "))
    create_tables = int(input("Wanna create tables? [0] - No [1] - Yes "))
    load_tables = int(input("Wanna load table mock data? [0] - No [1] - Yes "))

    restart_db(
        db_session=db_session,
        drop=bool(drop_tables),
        create=bool(create_tables),
        load=bool(load_tables)
    )
