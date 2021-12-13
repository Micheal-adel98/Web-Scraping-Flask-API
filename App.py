from flask import Flask, jsonify 
from flask_restful import Resource, Api , reqparse
import pandas as pd


app=Flask(__name__)
api=Api(app)

data_arg=reqparse.RequestParser()
data_arg.add_argument('id', required=True)
data_arg.add_argument('Author', required=True)
data_arg.add_argument('Authors link', required=True)
data_arg.add_argument('Book Name', required=True)
data_arg.add_argument('Book link', required=True)
data_arg.add_argument('country', required=True)
data_arg.add_argument('country link', required=True)

class getBook(Resource):
    def __init__(self):
        # read csv file
        self.data = pd.read_csv('books.csv',encoding='utf-16',delimiter="\t")
    # GET request on the url will hit this function
    def get(self):
        # find data from csv 
        data_fount=self.data.to_json(orient="records")
        # return data found in csv
        return jsonify({'message': data_fount})


class addBook(Resource):
    def __init__(self):
        # read csv file
        self.data = pd.read_csv('books.csv',encoding='utf-16',delimiter="\t")
    def post(self):
        # data parser to parse data from url
        args = data_arg.parse_args()
        # if ID is already present
        if((self.data['id']== args.id).any()):
            return jsonify({"message": 'ID already exist'})
        else:
            # Save data to csv
            self.data= self.data.append(args, ignore_index=True)
            self.data.to_csv("books.csv", index=False,encoding="utf-16")
            return jsonify({"message": 'Done'})  


class deleteBook(Resource):
    def delete(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        args = parser.parse_args()
        
        data = pd.read_csv('books.csv',encoding="utf-16")
        
        data = data[data['id'] != args['id']]
        
        data.to_csv('books.csv', index=False,encoding="utf-16")

        return {'message': 'Record deleted successfully.'}, 200

            
 
api.add_resource(getBook, '/getAllBooks',methods=['GET'])
api.add_resource(addBook, '/postBook',methods=['POST'])
api.add_resource(deleteBook, '/deleteBook',methods=['DELETE'])

if __name__ == '__main__':
    app.run(debug=True)   