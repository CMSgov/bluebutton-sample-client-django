import requests
import json

def get_practitioner(npi):
    """Returns a Practitioner Resource from Djmongo"""
    url = "https://registry.npi.io/search/fhir/Practitioner.json" \
          "?identifier.value=%s" % (npi)
    response = requests.get(url)
    try:
        jr = json.loads(response.text)

        if 'results' not in jr:
            jr = {'error', 'The lookup failed. Invalid response from server'}

        if not jr['results']:
                jr = {'error', 'Invalid NPI'}
    except ValueError:
        jr = {'error',
              'The lookup failed. JSON was not returned from the server.'}

    return jr['results'][0]

def convert_practitioner_fhir_to_form(pract_res, user):
    """Converts a Practitioner Resource into Values for Form"""
    data = {}
    data['user'] = user
    data['first_name']= pract_res['name'][0]['given'][0]
    data['last_name']= pract_res['name'][0]['family'][0]
    data['npi']= pract_res['identifier'][0]['value']
    data['fhir_id']= pract_res['id']


    return data


def convert_practitioner_fhir_to_meta(pract_res, user):
    """Converts a Practitioner Resource into Values for Meta"""
    data = {}
    data['user'] = user
    data['npi']= pract_res['identifier'][0]['value']
    data['first_name']= pract_res['name'][0]['given'][0]
    data['last_name']= pract_res['name'][0]['family'][0]
    data['fhir_id']= pract_res['id']


    return data

def get_pecos_individual_affliliation(npi):
    """Returns a Pecos Affiliation Resource from Djmongo"""
    url = "https://registry.npi.io/search/pecos/compiled_individuals." \
          "json?NPI=%s" % (npi)
    response = requests.get(url)
    try:
        jr = json.loads(response.text)

        if 'results' not in jr:
            jr = {'error', 'The lookup failed. Invalid response from server'}

        if not jr['results']:
                jr = {'error', 'Invalid NPI'}
    except ValueError:
        jr = {'error',
              'The lookup failed. JSON was not returned from the server.'}

    return jr['results'][0]['works_for']

def convert_pecos_to_form(pecos_res, user):
    """Converts a Practitioner Resource into Values for Form"""
    data = {}
    data['user'] = user
    data['name']= pecos_res[0]['NAME']
    data['npi']= pecos_res[0]['NPI']
    data['description']= pecos_res[0]['DESCRIPTION']

    return data


def convert_pecos_to_meta(pecos_res, user):
    """Converts a Practitioner Resource into Values for Meta"""
    data = {}
    data['user'] = user
    data['npi']= pecos_res['identifier'][0]['value']
    data['fhir_id']= pecos_res['id']

    return data

# if __name__ == "__main__":
#     print(get_pecos_individual_affliliation(1205824083))
