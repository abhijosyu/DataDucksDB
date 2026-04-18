from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error
 
employee = Blueprint("employee", __name__)

'''
GET /employee-reviews
Victoria-1, Joe-4: see employee reviews across the platform,
optionally filtered by category (e.g., "Work Environment")

Optional query params: category  (category name as string)
Example: /employee-reviews?category=Work%20Environment
'''
@employee.route("/employee-reviews", methods=["GET"])
def get_all_employee_reviews():
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("GET /employee-reviews")
 
        category = request.args.get("category")
 
        query = """
            SELECT er.emp_review_id,
                   er.review_text,
                   er.review_date,
                   u.user_id,
                   u.name AS employee_name,
                   rl.location_id,
                   c.name AS restaurant_name,
                   rl.city,
                   cat.name AS category,
                   erat.score
            FROM EmployeeReview er
            JOIN User u ON u.user_id = er.user_id
            JOIN RestaurantLocation rl ON rl.location_id = er.location_id
            JOIN Company c ON c.company_id = rl.company_id
            LEFT JOIN EmployeeRating erat ON erat.emp_review_id = er.emp_review_id
            LEFT JOIN Category cat ON cat.category_id = erat.category_id
            WHERE 1=1
        """
        params = []
        if category:
            query += " AND cat.name = %s"
            params.append(category)
 
        query += " ORDER BY er.review_date DESC"
 
        cursor.execute(query, params)
        return jsonify(cursor.fetchall()), 200
 
    except Error as e:
        current_app.logger.error(f"Database error in get_all_employee_reviews: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
'''
POST /employee-reviews
Victoria-5: submit a new employee review with category ratings

Required JSON body:
{
  "user_id": 2,
  "location_id": 1,
  "review_text": "Supportive team but long hours.",
  "ratings": [
        { "category_id": 4, "score": 3 }
   ]
}
'''
@employee.route("/employee-reviews", methods=["POST"])
def create_employee_review():    
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("POST /employee-reviews")
        data = request.get_json()
 
        required_fields = ["user_id", "location_id", "review_text", "ratings"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
 
        ratings = data["ratings"]
 
        cursor.execute("""
            INSERT INTO EmployeeReview (user_id, location_id, review_text, review_date)
            VALUES (%s, %s, %s, CURDATE())
        """, (data["user_id"], data["location_id"], data["review_text"]))
 
        new_review_id = cursor.lastrowid
 
        for r in ratings:
            cursor.execute(
                "INSERT INTO EmployeeRating (emp_review_id, category_id, score) VALUES (%s, %s, %s)",
                (new_review_id, r["category_id"], r["score"])
            )
 
        get_db().commit()
 
        return jsonify({
            "message": "Employee review created successfully",
            "emp_review_id": new_review_id
        }), 201
 
    except Error as e:
        current_app.logger.error(f"Database error in create_employee_review: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
'''
PUT /employee-reviews/<id>
Victoria-5: edit an existing employee review's text or ratings

Any subset of fields can be updated:
{ "review_text": "updated", "ratings": [{...}] }
'''
@employee.route("/employee-reviews/<int:emp_review_id>", methods=["PUT"])
def update_employee_review(emp_review_id):    
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"PUT /employee-reviews/{emp_review_id}")
        data = request.get_json()
 
        cursor.execute(
            "SELECT emp_review_id FROM EmployeeReview WHERE emp_review_id = %s",
            (emp_review_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Employee review not found"}), 404
 
        if "review_text" in data:
            cursor.execute(
                "UPDATE EmployeeReview SET review_text = %s WHERE emp_review_id = %s",
                (data["review_text"], emp_review_id)
            )
 
        if "ratings" in data:
            ratings = data["ratings"]
 
            cursor.execute(
                "DELETE FROM EmployeeRating WHERE emp_review_id = %s",
                (emp_review_id,)
            )

            for r in ratings:
                cursor.execute(
                    "INSERT INTO EmployeeRating (emp_review_id, category_id, score) VALUES (%s, %s, %s)",
                    (emp_review_id, r["category_id"], r["score"])
                )
 
        get_db().commit()
        return jsonify({"message": "Employee review updated successfully"}), 200
 
    except Error as e:
        current_app.logger.error(f"Database error in update_employee_review: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
'''
GET /locations/<id>/employee-reviews
Victoria-3, Joe-4: all employee reviews for a specific location

A prospective applicant uses this to research a workplace; a
company owner uses it to see internal feedback for one site.
'''
@employee.route("/locations/<int:location_id>/employee-reviews", methods=["GET"])
def get_location_employee_reviews(location_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info(f"GET /locations/{location_id}/employee-reviews")
 
        # First check the location exists, for a clean 404
        cursor.execute(
            "SELECT location_id FROM RestaurantLocation WHERE location_id = %s",
            (location_id,)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Location not found"}), 404
        
        cursor.execute("""
            SELECT er.emp_review_id,
                   er.review_text,
                   er.review_date,
                   u.user_id,
                   u.name AS employee_name,
                   ROUND(AVG(erat.score), 1) AS avg_score
            FROM EmployeeReview er
            JOIN User u ON u.user_id = er.user_id
            LEFT JOIN EmployeeRating erat
                   ON erat.emp_review_id = er.emp_review_id
            WHERE er.location_id = %s
            GROUP BY er.emp_review_id, er.review_text, er.review_date,
                     u.user_id, u.name
            ORDER BY er.review_date DESC
        """, (location_id,))
 
        return jsonify(cursor.fetchall()), 200
 
    except Error as e:
        current_app.logger.error(f"Database error in get_location_employee_reviews: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 
'''
POST /complaints
Victoria-6: file a complaint when HR / internal channels fail

Required JSON body:
{
   "user_id": 2,
   "description": "HR has not addressed ongoing management issues.",
   "status": "open"          (optional, defaults to "open")
}
'''
@employee.route("/complaints", methods=["POST"])
def create_complaint():    
    cursor = get_db().cursor(dictionary=True)
    try:
        current_app.logger.info("POST /complaints")
        data = request.get_json()
 
        if "user_id" not in data:
            return jsonify({"error": "Missing required field: user_id"}), 400
        if "description" not in data:
            return jsonify({"error": "Missing required field: description"}), 400
 
        description = data["description"]
 
        # status is optional — default to 'open' since a new complaint is
        # always unresolved at submission time.
        status = data.get("status", "open")
 
        cursor.execute("""
            INSERT INTO Complaint (user_id, description, status)
            VALUES (%s, %s, %s)
        """, (data["user_id"], description, status))
 
        get_db().commit()
 
        return jsonify({
            "message": "Complaint filed successfully",
            "complaint_id": cursor.lastrowid
        }), 201
 
    except Error as e:
        current_app.logger.error(f"Database error in create_complaint: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
 