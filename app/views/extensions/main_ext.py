import base64
from os import path, getcwd

import haversine as hs
from haversine import Unit

from dijkstar import Graph, find_path

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans

import folium
from folium import IFrame
from folium.plugins import MarkerCluster

from flask import g

from .create_app import create_app
from .local_config import Config


app_context = create_app(Config).app_context()

start_point = [55.679138, 37.263658]
stop_point = [56.091329, 49.876984]
popup_start = "Ура! Поехали."
popup_stop = "Ура! Доехали."

tooltip_start = "Начало маршрута"
tooltip_stop = "Конец маршрута"


# Шаблон ответа сервера на запрос
def generate_resp(status, message, data):
    return {
        'status': status,
        'message': message,
        'data': data
    }


# Ответы сервера
def resp_ok(data=None):
    if data is None:
        data = []
    return generate_resp('ok', 'SUCCESS', data), 200


def preprocessing():
    data_path = path.join(getcwd(), 'data', 'unesco_2021.xls')
    data = pd.read_excel(data_path)

    data = data[
        data['states_name_en'] == 'Russian Federation'
        ].reset_index(drop=True)

    data['short_description_en'] = data['short_description_en'].str \
        .replace('<p>', '').replace('</p>', '')

    with app_context:
        if 'data' not in g:
            g.data = data


def get_unesco_popups():
    unesco_logo_path = path.join(getcwd(), 'img', 'unesco_logo.png')
    file = open(unesco_logo_path, 'rb')
    unesco_logo = base64.b64encode(file.read())
    file.close()
    unesco_logo = unesco_logo.decode('UTF-8')

    unesco_popups = []

    with app_context:
        for index, row in g.data.iterrows():
            name = row['name_en']
            description = row['short_description_en']

            html = f"""
                <b> NAME: </b> {name} <br>  <p>
                <b> DESCRIPTION: </b> {description} <br>
                <center> <img src="data:image/png;base64,{unesco_logo}"> </canter>
            """

            iframe = IFrame(html, width=500, height=300)

            popup = folium.Popup(iframe)
            unesco_popups.append(popup)

    return unesco_popups


def get_unesco_objects_coords():
    with app_context:
        lats = g.data['latitude'].to_list()
        lons = g.data['longitude'].to_list()

        locations = list(zip(lats, lons))
        return locations


def clustering_and_model_training():
    kmeans = KMeans(n_clusters=3, random_state=2021)
    locations = get_unesco_objects_coords()
    kmeans.fit(locations)
    with app_context:
        g.data['kmeans_class'] = kmeans.predict(locations)


def get_distance(row):
    loc1 = (row['lats_start'], row['lons_start'])
    loc2 = (row['lats_stop'], row['lons_stop'])

    return round(hs.haversine(loc1, loc2, unit=Unit.METERS))


def get_routes():
    clustering_and_model_training()
    with app_context:
        locations = get_unesco_objects_coords()
        distance_between_object = pd.DataFrame({
            'lats': [start_point[0], stop_point[0]] + [x[0] for x in locations],
            'lons': [start_point[1], stop_point[1]] + [x[1] for x in locations],
            'name': ['Name: Star Point', 'Name: End Points'] + [name for name in g.data['name_en']],
            'kmeans_class': [None, None] + g.data['kmeans_class'].to_list()
        }).reset_index()

        distance_between_object['merge'] = 1
        distance_between_object = distance_between_object.merge(
            distance_between_object,
            on='merge',
            suffixes=('_start', '_stop')
        )
        distance_between_object['distance'] = distance_between_object.apply(get_distance, axis=1)

        # Если объекты расположены рядом относительно друг друга, то
        # искусственно уменьшаем расстояние между ними. Это дает возможность
        # алгоритму рассмотреть как можно больше интересных маршрутов.

        distance_upd = []

        for i, row in distance_between_object.iterrows():
            if (row['index_start'] != row['index_stop']) & (row['kmeans_class_start'] == row['kmeans_class_stop']):
                distance_upd.append(row['distance'] * .9)
            else:
                distance_upd.append(row['distance'])

        distance_between_object['distance_upd'] = distance_upd

        graph = Graph()

        for i, row in distance_between_object.iterrows():
            graph.add_edge(row['index_start'], row['index_stop'], row['distance_upd'])

        routes = [find_path(graph, 0, 1)]

        uniqie_object = distance_between_object[
            distance_between_object.columns[:4]
        ].drop_duplicates().reset_index(drop=True)

        route_coordinates = []

        for i in routes[0].nodes:
            point = [
                uniqie_object[uniqie_object['index_start'] == i]['lats_start'].iloc[0],
                uniqie_object[uniqie_object['index_start'] == i]['lons_start'].iloc[0]
            ]

            route_coordinates.append(point)

        return route_coordinates


def generate_map():
    vladimir_city_path = path.join(getcwd(), 'img', 'vladimir_city.png')
    file = open(vladimir_city_path, 'rb')
    vladimir_city_encoded = base64.b64encode(file.read())
    file.close()

    vladimir_city_encoded = vladimir_city_encoded.decode('UTF-8')

    vladimir_city_html = '<img src="data:image/png;base64,{}">'.format
    vladimir_city_iframe = IFrame(vladimir_city_html(vladimir_city_encoded), width=570, height=330)
    vladimir_city_popup = folium.Popup(vladimir_city_iframe)
    vladimir_city_icon = folium.Icon(color="cadetblue", icon="glyphicon glyphicon-camera")

    locations = get_unesco_objects_coords()
    unesco_popups = get_unesco_popups()
    route_coordinates = get_routes()
    m = folium.Map(
        location=[
            np.mean([start_point[0], stop_point[0]]),
            np.mean([start_point[1], stop_point[1]]),
        ],
        tiles="Cartodb Positron", zoom_start=6
    )

    marker_cluster = MarkerCluster(
        locations=locations,
        popups=unesco_popups,
        name="Объекты ЮНЕСКО",
        overlay=True,
        control=True,
    ).add_to(m)

    feature_group_1 = folium.FeatureGroup(name='Кратчайший путешествия', overlay=True)
    folium.Marker(
        start_point,
        popup=popup_start,
        tooltip=tooltip_start,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(feature_group_1)

    folium.Marker(
        stop_point,
        popup=popup_stop,
        tooltip=tooltip_stop,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(feature_group_1)

    folium.PolyLine([start_point, stop_point], color='red').add_to(feature_group_1)
    m.add_child(feature_group_1)

    feature_group_2 = folium.FeatureGroup(name='Рекомендованный маршрут', overlay=True)
    folium.PolyLine(route_coordinates, color='green').add_to(feature_group_2)
    m.add_child(feature_group_2)

    feature_group_3 = folium.FeatureGroup(name='Исследованные места', overlay=True)
    folium.Marker(
        [56.128966, 40.406287],
        popup=vladimir_city_popup, icon=vladimir_city_icon
    ).add_to(feature_group_3)
    m.add_child(feature_group_3)

    folium.LayerControl().add_to(m)

    return m

