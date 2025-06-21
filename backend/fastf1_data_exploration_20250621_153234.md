# FastF1 数据结构探索报告

生成时间: 2025-06-21 15:32:34
目标赛季: [2023, 2024, 2025]

## 探索结果

[2025-06-21 15:32:33] INFO: 🚀 开始 FastF1 数据探索...
[2025-06-21 15:32:33] INFO: 🎯 目标赛季: [2023, 2024, 2025]
[2025-06-21 15:32:33] INFO: 🔍 开始探索 FastF1 数据结构...
[2025-06-21 15:32:33] INFO: 🎯 目标赛季: [2023, 2024, 2025]
[2025-06-21 15:32:33] INFO: 📅 1. 探索赛季数据...
[2025-06-21 15:32:33] INFO: 
🎯 目标赛季数据:
[2025-06-21 15:32:33] INFO: 📏 数据形状: (0, 2)
[2025-06-21 15:32:33] INFO: 📝 列名: ['season', 'seasonUrl']
[2025-06-21 15:32:33] INFO: 📋 目标赛季: []
[2025-06-21 15:32:33] INFO: 
============================================================
[2025-06-21 15:32:33] INFO: 📊 目标赛季数据 (Target Seasons) 数据结构分析
[2025-06-21 15:32:33] INFO: ============================================================
[2025-06-21 15:32:33] INFO: 📋 数据类型: DataFrame
[2025-06-21 15:32:33] INFO: 📏 数据形状: (0, 2)
[2025-06-21 15:32:33] INFO: 📝 列名: ['season', 'seasonUrl']
[2025-06-21 15:32:33] INFO: 
📊 数据类型:
[2025-06-21 15:32:33] INFO:    season: int64
[2025-06-21 15:32:33] INFO:    seasonUrl: object
[2025-06-21 15:32:33] INFO:    数据为空
[2025-06-21 15:32:33] INFO: 🏁 2. 探索赛道数据...
[2025-06-21 15:32:33] INFO: 
============================================================
[2025-06-21 15:32:33] INFO: 📊 赛道数据 (Circuits - 2025) 数据结构分析
[2025-06-21 15:32:33] INFO: ============================================================
[2025-06-21 15:32:33] INFO: 📋 数据类型: DataFrame
[2025-06-21 15:32:33] INFO: 📏 数据形状: (24, 7)
[2025-06-21 15:32:33] INFO: 📝 列名: ['circuitId', 'circuitUrl', 'circuitName', 'lat', 'long', 'locality', 'country']
[2025-06-21 15:32:33] INFO: 
📊 数据类型:
[2025-06-21 15:32:33] INFO:    circuitId: object
[2025-06-21 15:32:33] INFO:    circuitUrl: object
[2025-06-21 15:32:33] INFO:    circuitName: object
[2025-06-21 15:32:33] INFO:    lat: float64
[2025-06-21 15:32:33] INFO:    long: float64
[2025-06-21 15:32:33] INFO:    locality: object
[2025-06-21 15:32:33] INFO:    country: object
[2025-06-21 15:32:33] INFO: 
📋 示例数据 (前3行):
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:      circuitId                                                   circuitUrl                     circuitName      lat      long   locality    country
0  albert_park            https://en.wikipedia.org/wiki/Albert_Park_Circuit  Albert Park Grand Prix Circuit -37.8497  144.9680  Melbourne  Australia
1     americas        https://en.wikipedia.org/wiki/Circuit_of_the_Americas         Circuit of the Americas  30.1328  -97.6411     Austin        USA
2      bahrain  https://en.wikipedia.org/wiki/Bahrain_International_Circuit   Bahrain International Circuit  26.0325   50.5106     Sakhir    Bahrain
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO: 
🔍 数据统计:
[2025-06-21 15:32:33] INFO:    非空值统计:
[2025-06-21 15:32:33] INFO:      circuitId: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      circuitUrl: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      circuitName: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      lat: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      long: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      locality: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      country: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO: 
🎯 唯一值统计:
[2025-06-21 15:32:33] INFO:      circuitId: 24 个唯一值
[2025-06-21 15:32:33] INFO:      circuitUrl: 24 个唯一值
[2025-06-21 15:32:33] INFO:      circuitName: 24 个唯一值
[2025-06-21 15:32:33] INFO:      lat: 24 个唯一值
[2025-06-21 15:32:33] INFO:      long: 24 个唯一值
[2025-06-21 15:32:33] INFO:      locality: 24 个唯一值
[2025-06-21 15:32:33] INFO:      country: 21 个唯一值
[2025-06-21 15:32:33] INFO: 
📈 数值列统计:
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:              lat        long
count  24.000000   24.000000
mean   30.249642   13.080856
std    22.621850   72.472233
min   -37.849700 -115.173000
25%    25.234300  -12.437630
50%    35.478900   10.498905
75%    45.528900   50.746500
max    52.388800  144.968000
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO: 🏎️ 3. 探索车队数据...
[2025-06-21 15:32:33] INFO: 
============================================================
[2025-06-21 15:32:33] INFO: 📊 车队数据 (Constructors - 2025) 数据结构分析
[2025-06-21 15:32:33] INFO: ============================================================
[2025-06-21 15:32:33] INFO: 📋 数据类型: DataFrame
[2025-06-21 15:32:33] INFO: 📏 数据形状: (10, 4)
[2025-06-21 15:32:33] INFO: 📝 列名: ['constructorId', 'constructorUrl', 'constructorName', 'constructorNationality']
[2025-06-21 15:32:33] INFO: 
📊 数据类型:
[2025-06-21 15:32:33] INFO:    constructorId: object
[2025-06-21 15:32:33] INFO:    constructorUrl: object
[2025-06-21 15:32:33] INFO:    constructorName: object
[2025-06-21 15:32:33] INFO:    constructorNationality: object
[2025-06-21 15:32:33] INFO: 
📋 示例数据 (前3行):
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:   constructorId                                            constructorUrl constructorName constructorNationality
0        alpine               http://en.wikipedia.org/wiki/Alpine_F1_Team  Alpine F1 Team                 French
1  aston_martin  http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One    Aston Martin                British
2       ferrari             http://en.wikipedia.org/wiki/Scuderia_Ferrari         Ferrari                Italian
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO: 
🔍 数据统计:
[2025-06-21 15:32:33] INFO:    非空值统计:
[2025-06-21 15:32:33] INFO:      constructorId: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      constructorUrl: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      constructorName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      constructorNationality: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO: 
🎯 唯一值统计:
[2025-06-21 15:32:33] INFO:      constructorId: 10 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['alpine', 'aston_martin', 'ferrari', 'haas', 'mclaren', 'mercedes', 'rb', 'red_bull', 'sauber', 'williams']
[2025-06-21 15:32:33] INFO:      constructorUrl: 10 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['http://en.wikipedia.org/wiki/Alpine_F1_Team', 'http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One', 'http://en.wikipedia.org/wiki/Scuderia_Ferrari', 'http://en.wikipedia.org/wiki/Haas_F1_Team', 'http://en.wikipedia.org/wiki/McLaren', 'http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One', 'http://en.wikipedia.org/wiki/RB_Formula_One_Team', 'http://en.wikipedia.org/wiki/Red_Bull_Racing', 'http://en.wikipedia.org/wiki/Sauber_Motorsport', 'http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering']
[2025-06-21 15:32:33] INFO:      constructorName: 10 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['Alpine F1 Team', 'Aston Martin', 'Ferrari', 'Haas F1 Team', 'McLaren', 'Mercedes', 'RB F1 Team', 'Red Bull', 'Sauber', 'Williams']
[2025-06-21 15:32:33] INFO:      constructorNationality: 7 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['French', 'British', 'Italian', 'American', 'German', 'Austrian', 'Swiss']
[2025-06-21 15:32:33] INFO: 👤 4. 探索车手数据...
[2025-06-21 15:32:33] INFO: 
============================================================
[2025-06-21 15:32:33] INFO: 📊 车手数据 (Drivers - 2025) 数据结构分析
[2025-06-21 15:32:33] INFO: ============================================================
[2025-06-21 15:32:33] INFO: 📋 数据类型: DataFrame
[2025-06-21 15:32:33] INFO: 📏 数据形状: (21, 8)
[2025-06-21 15:32:33] INFO: 📝 列名: ['driverId', 'driverNumber', 'driverCode', 'driverUrl', 'givenName', 'familyName', 'dateOfBirth', 'driverNationality']
[2025-06-21 15:32:33] INFO: 
📊 数据类型:
[2025-06-21 15:32:33] INFO:    driverId: object
[2025-06-21 15:32:33] INFO:    driverNumber: int64
[2025-06-21 15:32:33] INFO:    driverCode: object
[2025-06-21 15:32:33] INFO:    driverUrl: object
[2025-06-21 15:32:33] INFO:    givenName: object
[2025-06-21 15:32:33] INFO:    familyName: object
[2025-06-21 15:32:33] INFO:    dateOfBirth: datetime64[ns]
[2025-06-21 15:32:33] INFO:    driverNationality: object
[2025-06-21 15:32:33] INFO: 
📋 示例数据 (前3行):
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:     driverId  driverNumber driverCode                                            driverUrl    givenName familyName dateOfBirth driverNationality
0      albon            23        ALB         http://en.wikipedia.org/wiki/Alexander_Albon    Alexander      Albon  1996-03-23              Thai
1     alonso            14        ALO         http://en.wikipedia.org/wiki/Fernando_Alonso     Fernando     Alonso  1981-07-29           Spanish
2  antonelli            12        ANT  https://en.wikipedia.org/wiki/Andrea_Kimi_Antonelli  Andrea Kimi  Antonelli  2006-08-25           Italian
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO: 
🔍 数据统计:
[2025-06-21 15:32:33] INFO:    非空值统计:
[2025-06-21 15:32:33] INFO:      driverId: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      driverNumber: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      driverCode: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      driverUrl: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      givenName: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      familyName: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      dateOfBirth: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      driverNationality: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO: 
🎯 唯一值统计:
[2025-06-21 15:32:33] INFO:      driverId: 21 个唯一值
[2025-06-21 15:32:33] INFO:      driverNumber: 21 个唯一值
[2025-06-21 15:32:33] INFO:      driverCode: 21 个唯一值
[2025-06-21 15:32:33] INFO:      driverUrl: 21 个唯一值
[2025-06-21 15:32:33] INFO:      givenName: 21 个唯一值
[2025-06-21 15:32:33] INFO:      familyName: 21 个唯一值
[2025-06-21 15:32:33] INFO:      dateOfBirth: 21 个唯一值
[2025-06-21 15:32:33] INFO:      driverNationality: 14 个唯一值
[2025-06-21 15:32:33] INFO: 
📈 数值列统计:
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:        driverNumber
count     21.000000
mean      30.047619
std       24.276483
min        4.000000
25%       12.000000
50%       23.000000
75%       43.000000
max       87.000000
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO: 🏁 5. 探索比赛日程数据...
[2025-06-21 15:32:33] INFO: 
============================================================
[2025-06-21 15:32:33] INFO: 📊 比赛日程数据 (FastF1 - 2025) 数据结构分析
[2025-06-21 15:32:33] INFO: ============================================================
[2025-06-21 15:32:33] INFO: 📋 数据类型: DataFrame
[2025-06-21 15:32:33] INFO: 📏 数据形状: (25, 23)
[2025-06-21 15:32:33] INFO: 📝 列名: ['RoundNumber', 'Country', 'Location', 'OfficialEventName', 'EventDate', 'EventName', 'EventFormat', 'Session1', 'Session1Date', 'Session1DateUtc', 'Session2', 'Session2Date', 'Session2DateUtc', 'Session3', 'Session3Date', 'Session3DateUtc', 'Session4', 'Session4Date', 'Session4DateUtc', 'Session5', 'Session5Date', 'Session5DateUtc', 'F1ApiSupport']
[2025-06-21 15:32:33] INFO: 
📊 数据类型:
[2025-06-21 15:32:33] INFO:    RoundNumber: int64
[2025-06-21 15:32:33] INFO:    Country: object
[2025-06-21 15:32:33] INFO:    Location: object
[2025-06-21 15:32:33] INFO:    OfficialEventName: object
[2025-06-21 15:32:33] INFO:    EventDate: datetime64[ns]
[2025-06-21 15:32:33] INFO:    EventName: object
[2025-06-21 15:32:33] INFO:    EventFormat: object
[2025-06-21 15:32:33] INFO:    Session1: object
[2025-06-21 15:32:33] INFO:    Session1Date: object
[2025-06-21 15:32:33] INFO:    Session1DateUtc: datetime64[ns]
[2025-06-21 15:32:33] INFO:    Session2: object
[2025-06-21 15:32:33] INFO:    Session2Date: object
[2025-06-21 15:32:33] INFO:    Session2DateUtc: datetime64[ns]
[2025-06-21 15:32:33] INFO:    Session3: object
[2025-06-21 15:32:33] INFO:    Session3Date: object
[2025-06-21 15:32:33] INFO:    Session3DateUtc: datetime64[ns]
[2025-06-21 15:32:33] INFO:    Session4: object
[2025-06-21 15:32:33] INFO:    Session4Date: object
[2025-06-21 15:32:33] INFO:    Session4DateUtc: datetime64[ns]
[2025-06-21 15:32:33] INFO:    Session5: object
[2025-06-21 15:32:33] INFO:    Session5Date: object
[2025-06-21 15:32:33] INFO:    Session5DateUtc: datetime64[ns]
[2025-06-21 15:32:33] INFO:    F1ApiSupport: bool
[2025-06-21 15:32:33] INFO: 
📋 示例数据 (前3行):
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:    RoundNumber    Country   Location                                   OfficialEventName  EventDate              EventName        EventFormat    Session1               Session1Date     Session1DateUtc           Session2               Session2Date     Session2DateUtc    Session3               Session3Date     Session3DateUtc    Session4               Session4Date     Session4DateUtc Session5               Session5Date     Session5DateUtc  F1ApiSupport
0            0    Bahrain     Sakhir            FORMULA 1 ARAMCO PRE-SEASON TESTING 2025 2025-02-28     Pre-Season Testing            testing  Practice 1  2025-02-26 10:00:00+03:00 2025-02-26 07:00:00         Practice 2  2025-02-27 10:00:00+03:00 2025-02-27 07:00:00  Practice 3  2025-02-28 10:00:00+03:00 2025-02-28 07:00:00        None                        NaT                 NaT     None                        NaT                 NaT          True
1            1  Australia  Melbourne  FORMULA 1 LOUIS VUITTON AUSTRALIAN GRAND PRIX 2025 2025-03-16  Australian Grand Prix       conventional  Practice 1  2025-03-14 12:30:00+11:00 2025-03-14 01:30:00         Practice 2  2025-03-14 16:00:00+11:00 2025-03-14 05:00:00  Practice 3  2025-03-15 12:30:00+11:00 2025-03-15 01:30:00  Qualifying  2025-03-15 16:00:00+11:00 2025-03-15 05:00:00     Race  2025-03-16 15:00:00+11:00 2025-03-16 04:00:00          True
2            2      China   Shanghai          FORMULA 1 HEINEKEN CHINESE GRAND PRIX 2025 2025-03-23     Chinese Grand Prix  sprint_qualifying  Practice 1  2025-03-21 11:30:00+08:00 2025-03-21 03:30:00  Sprint Qualifying  2025-03-21 15:30:00+08:00 2025-03-21 07:30:00      Sprint  2025-03-22 11:00:00+08:00 2025-03-22 03:00:00  Qualifying  2025-03-22 15:00:00+08:00 2025-03-22 07:00:00     Race  2025-03-23 15:00:00+08:00 2025-03-23 07:00:00          True
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO: 
🔍 数据统计:
[2025-06-21 15:32:33] INFO:    非空值统计:
[2025-06-21 15:32:33] INFO:      RoundNumber: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Country: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Location: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      OfficialEventName: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      EventDate: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      EventName: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      EventFormat: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session1: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session1Date: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session1DateUtc: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session2: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session2Date: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session2DateUtc: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session3: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session3Date: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session3DateUtc: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session4: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session4Date: 24/25 (96.0%) 非空, 1 空值
[2025-06-21 15:32:33] INFO:      Session4DateUtc: 24/25 (96.0%) 非空, 1 空值
[2025-06-21 15:32:33] INFO:      Session5: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      Session5Date: 24/25 (96.0%) 非空, 1 空值
[2025-06-21 15:32:33] INFO:      Session5DateUtc: 24/25 (96.0%) 非空, 1 空值
[2025-06-21 15:32:33] INFO:      F1ApiSupport: 25/25 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO: 
🎯 唯一值统计:
[2025-06-21 15:32:33] INFO:      RoundNumber: 25 个唯一值
[2025-06-21 15:32:33] INFO:      Country: 21 个唯一值
[2025-06-21 15:32:33] INFO:      Location: 24 个唯一值
[2025-06-21 15:32:33] INFO:      OfficialEventName: 25 个唯一值
[2025-06-21 15:32:33] INFO:      EventDate: 25 个唯一值
[2025-06-21 15:32:33] INFO:      EventName: 25 个唯一值
[2025-06-21 15:32:33] INFO:      EventFormat: 3 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['testing', 'conventional', 'sprint_qualifying']
[2025-06-21 15:32:33] INFO:      Session1: 1 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['Practice 1']
[2025-06-21 15:32:33] INFO:      Session1Date: 25 个唯一值
[2025-06-21 15:32:33] INFO:      Session1DateUtc: 25 个唯一值
[2025-06-21 15:32:33] INFO:      Session2: 2 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['Practice 2', 'Sprint Qualifying']
[2025-06-21 15:32:33] INFO:      Session2Date: 25 个唯一值
[2025-06-21 15:32:33] INFO:      Session2DateUtc: 25 个唯一值
[2025-06-21 15:32:33] INFO:      Session3: 2 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['Practice 3', 'Sprint']
[2025-06-21 15:32:33] INFO:      Session3Date: 25 个唯一值
[2025-06-21 15:32:33] INFO:      Session3DateUtc: 25 个唯一值
[2025-06-21 15:32:33] INFO:      Session4: 2 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['None', 'Qualifying']
[2025-06-21 15:32:33] INFO:      Session4Date: 24 个唯一值
[2025-06-21 15:32:33] INFO:      Session4DateUtc: 24 个唯一值
[2025-06-21 15:32:33] INFO:      Session5: 2 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['None', 'Race']
[2025-06-21 15:32:33] INFO:      Session5Date: 24 个唯一值
[2025-06-21 15:32:33] INFO:      Session5DateUtc: 24 个唯一值
[2025-06-21 15:32:33] INFO:      F1ApiSupport: 1 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['True']
[2025-06-21 15:32:33] INFO: 
📈 数值列统计:
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:        RoundNumber
count    25.000000
mean     12.000000
std       7.359801
min       0.000000
25%       6.000000
50%      12.000000
75%      18.000000
max      24.000000
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO: 
============================================================
[2025-06-21 15:32:33] INFO: 📊 比赛日程数据 (Ergast - 2025) 数据结构分析
[2025-06-21 15:32:33] INFO: ============================================================
[2025-06-21 15:32:33] INFO: 📋 数据类型: DataFrame
[2025-06-21 15:32:33] INFO: 📏 数据形状: (24, 23)
[2025-06-21 15:32:33] INFO: 📝 列名: ['season', 'round', 'raceUrl', 'raceName', 'raceDate', 'raceTime', 'circuitId', 'circuitUrl', 'circuitName', 'lat', 'long', 'locality', 'country', 'fp1Date', 'fp1Time', 'fp2Date', 'fp2Time', 'fp3Date', 'fp3Time', 'qualifyingDate', 'qualifyingTime', 'sprintDate', 'sprintTime']
[2025-06-21 15:32:33] INFO: 
📊 数据类型:
[2025-06-21 15:32:33] INFO:    season: int64
[2025-06-21 15:32:33] INFO:    round: int64
[2025-06-21 15:32:33] INFO:    raceUrl: object
[2025-06-21 15:32:33] INFO:    raceName: object
[2025-06-21 15:32:33] INFO:    raceDate: datetime64[ns]
[2025-06-21 15:32:33] INFO:    raceTime: object
[2025-06-21 15:32:33] INFO:    circuitId: object
[2025-06-21 15:32:33] INFO:    circuitUrl: object
[2025-06-21 15:32:33] INFO:    circuitName: object
[2025-06-21 15:32:33] INFO:    lat: float64
[2025-06-21 15:32:33] INFO:    long: float64
[2025-06-21 15:32:33] INFO:    locality: object
[2025-06-21 15:32:33] INFO:    country: object
[2025-06-21 15:32:33] INFO:    fp1Date: datetime64[ns]
[2025-06-21 15:32:33] INFO:    fp1Time: object
[2025-06-21 15:32:33] INFO:    fp2Date: datetime64[ns]
[2025-06-21 15:32:33] INFO:    fp2Time: object
[2025-06-21 15:32:33] INFO:    fp3Date: datetime64[ns]
[2025-06-21 15:32:33] INFO:    fp3Time: object
[2025-06-21 15:32:33] INFO:    qualifyingDate: datetime64[ns]
[2025-06-21 15:32:33] INFO:    qualifyingTime: object
[2025-06-21 15:32:33] INFO:    sprintDate: datetime64[ns]
[2025-06-21 15:32:33] INFO:    sprintTime: object
[2025-06-21 15:32:33] INFO: 
📋 示例数据 (前3行):
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:    season  round                                                   raceUrl               raceName   raceDate        raceTime    circuitId                                                        circuitUrl                     circuitName      lat     long   locality    country    fp1Date         fp1Time    fp2Date         fp2Time    fp3Date         fp3Time qualifyingDate  qualifyingTime sprintDate      sprintTime
0    2025      1  https://en.wikipedia.org/wiki/2025_Australian_Grand_Prix  Australian Grand Prix 2025-03-16  04:00:00+00:00  albert_park                 https://en.wikipedia.org/wiki/Albert_Park_Circuit  Albert Park Grand Prix Circuit -37.8497  144.968  Melbourne  Australia 2025-03-14  01:30:00+00:00 2025-03-14  05:00:00+00:00 2025-03-15  01:30:00+00:00     2025-03-15  05:00:00+00:00        NaT             NaN
1    2025      2     https://en.wikipedia.org/wiki/2025_Chinese_Grand_Prix     Chinese Grand Prix 2025-03-23  07:00:00+00:00     shanghai      https://en.wikipedia.org/wiki/Shanghai_International_Circuit  Shanghai International Circuit  31.3389  121.220   Shanghai      China 2025-03-21  03:30:00+00:00        NaT             NaN        NaT             NaN     2025-03-22  07:00:00+00:00 2025-03-22  03:00:00+00:00
2    2025      3    https://en.wikipedia.org/wiki/2025_Japanese_Grand_Prix    Japanese Grand Prix 2025-04-06  05:00:00+00:00       suzuka  https://en.wikipedia.org/wiki/Suzuka_International_Racing_Course                  Suzuka Circuit  34.8431  136.541     Suzuka      Japan 2025-04-04  02:30:00+00:00 2025-04-04  06:00:00+00:00 2025-04-05  02:30:00+00:00     2025-04-05  06:00:00+00:00        NaT             NaN
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO: 
🔍 数据统计:
[2025-06-21 15:32:33] INFO:    非空值统计:
[2025-06-21 15:32:33] INFO:      season: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      round: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      raceUrl: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      raceName: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      raceDate: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      raceTime: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      circuitId: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      circuitUrl: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      circuitName: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      lat: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      long: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      locality: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      country: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      fp1Date: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      fp1Time: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      fp2Date: 18/24 (75.0%) 非空, 6 空值
[2025-06-21 15:32:33] INFO:      fp2Time: 18/24 (75.0%) 非空, 6 空值
[2025-06-21 15:32:33] INFO:      fp3Date: 18/24 (75.0%) 非空, 6 空值
[2025-06-21 15:32:33] INFO:      fp3Time: 18/24 (75.0%) 非空, 6 空值
[2025-06-21 15:32:33] INFO:      qualifyingDate: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      qualifyingTime: 24/24 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      sprintDate: 6/24 (25.0%) 非空, 18 空值
[2025-06-21 15:32:33] INFO:      sprintTime: 6/24 (25.0%) 非空, 18 空值
[2025-06-21 15:32:33] INFO: 
🎯 唯一值统计:
[2025-06-21 15:32:33] INFO:      season: 1 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['2025']
[2025-06-21 15:32:33] INFO:      round: 24 个唯一值
[2025-06-21 15:32:33] INFO:      raceUrl: 24 个唯一值
[2025-06-21 15:32:33] INFO:      raceName: 24 个唯一值
[2025-06-21 15:32:33] INFO:      raceDate: 24 个唯一值
[2025-06-21 15:32:33] INFO:      raceTime: 13 个唯一值
[2025-06-21 15:32:33] INFO:      circuitId: 24 个唯一值
[2025-06-21 15:32:33] INFO:      circuitUrl: 24 个唯一值
[2025-06-21 15:32:33] INFO:      circuitName: 24 个唯一值
[2025-06-21 15:32:33] INFO:      lat: 24 个唯一值
[2025-06-21 15:32:33] INFO:      long: 24 个唯一值
[2025-06-21 15:32:33] INFO:      locality: 24 个唯一值
[2025-06-21 15:32:33] INFO:      country: 21 个唯一值
[2025-06-21 15:32:33] INFO:      fp1Date: 24 个唯一值
[2025-06-21 15:32:33] INFO:      fp1Time: 13 个唯一值
[2025-06-21 15:32:33] INFO:      fp2Date: 18 个唯一值
[2025-06-21 15:32:33] INFO:      fp2Time: 10 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['05:00:00+00:00', '06:00:00+00:00', '15:00:00+00:00', '17:00:00+00:00', '21:00:00+00:00', '14:00:00+00:00', '12:00:00+00:00', '13:00:00+00:00', '22:00:00+00:00', '04:00:00+00:00']
[2025-06-21 15:32:33] INFO:      fp3Date: 18 个唯一值
[2025-06-21 15:32:33] INFO:      fp3Time: 10 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['01:30:00+00:00', '02:30:00+00:00', '12:30:00+00:00', '13:30:00+00:00', '10:30:00+00:00', '16:30:00+00:00', '09:30:00+00:00', '08:30:00+00:00', '17:30:00+00:00', '00:30:00+00:00']
[2025-06-21 15:32:33] INFO:      qualifyingDate: 24 个唯一值
[2025-06-21 15:32:33] INFO:      qualifyingTime: 12 个唯一值
[2025-06-21 15:32:33] INFO:      sprintDate: 6 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['2025-03-22 00:00:00', '2025-05-03 00:00:00', '2025-07-26 00:00:00', '2025-10-18 00:00:00', '2025-11-08 00:00:00', '2025-11-29 00:00:00']
[2025-06-21 15:32:33] INFO:      sprintTime: 5 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['03:00:00+00:00', '16:00:00+00:00', '10:00:00+00:00', '17:00:00+00:00', '14:00:00+00:00']
[2025-06-21 15:32:33] INFO: 
📈 数值列统计:
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:        season      round        lat        long
count    24.0  24.000000  24.000000   24.000000
mean   2025.0  12.500000  30.249642   13.080856
std       0.0   7.071068  22.621850   72.472233
min    2025.0   1.000000 -37.849700 -115.173000
25%    2025.0   6.750000  25.234300  -12.437630
50%    2025.0  12.500000  35.478900   10.498905
75%    2025.0  18.250000  45.528900   50.746500
max    2025.0  24.000000  52.388800  144.968000
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO: 🏆 6. 探索积分榜数据...
[2025-06-21 15:32:33] INFO: 
============================================================
[2025-06-21 15:32:33] INFO: 📊 车手积分榜数据 (Driver Standings - 2025) 数据结构分析
[2025-06-21 15:32:33] INFO: ============================================================
[2025-06-21 15:32:33] INFO: 📋 数据类型: ErgastMultiResponse
[2025-06-21 15:32:33] INFO: 📝 描述信息:    season  round
0    2025     10
[2025-06-21 15:32:33] INFO: 📏 内容数量: 1
[2025-06-21 15:32:33] INFO: 
📊 第 1 个数据集:
[2025-06-21 15:32:33] INFO:    数据类型: DataFrame
[2025-06-21 15:32:33] INFO:    数据形状: (21, 16)
[2025-06-21 15:32:33] INFO:    列名: ['position', 'positionText', 'points', 'wins', 'driverId', 'driverNumber', 'driverCode', 'driverUrl', 'givenName', 'familyName', 'dateOfBirth', 'driverNationality', 'constructorIds', 'constructorUrls', 'constructorNames', 'constructorNationalities']
[2025-06-21 15:32:33] INFO: 
   数据类型:
