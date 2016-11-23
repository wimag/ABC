from server import db

def init_db(app):
    import models
    try:
        db.create_all(app=app) # I DO create everything
    except e:
        print(e)
    return db