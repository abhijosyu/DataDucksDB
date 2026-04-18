from flask import Blueprint, jsonify, request
from backend.db_connection import get_db
from mysql.connector import Error

company = Blueprint("company", __name__)

@company.route("/", methods=["POST"])
def create_company():
    data = request.json
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO Company (name) VALUES (%s)",
            (data["name"],)
        )
        db.commit()
        return jsonify({"message": "Company created"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


@company.route("/<int:company_id>", methods=["GET"])
def get_company(company_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM Company WHERE company_id = %s",
            (company_id,)
        )
        return jsonify(cursor.fetchone()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@company.route("/<int:company_id>", methods=["PUT"])
def update_company(company_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE Company SET name = %s WHERE company_id = %s",
            (data["name"], company_id)
        )
        db.commit()
        return jsonify({"message": "Company updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@company.route("/<int:company_id>", methods=["DELETE"])
def delete_company(company_id):
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "DELETE FROM Company WHERE company_id = %s",
            (company_id,)
        )
        db.commit()
        return jsonify({"message": "Company deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@company.route("/<int:company_id>/locations", methods=["GET"])
def get_locations(company_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM RestaurantLocation WHERE company_id = %s",
            (company_id,)
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@company.route("/<int:company_id>/reviews", methods=["GET"])
def get_company_reviews(company_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT cr.*
            FROM CustomerReview cr
            JOIN RestaurantLocation rl
            ON cr.location_id = rl.location_id
            WHERE rl.company_id = %s
        """, (company_id,))
        
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


@company.route("/<int:company_id>/tags", methods=["GET"])
def get_company_tags(company_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT t.tag_name
            FROM Tag t
            JOIN CompanyTag ct ON t.tag_id = ct.tag_id
            WHERE ct.company_id = %s
        """, (company_id,))
        
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
