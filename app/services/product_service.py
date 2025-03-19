from psycopg2.extras import RealDictCursor

from app.database import get_db_connection
from app.models.product import ProductCreate


class ProductService:
    @staticmethod
    def full_update_product(product_id: int, product_data: ProductCreate):
        """
        Create a new product using raw SQL.
        """
        query = """
        UPDATE product
        SET name = %s, category_id = %s
        WHERE id = %s
        RETURNING id, name, category_id;
        """
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (product_data.name,
                               product_data.category_id, product_id))
                updated_product = cursor.fetchone()
                conn.commit()

                if not updated_product:
                    raise ValueError("create_product err: Value Error")

        return updated_product

    @staticmethod
    def create_product(product_data: ProductCreate):
        """
        Create a new product using raw SQL.
        """
        query = """
        INSERT INTO product (name, category_id)
        VALUES (%s, %s)
        RETURNING id, name, category_id;
        """
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (product_data.name,
                               product_data.category_id))
                new_product = cursor.fetchone()
                conn.commit()

                if not new_product:
                    raise ValueError("create_product err: Value Error")

        return new_product

    @staticmethod
    def get_product(product_id: int):
        """
        Retrieve a product by its ID using raw SQL.
        """
        query = """
        SELECT id, name, category_id
        FROM product
        WHERE id = %s;
        """
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (product_id,))
                product = cursor.fetchone()

                if not product:
                    raise ValueError("get_product err: Value Error")

        return product

    @staticmethod
    def get_all_products(limit: int, offset: int):
        """
        Retrieve all products using raw SQL.
        """
        query = """
        SELECT id, name, category_id
        FROM product
        LIMIT %s OFFSET %s;
        """
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (limit, offset))
                products = cursor.fetchall()

                if not products:
                    raise ValueError("get_all_product err: Value Error")

        return products

    @staticmethod
    def delete_product(product_id: int):
        """
        Delete a product using raw SQL.
        """
        query = """
        DELETE FROM product
        WHERE id = %s;
        """
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (product_id,))
                conn.commit()

        return {"message": "Product deleted successfully"}