[2025-06-21 15:32:33] INFO:      position: int64
[2025-06-21 15:32:33] INFO:      positionText: object
[2025-06-21 15:32:33] INFO:      points: float64
[2025-06-21 15:32:33] INFO:      wins: int64
[2025-06-21 15:32:33] INFO:      driverId: object
[2025-06-21 15:32:33] INFO:      driverNumber: int64
[2025-06-21 15:32:33] INFO:      driverCode: object
[2025-06-21 15:32:33] INFO:      driverUrl: object
[2025-06-21 15:32:33] INFO:      givenName: object
[2025-06-21 15:32:33] INFO:      familyName: object
[2025-06-21 15:32:33] INFO:      dateOfBirth: datetime64[ns]
[2025-06-21 15:32:33] INFO:      driverNationality: object
[2025-06-21 15:32:33] INFO:      constructorIds: object
[2025-06-21 15:32:33] INFO:      constructorUrls: object
[2025-06-21 15:32:33] INFO:      constructorNames: object
[2025-06-21 15:32:33] INFO:      constructorNationalities: object
[2025-06-21 15:32:33] INFO: 
   示例数据 (前3行):
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:    position positionText  points  wins        driverId  driverNumber driverCode                                    driverUrl givenName  familyName dateOfBirth driverNationality constructorIds                                 constructorUrls constructorNames constructorNationalities
0         1            1   198.0     5         piastri            81        PIA   http://en.wikipedia.org/wiki/Oscar_Piastri     Oscar     Piastri  2001-04-06        Australian      [mclaren]          [http://en.wikipedia.org/wiki/McLaren]        [McLaren]                [British]
1         2            2   176.0     2          norris             4        NOR    http://en.wikipedia.org/wiki/Lando_Norris     Lando      Norris  1999-11-13           British      [mclaren]          [http://en.wikipedia.org/wiki/McLaren]        [McLaren]                [British]
2         3            3   155.0     2  max_verstappen            33        VER  http://en.wikipedia.org/wiki/Max_Verstappen       Max  Verstappen  1997-09-30             Dutch     [red_bull]  [http://en.wikipedia.org/wiki/Red_Bull_Racing]       [Red Bull]               [Austrian]
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO: 
   数据统计:
