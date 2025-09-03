from db import get_connection

def create_travel(destination, notes, visit_date, rating):
    if not destination or not notes or not visit_date or not rating:
        raise ValueError("Illegal input")
    if rating < 0 or rating > 10:
        raise ValueError("Illegal rating value")
    if type(rating) != float or type(rating) != int:
        raise TypeError("Enter value between 0.0 and 10.0 for rating")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO travels (destination, visit_date, notes, rating), (%s, %s, %s, %s)", (destination, visit_date, notes, rating)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_all_travels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM travels"
    )
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res if res else "No records in journal"

def get_travel_by_id(travel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM travels WHERE id=%s", (travel_id,)
    )
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res


def delete_travel_by_id(travel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM travels WHERE id=%s", (travel_id,)
    )
    res = cursor.rowcount()
    cursor.close()
    conn.close()
    return res > 0

def update_travel_by_id(travel_id, destination=None, visit_date=None, notes=None, rating=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE travels SET "
    updates = []
    params = []

    if destination:
        updates.append("destination=%s")
        params.append(destination)
    
    if visit_date:
        updates.append("visit_date=%s")
        params.append(visit_date)
    
    if notes:
        updates.append("notes=%s")
        params.append(notes)
    
    if rating:
        if rating < 0 or rating > 10:
            raise ValueError("Illegal rating")
        
        updates.append("rating=%s")
        params.append(rating)
    
    if not updates:
        cursor.close()
        conn.close()
        return

    query += ", ".join(updates) + "WHERE id=%s"
    params.append(travel_id)

    cursor.execute(query, tuple(params))
    conn.commit()
    res = cursor.rowcount()
    cursor.close()
    conn.close()

    return res > 0
    
