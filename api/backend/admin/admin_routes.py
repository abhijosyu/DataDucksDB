from flask import Blueprint, jsonify, request
from backend.db_connection import get_db
from mysql.connector import Error

admin = Blueprint("admin", __name__)

@admin.route("/users", methods=["GET"])
def get_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM User")   
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

@admin.route("/companies", methods=["GET"])
def get_companies():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Company")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@admin.route("/companies/<int:company_id>", methods=["DELETE"])
def delete_company(company_id):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM Company WHERE company_id = %s", (company_id,))
        db.commit()
        return jsonify({"message": "Company deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

@admin.route("/all_reviews", methods=["GET"])
def get_all_reviews():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                cr.review_id,
                cr.user_id,
                cr.location_id,
                cr.review_text,
                cr.review_date,
                u.name,
                u.email,
                c.name AS restaurant_name,
                rl.address,
                rl.city,
                'customer' AS review_type
            FROM CustomerReview cr
            JOIN User u ON cr.user_id = u.user_id
            LEFT JOIN RestaurantLocation rl ON cr.location_id = rl.location_id
            LEFT JOIN Company c ON rl.company_id = c.company_id

            UNION ALL

            SELECT
                er.emp_review_id,
                er.user_id,
                er.location_id,
                er.review_text,
                er.review_date,
                u.name,
                u.email,
                c.name AS restaurant_name,
                rl.address,
                rl.city,
                'employee' AS review_type
            FROM EmployeeReview er
            JOIN User u ON er.user_id = u.user_id
            LEFT JOIN RestaurantLocation rl ON er.location_id = rl.location_id
            LEFT JOIN Company c ON rl.company_id = c.company_id

            ORDER BY review_date ASC
        """)
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@admin.route("/flags", methods=["POST"])
def create_flag():
    data = request.json
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO Flag (admin_id, review_id, reason) VALUES (%s, %s, %s)",
            (data["admin_id"], data["review_id"], data["reason"])
        )
        db.commit()
        return jsonify({"message": "Flag created"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


@admin.route("/flags", methods=["GET"])
def get_flags():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                f.flag_id,
                f.admin_id,
                f.review_id,
                f.reason,
                admin_user.name AS flagged_by_name,

                COALESCE(cr.review_text, er.review_text) AS review_text,
                COALESCE(cr.review_date, er.review_date) AS review_date,
                reviewer_user.name AS reviewer_name,
                reviewer_user.email AS reviewer_email,
                c.name AS restaurant_name,
                rl.address,
                rl.city,

                CASE
                    WHEN cr.review_id IS NOT NULL THEN 'customer'
                    WHEN er.emp_review_id IS NOT NULL THEN 'employee'
                END AS review_type

            FROM Flag f
            JOIN User admin_user
                ON f.admin_id = admin_user.user_id

            LEFT JOIN CustomerReview cr
                ON f.review_id = cr.review_id

            LEFT JOIN EmployeeReview er
                ON f.review_id = er.emp_review_id

            JOIN User reviewer_user
                ON reviewer_user.user_id = COALESCE(cr.user_id, er.user_id)

            LEFT JOIN RestaurantLocation rl
                ON rl.location_id = COALESCE(cr.location_id, er.location_id)

            LEFT JOIN Company c
                ON rl.company_id = c.company_id

            ORDER BY f.flag_id DESC
             """)
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@admin.route("/flags/<int:flag_id>", methods=["DELETE"])
def delete_flag(flag_id):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "DELETE FROM Flag WHERE flag_id = %s",
            (flag_id,)
        )
        db.commit()
        return jsonify({"message": "Flag removed"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    

@admin.route("/complaints", methods=["GET"])
def get_complaints():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
                            SELECT 
                                c.complaint_id,
                                c.description,
                                c.status,
                                u.user_id,
                                u.name,
                                u.email,
                                u.role
                            FROM Complaint c
                            JOIN User u ON c.user_id = u.user_id
                       """)
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@admin.route("/complaints/<int:complaint_id>", methods=["PUT"])
def update_complaint_status(complaint_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE Complaint SET status = %s WHERE complaint_id = %s",
            (data["status"], complaint_id)
        )
        db.commit()
        return jsonify({"message": "Complaint updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
@admin.route('/complaints/<int:complaint_id>', methods=['DELETE'])
def delete_complaint(complaint_id):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            DELETE FROM Complaint
            WHERE complaint_id = %s
        """, (complaint_id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Complaint not found"}), 404

        return jsonify({"message": "Complaint deleted successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
