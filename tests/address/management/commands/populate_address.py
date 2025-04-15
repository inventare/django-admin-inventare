from django.core.management import BaseCommand
from tests.address.models import Region, State, City
import requests

class Command(BaseCommand):
    populated_regions = {}

    def get_regions(self):
        url = 'https://raw.githubusercontent.com/chandez/Estados-Cidades-IBGE/refs/heads/master/json/regioes.json'
        response = requests.get(url)
        json = response.json()
        return json.get('data')
    
    def populate_regions(self, regions):
        self.populated_regions = {}
        for item in regions:
            id = item.get('Id')
            name = item.get('Nome')
            instance, _ = Region.objects.update_or_create(name=name)
            self.populated_regions[id] = instance

    def get_states(self):
        url = 'https://raw.githubusercontent.com/chandez/Estados-Cidades-IBGE/refs/heads/master/json/estados.json'
        response = requests.get(url)
        json = response.json()
        return json.get('data')

    def populate_states(self, states):
        for item in states:
            code = item.get('CodigoUf')
            name = item.get('Nome')
            acronym = item.get('Uf')
            region = item.get('Regiao')
            if not region in self.populated_regions:
                continue
            region = self.populated_regions[region]

            State.objects.update_or_create(
                acronym=acronym,
                defaults={
                    'code': code,
                    'name': name,
                    'region': region,
                }
            )

    def get_cities(self):
        url = 'https://raw.githubusercontent.com/chandez/Estados-Cidades-IBGE/refs/heads/master/json/municipios.json'
        response = requests.get(url)
        json = response.json()
        return json.get('data')

    def populate_cities(self, cities):
        for item in cities:
            code = item.get('Codigo')
            name = item.get('Nome')
            state = item.get('Uf')
            state = State.objects.get(acronym=state)

            City.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                    'state': state,
                }
            )

    def handle(self, *args, **options):
        regions = self.get_regions()
        self.populate_regions(regions)
        states = self.get_states()
        self.populate_states(states)
        cities = self.get_cities()
        self.populate_cities(cities)

