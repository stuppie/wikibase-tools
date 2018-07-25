#!/usr/bin/env python

"""
Initial setup of blank wikibase

Create a "equivalent property" property, set equiv prop statement on it to point to the OWL owl#equivalentProperty
Create an "equivalent class" property, which equiv prop -> owl#equivalentClass

"""
import time
from wikidataintegrator import wdi_core, wdi_login
CORE_PROPS = set()

from wikibase_tools.config import WDQS_FRONTEND_PORT, WIKIBASE_PORT, USER, PASS, HOST

mediawiki_api_url = "http://{}:{}/w/api.php".format(HOST, WIKIBASE_PORT)
sparql_endpoint_url = "http://{}:{}/proxy/wdqs/bigdata/namespace/wdq/sparql".format(HOST, WDQS_FRONTEND_PORT)
localItemEngine = wdi_core.WDItemEngine.wikibase_item_engine_factory(mediawiki_api_url, sparql_endpoint_url)


def create_equiv_property_property(login):
    # create a property for "equivalent property"
    # https://www.wikidata.org/wiki/Property:P1628
    item = localItemEngine(item_name="equivalent property", domain="foo")
    item.set_label("equivalent property")
    item.set_description("equivalent property in other ontologies (use in statements on properties, use property URI)")
    item.write(login, entity_type="property", property_datatype="url")

    equiv_prop_pid = item.wd_item_id
    # add equiv prop statement to equiv prop
    item = localItemEngine(wd_item_id=equiv_prop_pid)
    del item.wd_json_representation['sitelinks']
    s = wdi_core.WDUrl("http://www.w3.org/2002/07/owl#equivalentProperty", equiv_prop_pid)
    item.update(data=[s])
    item.write(login)
    # so the updater updates blazegraph
    time.sleep(30)
    return equiv_prop_pid


def create_equiv_class_property(login):
    label = "equivalent class"
    description = "equivalent class in other ontologies (use property URI)"
    property_datatype = "url"
    create_property(label, description, property_datatype, ["http://www.wikidata.org/entity/P1709",
                                                            "http://www.w3.org/2002/07/owl#equivalentClass",
                                                            "http://www.w3.org/2004/02/skos/core#exactMatch"], login)


def get_quiv_prop_pid():
    # get the equivalent property property without knowing the PID for equivalent property!!!
    query = '''SELECT * WHERE {
      ?item ?prop <http://www.w3.org/2002/07/owl#equivalentProperty> .
      ?item <http://wikiba.se/ontology#directClaim> ?prop .
    }'''
    pid = wdi_core.WDItemEngine.execute_sparql_query(query, endpoint=sparql_endpoint_url)
    pid = pid['results']['bindings'][0]['prop']['value']
    pid = pid.split("/")[-1]
    return pid


def get_quiv_class_pid():
    # get the equivalent property property without knowing the PID for equivalent property!!!
    query = '''SELECT * WHERE {{
      ?prop wdt:{} <http://www.w3.org/2002/07/owl#equivalentClass> .
    }}'''.format(get_quiv_prop_pid())
    pid = wdi_core.WDItemEngine.execute_sparql_query(query, endpoint=sparql_endpoint_url)
    pid = pid['results']['bindings'][0]['prop']['value']
    pid = pid.split("/")[-1]
    return pid


def create_property(label, description, property_datatype, equiv_props, login):
    CORE_PROPS.add(get_quiv_prop_pid())
    s = [wdi_core.WDUrl(equiv_prop, get_quiv_prop_pid()) for equiv_prop in equiv_props]
    item = localItemEngine(item_name=label, domain="foo", data=s)
    item.set_label(label)
    item.set_description(description)
    item.write(login, entity_type="property", property_datatype=property_datatype)
    return item


def create_item(label, description, equiv_classes, login):
    CORE_PROPS.add(get_quiv_class_pid())
    s = [wdi_core.WDUrl(equiv_class, get_quiv_class_pid()) for equiv_class in equiv_classes]
    item = localItemEngine(item_name=label, domain="foo", data=s)
    item.set_label(label)
    item.set_description(description)
    item.write(login)
    return item


if __name__ == "__main__":
    login = wdi_login.WDLogin(USER, PASS, mediawiki_api_url=mediawiki_api_url)
    create_equiv_property_property(login)
    create_equiv_class_property(login)

    # wdi_helpers.id_mapper(get_quiv_prop_pid(), endpoint=sparql_endpoint_url)
