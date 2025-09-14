import datetime
import psycopg2 as pg

class TotalPoints:
    fname: str
    lname: str
    rank_id: int
    division_id: int
    event_id: int
    tourn_id: int
    tourn_pts: float
    travel_pts: float
    total_pts: float
    top_ten_rank: int

def populate_top_ten(request=None):
    """Retrieves data from SQL DB and returns a dict for front end parsing"""

    division = request.args.get("division")
    event = request.args.get("events")
    school = request.args.get("school")
    belt_rank = request.args.get("belt_rank")
    fname = request.args.get("fname")
    lname = request.args.get("lname")

    values = list()

    query = """
    SELECT 
    top_ten.fname,
    top_ten.lname,
    top_ten.age,
    top_ten.tourn_pts,
    top_ten.total_pts,
    top_ten.tourn_place,
    division.name AS division,
    ranks.belt_rank AS belt_rank,
    schools.school,
    events.name  AS event,
    tournament.tournament
    FROM top_ten_main AS top_ten
        INNER JOIN division   ON top_ten.division_id = division.id
        INNER JOIN ranks      ON top_ten.rank_id = ranks.id
        INNER JOIN schools    ON top_ten.school_id = schools.id
        INNER JOIN events     ON top_ten.event_id = events.id
        INNER JOIN tournament ON top_ten.tourn_id = tournament.id  
    WHERE 1=1    
    """

    if division:
        query += " AND division.name = %s"
        values.append(division)
    if event:
        query += " AND events.name = %s"
        values.append(event)
    if school:
        query += " AND schools.school = %s"
        values.append(school)
    if belt_rank:
        query += " AND ranks.belt_rank = %s"
        values.append(belt_rank)
    if lname:
        query += " AND top_ten.lname = %s"
        values.append(lname)
    if fname:
        query += " AND top_ten.fname = %s"
        values.append(fname)

    if values:
        with pg.connect(_db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(query, values)
                data = cur.fetchall()
                return data

    else:
        with pg.connect(_db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
                return data

def two_column_helper(data):
    column_names = [
        "id",
        "name",
    ]

    cleaned = list()
    for entry in data:
        rows = entry
        data_dict = dict()
        for i in range(len(column_names)):
            data_dict[column_names[i]] = rows[i]
        cleaned.append(data_dict)
    return cleaned

def get_tournaments():
    cur_year = datetime.date.today().year

    with pg.connect(_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, tournament FROM tournament")
            data = cur.fetchall()
            return data

def tournament_helper(data):
    column_names = [
        "id",
        "tournament",
    ]

    cleaned = list()
    for entry in data:
        rows = entry
        data_dict = dict()
        for i in range(len(column_names)):
            data_dict[column_names[i]] = rows[i]
        cleaned.append(data_dict)
    return cleaned

def add_new_tourn_data(data:dict):
    query = """
    INSERT INTO top_ten_main
    (division_id, fname, lname, rank_id, school_id, age, event_id, tourn_pts, tourn_id)
    VALUES(
    (select id from division where name = %s),
    %s,
    %s,
    (select id from ranks where belt_rank = %s),
    (select id from schools where school = %s),
    %s,
    (select id from events where name = %s),
    %s,
    (select id from tournament where tournament = %s))
    """
    with pg.connect(_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (data['division'],
                                data['fname'],
                                data['lname'],
                                data['belt_rank'],
                                data['school'],
                                data['age'],
                                data['event'],
                                data['tourn_points'],
                                data['tournament']))
        conn.commit()

def top_ten_data_helper(data):
    old_column_names = [
        "division_id",
        "fname",
        "lname",
        "rank_id",
        "school_id",
        "age",
        "event_id",
        "top_ten_rank",
        "tourn_id",
        "tourn_pts",
        "total_pts",
        "tourn_place",
    ]
    column_names = [
        "fname",
        "lname",
        "age",
        "tourn_pts",
        "division",
        "belt_rank",
        "school",
        "event",
        "tournament"
    ]

    cleaned = list()
    for entry in data:
        rows = entry
        data_dict = dict()
        for i in range(len(column_names)):
            data_dict[column_names[i]] = rows[i]
        cleaned.append(data_dict)
    return cleaned

def updated_insert(data, tourn, tourn_points):
    with pg.connect(_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO top_ten_main (
                        division_id, fname, lname, rank_id, school_id, age, event_id, tourn_id, tourn_pts
                    )
                    VALUES (
                        (SELECT id FROM division WHERE name = %s),
                        %s,
                        %s,
                        (SELECT id FROM ranks WHERE belt_rank = %s),
                        (SELECT id FROM schools WHERE school = %s),
                        %s,
                        (SELECT id FROM events WHERE name = %s),
                        (SELECT id FROM tournament WHERE tournament = %s),
                        %s
                    )
                    ON CONFLICT (fname, lname, event_id, tourn_id)
                    DO UPDATE SET
                        tourn_id = (SELECT id FROM tournament WHERE tournament = %s),
                        tourn_pts = EXCLUDED.tourn_pts
                """,(
                str(data['division']).strip(),
                str(data['fname']).strip(),
                str(data['lname']).strip(),
                str(data['rank']).strip(),
                str(data['school']).strip(),
                int(data['age']),
                str(data['Event'].strip()),
                tourn,
                tourn_points,
                tourn,
            ))



def insertalldata(data):

    """INSERT INTO contacts(customer_id, contact_name ) VALUES (
(select customer_id from customers where customer_name = 'my_first_customer') ,'thomas');"""

    query = """
    INSERT INTO top_ten_main(
        division_id, fname, lname, rank_id, school_id, age, event_id
    ) 
    VALUES(
        (select id from division where name = %s),
        %s,
        %s,
        (select id from ranks where belt_rank = %s),
        (select id from schools where school = %s),
        %s,
        (select id from events where name = %s)
    )
    """

    with pg.connect(_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
            """
                INSERT INTO top_ten_main(
        division_id, fname, lname, rank_id, school_id, age, event_id
    ) 
    VALUES(
        (select id from division where name = %s),
        %s,
        %s,
        (select id from ranks where belt_rank = %s),
        (select id from schools where school = %s),
        %s,
        (select id from events where name = %s)
    )
    """
            , (
                str(data['division']).strip(),
                str(data['fname']).strip(),
                str(data['lname']).strip(),
                str(data['rank'][0]).strip(),
                str(data['school']).strip(),
                int(data['age']),
                str(data['Event'].strip())
            ))
        conn.commit()

def insert_points(fname, lname, event, tourn, points):

    with pg.connect(_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(    """
            INSERT INTO top_ten_main (
                tourn_id, tourn_pts
            )
            SELECT
                (SELECT id FROM tournament WHERE tournament = %s),
                %s
            WHERE EXISTS (
                SELECT 1 
                FROM top_ten_main 
                WHERE fname = %s 
                  AND lname = %s
                  AND event_id = (SELECT id FROM events WHERE name = %s)
            )
    """, ( tourn,
                float(points),
                fname,
                lname,
                event,
            ))
        conn.commit()

def test_points():
    """Unused"""
    query = """
    SELECT division_id, fname, lname, rank_id, event_id, tourn_id, tourn_pts, total_pts FROM top_ten_main
    """
    with pg.connect(_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            x = cur.fetchall()
            print("")
            for entry in x:
                TotalPoints.fname = entry[1]
                TotalPoints.lname = entry[2]
                TotalPoints.event_id = entry[4]
                TotalPoints.tourn_id = entry[5]
                TotalPoints.tourn_pts = entry[6]
                cur.execute(query + " WHERE fname = %s and lname = %s and event_id = %s", (TotalPoints.fname, TotalPoints.lname, TotalPoints.event_id))
                match = cur.fetchall()
                total_tourn_pts = match[0][6] + match[1][6]
                if match[0][7] != total_tourn_pts:
                    if match[0][7] == None or match[0][7] < total_tourn_pts:
                        cur.execute("""UPDATE top_ten_main
                                            SET total_pts = %s
                                            WHERE fname = %s
                                            AND lname = %s
                                            AND event_id = %s""",
                                    (total_tourn_pts, TotalPoints.fname, TotalPoints.lname, TotalPoints.event_id))
                conn.commit()
                print("")

def get_divisions():
    query = """
    SELECT * from division    
    """
    with pg.connect(_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def get_events():
    query = """
    SELECT * from events   
    """
    with pg.connect(_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def get_schools():
    with pg.connect(_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM schools")
            return cur.fetchall()

def school_data_helper(data):
    column_names = [
        "id",
        "school",
    ]

    cleaned = list()
    for entry in data:
        rows = entry
        data_dict = dict()
        for i in range(len(column_names)):
            data_dict[column_names[i]] = rows[i]
        cleaned.append(data_dict)
    return cleaned

def get_belt_ranks():
    with pg.connect(_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM ranks")
            return cur.fetchall()

def belt_rank_helper(data):
    column_names = [
        "id",
        "belt_rank",
    ]

    cleaned = list()
    for entry in data:
        rows = entry
        data_dict = dict()
        for i in range(len(column_names)):
            data_dict[column_names[i]] = rows[i]
        cleaned.append(data_dict)
    return cleaned

def update_rank(event, matches):
    TotalPoints.top_ten_rank = 1

    for row in matches:
        with pg.connect(_db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                UPDATE top_ten_main
                SET top_ten_rank = %s
                WHERE fname = %s
                AND lname = %s
                AND event_id = %s
                """,
            (TotalPoints.top_ten_rank, row[0], row[1], event))
        TotalPoints.top_ten_rank += 1


def rank():
    divisions = get_divisions()
    events = get_events()
    query = """
    SELECT DISTINCT fname, lname, total_pts, top_ten_rank from top_ten_main   
    """
    for div_entry in divisions:
        TotalPoints.division_id = div_entry[0]
        for event_entry in events:
            TotalPoints.event_id = event_entry[0]
            TotalPoints.top_ten_rank = 1
            with pg.connect(_db_url) as conn:
                with conn.cursor() as cur:
                    cur.execute(query + "WHERE division_id = %s and event_id = %s ORDER BY total_pts DESC", (TotalPoints.division_id, TotalPoints.event_id))
                    matches = cur.fetchall()
                    update_rank(TotalPoints.event_id, matches)
                    print("")

        print("")
