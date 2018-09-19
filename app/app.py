
import os
from urllib.parse import quote_plus

from flask import Flask, g, render_template
from pymongo import MongoClient


def _connect_db():
    """Connect to the MongoDB"""
    username = quote_plus(os.environ["MONGO_INITDB_ROOT_USERNAME"])
    password = quote_plus(os.environ["MONGO_INITDB_ROOT_PASSWORD"])
    uri = "mongodb://{}:{}@db".format(username, password)
    client = MongoClient(uri)
    return client.db


app = Flask(__name__)


@app.before_first_request
def initialize_db():
    """Initialize database."""

    ground_truth = """CPvalid1_48_40x_Tiles_p0003DAPI 23 24
    CPvalid1_48_40x_Tiles_p0151DAPI 14 17
    CPvalid1_48_40x_Tiles_p0313DAPI 11 13
    CPvalid1_48_40x_Tiles_p0529DAPI 18 21
    CPvalid1_48_40x_Tiles_p0719DAPI 7 9
    CPvalid1_48_40x_Tiles_p0881DAPI 15 18
    CPvalid1_48_40x_Tiles_p1016DAPI 13 14
    CPvalid1_48_40x_Tiles_p1205DAPI 10 13
    CPvalid1_48_40x_Tiles_p1394DAPI 18 20
    CPvalid1_48_40x_Tiles_p1583DAPI 18 21
    CPvalid1_340_40x_Tiles_p0002DAPI 17 19
    CPvalid1_340_40x_Tiles_p0109DAPI 14 19
    CPvalid1_340_40x_Tiles_p0244DAPI 10 17
    CPvalid1_340_40x_Tiles_p0378DAPI 9 18
    CPvalid1_340_40x_Tiles_p0540DAPI 9 14
    CPvalid1_340_40x_Tiles_p0702DAPI 17 20
    CPvalid1_340_40x_Tiles_p0865DAPI 7 11
    CPvalid1_340_40x_Tiles_p1013DAPI 10 13
    CPvalid1_340_40x_Tiles_p1175DAPI 15 19
    CPvalid1_340_40x_Tiles_p1365DAPI 9 14
    CPvalid1_Anillin_40x_Tiles_p0002DAPI 32 47
    CPvalid1_Anillin_40x_Tiles_p0081DAPI 21 32
    CPvalid1_Anillin_40x_Tiles_p0190DAPI 39 51
    CPvalid1_Anillin_40x_Tiles_p0338DAPI 34 53
    CPvalid1_Anillin_40x_Tiles_p0447DAPI 26 50
    CPvalid1_Anillin_40x_Tiles_p0582DAPI 47 71
    CPvalid1_Anillin_40x_Tiles_p0717DAPI 40 55
    CPvalid1_Anillin_40x_Tiles_p0852DAPI 43 68
    CPvalid1_Anillin_40x_Tiles_p1069DAPI 32 42
    CPvalid1_Anillin_40x_Tiles_p1286DAPI 28 46
    CPvalid1_mad2_40x_Tiles_p0004DAPI 137 128
    CPvalid1_mad2_40x_Tiles_p0044DAPI 106 101
    CPvalid1_mad2_40x_Tiles_p0125DAPI 127 120
    CPvalid1_mad2_40x_Tiles_p0260DAPI 72 75
    CPvalid1_mad2_40x_Tiles_p0394DAPI 134 132
    CPvalid1_mad2_40x_Tiles_p0841DAPI 172 160
    CPvalid1_mad2_40x_Tiles_p0853DAPI 148 142
    CPvalid1_mad2_40x_Tiles_p0880DAPI 141 126
    CPvalid1_mad2_40x_Tiles_p0907DAPI 187 183
    CPvalid1_mad2_40x_Tiles_p1072DAPI 153 146
    CPvalid1_nodsRNA_40x_Tiles_p0003DAPI 119 119
    CPvalid1_nodsRNA_40x_Tiles_p0016DAPI 114 112
    CPvalid1_nodsRNA_40x_Tiles_p0098DAPI 126 126
    CPvalid1_nodsRNA_40x_Tiles_p0151DAPI 156 159
    CPvalid1_nodsRNA_40x_Tiles_p0219DAPI 187 182
    CPvalid1_nodsRNA_40x_Tiles_p1540DAPI 106 107
    CPvalid1_nodsRNA_40x_Tiles_p1648DAPI 117 115
    CPvalid1_nodsRNA_40x_Tiles_p1703DAPI 144 144
    CPvalid1_nodsRNA_40x_Tiles_p1730DAPI 159 158
    CPvalid1_nodsRNA_40x_Tiles_p1745DAPI 149 147"""

    data = list()
    for field_id, row in enumerate(ground_truth.split("\n")):
        name, human1, human2 = row.split()
        entry = dict(field_id=field_id+1, name=name,
                human1=int(human1), human2=int(human2))
        data.append(entry)

    db = _connect_db()
    db.drosophila.drop()
    db.drosophila.insert_many(data)


@app.before_request
def connect_db() :
    g.db = _connect_db()


@app.route("/")
def index():
    return render_template("welcome.html", count=g.db.drosophila.count())


@app.route("/fields/")
@app.route("/fields/<int:field_id>")
def fields(field_id=None):
    if field_id is not None:
        count = g.db.drosophila.count()
        prev_id = count if field_id == 1 else field_id - 1
        next_id = 1 if field_id == count else field_id + 1
        return render_template("field.html", title="Field {}".format(field_id),
                prev_id=prev_id, next_id=next_id,
                entry=g.db.drosophila.find_one({"field_id":field_id}))
    else:
        return render_template("fields.html", title="All Fields", 
                data=g.db.drosophila.find())
