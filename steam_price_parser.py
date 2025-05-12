import asyncio

import aiohttp


class SteamPriceParser:
    def __init__(self):
        self.regions = {
            'us': 'U.S. Dollar',
            'ca': 'Canadian Dollar',
            'uk': 'British Pound',
            'eu': 'Euro',
            'ru': 'Russian Ruble',
            'ua': 'Ukrainian Hryvnia',
            'kz': 'Kazakhstani Tenge',
            # 'tr': 'Turkey',
            # 'ar': 'Argentina',
            'br': 'Brazilian Real',
            'mx': 'Mexican Peso',
            'in': 'Indian Rupee',
            'cn': 'Chinese Yuan',
            'jp': 'Japanese Yen',
            'au': 'Australian Dollar',
            'nz': 'New Zealand Dollar',
            'za': 'South African Rand',
            'ch': 'Swiss Franc',
            'no': 'Norwegian Krone',
            'pl': 'Polish Zloty',
            'sg': 'Singapore Dollar',
            'hk': 'Hong Kong Dollar',
            'kr': 'South Korean Won',
            'co': 'Colombian Peso',
            'vn': 'Vietnamese Dong',
            'id': 'Indonesian Rupiah',
            'cl': 'Chilean Peso',
            'pk': 'South Asia - USD',
            'ph': 'Philippine Peso',
            'uy': 'Uruguayan Peso',
            'pe': 'Peruvian Sol',
            'my': 'Malaysian Ringgit',
            'az': 'CIS - U.S. Dollar',
            'th': 'Thai Baht',
            'tw': 'Taiwan Dollar',
            'sa': 'Saudi Riyal',
            'qa': 'Qatari Riyal',
            'kw': 'Kuwaiti Dinar',
            'cr': 'Costa Rican Colon',
            'ae': 'U.A.E. Dirham',
            'il': 'Israeli New Shekel'
        }

        self.prices = {}
        self.all_steam_games_url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'

    async def check_game_price(self, app_id, regions='all'):
        if regions == 'all' or regions == '':
            iterator = self.regions.items()
        else:
            if isinstance(regions, str):
                # If regions is a string, split it by comma and remove spaces around each code.
                # The split(‘,’) method splits the string into substrings, and strip() removes extra spaces.
                region_codes = [code.strip() for code in regions.split(',')]
            elif isinstance(regions, list):
                region_codes = regions  # If regions is a list, just use it as is.
            elif isinstance(regions, dict):
                region_codes = regions.keys()  # If regions is a dictionary, iterate over its keys.
            else:
                raise ValueError(
                    f"Unsupported region type: {type(regions).__name__}")  # If regions is not a string or a list, throw an error.

            # Create an iterator that will return pairs (country code, name).
            # self.regions.get() safely gets the country name by code, returning ‘Unknown (code)’ if no code is found.
            iterator = ((cc, self.regions.get(cc, f"Unknown ({cc})")) for cc in region_codes)

        async with aiohttp.ClientSession() as session:
            for cc, region in iterator:
                url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc={cc}&l=en"

                try:
                    async with session.get(url) as r:
                        raw = await r.json()
                        is_aviable = raw[str(app_id)]['success']

                        if is_aviable is False:
                            self.prices[region] = 'The game is not available in this region'
                            continue

                        price = raw[str(app_id)]['data'].get('price_overview')

                        if price:
                            if 'Unknown' in region:
                                raise ValueError(f"Unsupported region type: {region}")

                            current_price = price['final_formatted']
                            self.prices[region] = current_price
                        else:
                            self.prices[region] = "N/A"
                            continue

                except Exception as e:
                    raise RuntimeError(f"Error during region processing {cc}: {e}")

    async def check_game_name_by_app_id(self, app_id):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.all_steam_games_url) as r:
                    raw = await r.json()
                    apps = raw['applist']['apps']
                    for app in apps:
                        if app['appid'] == app_id:
                            return app['name']
                    return None
            except Exception as e:
                raise RuntimeError(f"Error when checking game name processing: {e}")
