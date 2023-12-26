def query(self , cities , products_id):
        results_cairo=[]

        results_alex=[]

        results_psaid=[]

        products_id=tuple(products_id)
        
        query=text(f'''
            SELECT p_name, sex, quantity
            FROM products
            JOIN inventory ON products.ID = inventory.pid
            WHERE products.ID IN{products_id}
        ''')
        products_id=tuple(products_id)
        if "psaid" in cities:
            result=self.p_con.execute(query)
            results_psaid.append(result.fetchall())
            print(results_psaid) 
            return results_psaid
        if "cairo" in cities:
            result=self.c_con.execute(query)
            results_cairo.append(result.fetchall())
            print(results_cairo) 
            return results_cairo
        if "alex" in cities:
            result=self.a_con.execute(query)
            results_alex.append(result.fetchall())
            print(results_alex) 
            return results_alex
        
    def search():
        if request.method == 'POST':
            cities=request.form.getlist('city')
            products=request.form.getlist("product")
            print(cities)
            print(products)
            db.query(cities,products)
        return render_template("search.html")
