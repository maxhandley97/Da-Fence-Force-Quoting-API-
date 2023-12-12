# from main import db, ma
# from marshmallow import fields

# class Quote(db.Model):
#     quote_id = db.Column(db.Integer, primary_key=True)
#     fence_type = db.Column(db.String(255))
#     fence_height_mm = db.Column(db.Integer)
#     fence_length_m = db.Column(db.Float)
#     images_url = db.Column(db.String(255))
#     status = db.Column(db.String(255))
#     date_posted = db.Column(db.Date)

#     job = db.relationship('Job', uselist=False, back_populates='quote')
#     barters = db.relationship('Barter', back_populates='quote')

# class QuoteSchema(ma.Schema):
#     class Meta:
#         fields = ('quote_id', 'fence_type', 'fence_height_mm', 'fence_length_m',
#                   'images_url', 'status', 'date_posted')

#     job = fields.Nested('JobSchema', exclude=('quote',), dump_only=True)
#     barters = fields.Nested('BarterSchema', exclude=('quote',), many=True)