from extensions import db
from models import Stock

class StockDAO:
    def __init__(self):
        self.db = db
        self.model = Stock

    def add_stock(self, ticker, quantity, user_id):
        stock = Stock(
            ticker=ticker.upper(),
            quantity=quantity,
            user_id=user_id
        )
        self.db.session.add(stock)
        self.db.session.commit()
        return stock

    def get_user_stocks(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()

    def get_stock_by_id(self, stock_id, user_id):
        return self.model.query.filter_by(id=stock_id, user_id=user_id).first()

    def update_stock(self, stock_id, user_id, quantity):
        stock = self.get_stock_by_id(stock_id, user_id)
        if stock:
            stock.quantity = quantity
            self.db.session.commit()
            return True
        return False

    def delete_stock(self, stock_id, user_id):
        stock = self.get_stock_by_id(stock_id, user_id)
        if stock:
            self.db.session.delete(stock)
            self.db.session.commit()
            return True
        return False
