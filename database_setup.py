import random
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:

        print(e)


    return conn





def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print("sdk")

        print(e)






def setup_database():
    database = r"database.db"


    sql_create_gift_table = """ create table if not exists giftlog (
                                userid Integer,
                                gift_claim_time integer
                                ); """

    sql_create_actionlog_table = """ CREATE TABLE IF NOT EXISTS actionlog (
                                    userid INTEGER,
                                    actionid integer,
                                    actiontimestamp integer
                                   
                                ); """

    sql_create_home_record_table = """ create table if not exists home_record (
                                        userid Integer,
                                        login_time integer
    
    
                                ); """

    sql_create_userdata_table = """CREATE TABLE IF NOT EXISTS userdata (
                                    userid INTEGER PRIMARY KEY,
                                    username text NOT NULL,
                                    password integer,
                                    ep integer NOT NULL,
                                    challanges_competed integer
                                  
                                );"""

    sql_create_challange_table = """CREATE TABLE IF NOT EXISTS challangetable (
                                
                                    challange_date date,
                                    
                            
                                    actionid integer
                                  
                                );"""


    sql_create_action_table = """ CREATE TABLE IF NOT EXISTS action_table (
                                    actionid INTEGER PRIMARY KEY,
                                    action_message text,
                                    reward integer
                              
                                   
                                ); """


    sql_add_actions = """Insert into action_table ( action_message, reward)
                            values ('Use a reusable water bottle, cup, straw, takeout container, or a similar item. Or, avoid using one in the first place.',110),
                             ('Reuse old bags or use reusable bags or containers to avoid wasting plastic bags such as (but not limited to): grocery bags, produce bags, ziplock lunch bags, and takeout bags.',220),
                             ('Car pool or take public transportation.',330),
                             ('Walk or bike instead of driving',440),
                             ('Take a shower instead of a bath.',440),
                             ('Decide to eat vegetarian for a day.',440),
                             ('Buy produce localy',440),
                       
                             ('Wash clothes in cold water.',440);
                            
                        """





    sql_add_userdata = """Insert into userdata ( username, password, ep, challanges_competed)
                            values ('katnis', '12345', 51, 90),
                             ('JellyDonuts', 2019, 13478, 1),
                             ('vader', 555, 820, 80),
                             ('meep', 0, 100000000, 90),
                             ('grettle', 559, 1, 70);
                        """





    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_actionlog_table)

        # create tasks table
        create_table(conn, sql_create_userdata_table)


        #create action table
        create_table(conn,sql_create_action_table)

        #create challanges table

        create_table(conn,sql_create_challange_table)


        create_table(conn, sql_create_home_record_table)


        create_table(conn, sql_create_gift_table)



        conn.execute(sql_add_userdata)
        conn.execute(sql_add_actions)

        conn.commit()
        c = conn.cursor()
        c.execute("select reward from action_table where actionid=1")

        #fill challange table



        result = c.fetchall()
        print(result)
        number_of_actions = c.execute("select count(actionId) from action_table").fetchall()
        yesterday=0

        for i in range(20):
            random_id = random.randint(1,number_of_actions[0][0])
            print(random.randint(1,number_of_actions[0][0]))
            if random_id == yesterday:
                print("double id")
            yesterday = random_id

            c.execute("insert into challangetable (actionid, challange_date) values(?,?) ", (random_id,i))




        print(c.execute("select count(actionId) from action_table").fetchall())
        print(c.execute("select * from challangetable").fetchall())
        print("action log:")
        print(c.execute("select * from actionlog").fetchall())


        conn.commit()

    else:
        print("Error! cannot create the database connection.")









if __name__ == '__main__':
    main()
    c = sqlite3.connect("database.db")
    print(c.execute("select * from challangetable").fetchall())








