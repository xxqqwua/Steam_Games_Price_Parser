# Steam Game Price Parser

Script for parsing game prices on the Steam in different price regions!

## Table of Contents

- [Requirements](#Requirements)
- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)

## Features:

- Asynchrony, all actions are asynchronous
- Proxy support
- Support for all Steam price regions

## Requirements:

**On Windows the Visual C++ 2019 redistributable is required.**

This is due to the library for searching for games and their matches from the list issued by Steam, which uses this
dependency.

## Installation:

**1. Clone the Repository**

```bash
git clone https://github.com/xxqqwua/Steam_Games_Price_Parser
cd Steam_Games_Price_Parser
```

**2. Install Dependencies**

```bash
pip install -r requirements.txt
```

## Usage:

To implement this script in your project, you can follow a similar approach as shown below:

```python
import asyncio

from SteamGamePriceParser import SteamGamePriceParser

s = SteamGamePriceParser()


async def main():
    game_id = await s.check_game_app_id_by_name('Shadows of Doubt')
    prices = await s.check_game_price(game_id)
    print(prices)


if __name__ == '__main__':
    asyncio.run(main())
```
**Output:** `{'U.S. Dollar': '$19.99', 'Canadian Dollar': 'CDN$ 26.00', ...other 35 currencies... 'Israeli New Shekel': '₪74.36'}`

The script supports **different price regions** for each of the games:

```python
import asyncio

from SteamGamePriceParser import SteamGamePriceParser

s = SteamGamePriceParser()

regions_tuple = ('us', 'eu', 'uk')

async def main():
    game_id = await s.check_game_app_id_by_name('Shadows of Doubt')
    prices = await s.check_game_price(game_id, regions=regions_tuple)
    print(prices)


if __name__ == '__main__':
    asyncio.run(main())
```

**Output:** `{'U.S. Dollar': '$1.94', 'Euro': '$1.94 USD', 'British Pound': '£1.66'}`

<br>`regions` supports several types of data: string, list, tuple, and dictionary.

## How does it work?

By sending requests to several api.steam sites, the script receives the necessary information in json format.