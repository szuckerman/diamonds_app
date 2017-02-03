from app import app, db, models as m
from sqlalchemy import func
from flask import render_template
from flask_table import Table, Col, create_table
import pandas as pd

conn = db.engine

class DollarCol(Col):
    def td_format(self, content):
        if type(content) is str: #Change to the next line for python2
        # if type(content) is unicode:
            return content
        else:
            return "${:,.0f}".format(content)


class DIAMONDS_Table(Table):
    classes = ['table', 'table-bordered', 'table-hover', 'table-striped']
    diamond_id = Col('diamond_id')
    carat = Col('carat')
    cut = Col('cut')
    color = Col('color')
    clarity = Col('clarity')
    depth = Col('depth')
    table = Col('table')
    price = DollarCol('price')
    x = Col('x')
    y = Col('y')
    z = Col('z')


@app.route('/')
def index():

    # Top boxes of 'counts'
    ideal = m.diamonds.query.filter_by(cut='Ideal').count()
    premium = m.diamonds.query.filter_by(cut='Premium').count()
    very_good = m.diamonds.query.filter_by(cut='Very Good').count()
    good = m.diamonds.query.filter_by(cut='Good').count()

    # Dropdown tables
    ideal_expensive = m.diamonds.query.filter_by(cut='Ideal').order_by(m.diamonds.price.desc()).all()
    ideal_expensive = DIAMONDS_Table(ideal_expensive[:15]).__html__()

    premium_expensive = m.diamonds.query.filter_by(cut='Premium').order_by(m.diamonds.price.desc()).all()
    premium_expensive = DIAMONDS_Table(premium_expensive[:15]).__html__()

    very_good_expensive = m.diamonds.query.filter_by(cut='Very Good').order_by(m.diamonds.price.desc()).all()
    very_good_expensive = DIAMONDS_Table(very_good_expensive[:15]).__html__()

    good_expensive = m.diamonds.query.filter_by(cut='Good').order_by(m.diamonds.price.desc()).all()
    good_expensive = DIAMONDS_Table(good_expensive[:15]).__html__()

    # Average price table
    u = (db.session.query(
            m.diamonds.color,
            m.diamonds.cut,
            func.avg(m.diamonds.price).label('AVERAGE_PRICE'))
            .group_by(m.diamonds.color,
            m.diamonds.cut).all())

    colors = {'D', 'E', 'F', 'G', 'H', 'I', 'J'}

    morris_data_list = []
    morris_flattened_list = []
    for c in colors:
        for i in range(len(u)):
            if u[i][0] == c:
                morris_data_list.append({'COLOR': c, u[i][1]: round(u[i][2])})
        temp_dict = {}
        for d in morris_data_list:
            temp_dict.update(d)
        morris_flattened_list.append(temp_dict)    

    morris_flattened_list = sorted(morris_flattened_list, key=lambda x: x['COLOR'])

    # Largest diamonds
    dat = pd.read_sql_table('diamonds', conn)
    volume = dat.x * dat.y * dat.z
    dat['volume'] = round(volume,2)
    largest_diamonds = (dat.sort_values('volume', ascending = False)
        .head(15)
        .to_html(index=False, 
        classes=['table', 'table-bordered', 'table-hover', 'table-striped'], 
        columns=['diamond_id', 'carat', 'cut', 'color', 'clarity', 'depth', 
                 'table', 'price', 'x', 'y', 'z', 'volume']))

    # Pie chart
    pie_chart_data_list = []
    pie_chart_data = (db.session.query(
            m.diamonds.color,
            func.count(m.diamonds.color).label('NUM_DIAMONDS'))
            .group_by(m.diamonds.color).all())

    for item in pie_chart_data:
        pie_chart_data_list.append({'label': item[0], 'value': item[1]})

    return render_template('diamonds.html',
            ideal = ideal,
            premium = premium,
            very_good = very_good,
            good = good,
            ideal_expensive = ideal_expensive,
            premium_expensive = premium_expensive,
            very_good_expensive = very_good_expensive,
            good_expensive = good_expensive,
            morris_flattened_list = morris_flattened_list,
            largest_diamonds = largest_diamonds,
            donut_chart = pie_chart_data_list
    )




