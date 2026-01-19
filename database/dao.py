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
            results.append(Prodotti(row['id'], row['product_name'])) # questi sono i noti quindi preso tutto

        cursor.close()
        conn.close()
        return results
    @staticmethod
    def read_connessioni_archi(categoria_id, data_inizio,data_fine):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ with vendite as (select p.id, count(*) as num 
                    from product p, order_item oi, `order` o 
                    where p.category_id=%s and p.id=oi.product_id and oi.order_id =o.id 
                    and o.order_date between %s and %s
                    group by p.id)
                    SELECT v1.id AS n1, v2.id AS n2, (v1.num + v2.num) AS peso
                    FROM vendite v1, vendite v2
                    WHERE v1.id <> v2.id 
                    AND v1.num >= v2.num
                    ORDER BY peso DESC, n1 ASC, n2 asc """
        cursor.execute(query, (categoria_id,data_inizio,data_fine))

        for row in cursor:
            results.append((row['n1'], row['n2'], row['peso']))

        cursor.close()
        conn.close()
        return results


# ho messo maggiore, uguale perche in questo modo può ritornare due archi visto che il grafo e orientato e pesato




