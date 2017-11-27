import sqlite3
import re
import os

class sqlite3_class():

    def __init__(self):
        self.delimiter = r'␞'
        self.con = False
        self.cur = False

    def error_check(self):
        """Check if database has loaded"""
        if not self.conn or not self.c:
            print('Error: Database not loaded!')
        quit()
        return 0

    def close_db(self):
        """Close connection"""
        self.error_check()
        self.con.commit()
        self.con.close()

    def commit_db(self):
        """Simple commit with an error check"""
        self.error_check()
        self.con.commit()

    def export_to_db(self, db_name):
        """Load export file (.sqlite3) as a database"""
        if os.path.isfile(os.path.splitext(db_name)[0] + '.db'):
            print('Database found with name {}. Loading...'.format(os.path.splitext(db_name)[0] + '.db'))
            self.con = sqlite3.connect(os.path.splitext(db_name)[0] + '.db')
            self.cur = self.con.cursor()
            return 0
        with open(db_name, 'r') as f:
            file_contents = f.read()
            self.con = sqlite3.connect(os.path.splitext(db_name)[0] + '.db')
            self.cur = self.con.cursor()
            try:
                self.cur.executescript(file_contents)
                self.con.commit()
                # If it could commit, it is a valid database
                print('Export loaded. Created new database: {}'.format(os.path.splitext(db_name)[0] + '.db'))
                return 0
            except Exception as e:
                print('ERROR: ' + str(e))
                print('Error loading export, exiting...')
                quit()
        
    def load_db(self, db_name):
        """Will try to load database from file and save the connection in self"""
        if not os.path.isfile(db_name):
            print('Database not found, creating new database')
            self.con = sqlite3.connect(db_name)
            self.cur = self.con.cursor()
            return 0
        try:
            """Check if database by doing a query where you get all the table names"""
            self.con = sqlite3.connect(db_name)
            self.cur = self.con.cursor()
            self.cur.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table';")
            """If script got here, everything is ok!"""
            print('DB loaded')
        except Exception as e:
                print('ERROR: '+ str(e))
                print('File is not a database. Checking if export')
                working = self.export_to_db(db_name)

    def create_table(self, table_name, column_tuple):
        # RISK FOR SQL INJECTION, BEWARE
        self.cur.execute('''CREATE TABLE IF NOT EXISTS {} {}'''.format(table_name, str(column_tuple)))
        self.con.commit()
        return 0

    def alter_table(self, alter_list):
        """Needs to be fed a list with lists, example:
        [[table_name, column_name, type]]"""
        for i in alter_list:               
            self.cur.execute('''ALTER TABLE {} ADD {} {}'''.format(i[0], i[1], i[2]))
        self.con.commit()
        return 0

    def add(self, table_name, column_tuple):
        self.cur.execute('''INSERT INTO {} VALUES{};'''.format(table_name, str(column_tuple)))
        self.con.commit()
        return 0

    def find(self, column_name, table_name, extra='', flatten=False):
        self.cur.execute('SELECT {} FROM {} {}'.format(column_name, table_name, extra))
        query_result = self.query_to_list(self.cur.fetchall(), flatten)
        return query_result

    def raw(self, string, flatten=False):
        """Here, you can write pretty much any sql query"""
        query_result = self.cur.execute(string)
        query_result = self.query_to_list(self.cur.fetchall(), flatten)
        self.con.commit()
        return query_result

    def show_tables(self, verbose=True, flatten=False):
        query_result = self.cur.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table'")
        query_result = self.query_to_list(self.cur.fetchall(), flatten)
        if verbose:
            for line in query_result:
                print(line)                
        return query_result

    def schema(self, verbose=True, flatten=False):
        query_result = self.cur.execute("SELECT sql FROM sqlite_master WHERE TYPE = 'table' ORDER BY 'name';")
        query_result = self.query_to_list(self.cur.fetchall(), flatten)
        if verbose:
            for line in query_result:
                print(line)
        return query_result

    def query_to_list(self, query_result, flatten=False):
        """Converts tuple from SQL query into a list
        INPUT: [('Hs',),('Ls',)], OUTPUT: [['Hs'], ['Ls']]
        flatten = combines lists in list to one list
        """
        if query_result == None:
            return None
        for i,j in enumerate(query_result):
            query_result[i] = list(j)
        if flatten:
            query_result = [item for sublist in query_result for item in sublist]
        return query_result



"""
I choose to work with this assignment as a class, since it is much better
for modularization and can be utilized in many different ways.
This class is based from the Biotools flask project. See github for more information.

Questions:
What is the schema of the database?
What species are in the database?
Add species Sus scropa in the database! (species table)
What proteins are longer than 1000AA?
Which species are present in the NHR3 family? Give full list.
How many proteins from each specie are present in the database?
Change the schema and add column for structure, resolution and method. Add example protein with all.
How do you extract the data from the results of SELECT commands?
What happens when you insert Sus scrofa a second time?
"""

if __name__=='__main__':
    sql = sqlite3_class()
    sql.load_db('protdb.sqlite3')
    # Q1, idea from here: https://stackoverflow.com/questions/305378/list-of-tables-db-schema-dump-etc-using-the-python-sqlite3-api
    print('\nTables:')
    sql.show_tables(flatten=True)
    print('\nSchema:')
    sql.schema(flatten=True)

    # Q2 The data is extracted as a list with tuples. 
    print('\nSpecies')
    query_result = sql.find('*', 'species')
    for line in query_result:
        print(line)

    # Q3
    print('\nAdded Sus scorpa')
    try:
        sql.add('species',('Ss','Sus scropa','Wild boar'))
    except sqlite3.IntegrityError as e:
        print('Wild boar already added :) Specific for this exercise')
    query_result = sql.find('*', 'species')
    for line in query_result:
        print(line)

    # Q4
    print('\nCount proteins with longer than 1000 AA')
    query_result = sql.raw('SELECT COUNT("sequence") FROM protein WHERE LENGTH("sequence")>1000', flatten=True)
    for line in query_result:
        print(line)

    # Q5
    print('\nFinding all species present in NHR3')
    query_result = sql.raw("""SELECT species.name FROM species WHERE species.abbrev IN
                            (SELECT protein.species FROM protein WHERE protein.accession IN
                            (SELECT familymembers.protein FROM familymembers WHERE familymembers.family LIKE 'NHR3'));""",
                           flatten=True)
    for line in query_result:
        print(line)

    # Q6
    print('\nAdding new columns to protein table')
    alter_list = [['protein', 'structure', 'VARCHAR(50)'],
                  ['protein', 'resolution', 'VARCHAR(20)'],
                  ['protein', 'method', 'VARCHAR(100)']]
    try:
        sql.alter_table(alter_list)
        sql.add('protein', ('NH3', 'Ss', 'TESTTESTTEST', '2xkg, 5fvl, 6eny', '1.6Å', 'Solution NMR and X-ray diffraction'))
    except:
        print('Table already altered')
    query_result = sql.find('*', 'protein', extra='WHERE resolution LIKE "%Å"', flatten=True)  # Take last entry
    for line in query_result:
        print(line)