[2025-06-21 15:32:33] INFO:    非空值统计:
[2025-06-21 15:32:33] INFO:      position: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      positionText: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      points: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      wins: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      driverId: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      driverNumber: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      driverCode: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      driverUrl: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      givenName: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      familyName: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      dateOfBirth: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      driverNationality: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      constructorIds: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      constructorUrls: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      constructorNames: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO:      constructorNationalities: 21/21 (100.0%) 非空, 0 空值
[2025-06-21 15:32:33] INFO: 
   唯一值统计:
[2025-06-21 15:32:33] INFO:      position: 21 个唯一值
[2025-06-21 15:32:33] INFO:      positionText: 21 个唯一值
[2025-06-21 15:32:33] INFO:      points: 19 个唯一值
[2025-06-21 15:32:33] INFO:      wins: 4 个唯一值
[2025-06-21 15:32:33] INFO:        唯一值: ['5', '2', '1', '0']
[2025-06-21 15:32:33] INFO:      driverId: 21 个唯一值
[2025-06-21 15:32:33] INFO:      driverNumber: 21 个唯一值
[2025-06-21 15:32:33] INFO:      driverCode: 21 个唯一值
[2025-06-21 15:32:33] INFO:      driverUrl: 21 个唯一值
[2025-06-21 15:32:33] INFO:      givenName: 21 个唯一值
[2025-06-21 15:32:33] INFO:      familyName: 21 个唯一值
[2025-06-21 15:32:33] INFO:      dateOfBirth: 21 个唯一值
[2025-06-21 15:32:33] INFO:      driverNationality: 14 个唯一值
[2025-06-21 15:32:33] ERROR:      constructorIds: 唯一值统计失败 - unhashable type: 'list'
[2025-06-21 15:32:33] ERROR:      constructorUrls: 唯一值统计失败 - unhashable type: 'list'
[2025-06-21 15:32:33] ERROR:      constructorNames: 唯一值统计失败 - unhashable type: 'list'
[2025-06-21 15:32:33] ERROR:      constructorNationalities: 唯一值统计失败 - unhashable type: 'list'
[2025-06-21 15:32:33] INFO: 
   数值列统计:
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:33] INFO:         position      points       wins  driverNumber
count  21.000000   21.000000  21.000000     21.000000
mean   11.000000   51.523810   0.476190     30.047619
std     6.204837   63.941082   1.209093     24.276483
min     1.000000    0.000000   0.000000      4.000000
25%     6.000000    8.000000   0.000000     12.000000
50%    11.000000   20.000000   0.000000     23.000000
75%    16.000000   79.000000   0.000000     43.000000
max    21.000000  198.000000   5.000000     87.000000
[2025-06-21 15:32:33] INFO: ```
[2025-06-21 15:32:34] INFO: 
============================================================
[2025-06-21 15:32:34] INFO: 📊 车队积分榜数据 (Constructor Standings - 2025) 数据结构分析
[2025-06-21 15:32:34] INFO: ============================================================
[2025-06-21 15:32:34] INFO: 📋 数据类型: ErgastMultiResponse
[2025-06-21 15:32:34] INFO: 📝 描述信息:    season  round
0    2025     10
[2025-06-21 15:32:34] INFO: 📏 内容数量: 1
[2025-06-21 15:32:34] INFO: 
📊 第 1 个数据集:
[2025-06-21 15:32:34] INFO:    数据类型: DataFrame
[2025-06-21 15:32:34] INFO:    数据形状: (10, 8)
[2025-06-21 15:32:34] INFO:    列名: ['position', 'positionText', 'points', 'wins', 'constructorId', 'constructorUrl', 'constructorName', 'constructorNationality']
[2025-06-21 15:32:34] INFO: 
   数据类型:
[2025-06-21 15:32:34] INFO:      position: int64
[2025-06-21 15:32:34] INFO:      positionText: object
[2025-06-21 15:32:34] INFO:      points: float64
[2025-06-21 15:32:34] INFO:      wins: int64
[2025-06-21 15:32:34] INFO:      constructorId: object
[2025-06-21 15:32:34] INFO:      constructorUrl: object
[2025-06-21 15:32:34] INFO:      constructorName: object
[2025-06-21 15:32:34] INFO:      constructorNationality: object
[2025-06-21 15:32:34] INFO: 
   示例数据 (前3行):
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:    position positionText  points  wins constructorId                                             constructorUrl constructorName constructorNationality
0         1            1   374.0     7       mclaren                       http://en.wikipedia.org/wiki/McLaren         McLaren                British
1         2            2   199.0     1      mercedes  http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One        Mercedes                 German
2         3            3   183.0     0       ferrari              http://en.wikipedia.org/wiki/Scuderia_Ferrari         Ferrari                Italian
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 
   数据统计:
[2025-06-21 15:32:34] INFO:    非空值统计:
[2025-06-21 15:32:34] INFO:      position: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      positionText: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      points: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      wins: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorId: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorUrl: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorNationality: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO: 
   唯一值统计:
[2025-06-21 15:32:34] INFO:      position: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
[2025-06-21 15:32:34] INFO:      positionText: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
[2025-06-21 15:32:34] INFO:      points: 9 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['374.0', '199.0', '183.0', '162.0', '55.0', '28.0', '22.0', '20.0', '11.0']
[2025-06-21 15:32:34] INFO:      wins: 4 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['7', '1', '0', '2']
[2025-06-21 15:32:34] INFO:      constructorId: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['mclaren', 'mercedes', 'ferrari', 'red_bull', 'williams', 'haas', 'rb', 'aston_martin', 'sauber', 'alpine']
[2025-06-21 15:32:34] INFO:      constructorUrl: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['http://en.wikipedia.org/wiki/McLaren', 'http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One', 'http://en.wikipedia.org/wiki/Scuderia_Ferrari', 'http://en.wikipedia.org/wiki/Red_Bull_Racing', 'http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering', 'http://en.wikipedia.org/wiki/Haas_F1_Team', 'http://en.wikipedia.org/wiki/RB_Formula_One_Team', 'http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One', 'http://en.wikipedia.org/wiki/Sauber_Motorsport', 'http://en.wikipedia.org/wiki/Alpine_F1_Team']
[2025-06-21 15:32:34] INFO:      constructorName: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['McLaren', 'Mercedes', 'Ferrari', 'Red Bull', 'Williams', 'Haas F1 Team', 'RB F1 Team', 'Aston Martin', 'Sauber', 'Alpine F1 Team']
[2025-06-21 15:32:34] INFO:      constructorNationality: 7 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['British', 'German', 'Italian', 'Austrian', 'American', 'Swiss', 'French']
[2025-06-21 15:32:34] INFO: 
   数值列统计:
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:        position      points       wins
count  10.00000   10.000000  10.000000
mean    5.50000  108.200000   1.000000
std     3.02765  119.133725   2.211083
min     1.00000   11.000000   0.000000
25%     3.25000   23.500000   0.000000
50%     5.50000   41.500000   0.000000
75%     7.75000  177.750000   0.750000
max    10.00000  374.000000   7.000000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 🏁 7. 探索比赛结果数据...
[2025-06-21 15:32:34] INFO: 
============================================================
[2025-06-21 15:32:34] INFO: 📊 比赛结果数据 (Race Results - 2025) 数据结构分析
[2025-06-21 15:32:34] INFO: ============================================================
[2025-06-21 15:32:34] INFO: 📋 数据类型: ErgastMultiResponse
[2025-06-21 15:32:34] INFO: 📝 描述信息:    season  round                                            raceUrl  ...     long   locality    country
0    2025      1  https://en.wikipedia.org/wiki/2025_Australian_...  ...  144.968  Melbourne  Australia
1    2025      2  https://en.wikipedia.org/wiki/2025_Chinese_Gra...  ...  121.220   Shanghai      China

[2 rows x 13 columns]
[2025-06-21 15:32:34] INFO: 📏 内容数量: 2
[2025-06-21 15:32:34] INFO: 
📊 第 1 个数据集:
[2025-06-21 15:32:34] INFO:    数据类型: DataFrame
[2025-06-21 15:32:34] INFO:    数据形状: (20, 24)
[2025-06-21 15:32:34] INFO:    列名: ['number', 'position', 'positionText', 'points', 'grid', 'laps', 'status', 'driverId', 'driverNumber', 'driverCode', 'driverUrl', 'givenName', 'familyName', 'dateOfBirth', 'driverNationality', 'constructorId', 'constructorUrl', 'constructorName', 'constructorNationality', 'totalRaceTimeMillis', 'totalRaceTime', 'fastestLapRank', 'fastestLapNumber', 'fastestLapTime']
[2025-06-21 15:32:34] INFO: 
   数据类型:
[2025-06-21 15:32:34] INFO:      number: int64
[2025-06-21 15:32:34] INFO:      position: int64
[2025-06-21 15:32:34] INFO:      positionText: object
[2025-06-21 15:32:34] INFO:      points: float64
[2025-06-21 15:32:34] INFO:      grid: int64
[2025-06-21 15:32:34] INFO:      laps: int64
[2025-06-21 15:32:34] INFO:      status: object
[2025-06-21 15:32:34] INFO:      driverId: object
[2025-06-21 15:32:34] INFO:      driverNumber: int64
[2025-06-21 15:32:34] INFO:      driverCode: object
[2025-06-21 15:32:34] INFO:      driverUrl: object
[2025-06-21 15:32:34] INFO:      givenName: object
[2025-06-21 15:32:34] INFO:      familyName: object
[2025-06-21 15:32:34] INFO:      dateOfBirth: datetime64[ns]
[2025-06-21 15:32:34] INFO:      driverNationality: object
[2025-06-21 15:32:34] INFO:      constructorId: object
[2025-06-21 15:32:34] INFO:      constructorUrl: object
[2025-06-21 15:32:34] INFO:      constructorName: object
[2025-06-21 15:32:34] INFO:      constructorNationality: object
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: float64
[2025-06-21 15:32:34] INFO:      totalRaceTime: timedelta64[ns]
[2025-06-21 15:32:34] INFO:      fastestLapRank: float64
[2025-06-21 15:32:34] INFO:      fastestLapNumber: float64
[2025-06-21 15:32:34] INFO:      fastestLapTime: timedelta64[ns]
[2025-06-21 15:32:34] INFO: 
   示例数据 (前3行):
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:    number  position positionText  points  grid  laps    status        driverId  driverNumber driverCode                                                    driverUrl givenName  familyName dateOfBirth driverNationality constructorId                                             constructorUrl constructorName constructorNationality  totalRaceTimeMillis          totalRaceTime  fastestLapRank  fastestLapNumber         fastestLapTime
0       4         1            1    25.0     1    57  Finished          norris             4        NOR                    http://en.wikipedia.org/wiki/Lando_Norris     Lando      Norris  1999-11-13           British       mclaren                       http://en.wikipedia.org/wiki/McLaren         McLaren                British            6126304.0 0 days 01:42:06.304000             1.0              43.0 0 days 00:01:22.167000
1       1         2            2    18.0     3    57  Finished  max_verstappen            33        VER                  http://en.wikipedia.org/wiki/Max_Verstappen       Max  Verstappen  1997-09-30             Dutch      red_bull               http://en.wikipedia.org/wiki/Red_Bull_Racing        Red Bull               Austrian            6127199.0 0 days 00:00:00.895000             3.0              43.0 0 days 00:01:23.081000
2      63         3            3    15.0     4    57  Finished         russell            63        RUS  http://en.wikipedia.org/wiki/George_Russell_(racing_driver)    George     Russell  1998-02-15           British      mercedes  http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One        Mercedes                 German            6134785.0 0 days 00:00:08.481000            11.0              43.0 0 days 00:01:25.065000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 
   数据统计:
[2025-06-21 15:32:34] INFO:    非空值统计:
[2025-06-21 15:32:34] INFO:      number: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      position: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      positionText: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      points: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      grid: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      laps: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      status: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverId: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNumber: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverCode: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverUrl: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      givenName: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      familyName: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      dateOfBirth: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNationality: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorId: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorUrl: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorName: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorNationality: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: 14/20 (70.0%) 非空, 6 空值
[2025-06-21 15:32:34] INFO:      totalRaceTime: 14/20 (70.0%) 非空, 6 空值
[2025-06-21 15:32:34] INFO:      fastestLapRank: 17/20 (85.0%) 非空, 3 空值
[2025-06-21 15:32:34] INFO:      fastestLapNumber: 17/20 (85.0%) 非空, 3 空值
[2025-06-21 15:32:34] INFO:      fastestLapTime: 17/20 (85.0%) 非空, 3 空值
[2025-06-21 15:32:34] INFO: 
   唯一值统计:
[2025-06-21 15:32:34] INFO:      number: 20 个唯一值
[2025-06-21 15:32:34] INFO:      position: 20 个唯一值
[2025-06-21 15:32:34] INFO:      positionText: 15 个唯一值
[2025-06-21 15:32:34] INFO:      points: 11 个唯一值
[2025-06-21 15:32:34] INFO:      grid: 20 个唯一值
[2025-06-21 15:32:34] INFO:      laps: 5 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['57', '46', '45', '32', '0']
[2025-06-21 15:32:34] INFO:      status: 2 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Finished', 'Retired']
[2025-06-21 15:32:34] INFO:      driverId: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverNumber: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverCode: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverUrl: 20 个唯一值
[2025-06-21 15:32:34] INFO:      givenName: 20 个唯一值
[2025-06-21 15:32:34] INFO:      familyName: 20 个唯一值
[2025-06-21 15:32:34] INFO:      dateOfBirth: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverNationality: 13 个唯一值
[2025-06-21 15:32:34] INFO:      constructorId: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['mclaren', 'red_bull', 'mercedes', 'williams', 'aston_martin', 'sauber', 'ferrari', 'alpine', 'rb', 'haas']
[2025-06-21 15:32:34] INFO:      constructorUrl: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['http://en.wikipedia.org/wiki/McLaren', 'http://en.wikipedia.org/wiki/Red_Bull_Racing', 'http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One', 'http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering', 'http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One', 'http://en.wikipedia.org/wiki/Sauber_Motorsport', 'http://en.wikipedia.org/wiki/Scuderia_Ferrari', 'http://en.wikipedia.org/wiki/Alpine_F1_Team', 'http://en.wikipedia.org/wiki/RB_Formula_One_Team', 'http://en.wikipedia.org/wiki/Haas_F1_Team']
[2025-06-21 15:32:34] INFO:      constructorName: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['McLaren', 'Red Bull', 'Mercedes', 'Williams', 'Aston Martin', 'Sauber', 'Ferrari', 'Alpine F1 Team', 'RB F1 Team', 'Haas F1 Team']
[2025-06-21 15:32:34] INFO:      constructorNationality: 7 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['British', 'Austrian', 'German', 'Swiss', 'Italian', 'French', 'American']
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: 14 个唯一值
[2025-06-21 15:32:34] INFO:      totalRaceTime: 14 个唯一值
[2025-06-21 15:32:34] INFO:      fastestLapRank: 17 个唯一值
[2025-06-21 15:32:34] INFO:      fastestLapNumber: 3 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['43.0', '42.0', '32.0']
[2025-06-21 15:32:34] INFO:      fastestLapTime: 17 个唯一值
[2025-06-21 15:32:34] INFO: 
   数值列统计:
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:         number  position     points      grid       laps  driverNumber  totalRaceTimeMillis              totalRaceTime  fastestLapRank  fastestLapNumber             fastestLapTime
count  20.0000  20.00000  20.000000  20.00000  20.000000      20.00000         1.400000e+01                         14       17.000000         17.000000                         17
mean   27.8000  10.50000   5.050000  10.50000  46.050000      29.40000         6.144930e+06  0 days 00:07:36.219214285        9.000000         42.235294  0 days 00:01:24.875588235
std    25.4984   5.91608   7.359026   5.91608  20.823759      24.72033         1.164765e+04  0 days 00:27:11.995423414        5.049752          2.658228  0 days 00:00:01.688964958
min     1.0000   1.00000   0.000000   1.00000   0.000000       4.00000         6.126304e+06     0 days 00:00:00.895000        1.000000         32.000000     0 days 00:01:22.167000
25%     9.2500   5.75000   0.000000   5.75000  45.750000      11.50000         6.137098e+06     0 days 00:00:13.933000        5.000000         43.000000     0 days 00:01:24.192000
50%    20.0000  10.50000   0.500000  10.50000  57.000000      22.50000         6.145428e+06     0 days 00:00:20.137000        9.000000         43.000000     0 days 00:01:24.901000
75%    34.2500  15.25000   8.500000  15.25000  57.000000      35.75000         6.151799e+06     0 days 00:00:29.038500       13.000000         43.000000     0 days 00:01:25.271000
max    87.0000  20.00000  25.000000  20.00000  57.000000      87.00000         6.166655e+06     0 days 01:42:06.304000       17.000000         43.000000     0 days 00:01:28.819000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 
📊 第 2 个数据集:
[2025-06-21 15:32:34] INFO:    数据类型: DataFrame
[2025-06-21 15:32:34] INFO:    数据形状: (10, 24)
[2025-06-21 15:32:34] INFO:    列名: ['number', 'position', 'positionText', 'points', 'grid', 'laps', 'status', 'driverId', 'driverNumber', 'driverCode', 'driverUrl', 'givenName', 'familyName', 'dateOfBirth', 'driverNationality', 'constructorId', 'constructorUrl', 'constructorName', 'constructorNationality', 'totalRaceTimeMillis', 'totalRaceTime', 'fastestLapRank', 'fastestLapNumber', 'fastestLapTime']
[2025-06-21 15:32:34] INFO: 
   数据类型:
[2025-06-21 15:32:34] INFO:      number: int64
[2025-06-21 15:32:34] INFO:      position: int64
[2025-06-21 15:32:34] INFO:      positionText: object
[2025-06-21 15:32:34] INFO:      points: float64
[2025-06-21 15:32:34] INFO:      grid: int64
[2025-06-21 15:32:34] INFO:      laps: int64
[2025-06-21 15:32:34] INFO:      status: object
[2025-06-21 15:32:34] INFO:      driverId: object
[2025-06-21 15:32:34] INFO:      driverNumber: int64
[2025-06-21 15:32:34] INFO:      driverCode: object
[2025-06-21 15:32:34] INFO:      driverUrl: object
[2025-06-21 15:32:34] INFO:      givenName: object
[2025-06-21 15:32:34] INFO:      familyName: object
[2025-06-21 15:32:34] INFO:      dateOfBirth: datetime64[ns]
[2025-06-21 15:32:34] INFO:      driverNationality: object
[2025-06-21 15:32:34] INFO:      constructorId: object
[2025-06-21 15:32:34] INFO:      constructorUrl: object
[2025-06-21 15:32:34] INFO:      constructorName: object
[2025-06-21 15:32:34] INFO:      constructorNationality: object
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: int64
[2025-06-21 15:32:34] INFO:      totalRaceTime: timedelta64[ns]
[2025-06-21 15:32:34] INFO:      fastestLapRank: int64
[2025-06-21 15:32:34] INFO:      fastestLapNumber: int64
[2025-06-21 15:32:34] INFO:      fastestLapTime: timedelta64[ns]
[2025-06-21 15:32:34] INFO: 
   示例数据 (前3行):
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:    number  position positionText  points  grid  laps    status driverId  driverNumber driverCode                                                    driverUrl givenName familyName dateOfBirth driverNationality constructorId                                             constructorUrl constructorName constructorNationality  totalRaceTimeMillis          totalRaceTime  fastestLapRank  fastestLapNumber         fastestLapTime
0      81         1            1    25.0     1    56  Finished  piastri            81        PIA                   http://en.wikipedia.org/wiki/Oscar_Piastri     Oscar    Piastri  2001-04-06        Australian       mclaren                       http://en.wikipedia.org/wiki/McLaren         McLaren                British              5455026 0 days 01:30:55.026000               3                53 0 days 00:01:35.520000
1       4         2            2    18.0     3    56  Finished   norris             4        NOR                    http://en.wikipedia.org/wiki/Lando_Norris     Lando     Norris  1999-11-13           British       mclaren                       http://en.wikipedia.org/wiki/McLaren         McLaren                British              5464774 0 days 00:00:09.748000               1                53 0 days 00:01:35.454000
2      63         3            3    15.0     2    56  Finished  russell            63        RUS  http://en.wikipedia.org/wiki/George_Russell_(racing_driver)    George    Russell  1998-02-15           British      mercedes  http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One        Mercedes                 German              5466123 0 days 00:00:11.097000               5                55 0 days 00:01:35.816000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 
   数据统计:
[2025-06-21 15:32:34] INFO:    非空值统计:
[2025-06-21 15:32:34] INFO:      number: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      position: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      positionText: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      points: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      grid: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      laps: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      status: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverId: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNumber: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverCode: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverUrl: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      givenName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      familyName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      dateOfBirth: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNationality: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorId: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorUrl: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorNationality: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      totalRaceTime: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      fastestLapRank: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      fastestLapNumber: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      fastestLapTime: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO: 
   唯一值统计:
[2025-06-21 15:32:34] INFO:      number: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['81', '4', '63', '1', '31', '12', '23', '87', '18', '55']
[2025-06-21 15:32:34] INFO:      position: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
[2025-06-21 15:32:34] INFO:      positionText: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
[2025-06-21 15:32:34] INFO:      points: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['25.0', '18.0', '15.0', '12.0', '10.0', '8.0', '6.0', '4.0', '2.0', '1.0']
[2025-06-21 15:32:34] INFO:      grid: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['1', '3', '2', '4', '11', '8', '10', '17', '14', '15']
[2025-06-21 15:32:34] INFO:      laps: 1 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['56']
[2025-06-21 15:32:34] INFO:      status: 1 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Finished']
[2025-06-21 15:32:34] INFO:      driverId: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['piastri', 'norris', 'russell', 'max_verstappen', 'ocon', 'antonelli', 'albon', 'bearman', 'stroll', 'sainz']
[2025-06-21 15:32:34] INFO:      driverNumber: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['81', '4', '63', '33', '31', '12', '23', '87', '18', '55']
[2025-06-21 15:32:34] INFO:      driverCode: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['PIA', 'NOR', 'RUS', 'VER', 'OCO', 'ANT', 'ALB', 'BEA', 'STR', 'SAI']
[2025-06-21 15:32:34] INFO:      driverUrl: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['http://en.wikipedia.org/wiki/Oscar_Piastri', 'http://en.wikipedia.org/wiki/Lando_Norris', 'http://en.wikipedia.org/wiki/George_Russell_(racing_driver)', 'http://en.wikipedia.org/wiki/Max_Verstappen', 'http://en.wikipedia.org/wiki/Esteban_Ocon', 'https://en.wikipedia.org/wiki/Andrea_Kimi_Antonelli', 'http://en.wikipedia.org/wiki/Alexander_Albon', 'http://en.wikipedia.org/wiki/Oliver_Bearman', 'http://en.wikipedia.org/wiki/Lance_Stroll', 'http://en.wikipedia.org/wiki/Carlos_Sainz_Jr.']
[2025-06-21 15:32:34] INFO:      givenName: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Oscar', 'Lando', 'George', 'Max', 'Esteban', 'Andrea Kimi', 'Alexander', 'Oliver', 'Lance', 'Carlos']
[2025-06-21 15:32:34] INFO:      familyName: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Piastri', 'Norris', 'Russell', 'Verstappen', 'Ocon', 'Antonelli', 'Albon', 'Bearman', 'Stroll', 'Sainz']
[2025-06-21 15:32:34] INFO:      dateOfBirth: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['2001-04-06 00:00:00', '1999-11-13 00:00:00', '1998-02-15 00:00:00', '1997-09-30 00:00:00', '1996-09-17 00:00:00', '2006-08-25 00:00:00', '1996-03-23 00:00:00', '2005-05-08 00:00:00', '1998-10-29 00:00:00', '1994-09-01 00:00:00']
[2025-06-21 15:32:34] INFO:      driverNationality: 8 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Australian', 'British', 'Dutch', 'French', 'Italian', 'Thai', 'Canadian', 'Spanish']
[2025-06-21 15:32:34] INFO:      constructorId: 6 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['mclaren', 'mercedes', 'red_bull', 'haas', 'williams', 'aston_martin']
[2025-06-21 15:32:34] INFO:      constructorUrl: 6 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['http://en.wikipedia.org/wiki/McLaren', 'http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One', 'http://en.wikipedia.org/wiki/Red_Bull_Racing', 'http://en.wikipedia.org/wiki/Haas_F1_Team', 'http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering', 'http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One']
[2025-06-21 15:32:34] INFO:      constructorName: 6 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['McLaren', 'Mercedes', 'Red Bull', 'Haas F1 Team', 'Williams', 'Aston Martin']
[2025-06-21 15:32:34] INFO:      constructorNationality: 4 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['British', 'German', 'Austrian', 'American']
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['5455026', '5464774', '5466123', '5471682', '5504995', '5508774', '5511347', '5516329', '5525230', '5531413']
[2025-06-21 15:32:34] INFO:      totalRaceTime: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['0 days 01:30:55.026000', '0 days 00:00:09.748000', '0 days 00:00:11.097000', '0 days 00:00:16.656000', '0 days 00:00:49.969000', '0 days 00:00:53.748000', '0 days 00:00:56.321000', '0 days 00:01:01.303000', '0 days 00:01:10.204000', '0 days 00:01:16.387000']
[2025-06-21 15:32:34] INFO:      fastestLapRank: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['3', '1', '5', '2', '4', '11', '12', '13', '10', '15']
[2025-06-21 15:32:34] INFO:      fastestLapNumber: 6 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['53', '55', '56', '52', '39', '50']
[2025-06-21 15:32:34] INFO:      fastestLapTime: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['0 days 00:01:35.520000', '0 days 00:01:35.454000', '0 days 00:01:35.816000', '0 days 00:01:35.488000', '0 days 00:01:35.740000', '0 days 00:01:36.046000', '0 days 00:01:36.254000', '0 days 00:01:36.363000', '0 days 00:01:36.044000', '0 days 00:01:36.779000']
[2025-06-21 15:32:34] INFO: 
   数值列统计:
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:           number  position     points       grid  laps  driverNumber  totalRaceTimeMillis              totalRaceTime  fastestLapRank  fastestLapNumber             fastestLapTime
count  10.000000  10.00000  10.000000  10.000000  10.0     10.000000         1.000000e+01                         10       10.000000         10.000000                         10
mean   37.500000   5.50000  10.100000   8.500000  56.0     40.700000         5.495569e+06     0 days 00:09:46.045900        7.600000         52.200000     0 days 00:01:35.950400
std    31.686836   3.02765   7.593126   5.797509   0.0     29.101546         2.816111e+04  0 days 00:28:30.957682363        5.125102          5.072803  0 days 00:00:00.431366356
min     1.000000   1.00000   1.000000   1.000000  56.0      4.000000         5.455026e+06     0 days 00:00:09.748000        1.000000         39.000000     0 days 00:01:35.454000
25%    13.500000   3.25000   4.500000   3.250000  56.0     19.250000         5.467513e+06     0 days 00:00:24.984250        3.250000         52.000000     0 days 00:01:35.575000
50%    27.000000   5.50000   9.000000   9.000000  56.0     32.000000         5.506884e+06     0 days 00:00:55.034500        7.500000         53.000000     0 days 00:01:35.930000
75%    61.000000   7.75000  14.250000  13.250000  56.0     61.000000         5.515084e+06     0 days 00:01:07.978750       11.750000         55.750000     0 days 00:01:36.202000
max    87.000000  10.00000  25.000000  17.000000  56.0     87.000000         5.531413e+06     0 days 01:30:55.026000       15.000000         56.000000     0 days 00:01:36.779000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 🏁 8. 探索排位赛结果数据...
[2025-06-21 15:32:34] INFO: 
============================================================
[2025-06-21 15:32:34] INFO: 📊 排位赛结果数据 (Qualifying Results - 2025) 数据结构分析
[2025-06-21 15:32:34] INFO: ============================================================
[2025-06-21 15:32:34] INFO: 📋 数据类型: ErgastMultiResponse
[2025-06-21 15:32:34] INFO: 📝 描述信息:    season  round                                            raceUrl  ...     long   locality    country
0    2025      1  https://en.wikipedia.org/wiki/2025_Australian_...  ...  144.968  Melbourne  Australia
1    2025      2  https://en.wikipedia.org/wiki/2025_Chinese_Gra...  ...  121.220   Shanghai      China

[2 rows x 13 columns]
[2025-06-21 15:32:34] INFO: 📏 内容数量: 2
[2025-06-21 15:32:34] INFO: 
📊 第 1 个数据集:
[2025-06-21 15:32:34] INFO:    数据类型: DataFrame
[2025-06-21 15:32:34] INFO:    数据形状: (20, 17)
[2025-06-21 15:32:34] INFO:    列名: ['number', 'position', 'Q1', 'Q2', 'Q3', 'driverId', 'driverNumber', 'driverCode', 'driverUrl', 'givenName', 'familyName', 'dateOfBirth', 'driverNationality', 'constructorId', 'constructorUrl', 'constructorName', 'constructorNationality']
[2025-06-21 15:32:34] INFO: 
   数据类型:
[2025-06-21 15:32:34] INFO:      number: int64
[2025-06-21 15:32:34] INFO:      position: int64
[2025-06-21 15:32:34] INFO:      Q1: timedelta64[ns]
[2025-06-21 15:32:34] INFO:      Q2: timedelta64[ns]
[2025-06-21 15:32:34] INFO:      Q3: timedelta64[ns]
[2025-06-21 15:32:34] INFO:      driverId: object
[2025-06-21 15:32:34] INFO:      driverNumber: int64
[2025-06-21 15:32:34] INFO:      driverCode: object
[2025-06-21 15:32:34] INFO:      driverUrl: object
[2025-06-21 15:32:34] INFO:      givenName: object
[2025-06-21 15:32:34] INFO:      familyName: object
[2025-06-21 15:32:34] INFO:      dateOfBirth: datetime64[ns]
[2025-06-21 15:32:34] INFO:      driverNationality: object
[2025-06-21 15:32:34] INFO:      constructorId: object
[2025-06-21 15:32:34] INFO:      constructorUrl: object
[2025-06-21 15:32:34] INFO:      constructorName: object
[2025-06-21 15:32:34] INFO:      constructorNationality: object
[2025-06-21 15:32:34] INFO: 
   示例数据 (前3行):
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:    number  position                     Q1                     Q2                     Q3        driverId  driverNumber driverCode                                    driverUrl givenName  familyName dateOfBirth driverNationality constructorId                                constructorUrl constructorName constructorNationality
0       4         1 0 days 00:01:15.912000 0 days 00:01:15.415000 0 days 00:01:15.096000          norris             4        NOR    http://en.wikipedia.org/wiki/Lando_Norris     Lando      Norris  1999-11-13           British       mclaren          http://en.wikipedia.org/wiki/McLaren         McLaren                British
1      81         2 0 days 00:01:16.062000 0 days 00:01:15.468000 0 days 00:01:15.180000         piastri            81        PIA   http://en.wikipedia.org/wiki/Oscar_Piastri     Oscar     Piastri  2001-04-06        Australian       mclaren          http://en.wikipedia.org/wiki/McLaren         McLaren                British
2       1         3 0 days 00:01:16.018000 0 days 00:01:15.565000 0 days 00:01:15.481000  max_verstappen            33        VER  http://en.wikipedia.org/wiki/Max_Verstappen       Max  Verstappen  1997-09-30             Dutch      red_bull  http://en.wikipedia.org/wiki/Red_Bull_Racing        Red Bull               Austrian
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 
   数据统计:
[2025-06-21 15:32:34] INFO:    非空值统计:
[2025-06-21 15:32:34] INFO:      number: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      position: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      Q1: 19/20 (95.0%) 非空, 1 空值
[2025-06-21 15:32:34] INFO:      Q2: 15/20 (75.0%) 非空, 5 空值
[2025-06-21 15:32:34] INFO:      Q3: 10/20 (50.0%) 非空, 10 空值
[2025-06-21 15:32:34] INFO:      driverId: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNumber: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverCode: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverUrl: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      givenName: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      familyName: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      dateOfBirth: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNationality: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorId: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorUrl: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorName: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorNationality: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO: 
   唯一值统计:
[2025-06-21 15:32:34] INFO:      number: 20 个唯一值
[2025-06-21 15:32:34] INFO:      position: 20 个唯一值
[2025-06-21 15:32:34] INFO:      Q1: 19 个唯一值
[2025-06-21 15:32:34] INFO:      Q2: 15 个唯一值
[2025-06-21 15:32:34] INFO:      Q3: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['0 days 00:01:15.096000', '0 days 00:01:15.180000', '0 days 00:01:15.481000', '0 days 00:01:15.546000', '0 days 00:01:15.670000', '0 days 00:01:15.737000', '0 days 00:01:15.755000', '0 days 00:01:15.973000', '0 days 00:01:15.980000', '0 days 00:01:16.062000']
[2025-06-21 15:32:34] INFO:      driverId: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverNumber: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverCode: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverUrl: 20 个唯一值
[2025-06-21 15:32:34] INFO:      givenName: 20 个唯一值
[2025-06-21 15:32:34] INFO:      familyName: 20 个唯一值
[2025-06-21 15:32:34] INFO:      dateOfBirth: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverNationality: 13 个唯一值
[2025-06-21 15:32:34] INFO:      constructorId: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['mclaren', 'red_bull', 'mercedes', 'rb', 'williams', 'ferrari', 'alpine', 'aston_martin', 'sauber', 'haas']
[2025-06-21 15:32:34] INFO:      constructorUrl: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['http://en.wikipedia.org/wiki/McLaren', 'http://en.wikipedia.org/wiki/Red_Bull_Racing', 'http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One', 'http://en.wikipedia.org/wiki/RB_Formula_One_Team', 'http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering', 'http://en.wikipedia.org/wiki/Scuderia_Ferrari', 'http://en.wikipedia.org/wiki/Alpine_F1_Team', 'http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One', 'http://en.wikipedia.org/wiki/Sauber_Motorsport', 'http://en.wikipedia.org/wiki/Haas_F1_Team']
[2025-06-21 15:32:34] INFO:      constructorName: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['McLaren', 'Red Bull', 'Mercedes', 'RB F1 Team', 'Williams', 'Ferrari', 'Alpine F1 Team', 'Aston Martin', 'Sauber', 'Haas F1 Team']
[2025-06-21 15:32:34] INFO:      constructorNationality: 7 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['British', 'Austrian', 'German', 'Italian', 'French', 'Swiss', 'American']
[2025-06-21 15:32:34] INFO: 
   数值列统计:
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:         number  position                         Q1                         Q2                         Q3  driverNumber
count  20.0000  20.00000                         19                         15                         10      20.00000
mean   27.8000  10.50000  0 days 00:01:16.344736842  0 days 00:01:16.103666666     0 days 00:01:15.648000      29.40000
std    25.4984   5.91608  0 days 00:00:00.331828577  0 days 00:00:00.552431853  0 days 00:00:00.328146308      24.72033
min     1.0000   1.00000     0 days 00:01:15.912000     0 days 00:01:15.415000     0 days 00:01:15.096000       4.00000
25%     9.2500   5.75000     0 days 00:01:16.137500     0 days 00:01:15.812500     0 days 00:01:15.497250      11.50000
50%    20.0000  10.50000     0 days 00:01:16.315000     0 days 00:01:16.009000     0 days 00:01:15.703500      22.50000
75%    34.2500  15.25000     0 days 00:01:16.442500     0 days 00:01:16.314000     0 days 00:01:15.918500      35.75000
max    87.0000  20.00000     0 days 00:01:17.147000     0 days 00:01:17.520000     0 days 00:01:16.062000      87.00000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 
📊 第 2 个数据集:
[2025-06-21 15:32:34] INFO:    数据类型: DataFrame
[2025-06-21 15:32:34] INFO:    数据形状: (10, 17)
[2025-06-21 15:32:34] INFO:    列名: ['number', 'position', 'Q1', 'Q2', 'Q3', 'driverId', 'driverNumber', 'driverCode', 'driverUrl', 'givenName', 'familyName', 'dateOfBirth', 'driverNationality', 'constructorId', 'constructorUrl', 'constructorName', 'constructorNationality']
[2025-06-21 15:32:34] INFO: 
   数据类型:
[2025-06-21 15:32:34] INFO:      number: int64
[2025-06-21 15:32:34] INFO:      position: int64
[2025-06-21 15:32:34] INFO:      Q1: timedelta64[ns]
[2025-06-21 15:32:34] INFO:      Q2: timedelta64[ns]
[2025-06-21 15:32:34] INFO:      Q3: timedelta64[ns]
[2025-06-21 15:32:34] INFO:      driverId: object
[2025-06-21 15:32:34] INFO:      driverNumber: int64
[2025-06-21 15:32:34] INFO:      driverCode: object
[2025-06-21 15:32:34] INFO:      driverUrl: object
[2025-06-21 15:32:34] INFO:      givenName: object
[2025-06-21 15:32:34] INFO:      familyName: object
[2025-06-21 15:32:34] INFO:      dateOfBirth: datetime64[ns]
[2025-06-21 15:32:34] INFO:      driverNationality: object
[2025-06-21 15:32:34] INFO:      constructorId: object
[2025-06-21 15:32:34] INFO:      constructorUrl: object
[2025-06-21 15:32:34] INFO:      constructorName: object
[2025-06-21 15:32:34] INFO:      constructorNationality: object
[2025-06-21 15:32:34] INFO: 
   示例数据 (前3行):
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:    number  position                     Q1                     Q2                     Q3 driverId  driverNumber driverCode                                                    driverUrl givenName familyName dateOfBirth driverNationality constructorId                                             constructorUrl constructorName constructorNationality
0      81         1 0 days 00:01:31.591000 0 days 00:01:31.200000 0 days 00:01:30.641000  piastri            81        PIA                   http://en.wikipedia.org/wiki/Oscar_Piastri     Oscar    Piastri  2001-04-06        Australian       mclaren                       http://en.wikipedia.org/wiki/McLaren         McLaren                British
1      63         2 0 days 00:01:31.295000 0 days 00:01:31.307000 0 days 00:01:30.723000  russell            63        RUS  http://en.wikipedia.org/wiki/George_Russell_(racing_driver)    George    Russell  1998-02-15           British      mercedes  http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One        Mercedes                 German
2       4         3 0 days 00:01:30.983000 0 days 00:01:30.787000 0 days 00:01:30.793000   norris             4        NOR                    http://en.wikipedia.org/wiki/Lando_Norris     Lando     Norris  1999-11-13           British       mclaren                       http://en.wikipedia.org/wiki/McLaren         McLaren                British
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 
   数据统计:
[2025-06-21 15:32:34] INFO:    非空值统计:
[2025-06-21 15:32:34] INFO:      number: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      position: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      Q1: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      Q2: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      Q3: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverId: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNumber: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverCode: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverUrl: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      givenName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      familyName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      dateOfBirth: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNationality: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorId: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorUrl: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorNationality: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO: 
   唯一值统计:
[2025-06-21 15:32:34] INFO:      number: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['81', '63', '4', '1', '44', '16', '6', '12', '22', '23']
[2025-06-21 15:32:34] INFO:      position: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
[2025-06-21 15:32:34] INFO:      Q1: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['0 days 00:01:31.591000', '0 days 00:01:31.295000', '0 days 00:01:30.983000', '0 days 00:01:31.424000', '0 days 00:01:31.690000', '0 days 00:01:31.579000', '0 days 00:01:31.162000', '0 days 00:01:31.676000', '0 days 00:01:31.238000', '0 days 00:01:31.503000']
[2025-06-21 15:32:34] INFO:      Q2: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['0 days 00:01:31.200000', '0 days 00:01:31.307000', '0 days 00:01:30.787000', '0 days 00:01:31.142000', '0 days 00:01:31.501000', '0 days 00:01:31.450000', '0 days 00:01:31.253000', '0 days 00:01:31.590000', '0 days 00:01:31.260000', '0 days 00:01:31.595000']
[2025-06-21 15:32:34] INFO:      Q3: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['0 days 00:01:30.641000', '0 days 00:01:30.723000', '0 days 00:01:30.793000', '0 days 00:01:30.817000', '0 days 00:01:30.927000', '0 days 00:01:31.021000', '0 days 00:01:31.079000', '0 days 00:01:31.103000', '0 days 00:01:31.638000', '0 days 00:01:31.706000']
[2025-06-21 15:32:34] INFO:      driverId: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['piastri', 'russell', 'norris', 'max_verstappen', 'hamilton', 'leclerc', 'hadjar', 'antonelli', 'tsunoda', 'albon']
[2025-06-21 15:32:34] INFO:      driverNumber: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['81', '63', '4', '33', '44', '16', '6', '12', '22', '23']
[2025-06-21 15:32:34] INFO:      driverCode: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['PIA', 'RUS', 'NOR', 'VER', 'HAM', 'LEC', 'HAD', 'ANT', 'TSU', 'ALB']
[2025-06-21 15:32:34] INFO:      driverUrl: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['http://en.wikipedia.org/wiki/Oscar_Piastri', 'http://en.wikipedia.org/wiki/George_Russell_(racing_driver)', 'http://en.wikipedia.org/wiki/Lando_Norris', 'http://en.wikipedia.org/wiki/Max_Verstappen', 'http://en.wikipedia.org/wiki/Lewis_Hamilton', 'http://en.wikipedia.org/wiki/Charles_Leclerc', 'https://en.wikipedia.org/wiki/Isack_Hadjar', 'https://en.wikipedia.org/wiki/Andrea_Kimi_Antonelli', 'http://en.wikipedia.org/wiki/Yuki_Tsunoda', 'http://en.wikipedia.org/wiki/Alexander_Albon']
[2025-06-21 15:32:34] INFO:      givenName: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Oscar', 'George', 'Lando', 'Max', 'Lewis', 'Charles', 'Isack', 'Andrea Kimi', 'Yuki', 'Alexander']
[2025-06-21 15:32:34] INFO:      familyName: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Piastri', 'Russell', 'Norris', 'Verstappen', 'Hamilton', 'Leclerc', 'Hadjar', 'Antonelli', 'Tsunoda', 'Albon']
[2025-06-21 15:32:34] INFO:      dateOfBirth: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['2001-04-06 00:00:00', '1998-02-15 00:00:00', '1999-11-13 00:00:00', '1997-09-30 00:00:00', '1985-01-07 00:00:00', '1997-10-16 00:00:00', '2004-09-28 00:00:00', '2006-08-25 00:00:00', '2000-05-11 00:00:00', '1996-03-23 00:00:00']
[2025-06-21 15:32:34] INFO:      driverNationality: 8 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Australian', 'British', 'Dutch', 'Monegasque', 'French', 'Italian', 'Japanese', 'Thai']
[2025-06-21 15:32:34] INFO:      constructorId: 6 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['mclaren', 'mercedes', 'red_bull', 'ferrari', 'rb', 'williams']
[2025-06-21 15:32:34] INFO:      constructorUrl: 6 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['http://en.wikipedia.org/wiki/McLaren', 'http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One', 'http://en.wikipedia.org/wiki/Red_Bull_Racing', 'http://en.wikipedia.org/wiki/Scuderia_Ferrari', 'http://en.wikipedia.org/wiki/RB_Formula_One_Team', 'http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering']
[2025-06-21 15:32:34] INFO:      constructorName: 6 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['McLaren', 'Mercedes', 'Red Bull', 'Ferrari', 'RB F1 Team', 'Williams']
[2025-06-21 15:32:34] INFO:      constructorNationality: 4 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['British', 'German', 'Austrian', 'Italian']
[2025-06-21 15:32:34] INFO: 
   数值列统计:
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:           number  position                         Q1                         Q2                         Q3  driverNumber
count  10.000000  10.00000                         10                         10                         10     10.000000
mean   27.200000   5.50000     0 days 00:01:31.414100     0 days 00:01:31.308500     0 days 00:01:31.044800     30.400000
std    26.943562   3.02765  0 days 00:00:00.237064665  0 days 00:00:00.243879410  0 days 00:00:00.363620314     25.338596
min     1.000000   1.00000     0 days 00:01:30.983000     0 days 00:01:30.787000     0 days 00:01:30.641000      4.000000
25%     7.500000   3.25000     0 days 00:01:31.252250     0 days 00:01:31.213250     0 days 00:01:30.799000     13.000000
50%    19.000000   5.50000     0 days 00:01:31.463500     0 days 00:01:31.283500     0 days 00:01:30.974000     22.500000
75%    38.750000   7.75000     0 days 00:01:31.588000     0 days 00:01:31.488250     0 days 00:01:31.097000     41.250000
max    81.000000  10.00000     0 days 00:01:31.690000     0 days 00:01:31.595000     0 days 00:01:31.706000     81.000000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 🏁 9. 探索冲刺赛结果数据...
[2025-06-21 15:32:34] INFO: 
============================================================
[2025-06-21 15:32:34] INFO: 📊 冲刺赛结果数据 (Sprint Results - 2025) 数据结构分析
[2025-06-21 15:32:34] INFO: ============================================================
[2025-06-21 15:32:34] INFO: 📋 数据类型: ErgastMultiResponse
[2025-06-21 15:32:34] INFO: 📝 描述信息:    season  round                                            raceUrl  ...      long  locality country
0    2025      2  https://en.wikipedia.org/wiki/2025_Chinese_Gra...  ...  121.2200  Shanghai   China
1    2025      6  https://en.wikipedia.org/wiki/2025_Miami_Grand...  ...  -80.2389     Miami     USA

[2 rows x 13 columns]
[2025-06-21 15:32:34] INFO: 📏 内容数量: 2
[2025-06-21 15:32:34] INFO: 
📊 第 1 个数据集:
[2025-06-21 15:32:34] INFO:    数据类型: DataFrame
[2025-06-21 15:32:34] INFO:    数据形状: (20, 24)
[2025-06-21 15:32:34] INFO:    列名: ['number', 'position', 'positionText', 'points', 'grid', 'laps', 'status', 'driverId', 'driverNumber', 'driverCode', 'driverUrl', 'givenName', 'familyName', 'dateOfBirth', 'driverNationality', 'constructorId', 'constructorUrl', 'constructorName', 'constructorNationality', 'totalRaceTimeMillis', 'totalRaceTime', 'fastestLapRank', 'fastestLapNumber', 'fastestLapTime']
[2025-06-21 15:32:34] INFO: 
   数据类型:
[2025-06-21 15:32:34] INFO:      number: int64
[2025-06-21 15:32:34] INFO:      position: int64
[2025-06-21 15:32:34] INFO:      positionText: object
[2025-06-21 15:32:34] INFO:      points: float64
[2025-06-21 15:32:34] INFO:      grid: int64
[2025-06-21 15:32:34] INFO:      laps: int64
[2025-06-21 15:32:34] INFO:      status: object
[2025-06-21 15:32:34] INFO:      driverId: object
[2025-06-21 15:32:34] INFO:      driverNumber: int64
[2025-06-21 15:32:34] INFO:      driverCode: object
[2025-06-21 15:32:34] INFO:      driverUrl: object
[2025-06-21 15:32:34] INFO:      givenName: object
[2025-06-21 15:32:34] INFO:      familyName: object
[2025-06-21 15:32:34] INFO:      dateOfBirth: datetime64[ns]
[2025-06-21 15:32:34] INFO:      driverNationality: object
[2025-06-21 15:32:34] INFO:      constructorId: object
[2025-06-21 15:32:34] INFO:      constructorUrl: object
[2025-06-21 15:32:34] INFO:      constructorName: object
[2025-06-21 15:32:34] INFO:      constructorNationality: object
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: int64
[2025-06-21 15:32:34] INFO:      totalRaceTime: timedelta64[ns]
[2025-06-21 15:32:34] INFO:      fastestLapRank: int64
[2025-06-21 15:32:34] INFO:      fastestLapNumber: int64
[2025-06-21 15:32:34] INFO:      fastestLapTime: timedelta64[ns]
[2025-06-21 15:32:34] INFO: 
   示例数据 (前3行):
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:    number  position positionText  points  grid  laps    status        driverId  driverNumber driverCode                                    driverUrl givenName  familyName dateOfBirth driverNationality constructorId                                 constructorUrl constructorName constructorNationality  totalRaceTimeMillis          totalRaceTime  fastestLapRank  fastestLapNumber         fastestLapTime
0      44         1            1     8.0     1    19  Finished        hamilton            44        HAM  http://en.wikipedia.org/wiki/Lewis_Hamilton     Lewis    Hamilton  1985-01-07           British       ferrari  http://en.wikipedia.org/wiki/Scuderia_Ferrari         Ferrari                Italian              1839965 0 days 00:30:39.965000               1                 2 0 days 00:01:35.399000
1      81         2            2     7.0     3    19  Finished         piastri            81        PIA   http://en.wikipedia.org/wiki/Oscar_Piastri     Oscar     Piastri  2001-04-06        Australian       mclaren           http://en.wikipedia.org/wiki/McLaren         McLaren                British              1846854 0 days 00:00:06.889000               4                 7 0 days 00:01:35.854000
2       1         3            3     6.0     2    19  Finished  max_verstappen            33        VER  http://en.wikipedia.org/wiki/Max_Verstappen       Max  Verstappen  1997-09-30             Dutch      red_bull   http://en.wikipedia.org/wiki/Red_Bull_Racing        Red Bull               Austrian              1849769 0 days 00:00:09.804000               2                 2 0 days 00:01:35.745000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 
   数据统计:
[2025-06-21 15:32:34] INFO:    非空值统计:
[2025-06-21 15:32:34] INFO:      number: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      position: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      positionText: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      points: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      grid: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      laps: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      status: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverId: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNumber: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverCode: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverUrl: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      givenName: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      familyName: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      dateOfBirth: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNationality: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorId: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorUrl: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorName: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorNationality: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      totalRaceTime: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      fastestLapRank: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      fastestLapNumber: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      fastestLapTime: 20/20 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO: 
   唯一值统计:
[2025-06-21 15:32:34] INFO:      number: 20 个唯一值
[2025-06-21 15:32:34] INFO:      position: 20 个唯一值
[2025-06-21 15:32:34] INFO:      positionText: 20 个唯一值
[2025-06-21 15:32:34] INFO:      points: 9 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['8.0', '7.0', '6.0', '5.0', '4.0', '3.0', '2.0', '1.0', '0.0']
[2025-06-21 15:32:34] INFO:      grid: 20 个唯一值
[2025-06-21 15:32:34] INFO:      laps: 1 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['19']
[2025-06-21 15:32:34] INFO:      status: 1 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Finished']
[2025-06-21 15:32:34] INFO:      driverId: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverNumber: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverCode: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverUrl: 20 个唯一值
[2025-06-21 15:32:34] INFO:      givenName: 20 个唯一值
[2025-06-21 15:32:34] INFO:      familyName: 20 个唯一值
[2025-06-21 15:32:34] INFO:      dateOfBirth: 20 个唯一值
[2025-06-21 15:32:34] INFO:      driverNationality: 13 个唯一值
[2025-06-21 15:32:34] INFO:      constructorId: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['ferrari', 'mclaren', 'red_bull', 'mercedes', 'rb', 'aston_martin', 'williams', 'alpine', 'haas', 'sauber']
[2025-06-21 15:32:34] INFO:      constructorUrl: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['http://en.wikipedia.org/wiki/Scuderia_Ferrari', 'http://en.wikipedia.org/wiki/McLaren', 'http://en.wikipedia.org/wiki/Red_Bull_Racing', 'http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One', 'http://en.wikipedia.org/wiki/RB_Formula_One_Team', 'http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One', 'http://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering', 'http://en.wikipedia.org/wiki/Alpine_F1_Team', 'http://en.wikipedia.org/wiki/Haas_F1_Team', 'http://en.wikipedia.org/wiki/Sauber_Motorsport']
[2025-06-21 15:32:34] INFO:      constructorName: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Ferrari', 'McLaren', 'Red Bull', 'Mercedes', 'RB F1 Team', 'Aston Martin', 'Williams', 'Alpine F1 Team', 'Haas F1 Team', 'Sauber']
[2025-06-21 15:32:34] INFO:      constructorNationality: 7 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Italian', 'British', 'Austrian', 'German', 'French', 'American', 'Swiss']
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: 20 个唯一值
[2025-06-21 15:32:34] INFO:      totalRaceTime: 20 个唯一值
[2025-06-21 15:32:34] INFO:      fastestLapRank: 20 个唯一值
[2025-06-21 15:32:34] INFO:      fastestLapNumber: 7 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['2', '7', '4', '5', '8', '3', '13']
[2025-06-21 15:32:34] INFO:      fastestLapTime: 20 个唯一值
[2025-06-21 15:32:34] INFO: 
   数值列统计:
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:         number  position     points      grid  laps  driverNumber  totalRaceTimeMillis              totalRaceTime  fastestLapRank  fastestLapNumber             fastestLapTime
count  20.0000  20.00000  20.000000  20.00000  20.0      20.00000         2.000000e+01                         20        20.00000         20.000000                         20
mean   27.8000  10.50000   1.800000  10.50000  19.0      29.40000         1.873100e+06     0 days 00:02:05.132850        10.50000          4.500000     0 days 00:01:36.688950
std    25.4984   5.91608   2.706717   5.91608   0.0      24.72033         1.914840e+04  0 days 00:06:44.008285050         5.91608          2.564946  0 days 00:00:00.720896917
min     1.0000   1.00000   0.000000   1.00000  19.0       4.00000         1.839965e+06     0 days 00:00:06.889000         1.00000          2.000000     0 days 00:01:35.399000
25%     9.2500   5.75000   0.000000   5.75000  19.0      11.50000         1.859728e+06     0 days 00:00:22.850500         5.75000          3.000000     0 days 00:01:36.164000
50%    20.0000  10.50000   0.000000  10.50000  19.0      22.50000         1.878720e+06     0 days 00:00:39.470500        10.50000          4.000000     0 days 00:01:36.618500
75%    34.2500  15.25000   3.250000  15.25000  19.0      35.75000         1.885747e+06     0 days 00:00:47.480500        15.25000          4.250000     0 days 00:01:37.376750
max    87.0000  20.00000   8.000000  20.00000  19.0      87.00000         1.910177e+06     0 days 00:30:39.965000        20.00000         13.000000     0 days 00:01:37.686000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 
📊 第 2 个数据集:
[2025-06-21 15:32:34] INFO:    数据类型: DataFrame
[2025-06-21 15:32:34] INFO:    数据形状: (10, 24)
[2025-06-21 15:32:34] INFO:    列名: ['number', 'position', 'positionText', 'points', 'grid', 'laps', 'status', 'driverId', 'driverNumber', 'driverCode', 'driverUrl', 'givenName', 'familyName', 'dateOfBirth', 'driverNationality', 'constructorId', 'constructorUrl', 'constructorName', 'constructorNationality', 'totalRaceTimeMillis', 'totalRaceTime', 'fastestLapRank', 'fastestLapNumber', 'fastestLapTime']
[2025-06-21 15:32:34] INFO: 
   数据类型:
[2025-06-21 15:32:34] INFO:      number: int64
[2025-06-21 15:32:34] INFO:      position: int64
[2025-06-21 15:32:34] INFO:      positionText: object
[2025-06-21 15:32:34] INFO:      points: float64
[2025-06-21 15:32:34] INFO:      grid: int64
[2025-06-21 15:32:34] INFO:      laps: int64
[2025-06-21 15:32:34] INFO:      status: object
[2025-06-21 15:32:34] INFO:      driverId: object
[2025-06-21 15:32:34] INFO:      driverNumber: int64
[2025-06-21 15:32:34] INFO:      driverCode: object
[2025-06-21 15:32:34] INFO:      driverUrl: object
[2025-06-21 15:32:34] INFO:      givenName: object
[2025-06-21 15:32:34] INFO:      familyName: object
[2025-06-21 15:32:34] INFO:      dateOfBirth: datetime64[ns]
[2025-06-21 15:32:34] INFO:      driverNationality: object
[2025-06-21 15:32:34] INFO:      constructorId: object
[2025-06-21 15:32:34] INFO:      constructorUrl: object
[2025-06-21 15:32:34] INFO:      constructorName: object
[2025-06-21 15:32:34] INFO:      constructorNationality: object
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: int64
[2025-06-21 15:32:34] INFO:      totalRaceTime: timedelta64[ns]
[2025-06-21 15:32:34] INFO:      fastestLapRank: int64
[2025-06-21 15:32:34] INFO:      fastestLapNumber: int64
[2025-06-21 15:32:34] INFO:      fastestLapTime: timedelta64[ns]
[2025-06-21 15:32:34] INFO: 
   示例数据 (前3行):
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:    number  position positionText  points  grid  laps    status  driverId  driverNumber driverCode                                    driverUrl givenName familyName dateOfBirth driverNationality constructorId                                 constructorUrl constructorName constructorNationality  totalRaceTimeMillis          totalRaceTime  fastestLapRank  fastestLapNumber         fastestLapTime
0       4         1            1     8.0     3    18  Finished    norris             4        NOR    http://en.wikipedia.org/wiki/Lando_Norris     Lando     Norris  1999-11-13           British       mclaren           http://en.wikipedia.org/wiki/McLaren         McLaren                British              2197647 0 days 00:36:37.647000               5                 4 0 days 00:01:40.334000
1      81         2            2     7.0     2    18  Finished   piastri            81        PIA   http://en.wikipedia.org/wiki/Oscar_Piastri     Oscar    Piastri  2001-04-06        Australian       mclaren           http://en.wikipedia.org/wiki/McLaren         McLaren                British              2198319 0 days 00:00:00.672000               4                 7 0 days 00:01:40.238000
2      44         3            3     6.0     7    18  Finished  hamilton            44        HAM  http://en.wikipedia.org/wiki/Lewis_Hamilton     Lewis   Hamilton  1985-01-07           British       ferrari  http://en.wikipedia.org/wiki/Scuderia_Ferrari         Ferrari                Italian              2198720 0 days 00:00:01.073000               1                13 0 days 00:01:36.368000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: 
   数据统计:
[2025-06-21 15:32:34] INFO:    非空值统计:
[2025-06-21 15:32:34] INFO:      number: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      position: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      positionText: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      points: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      grid: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      laps: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      status: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverId: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNumber: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverCode: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverUrl: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      givenName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      familyName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      dateOfBirth: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      driverNationality: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorId: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorUrl: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorName: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      constructorNationality: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      totalRaceTime: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      fastestLapRank: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      fastestLapNumber: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO:      fastestLapTime: 10/10 (100.0%) 非空, 0 空值
[2025-06-21 15:32:34] INFO: 
   唯一值统计:
[2025-06-21 15:32:34] INFO:      number: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['4', '81', '44', '63', '18', '22', '12', '10', '27', '6']
[2025-06-21 15:32:34] INFO:      position: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
[2025-06-21 15:32:34] INFO:      positionText: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
[2025-06-21 15:32:34] INFO:      points: 9 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['8.0', '7.0', '6.0', '5.0', '4.0', '3.0', '2.0', '1.0', '0.0']
[2025-06-21 15:32:34] INFO:      grid: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['3', '2', '7', '5', '16', '20', '1', '13', '11', '9']
[2025-06-21 15:32:34] INFO:      laps: 1 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['18']
[2025-06-21 15:32:34] INFO:      status: 1 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Finished']
[2025-06-21 15:32:34] INFO:      driverId: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['norris', 'piastri', 'hamilton', 'russell', 'stroll', 'tsunoda', 'antonelli', 'gasly', 'hulkenberg', 'hadjar']
[2025-06-21 15:32:34] INFO:      driverNumber: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['4', '81', '44', '63', '18', '22', '12', '10', '27', '6']
[2025-06-21 15:32:34] INFO:      driverCode: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['NOR', 'PIA', 'HAM', 'RUS', 'STR', 'TSU', 'ANT', 'GAS', 'HUL', 'HAD']
[2025-06-21 15:32:34] INFO:      driverUrl: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['http://en.wikipedia.org/wiki/Lando_Norris', 'http://en.wikipedia.org/wiki/Oscar_Piastri', 'http://en.wikipedia.org/wiki/Lewis_Hamilton', 'http://en.wikipedia.org/wiki/George_Russell_(racing_driver)', 'http://en.wikipedia.org/wiki/Lance_Stroll', 'http://en.wikipedia.org/wiki/Yuki_Tsunoda', 'https://en.wikipedia.org/wiki/Andrea_Kimi_Antonelli', 'http://en.wikipedia.org/wiki/Pierre_Gasly', 'http://en.wikipedia.org/wiki/Nico_H%C3%BClkenberg', 'https://en.wikipedia.org/wiki/Isack_Hadjar']
[2025-06-21 15:32:34] INFO:      givenName: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Lando', 'Oscar', 'Lewis', 'George', 'Lance', 'Yuki', 'Andrea Kimi', 'Pierre', 'Nico', 'Isack']
[2025-06-21 15:32:34] INFO:      familyName: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['Norris', 'Piastri', 'Hamilton', 'Russell', 'Stroll', 'Tsunoda', 'Antonelli', 'Gasly', 'Hülkenberg', 'Hadjar']
[2025-06-21 15:32:34] INFO:      dateOfBirth: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['1999-11-13 00:00:00', '2001-04-06 00:00:00', '1985-01-07 00:00:00', '1998-02-15 00:00:00', '1998-10-29 00:00:00', '2000-05-11 00:00:00', '2006-08-25 00:00:00', '1996-02-07 00:00:00', '1987-08-19 00:00:00', '2004-09-28 00:00:00']
[2025-06-21 15:32:34] INFO:      driverNationality: 7 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['British', 'Australian', 'Canadian', 'Japanese', 'Italian', 'French', 'German']
[2025-06-21 15:32:34] INFO:      constructorId: 8 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['mclaren', 'ferrari', 'mercedes', 'aston_martin', 'red_bull', 'alpine', 'sauber', 'rb']
[2025-06-21 15:32:34] INFO:      constructorUrl: 8 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['http://en.wikipedia.org/wiki/McLaren', 'http://en.wikipedia.org/wiki/Scuderia_Ferrari', 'http://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One', 'http://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One', 'http://en.wikipedia.org/wiki/Red_Bull_Racing', 'http://en.wikipedia.org/wiki/Alpine_F1_Team', 'http://en.wikipedia.org/wiki/Sauber_Motorsport', 'http://en.wikipedia.org/wiki/RB_Formula_One_Team']
[2025-06-21 15:32:34] INFO:      constructorName: 8 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['McLaren', 'Ferrari', 'Mercedes', 'Aston Martin', 'Red Bull', 'Alpine F1 Team', 'Sauber', 'RB F1 Team']
[2025-06-21 15:32:34] INFO:      constructorNationality: 6 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['British', 'Italian', 'German', 'Austrian', 'French', 'Swiss']
[2025-06-21 15:32:34] INFO:      totalRaceTimeMillis: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['2197647', '2198319', '2198720', '2200774', '2201059', '2202800', '2203282', '2203620', '2203800', '2205149']
[2025-06-21 15:32:34] INFO:      totalRaceTime: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['0 days 00:36:37.647000', '0 days 00:00:00.672000', '0 days 00:00:01.073000', '0 days 00:00:03.127000', '0 days 00:00:03.412000', '0 days 00:00:05.153000', '0 days 00:00:05.635000', '0 days 00:00:05.973000', '0 days 00:00:06.153000', '0 days 00:00:07.502000']
[2025-06-21 15:32:34] INFO:      fastestLapRank: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['5', '4', '1', '7', '2', '3', '8', '16', '17', '13']
[2025-06-21 15:32:34] INFO:      fastestLapNumber: 5 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['4', '7', '13', '6', '5']
[2025-06-21 15:32:34] INFO:      fastestLapTime: 10 个唯一值
[2025-06-21 15:32:34] INFO:        唯一值: ['0 days 00:01:40.334000', '0 days 00:01:40.238000', '0 days 00:01:36.368000', '0 days 00:01:40.963000', '0 days 00:01:36.839000', '0 days 00:01:38.078000', '0 days 00:01:41.012000', '0 days 00:01:42.694000', '0 days 00:01:42.871000', '0 days 00:01:42.260000']
[2025-06-21 15:32:34] INFO: 
   数值列统计:
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO:           number  position     points       grid  laps  driverNumber  totalRaceTimeMillis              totalRaceTime  fastestLapRank  fastestLapNumber             fastestLapTime
count  10.000000  10.00000  10.000000  10.000000  10.0     10.000000         1.000000e+01                         10       10.000000         10.000000                         10
mean   28.700000   5.50000   3.600000   8.700000  18.0     28.700000         2.201517e+06     0 days 00:03:43.634700        7.600000          8.000000     0 days 00:01:40.165700
std    25.953163   3.02765   2.875181   6.307843   0.0     25.953163         2.611440e+03  0 days 00:11:33.600805116        5.815688          3.559026  0 days 00:00:02.341188067
min     4.000000   1.00000   0.000000   1.000000  18.0      4.000000         2.197647e+06     0 days 00:00:00.672000        1.000000          4.000000     0 days 00:01:36.368000
25%    10.500000   3.25000   1.250000   3.500000  18.0     10.500000         2.199234e+06     0 days 00:00:03.198250        3.250000          6.000000     0 days 00:01:38.618000
50%    20.000000   5.50000   3.500000   8.000000  18.0     20.000000         2.201930e+06     0 days 00:00:05.394000        6.000000          6.500000     0 days 00:01:40.648500
75%    39.750000   7.75000   5.750000  12.500000  18.0     39.750000         2.203536e+06     0 days 00:00:06.108000       11.750000         11.500000     0 days 00:01:41.948000
max    81.000000  10.00000   8.000000  20.000000  18.0     81.000000         2.205149e+06     0 days 00:36:37.647000       17.000000         13.000000     0 days 00:01:42.871000
[2025-06-21 15:32:34] INFO: ```
[2025-06-21 15:32:34] INFO: ✅ 数据探索完成
[2025-06-21 15:32:34] INFO: 
============================================================
[2025-06-21 15:32:34] INFO: 💡 数据建模建议
[2025-06-21 15:32:34] INFO: ============================================================
[2025-06-21 15:32:34] INFO: 
基于 FastF1 数据结构分析，建议采用以下建模策略：

