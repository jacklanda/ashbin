import time


def find(query=None, id=None, page=0, sort_query=None):
    if sort_query is None:
        sort_query = [("_id", 1)]
    if id:
        for document in find({'_id': {'$gt': id}}).sort(sort_query).limit(1):
            return document
    else:
        for document in find(query).sort(sort_query).limit(1).skip(page):
            return document


def find_one(collection=None, query=None):
    try:
        document = collection.find_one(query)
        return document
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '查找失败', query, e)


def insert_one(collection=None, query=None):
    try:
        if collection.find_one({'_id': query['_id']}):
            print(time.strftime('%Y-%m-%d %H:%M:%S'), '已经存在', query)
        else:
            document = collection.insert_one(query)
            print(time.strftime('%Y-%m-%d %H:%M:%S'), '插入成功', query)
            return document
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '插入失败', query, e)


def delete_one(collection=None, query=None):
    try:
        if collection.find_one({'_id': query['_id']}):
            collection.delete_one({'_id': query['_id']})
            print(time.strftime('%Y-%m-%d %H:%M:%S'), '删除成功', query)
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), '删除失败', query, e)


def get_count(collection=None, query=None):
    if collection.find_one({'_id': query['_id']}):
        count = collection.count_documents(query)
        return count
