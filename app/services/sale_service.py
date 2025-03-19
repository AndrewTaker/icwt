from psycopg2.extras import RealDictCursor

from app.database import get_db_connection


class SaleService:
    @staticmethod
    def get_total_for_period(start_date: str, end_date: str):
        """
        Retrieve all products using raw SQL.
        """
        query = """
        SELECT product.name, sum(sale.quantity) AS sold
        FROM product
        WHERE sale.sale_date BETWEEN %s AND %s
        JOIN sale ON sale.product_id = product.id
        GROUP BY product.name
        """
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (start_date, end_date))
                products = cursor.fetchall()

                if not products:
                    raise ValueError("get_all_product err: Value Error")

        return products
