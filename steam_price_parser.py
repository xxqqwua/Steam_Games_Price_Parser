import asyncio


class SteamPriceParser:
    def __init__(self):
        self.regions = {
            'us': 'USA',
            'ca': 'Canada',
            'gb': 'Great Britain',
            'eu': 'Europe',  # European Union
            'ru': 'Russia',
            'ua': 'Ukraine',
            'kz': 'Kazakhstan',
            # 'tr': 'Turkey',
            'ar': 'Argentina',
            'br': 'Brazil',
            'mx': 'Mexico',
            'in': 'India',
            'cn': 'China',
            'jp': 'Japan',
            'au': 'Australia',
            'nz': 'New Zealand',
            'za': 'South Africa',
            'ch': 'Switzerland',
            'no': 'Norway',
            'se': 'Sweden',
            'dk': 'Denmark',
            'pl': 'Poland',
            'cz': 'Czech Republic',
            'hu': 'Hungary',
            'sg': 'Singapore',
            'hk': 'Hong Kong',
            'kr': 'Korea',
        }
