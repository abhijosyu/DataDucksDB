from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error
 
reviewer = Blueprint("reviewer", __name__)

'''
GET /locations
Jake-5: filter restaurants by location, price, min rating

Optional query params: city, price_range, min_rating
'''
@reviewer.route("/locations", methods=["GET"])
def get_locations():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /locations")
 
        city = request.args.get("city")
        price_range = request.args.get("price_range")
        min_rating = request.args.get("min_rating")
 
        # Join Company so the caller sees the restaurant name, and
        # LEFT JOIN the reviews/ratings so locations with zero reviews
        # still show up (they'd just have NULL avg_rating).
        query = '''
            SELECT rl.location_id,
                   c.name AS restaurant_name,
                   rl.address,
                   rl.city,
                   rl.price_range,
                   ROUND(AVG(r.score), 1) AS avg_rating,
                   COUNT(DISTINCT cr.review_id) AS review_count
            FROM RestaurantLocation rl
            JOIN Company c ON rl.company_id = c.company_id
            LEFT JOIN CustomerReview cr ON cr.location_id = rl.location_id
            LEFT JOIN Rating r ON r.review_id = cr.review_id
            WHERE 1=1
        '''
        params = []
        if city:
            query += " AND rl.city = %s"
            params.append(city)
        if price_range:
            query += " AND rl.price_range = %s"
            params.append(price_range)
 
        query += " GROUP BY rl.location_id, c.name, rl.address, rl.city, rl.price_range"
 
        if min_rating:
            query += " HAVING avg_rating >= %s"
            params.append(min_rating)
 
        cursor.execute(query, params)
        return jsonify(cursor.fetchall()), 200
 
    except Error as e:
        current_app.logger.error(f"Database error in get_locations: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
'''
GET /locations/<id>
Jake-1, Jake-2, Victoria-2, Victoria-4:
Return location details + category average ratings + tags
'''
@reviewer.route("/locations/<int:location_id>", methods=["GET"])
def get_location(location_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /locations/{location_id}")
 
        # Main location record
        cursor.execute("""
            SELECT rl.location_id, rl.address, rl.city, rl.price_range,
                   c.company_id, c.name AS restaurant_name
            FROM RestaurantLocation rl
            JOIN Company c ON rl.company_id = c.company_id
            WHERE rl.location_id = %s
        """, (location_id,))
        location = cursor.fetchone()
 
        if not location:
            return jsonify({"error": "Location not found"}), 404
 
        # Category averages (Jake-1)
        cursor.execute("""
            SELECT cat.name AS category, ROUND(AVG(r.score), 1) AS avg_score
            FROM CustomerReview cr
            JOIN Rating r ON r.review_id = cr.review_id
            JOIN Category cat ON cat.category_id = r.category_id
            WHERE cr.location_id = %s
            GROUP BY cat.name
        """, (location_id,))
        location["category_ratings"] = cursor.fetchall()
 
        # Tags that apply to this location's parent company (Victoria-4)
        cursor.execute("""
            SELECT t.tag_id, t.tag_name
            FROM CompanyTag ct
            JOIN Tag t ON t.tag_id = ct.tag_id
            WHERE ct.company_id = %s
        """, (location["company_id"],))
        location["tags"] = cursor.fetchall()
 
        return jsonify(location), 200
 
    except Error as e:
        current_app.logger.error(f"Database error in get_location: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
'''
GET /locations/<id>/reviews
Jake-1, Jake-6, Victoria-2, Alex-1:
All customer reviews for a specific location
'''
@reviewer.route("/locations/<int:location_id>/reviews", methods=["GET"])
def get_location_reviews(location_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /locations/{location_id}/reviews")
 
        cursor.execute("""
            SELECT cr.review_id,
                   cr.review_text,
                   cr.review_date,
                   u.user_id,
                   u.name AS reviewer_name,
                   ROUND(AVG(r.score), 1) AS avg_score
            FROM CustomerReview cr
            JOIN User u ON u.user_id = cr.user_id
            LEFT JOIN Rating r ON r.review_id = cr.review_id
            WHERE cr.location_id = %s
            GROUP BY cr.review_id, cr.review_text, cr.review_date, u.user_id, u.name
            ORDER BY cr.review_date DESC
        """, (location_id,))
 
        return jsonify(cursor.fetchall()), 200
 
    except Error as e:
        current_app.logger.error(f"Database error in get_location_reviews: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
'''
GET /locations/<id>/photos
Jake-4: browse photos of restaurant interior and food
'''
@reviewer.route("/locations/<int:location_id>/photos", methods=["GET"])
def get_location_photos(location_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /locations/{location_id}/photos")
        cursor.execute(
            "SELECT photo_id, url FROM Photo WHERE location_id = %s",
            (location_id,)
        )
        return jsonify(cursor.fetchall()), 200
 
    except Error as e:
        current_app.logger.error(f"Database error in get_location_photos: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
'''
POST /locations/<id>/photos
Jake-4: upload a new photo for a location

Required JSON body: { "url": "https://..." }
'''
@reviewer.route("/locations/<int:location_id>/photos", methods=["POST"])
def create_location_photo(location_id):    
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"POST /locations/{location_id}/photos")
        data = request.get_json()
 
        if "url" not in data:
            return jsonify({"error": "Missing required field: url"}), 400
 
        # Verify the location exists before linking a photo to it (avoids
        # orphaned photos and gives a clearer 404 than a FK constraint error).
        cursor.execute(
            "SELECT location_id FROM RestaurantLocation WHERE location_id = %s",
            (location_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Location not found"}), 404
 
        cursor.execute(
            "INSERT INTO Photo (location_id, url) VALUES (%s, %s)",
            (location_id, data["url"])
        )
        get_db().commit()
 
        return jsonify({
            "message": "Photo uploaded successfully",
            "photo_id": cursor.lastrowid
        }), 201
 
    except Error as e:
        current_app.logger.error(f"Database error in create_location_photo: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
'''
GET /reviews
Jake-6, Alex-1: platform-wide review feed / moderation list
'''
@reviewer.route("/reviews", methods=["GET"])
def get_all_reviews():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /reviews")
        cursor.execute("""
            SELECT cr.review_id,
                   cr.review_text,
                   cr.review_date,
                   u.name AS reviewer_name,
                   c.name AS restaurant_name,
                   rl.city,
                   ROUND(AVG(r.score), 1) AS avg_score
            FROM CustomerReview cr
            JOIN User u ON u.user_id = cr.user_id
            JOIN RestaurantLocation rl ON rl.location_id = cr.location_id
            JOIN Company c ON c.company_id = rl.company_id
            LEFT JOIN Rating r ON r.review_id = cr.review_id
            GROUP BY cr.review_id, cr.review_text, cr.review_date,
                     u.name, c.name, rl.city
            ORDER BY cr.review_date DESC
        """)
        return jsonify(cursor.fetchall()), 200
 
    except Error as e:
        current_app.logger.error(f"Database error in get_all_reviews: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
 
'''
POST /reviews
Jake-3: submit a new customer review with category ratings

Required JSON body:
{
  "user_id": 1,
  "location_id": 1,
  "review_text": "Great food!",
  "ratings": [
      { "category_id": 1, "score": 5 },
      { "category_id": 2, "score": 4 }
 ]
}
'''
@reviewer.route("/reviews", methods=["POST"])
def create_review():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("POST /reviews")
        data = request.get_json()
 
        required_fields = ["user_id", "location_id", "review_text", "ratings"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
 
        ratings = data["ratings"]

        # Insert the review first, capture its ID, then batch-insert the
        # per-category scores. If the rating insert fails, 
        # we rollback and the review row is never persisted.
        cursor.execute("""
            INSERT INTO CustomerReview (user_id, location_id, review_text, review_date)
            VALUES (%s, %s, %s, CURDATE())
        """, (data["user_id"], data["location_id"], data["review_text"]))
 
        new_review_id = cursor.lastrowid
 
        for r in ratings:
            cursor.execute(
                "INSERT INTO Rating (review_id, category_id, score) VALUES (%s, %s, %s)",
                (new_review_id, r["category_id"], r["score"])
            )
 
        get_db().commit()
 
        return jsonify({
            "message": "Review created successfully",
            "review_id": new_review_id
        }), 201
 
    except Error as e:
        current_app.logger.error(f"Database error in create_review: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 

'''
PUT /reviews/<id>
Jake-3: edit an existing review's text or ratings

Any subset of fields can be updated:
{ "review_text": "updated", "ratings": [...] }
'''
@reviewer.route("/reviews/<int:review_id>", methods=["PUT"])
def update_review(review_id):    
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /reviews/{review_id}")
        data = request.get_json()
 
        # Check the review exists first
        cursor.execute(
            "SELECT review_id FROM CustomerReview WHERE review_id = %s",
            (review_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Review not found"}), 404
 
        # Update the text if provided
        if "review_text" in data:
            cursor.execute(
                "UPDATE CustomerReview SET review_text = %s WHERE review_id = %s",
                (data["review_text"], review_id)
            )
 
        # Replace ratings if provided (simpler than diffing: delete + re-insert)
        if "ratings" in data:
            ratings = data["ratings"]
 
            cursor.execute("DELETE FROM Rating WHERE review_id = %s", (review_id,))

            for r in ratings:
                cursor.execute(
                    "INSERT INTO Rating (review_id, category_id, score) VALUES (%s, %s, %s)",
                    (review_id, r["category_id"], r["score"])
                )
 
        get_db().commit()
        return jsonify({"message": "Review updated successfully"}), 200
 
    except Error as e:
        current_app.logger.error(f"Database error in update_review: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
'''
GET /tags
Jake-5, Victoria-4: return all available cuisine/type tags
'''
@reviewer.route("/tags", methods=["GET"])
def get_tags():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /tags")
        cursor.execute("SELECT tag_id, tag_name FROM Tag ORDER BY tag_name")
        return jsonify(cursor.fetchall()), 200
 
    except Error as e:
        current_app.logger.error(f"Database error in get_tags: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 