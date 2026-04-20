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

@admin.route("/reviews", methods=["GET"])
def get_reviews():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM CustomerReview")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@admin.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "DELETE FROM CustomerReview WHERE review_id = %s",
            (review_id,)
        )
        db.commit()
        return jsonify({"message": "Review deleted"}), 200
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
        cursor.execute("SELECT * FROM Flag")
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
