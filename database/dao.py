from database.DB_connect import DBConnect
from model.categoria import Category
from model.prodotti import Prodotti

class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last
    @staticmethod
    def read_categorie_biciclette():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select id, category_name 
                        from  category c  """
        cursor.execute(query)

        for row in cursor:
            results.append(Category(row['id'], row['category_name']))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def get_prodotti(categoria):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select p.id, p.product_name 
                    from product p, category c 
                    where c.id=p.category_id and c.id=%s """  # metto l'id cosi posso arrivarci direttamente
        cursor.execute(query,(categoria,))

        for row in cursor:
            results.append(Prodotti(row['id'], row['product_name']))

        cursor.close()
        conn.close()
        return results



