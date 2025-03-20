from psycopg2.extras import RealDictCursor

from app.database import get_db_connection


class SaleService:
    @staticmethod
    def get_total_for_period(start_date: str, end_date: str):
        query = """
        SELECT COALESCE(SUM(quantity), 0) AS total
        FROM sale
        WHERE sale_date BETWEEN %s AND %s
        """
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (start_date, end_date))
                total = cursor.fetchone()

                if not total:
                    raise (ValueError("get_total_for_period err: ValueError"))

                return total

    @staticmethod
    def get_n_top_products(start_date: str, end_date: str, limit: int):
        query = """
        SELECT product.name AS name, sale.quantity AS sold_amount
        FROM product
        JOIN sale ON sale.product_id = product.id
        WHERE sale_date BETWEEN %s AND %s
        ORDER BY sale.quantity DESC
        LIMIT %s
        """
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (start_date, end_date, limit))
                total = cursor.fetchall()
                return total if total else []