## 1. 基础维度表 (独立实体)

### Season (赛季)
- 主键: year (INTEGER)
- 字段: name, description, start_date, end_date
- 特点: 独立存在，其他表的基础
- 范围: 2023-2025赛季

### Circuit (赛道)
- 主键: circuit_id (VARCHAR)
- 字段: name, location, country, length, corners
- 特点: 独立存在，可跨赛季使用

### Constructor (车队)
- 主键: constructor_id (VARCHAR)
- 字段: name, nationality, base, power_unit
- 特点: 独立存在，可跨赛季使用

## 2. 依赖维度表 (需要关联)

### Driver (车手)
- 主键: driver_id (VARCHAR)
- 外键: constructor_id, season_id
- 字段: first_name, last_name, nationality, number
- 特点: 依赖车队和赛季

### Race (比赛)
- 主键: race_id (VARCHAR)
- 外键: circuit_id, season_id
- 字段: name, round_number, race_date, status
- 特点: 依赖赛道和赛季

## 3. 事实表 (业务事件)

### Result (比赛结果)
- 主键: id (AUTO_INCREMENT)
- 外键: race_id, driver_id, constructor_id
- 字段: position, points, status, laps_completed
- 特点: 记录具体比赛结果

### QualifyingResult (排位赛结果)
- 主键: id (AUTO_INCREMENT)
- 外键: race_id, driver_id, constructor_id
- 字段: position, q1_time, q2_time, q3_time
- 特点: 记录排位赛结果

