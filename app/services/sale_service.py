from psycopg2.extras import RealDictCursor, RealDictRow

from app.database import get_db_connection


class SaleService:
    @staticmethod
    def get_total_for_period(start_date: str, end_date: str):
        """
        Retrieve all products using raw SQL.
        """
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
                    raise(ValueError("get_total_for_period err: ValueError"))

                return total
