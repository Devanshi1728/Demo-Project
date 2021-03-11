from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from CustomDecorators import *
from models.category import *

class Item(Resource):    
   #@admin_required
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('item_name', type=str, required=True)
        parse.add_argument('item_price', type=str, required=True)
        parse.add_argument('category_id', type=str, required=True)
    
        data = parse.parse_args()
        item = ItemModel.find_by_item_name(data['item_name'])
        if item:
            return {
                "ItemAlreadyExistsError": {
                    "message": "Item with given name already exists"
                }}, 400

        category = CategoryModel.find_by_cat_id(data['category_id'])
        if category:
            item = ItemModel(data['item_name'],
                             data['item_price'], data['category_id'])
            item.save_to_db()

            return {
                "message": "Item Added Successfully"
            }, 200

        return {
            "message": "Category is not added"
        }

    @admin_required
    def get(self, id):
        parse = reqparse.RequestParser()
        parse.add_argument('item_name', type=str, required=True)
        item = ItemModel.find_by_id(id)
        if item:
            return item.json()
        return {
            "ItemNotExistsError": {
                "message": "Item with given name doesn't exists",
            }}, 400

    @admin_required
    def delete(self):
        parse = reqparse.RequestParser()
        parse.add_argument('item_name', type=str, required=True)

        data = parse.parse_args()
        item = ItemModel.find_by_item_name(data['item_name'])
        if item:
            item.delete_from_db()
            return {
                "message": "Item Deleted"
            }, 200
        return{
            "NotFoundError": "Item not Found.."
        }, 404

    @admin_required
    def put(self, id):
        parse = reqparse.RequestParser()
        parse.add_argument('item_name', type=str, required=True)
        parse.add_argument('item_price', type=str, required=True)
        parse.add_argument('category_id', type=str, required=True)

        Item = ItemModel.find_by_id(id)
        
        if Item:
            data = parse.parse_args()
            Item.item_name = data['item_name']
            Item.item_price = data['item_price']
            Item.category_id = data['category_id']
            Item.save_to_db()
            return {"updated": True, "data": Item.json()}, 200

class ItemList(Resource):
    @admin_required
    def get(self):
        items = [item.json() for item in ItemModel.query.all()]
        return {"TotalItems": len(items), "Items": items,  "status": 'ok'}, 200