### SprintResult (冲刺赛结果)
- 主键: id (AUTO_INCREMENT)
- 外键: race_id, driver_id, constructor_id
- 字段: position, points, status, laps_completed
- 特点: 记录冲刺赛结果

### DriverStanding (车手积分榜)
- 主键: id (AUTO_INCREMENT)
- 外键: driver_id, constructor_id
- 字段: season, position, points, wins
- 特点: 记录积分榜状态

### ConstructorStanding (车队积分榜)
- 主键: id (AUTO_INCREMENT)
- 外键: constructor_id
- 字段: season, position, points, wins
- 特点: 记录车队积分榜状态

## 4. 同步顺序建议

1. Season (独立) - 2023, 2024, 2025
2. Circuit (独立)
3. Constructor (独立)
4. Driver (依赖 Constructor, Season)
5. Race (依赖 Circuit, Season)
6. Result (依赖 Driver, Constructor, Race)
7. QualifyingResult (依赖 Driver, Constructor, Race)
8. SprintResult (依赖 Driver, Constructor, Race)
9. Standings (依赖 Driver, Constructor)

## 5. 关键设计原则

- 使用自然键作为业务标识 (driver_id, constructor_id)
- 使用自增ID作为物理主键
- 建立适当的外键约束
- 考虑数据的历史性和时效性
- 优化查询性能的索引设计
- 处理 ErgastMultiResponse 的复杂数据结构
- 只同步目标赛季数据 (2023-2025)，避免历史数据冗余

## 6. 数据范围控制

- 赛季范围: 2023-2025
- 避免获取过多历史数据
- 提高同步效率和性能
- 减少存储空间占用

[2025-06-21 15:32:34] INFO: ✅ 数据探索和建议生成完成
