from db import get_connection
from datetime import datetime
from iso3166 import countries

country_codes = [c.alpha2 for c in countries]

def create_travel(destination, visit_date, country, notes=None, rating=None):
    if not destination or not visit_date:
        raise ValueError("Must have destination and visit_date")
   
    if country not in country_codes:
        raise ValueError("Must enter valid country code.")
    
    try:
        datetime.strptime(visit_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("visit_date must be in YYYY-MM-DD format")

    if rating is not None:
        if not isinstance(rating, (int, float)) or not 0 <= rating <= 10:
            raise TypeError("Enter value between 0.0 and 10.0 for rating")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO travels (destination, visit_date, notes, rating, country) VALUES (%s, %s, %s, %s, %s)", (destination, visit_date, notes, rating, country)
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
    return res

def get_travel_by_id(travel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM travels WHERE id=%s", (travel_id,)
    )
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res


def delete_travel_by_id(travel_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM travels WHERE id=%s", (travel_id,)
    )
    res = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return res > 0

def update_travel_by_id(travel_id, destination=None, visit_date=None, country=None, notes=None, rating=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "UPDATE travels SET "
    updates = []
    params = []

    if destination:
        updates.append("destination=%s")
        params.append(destination)
    
    if visit_date:
        try:
            datetime.strptime(visit_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("visit_date must be in YYYY-MM-DD format")
        
        updates.append("visit_date=%s")
        params.append(visit_date)
    
    if country:
        if country not in country_codes:
           raise ValueError("Must enter valid country code.")
        
        updates.append("country=%s")
        params.append(country) 
    
    if notes:
        updates.append("notes=%s")
        params.append(notes)
    
    if rating:
        if not isinstance(rating, (int, float)) or not 0 <= rating <= 10:
            raise ValueError("Illegal rating")
        
        updates.append("rating=%s")
        params.append(rating)
    
    if not updates:
        cursor.close()
        conn.close()
        return

    query += ", ".join(updates) + " WHERE id=%s"
    params.append(travel_id)

    cursor.execute(query, tuple(params))
    conn.commit()
    res = cursor.rowcount
    cursor.close()
    conn.close()

    return res > 0
    
    
