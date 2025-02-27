"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE = "https://tinyurl.com/demo-cupcake"

db = SQLAlchemy()

class Cupcake(db.Model):
    """Cupcake"""

    __tablename__ = "cupcake"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    flavor = db.Column(db.Text,
                       nullable=False)
    size = db.Column(db.Text,
                     nullable=False)
    rating =db.Column(db.Float,
                      nullable=False)
    image = db.Column(db.Text,
                      nullable=False,
                      default=DEFAULT_IMAGE)
    
    def to_dict(self):
        """Serialize cupcake to dict of cupcake info"""
    
        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image,
        }
    
def connect_db(app):
    """Connect this database to provide Flask app"""

    db.app = app
    db.init_app(app)