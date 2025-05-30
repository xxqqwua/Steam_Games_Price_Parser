import aiohttp
from rapidfuzz import fuzz


class SteamGamePriceParser:
    def __init__(self, proxy=None):
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
        self.filter = [  # You can add additional words to filter the data
            'soundtrack',
            'sound track',
            'art book',
            'ost',
            'demo',
            'dlc',
            'trailer',
            'beta',
            'test',
            'editor',
            'tool',
            'server',
            'mod',
            'expansion',
            'pack',
            'bundle',
            'manual',
            'guide',
            'wallpaper',
            'sketchbook',
            'sound',
            'pass',
            ' -',  # Some dlc's are labeled with a '-' after the name of the game
            'edition'
        ]

        self.all_steam_games_url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        self.all_games = None
        self.proxy = proxy

    async def check_game_price(self, app_id, regions='all'):
        prices = {}

        if regions == 'all' or regions == '':
            iterator = self.regions.items()
        else:
            if isinstance(regions, str):
                # If regions is a string, split it by comma and remove spaces around each code.
                # The split(‘,’) method splits the string into substrings, and strip() removes extra spaces.
                region_codes = [code.strip() for code in regions.split(',')]
            elif isinstance(regions, list) or isinstance(regions, tuple):
                region_codes = regions  # If regions is a list or tuple, just use it as is.
            elif isinstance(regions, dict):
                region_codes = regions.keys()  # If regions is a dictionary, iterate over its keys.
            else:
                raise ValueError(
                    f"Unsupported 'regions' type: {type(regions).__name__}")  # If regions is not a string or a list, throw an error.

            # Create an iterator that will return pairs (country code, name).
            # self.regions.get() safely gets the country name by code, returning ‘Unknown (code)’ if no code is found.
            iterator = ((cc, self.regions.get(cc, f"Unknown ({cc})")) for cc in region_codes)

        async with aiohttp.ClientSession() as session:
            for cc, region in iterator:
                url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc={cc}&l=en"

                try:
                    async with session.get(url, proxy=self.proxy) as r:
                        raw = await r.json()
                        is_aviable = raw[str(app_id)]['success']

                        if is_aviable is False:
                            prices[region] = 'The game is not available in this region'
                            continue

                        price = raw[str(app_id)]['data'].get('price_overview')

                        if price:
                            if 'Unknown' in region:
                                raise ValueError(f"Unsupported region type: {region}")

                            current_price = price['final_formatted']
                            prices[region] = current_price
                        else:
                            prices[region] = "N/A"  # Some games on Steam have no price
                            continue

                except Exception as e:
                    return None, f"Error during region processing. Region: '{cc}'. Error: {e}"

        return prices

    async def check_game_name_by_app_id(self, app_id):
        if self.all_games is None:
            self.all_games = await checker(self.all_steam_games_url, proxy=self.proxy)

            apps = self.all_games['applist']['apps']
            for app in apps:
                if app['appid'] == app_id:
                    return app['name']
        return None

    async def check_game_app_id_by_name(self, game_name: str):
        """
        The performance of the method directly depends on the game name entered by the user
        Some games have a different name than the one displayed on the Steam website
        """
        if self.all_games is None:
            self.all_games = await checker(self.all_steam_games_url, proxy=self.proxy)

        seen_appids = set()
        games = []

        for app in self.all_games['applist']['apps']:
            if app['appid'] not in seen_appids:
                games.append(app)
                seen_appids.add(app['appid'])

        user_game_name = game_name.lower()
        filter_words = [word for word in self.filter if word not in game_name.lower()]
        threshold = 90

        for game in games:
            steam_game_name = game['name'].lower()

            if any(ban_word in steam_game_name for ban_word in filter_words):
                continue

            score = fuzz.token_sort_ratio(steam_game_name, user_game_name)
            if score >= threshold:
                return game['appid']
        return None


async def checker(url, proxy=None):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120)) as session:
        try:
            async with session.get(url, proxy=proxy) as r:
                raw = await r.json()
                return raw

        except Exception as e:
            raise RuntimeError(f"Error when parsing games. Error: {e}")
