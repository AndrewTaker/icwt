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

    @staticmethod
    def get_n_top_products(start_date: str, end_date: str, limit: int):
        """
        Retrieve all products using raw SQL.
        """
# select product.name, sale.quantity from product join sale on sale.product_id = product.id where sale.sale_date between '2023-10-01' and '2023-10-30' order by sale.quantity DESC limit 5;
        query = """
        SELECT product.name, sale.quantity
        FROM product
        JOIN sale ON sale.product_id = product.id
        WHERE sale_date BETWEEN %s AND %s
        ORDER BY sale.quantity DESC
        LIMIT %s
        """
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (start_date, end_date, limit))
                total = cursor.fetchone()

                if not total:
                    raise(ValueError("get_total_for_period err: ValueError"))

                return total
