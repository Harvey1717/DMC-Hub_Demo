# DMC HUB

A management tool for "Bots" and "Monitors".

- Bots are pieces of automated checkout software for e-commerce sites.
- Monitors are pieces of software that check and notify for changes in a websites stock/HTML.

## Info

This repo has been created purely for demonstration purposes as it is currently my main side project that I have put effort into maintaining clean, documented code but some of it is private code that I have decided to remove. All site specific code has been removed therefore only the "Hub/Manger" code remains. The README may not be 100% correct and may contain some errors / outdated explainations.

> As of **16/11/2021** this project overall has recieved hundreds of commits and is on it's 3rd full version and is constantly being improved each week.

Throughout the README all the site names currently supported have been replaced with _redacted_site_.

# Table of Contents

- [DMC HUB](#dmc-hub)
  - [Info](#info)
- [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Setup](#setup)
    - [Important and Tips](#important-and-tips)
    - [Settings](#settings)
      - [Settings (settings.json)](#settings-settingsjson)
      - [Profiles (profiles.json)](#profiles-profilesjson)
      - [Proxies (proxies.txt)](#proxies-proxiestxt)
    - [Creating Task Files](#creating-task-files)
    - [Site Specific Setup](#site-specific-setup)
    - [Botting](#botting)
      - [Redacted Site 1](#redacted-site-1)
    - [Monitors](#monitors)
      - [Redacted Site 2](#redacted-site-2)
      - [Redacted Site 3](#redacted-site-3)
      - [Redacted Site 4](#redacted-site-4)
      - [Redacted Site 5](#redacted-site-5)
  - [Running The Bot](#running-the-bot)
  - [License](#license)

## Installation

**Install Required Packages Using PIP**

1. CD to directory of bot
2. Run

```
pip3 install -r requirements.txt
```

`requirements.txt` not available at the moment.

**Download Chromedriver**

1. Go to `chrome://version/` in Chrome
2. Download the correct chrome driver for your version of Chrome
3. Place it in the root of the bot folder

## Setup

### Important and Tips

**Override Default Webhook URL**

- Put a `webhookURL` field in a task file when using the advanced task layout under the `settings`.

**Skip Task Selection For a Specifc site**

- Name a task file `default.json` and it will automatically run when that site is selected.

### Settings

> The following settings are located in the `settings` folder

#### Settings (settings.json)

This file is where you can set the following settings:

- `monitorDelay` - An integer representing the time in ms to sleep in between requests while monitoring.
- `errorDelay` - An integer representing the time in ms to sleep in between requests after an error occurs.
- `catchall` - A string representing your catchall domain.
- `webhookURL` - A string representing your main Discord webhook URL.

Example:

```json
{
  "defaultSite": "",
  "monitorDelay": 3000,
  "errorDelay": 3000,
  "catchall": "my-catchall.com",
  "webhookURL": "https://disocrd.com/api..."
}
```

#### Profiles (profiles.json)

This file should contain all your profiles in the format below. Example:

```json
[
  {
    "name": "Revolut 1",
    "email": "dmc@hub.com",
    "phone": "07123456789",
    "shipping": {
      "firstName": "DMC",
      "lastName": "Hub",
      "address": "1 DMC Road",
      "address2": "",
      "city": "London",
      "zipcode": "",
      "country": "GB",
      "state": "?"
    },
    "billing": {
      "firstName": "DMC",
      "lastName": "Hub",
      "address": "1 DMC Road",
      "address2": "",
      "city": "London",
      "zipcode": "",
      "country": "GB",
      "state": "?"
    },
    "card": {
      "number": "1234123412341234",
      "expiryMonth": "01",
      "expiryYear": "2021",
      "cvv": "123"
    }
  }
]
```

#### Proxies (proxies.txt)

This file should contain your proxies with each proxy on a new line, they can be IP authentication proxies or user:pass. Example:

```
proxy.dmc.com:8901:dmcaio:93btoebawd3dwmas
proxy.dmc.com:8901:dmcaio:93btoebawd3dwmas
```

### Creating Task Files

All task files are JSON files, and they must be placed in the `settings/tasks/siteName` directory, for example `redacted_site` tasks would go in `settings/tasks/redacted_site`. You can name your task files whatever you like as long as they are JSON files and in the correct folder as the bot will ask you which file you want to run when you start the bot:

![Bot Choose Task File](https://imgur.com/0zOdnej.png)

As well as the normal task file layout you can also format the file to be JSON data with `settings` and `tasks` properties so that you can set settings that will be carried across to every task.

### Site Specific Setup

> The following site headings demonstrate and explain how to create a task for a specific site.

> Variables that have a `*` at the start are optional so they can be kept blank (`*variable`).

> Variables that have `-` at the start should be placed under a `settings` property meaning the advanced task format must be used (`-variable`).

### Botting

#### Redacted Site 1

- `eventPage` (string) - Event page URL on redacted_site site.
- `startDateToMatch` (string) - Start date of the event you want to purchase (American format), if no event is matched then the first event is used.
- `taskType` (string) - `RESERVE` OR `ACO` (Currently not working), default is ACO and RESERVE means browser will open on checkout page.

Bot will checkout last ticket on ticket page, if it fails to ATC it will do random.
Bot will chose cheapest delivery method.

Example task:

```json
[
  {
    "eventPage": "https://...",
    "startDateToMatch": "2021-10-18"
  }
]
```

### Monitors

#### Redacted Site 2

- `blockedStoreIDs` (list of strings) - Store IDs to not monitor for.
- `accessToken(userData)` (string) - redacted_site account access token.
- `refreshToken(userData)` (string) - redacted_site account refresh token.
- `refreshToken(userData)` (string) - redacted_site account refresh token.
- `userID(userData)` (string) - redacted_site account user ID.
- `longitude(userData)` (integer) - Longitude of where to check for items from.
- `latitude(userData)` (integer) - Latitude of where to check for items from.
- `range(userData)` (integer) - Range limit of items in stock.

Example task:

```json
[
  {
    "blockedStoreIDs": [],
    "userData": {
      "accessToken": "...",
      "refreshToken": "...",
      "userID": "1234",
      "longitude": 123,
      "latitude": 123,
      "range": 3 // Should be left at 3 to avoid errors
    }
  }
]
```

#### Redacted Site 3

- `eventName` (string) - This is the redacted_site event name in redacted_site.
- `*startDate` (string) - This is the start date of the event, it is only required if there are more than 1 events with the same name. The format is: `YYYY-MM-DD`.
- `notifyStockDecrease` (boolean) - This represents whether or not to send Discord webhooks when the stock decreases (the bot will always send notifications for stock increases).

Example task:

```json
[
  {
    "eventName": "...",
    "startDate": "2021-09-24",
    "notifyStockDecrease": true
  }
]
```

#### Redacted Site 4

- `eventType` (string) - Event type, only options are `redacted` or `redacted`.
- `monitorMode*` (string) - `NORMAL` or `SAFE`, default is NORMAL.

Example task:

```json
[
  {
    "eventName": "...",
    "startDate": "2021-09-24",
    "notifyStockDecrease": true
  }
]
```

#### Redacted Site 5

- `eventURL` (string) - This is a redacted.redacted event URL.
- `notifyStockDecrease` (boolean) - This represents whether or not to send Discord webhooks when the stock decreases (the bot will always send notifications for stock increases).

Example task:

```json
[
  {
    "eventURL": "https://...",
    "notifyStockDecrease": true
  }
]
```

## Running The Bot

Start the bot `./Run\ DMC-Hub.sh`

## License

Need to add license

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

---

Made with ❤ by [@dmc8787](https://twitter.com/dmc8787)
