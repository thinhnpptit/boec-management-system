from store.models import Product
from decimal import Decimal


class Basket:
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get("basket")
        if 'basket' not in self.session:
            basket = self.session['basket'] = {}

        self.basket = basket

    def add(self, product, qty):
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def get_total_price(self):

        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(11.50)

        total = subtotal + Decimal(shipping)
        return total

    def update(self, product_id, qty):
        product_id = str(product_id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def delete(self, product_id):
        product_id = str(product_id)

        if product_id in self.basket:
            del self.basket[product_id]
            print(product_id)
            self.save()
            
    def clear(self):
        # Remove basket from session
        del self.session['basket']
        self.save()
