import sqlite3

class Database:
    def __init__(self, db_name):
        self.database_name = db_name
        self.connection = None
        self.cursor = None
        self.db_version = 1

    def open_database(self):
        if not self.connection:
            self.connection = sqlite3.connect(self.database_name)
            self.cursor = self.connection.cursor()

    def close_database(self):
        if self.connection:
            self.cursor.close()
            self.cursor = None
            self.connection.close()
            self.connection = None

    def test_database(self):
        try:
            # Execute a query to get the SQLite version
            query = 'SELECT sqlite_version();'
            self.cursor.execute(query)

            # Fetch and print the result
            result = self.cursor.fetchall()
            print('SQLite Version is {}'.format(result[0][0]))

            query = 'SELECT version from db_version;'
            self.cursor.execute(query);
            result = self.cursor.fetchall()
            current_version = result[0][0]
            print('Database Version is {} application expects {}'.format(current_version, self.db_version) )
            if current_version != self.db_version:
                self.upgrade_database(current_version, self.db_version)

        except sqlite3.Error as error:
            print('Error occurred: ({}) - {} {}'.format(error.sqlite_errorcode, error.sqlite_errorname, error.args))
            self.init_database()

    def init_database(self):
        try:
            query = 'create table main.db_version (version integer);'
            self.cursor.execute(query)
            data = {'version': self.db_version}
            query = 'insert into main.db_version (version) values (:version);'
            self.cursor.execute(query, data)
            self.connection.commit()

        except sqlite3.Error as error:
            print('Error occurred -', error)

    def upgrade_database(self, old_version, new_version):
        try:
            print('Upgrading database from {} to {}'.format(old_version, new_version))
            if old_version < 2:
                # Upgrade to version 2 database
                query = '''create table main.npc
(
    id           integer
        constraint npc_pk
            primary key autoincrement,
    formal_name  TEXT,
    common_name  TEXT,
    description  TEXT,
    strength     integer,
    dexterity    integer,
    constitution integer,
    intelligence integer,
    wisdom       integer,
    charisma     integer
);''''
                self.cursor.execute(query)
                query = '''create table main.npc_languages
(
    id       integer
        constraint npc_languages_pk
            primary key autoincrement,
    npc_id   integer
        constraint npc_languages_npc_id_fk
            references main.npc,
    language TEXT
);'''
                self.cursor.execute(query)

            # Mark the new database version
            data = {'old_version': old_version, 'new_version': new_version}
            query = 'update main.db_version set version = :new_version where version = :old_version;'
            self.cursor.execute(query, data)
            self.connection.commit()

        except sqlite3.Error as error:
            print('Error occurred -', error)
