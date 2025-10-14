
# Flask-RESTX version of the API
from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
from .database import db
from .models import Product
from .utils import parse_csv, validate_row

api = Namespace("products", description="Product operations")

product_model = api.model('Product', {
    'sku': fields.String(required=True),
    'name': fields.String(required=True),
    'brand': fields.String(required=True),
    'color': fields.String,
    'size': fields.String,
    'mrp': fields.Float(required=True),
    'price': fields.Float(required=True),
    'quantity': fields.Integer,
})

upload_response = api.model('UploadResponse', {
    'stored': fields.Integer,
    'failed': fields.List(fields.Raw)
})

list_response = api.model('ListResponse', {
    'total': fields.Integer,
    'page': fields.Integer,
    'limit': fields.Integer,
    'items': fields.List(fields.Nested(product_model))
})

@api.route('/upload')
class UploadResource(Resource):
    @api.expect(api.parser().add_argument('file', location='files', type='file', required=True))
    @api.marshal_with(upload_response)
    def post(self):
        """Upload a CSV file of products"""
        if "file" not in request.files:
            api.abort(400, "file_required")
        f = request.files["file"]
        rows = parse_csv(f.stream)
        stored = 0
        failed = []
        for i, row in enumerate(rows, start=1):
            ok, errors, parsed = validate_row(row)
            if not ok:
                failed.append({"sku": row.get("sku"), "errors": errors})
                continue
            existing = Product.query.filter_by(sku=row.get("sku")).first()
            if existing:
                # Do not update, treat as duplicate
                failed.append({"sku": row.get("sku"), "errors": ["duplicate_or_constraint_error"]})
                continue
            p = Product(
                sku=row.get("sku"),
                name=row.get("name"),
                brand=row.get("brand"),
                color=row.get("color"),
                size=row.get("size"),
                mrp=parsed["mrp"],
                price=parsed["price"],
                quantity=parsed["quantity"] or 0,
            )
            db.session.add(p)
            try:
                db.session.commit()
                stored += 1
            except Exception as e:
                db.session.rollback()
                failed.append({"sku": row.get("sku"), "errors": ["duplicate_or_constraint_error"]})
        return {"stored": stored, "failed": failed}


@api.route('/products')
class ListProductsResource(Resource):
    @api.doc(params={
        'page': {'description': 'Page number', 'type': 'int', 'default': 1},
        'limit': {'description': 'Items per page', 'type': 'int', 'default': 20},
    })
    @api.marshal_with(list_response)
    def get(self):
        """List all products with pagination"""
        try:
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 20))
        except Exception:
            api.abort(400, "invalid_pagination")
        query = Product.query
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "items": [i.to_dict() for i in items],
        }


@api.route('/products/search')
class SearchProductsResource(Resource):
    @api.doc(params={
        'brand': {'description': 'Brand name', 'type': 'string'},
        'color': {'description': 'Color', 'type': 'string'},
        'minPrice': {'description': 'Minimum price', 'type': 'float'},
        'maxPrice': {'description': 'Maximum price', 'type': 'float'},
    })
    @api.marshal_list_with(product_model)
    def get(self):
        """Search products by brand, color, price range"""
        brand = request.args.get("brand")
        color = request.args.get("color")
        try:
            min_price = float(request.args.get("minPrice")) if request.args.get("minPrice") else None
            max_price = float(request.args.get("maxPrice")) if request.args.get("maxPrice") else None
        except Exception:
            api.abort(400, "invalid_price_range")
        query = Product.query
        if brand:
            query = query.filter(Product.brand.ilike(f"%{brand}%"))
        if color:
            query = query.filter(Product.color.ilike(f"%{color}%"))
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        items = query.all()
        return [i.to_dict() for i in items]
