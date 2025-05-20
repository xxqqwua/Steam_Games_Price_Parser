# [NAME OF SCRIPT]

desc


## Table of Contents

- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)
- [Req](#Req)


## Features:

- Asynchrony, all actions are asynchronous
- Optimization, no repetitive requests to the server
- Proxy support
- Support for different data types

## Req:
On Windows the Visual C++ 2019 redistributable is required

## Installation:

**Clone the Repository**

```bash
git clone [url]
cd [represetoryName]
```

**Install Dependencies**

```bash
pip install -r requirements.txt
```


## Usage:

To implement this script in your project, you can follow a similar approach as shown below:

```python
import asyncio

from steam_price_parser import SteamPriceParser

s = SteamPriceParser()


async def main():
    game_id = await s.check_game_app_id_by_name('Shadows of Doubt')
    prices = await s.check_game_price(game_id)
    print(prices)


if __name__ == '__main__':
    asyncio.run(main())
```


## How does it work?

By sending requests to several api.steam sites, the script receives the necessary information in json format.

**One warning:** Sometimes Steam servers send incomplete or truncated json file