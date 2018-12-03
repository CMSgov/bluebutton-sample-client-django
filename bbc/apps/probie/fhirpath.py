#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
Project: bbc_pd
App: apps.probie
FILE: fhirpath.py
Created: 7/20/18 9:01 AM

Created by: '@ekivemark'
"""

# import json
import jsonpath_rw_ext as jpath


def next_jpathname(parent_name, item):
    """

    :param parent_name:
    :param item:
    :return:
    """
    if len(parent_name) > 0:
        pathname = "%s.%s" % (parent_name, str(item))
    else:
        pathname = "$.%s" % (str(item))

    return pathname


def probie_jdict(item, val, ilist=[], parent_name="$"):  # , parent_seq="0"):
    """
    Receive item and value and return probie_dict
    :param item:
    :param val:
    :return:
    """

    o_dict = {}
    o_dict['name'] = item
    o_dict['type'] = type(val).__name__
    o_dict['value'] = val

    # print("Parent/Item:%s / %s" % (parent_name, str(item)))

    o_dict['pathName'] = next_jpathname(parent_name, str(item))

    # print("pathName:%s [parent:%s" % (o_dict['pathName'],parent_name))
    o_dict['level'] = o_dict['pathName'].count('.') - 1
    # print("Level:%s" % o_dict['level'])

    return o_dict


def get_fhir_jdict(idict={}, parent_name="$", flatten=True):
    """
    Pass in a dict and evaluate
    :param idict:
    :return: dict with fields {name, type, value, pathName, pathSeq}
    """

    o_list = []
    seq = 0

    for item, val in idict.items():
        oo_list = []

        if type(val) is dict:
            oo_list = get_fhir_jdict(val,
                                     next_jpathname(parent_name, str(item)),
                                     flatten)
            # print("In jdict with dict - Item:%s [parent:%s]" % (item, parent_name))
            o = probie_jdict(item,
                             val,
                             oo_list,
                             parent_name,
                             )

        elif type(val) is list:
            # print("Item[type]:%s[%s]" % (item, type(item)))
            # print("List Parent:%s" % parent_name)
            oo_list = get_fhir_jlist(val,
                                     next_jpathname(parent_name,
                                                    str(item),
                                                    ),
                                     flatten)
            # print("In jdict with list - Item:%s [parent:%s]" % (item, parent_name))

            o = probie_jdict('[*]',
                             val,
                             oo_list,
                             parent_name,
                             )

        elif type(val) is int:
            oo_list = []
            o = probie_jdict(item,
                             val,
                             oo_list,
                             parent_name,
                             )

        else:
            oo_list = []
            o = probie_jdict(item,
                             val,
                             oo_list,
                             parent_name,
                             )

        if type(val) is not 'list':
            o = probie_jdict(item,
                             val,
                             oo_list,
                             parent_name,
                             )

        # o = {}
        # o['name'] = item
        # o['type'] = type(val).__name__
        # o['value'] = val
        # o['pathName'] = parent_name + item

        o_list.append(o)
        if flatten:
            if len(oo_list) > 0:
                for i in oo_list:
                    o_list.append(i)

        seq += 1

    if o_list:
        if len(o_list) > 0:
            return o_list
    else:
        return


def get_fhir_jlist(ilist=[], parent_name="$", flatten=True):
    """
    Pass in list and evaluate
    :param ilist:
    :param parent_name:
    :param parent_seq:
    :return: dict with fields {name, type, value, pathName, pathSeq}
    """

    o_list = []
    o_dict = []
    seq = 0

    for item in ilist:
        oo_list = []
        if type(item) in [dict, list]:
            if type(item) is dict:
                # print("Parent_name/item:%s / %s" % (parent_name, item))
                oo_list = get_fhir_jdict(item,
                                         next_jpathname(parent_name,
                                                        "[%s]" % str(seq)),
                                         flatten)
                # print("In jlist with dict - Item:%s [parent:%s]" % (item, parent_name))

            else:
                oo_list = get_fhir_jlist(item,
                                         next_jpathname(parent_name,
                                                        "[%s]" % str(seq)),
                                         flatten)
                # print("In jlist with list - Item:%s [parent:%s]" % (item, parent_name))

            o_dict = probie_jdict('[*]',
                                  # str(seq),
                                  item,
                                  oo_list,
                                  parent_name,
                                  )
        else:
            # string
            # integer
            # bool
            o_dict = probie_jdict(str(seq),
                                  item,
                                  [],
                                  parent_name,
                                  )
        o_list.append(o_dict)
        if flatten:
            if len(oo_list) > 0:
                for i in oo_list:
                    o_list.append(i)

        seq += 1

    return o_list


def get_jpath(path="$", fhir_json={}):
    """

    :param path:
    :param fhir_json:
    :return result:
    """

    if path == "$.":
        return None

    return jpath.match(path, fhir_json)
