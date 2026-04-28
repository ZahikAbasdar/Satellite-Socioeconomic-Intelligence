"""
Satellite-Driven Socioeconomic Intelligence
Pipeline — Satellite Feature Extraction + Comprehensive Global Geography
Covers India (40+ cities & rural zones), South Asia, Africa, Middle East,
Americas, Europe, East Asia, Oceania — 200+ city coordinate database
"""

import numpy as np
from PIL import Image
import io
import math
import logging
from typing import Union

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CITY DATABASE  (lat, lon, radius_deg, development_score 0–1)
# Score legend:
#   0.80–1.00  → High Development (Singapore, Tokyo, NYC, London …)
#   0.60–0.80  → Upper-Medium    (Bangalore, Seoul, Dubai, Shanghai …)
#   0.40–0.60  → Medium          (Mumbai, Jakarta, Cairo, São Paulo …)
#   0.20–0.40  → Low-Medium      (Dhaka, Lagos, Patna, rural zones …)
#   0.05–0.20  → Low             (Kinshasa, extreme rural …)
# ─────────────────────────────────────────────────────────────────────────────
CITY_DATABASE = [

    # ══════════════════════════════════════════════════════════════════════════
    # INDIA — TIER A: Major metros & IT hubs
    # ══════════════════════════════════════════════════════════════════════════
    (12.97,  77.59, 1.5, 0.73),   # Bangalore / Bengaluru (IT Silicon Valley)
    (17.38,  78.47, 1.5, 0.69),   # Hyderabad (HITEC City, pharma)
    (28.61,  77.21, 2.0, 0.67),   # New Delhi (national capital)
    (19.08,  72.88, 1.8, 0.66),   # Mumbai (financial capital)
    (13.08,  80.27, 1.5, 0.70),   # Chennai (auto, IT, port)
    (18.52,  73.86, 1.5, 0.70),   # Pune (auto, IT, education)
    (23.02,  72.57, 1.5, 0.70),   # Ahmedabad (GIFT City, industry)
    (22.57,  88.36, 1.5, 0.59),   # Kolkata (trade, culture)
    (21.17,  72.83, 1.2, 0.60),   # Surat (diamond, textile hub)
    (30.73,  76.78, 1.2, 0.70),   # Chandigarh (planned, high HDI)

    # ══════════════════════════════════════════════════════════════════════════
    # INDIA — TIER B: Secondary cities, good infrastructure
    # ══════════════════════════════════════════════════════════════════════════
    (26.91,  75.79, 1.2, 0.57),   # Jaipur (Pink City, tourism, IT)
    ( 9.93,  76.26, 1.2, 0.59),   # Kochi (port, IT, backwaters)
    (11.00,  76.96, 1.0, 0.58),   # Coimbatore (textile, engineering)
    (21.15,  79.09, 1.0, 0.55),   # Nagpur (geo-center, orange city)
    (15.34,  75.12, 1.0, 0.55),   # Hubli-Dharwad
    (12.30,  76.64, 1.0, 0.57),   # Mysore (heritage, IT)
    (16.31,  80.44, 1.0, 0.52),   # Vijayawada (Andhra capital area)
    (17.68,  83.22, 1.2, 0.54),   # Visakhapatnam (port, steel)
    (10.80,  78.69, 1.0, 0.50),   # Tiruchirappalli
    (22.32,  73.18, 1.0, 0.53),   # Vadodara (Baroda, industry)
    (20.45,  85.88, 1.2, 0.50),   # Bhubaneswar (Odisha capital)
    (29.87,  77.90, 1.0, 0.50),   # Saharanpur
    (28.98,  77.71, 1.0, 0.52),   # Meerut (sports goods)
    (31.10,  77.17, 0.8, 0.54),   # Shimla (HP capital, hill station)
    (32.08,  76.92, 0.8, 0.52),   # Dharamshala (HP, tourism)
    (30.37,  78.07, 0.8, 0.47),   # Dehradun (Uttarakhand capital)
    (26.18,  91.74, 1.2, 0.49),   # Guwahati (NE India gateway)
    (22.72,  75.86, 1.0, 0.50),   # Indore (MP's commercial hub)
    (23.26,  77.41, 1.2, 0.50),   # Bhopal (MP capital)
    (26.82,  75.79, 1.0, 0.48),   # Jodhpur (Blue City, tourism)
    (27.18,  78.01, 1.0, 0.48),   # Agra (Taj Mahal, tourism)
    (25.32,  83.00, 1.0, 0.46),   # Varanasi (holy city, silk)
    (26.85,  80.95, 1.2, 0.50),   # Lucknow (UP capital, IT growing)
    (28.36,  79.42, 1.0, 0.45),   # Bareilly (UP, industrial)
    (27.56,  80.67, 0.8, 0.43),   # Sitapur (UP semi-urban)
    (27.18,  81.30, 0.8, 0.42),   # Faizabad / Ayodhya (UP)
    (25.93,  81.68, 0.8, 0.43),   # Allahabad / Prayagraj
    (24.58,  73.71, 0.8, 0.48),   # Udaipur (lake city, tourism)
    (27.61,  74.54, 0.8, 0.45),   # Sikar (Rajasthan)
    ( 8.48,  76.95, 1.0, 0.57),   # Thiruvananthapuram (Kerala capital)
    (11.86,  75.37, 0.8, 0.56),   # Kozhikode / Calicut (Kerala)
    (10.52,  76.21, 0.8, 0.54),   # Thrissur (Kerala)

    # ══════════════════════════════════════════════════════════════════════════
    # INDIA — TIER C: Smaller cities & semi-urban
    # ══════════════════════════════════════════════════════════════════════════
    (25.59,  85.13, 1.2, 0.41),   # Patna (Bihar capital)
    (26.12,  91.62, 0.8, 0.40),   # Dispur / Guwahati outskirts
    (25.37,  86.47, 0.8, 0.36),   # Bhagalpur (Bihar)
    (24.79,  84.99, 0.8, 0.34),   # Gaya (Bihar, Buddhist circuit)
    (26.54,  84.00, 0.8, 0.33),   # Gopalganj (Bihar rural)
    (25.80,  87.07, 0.8, 0.34),   # Saharsa (Bihar)
    (25.74,  84.50, 0.8, 0.34),   # Saran / Chhapra (Bihar)
    (26.50,  84.84, 0.8, 0.33),   # Sitamarhi (Bihar-Nepal border)
    (27.55,  85.00, 0.8, 0.36),   # Raxaul (Bihar, Nepal entry)
    (23.17,  85.33, 1.0, 0.44),   # Ranchi (Jharkhand capital)
    (22.80,  86.18, 0.8, 0.42),   # Jamshedpur (steel city)
    (22.00,  82.00, 1.0, 0.40),   # Bilaspur (Chhattisgarh)
    (21.25,  81.63, 1.2, 0.42),   # Raipur (CG capital)
    (18.52,  75.01, 0.8, 0.46),   # Solapur (Maharashtra)
    (20.93,  77.76, 0.8, 0.46),   # Amravati (Maharashtra)
    (24.77,  92.79, 0.8, 0.38),   # Silchar (Assam)
    (27.10,  93.61, 0.6, 0.32),   # Dibrugarh (Assam, tea)
    (25.58,  91.88, 0.8, 0.38),   # Shillong (Meghalaya capital)
    (23.73,  92.72, 0.6, 0.34),   # Aizawl (Mizoram capital)
    (25.67,  94.11, 0.6, 0.30),   # Kohima (Nagaland capital)
    (24.82,  93.94, 0.6, 0.32),   # Imphal (Manipur capital)
    (27.33,  88.61, 0.6, 0.40),   # Gangtok (Sikkim capital)
    (11.67,  92.73, 0.6, 0.42),   # Port Blair (Andaman)

    # ══════════════════════════════════════════════════════════════════════════
    # INDIA — TIER D: Rural zones (various states)
    # ══════════════════════════════════════════════════════════════════════════
    (25.00,  85.50, 0.9, 0.28),   # Rural Bihar (central)
    (24.50,  86.00, 0.9, 0.27),   # Rural Bihar (east)
    (20.00,  84.00, 0.9, 0.30),   # Rural Odisha
    (18.00,  79.50, 0.9, 0.35),   # Rural Telangana (north)
    (15.50,  76.00, 0.9, 0.34),   # Rural Karnataka (north)
    (10.50,  77.50, 0.9, 0.38),   # Rural Tamil Nadu (hills)
    (10.00,  76.50, 0.9, 0.40),   # Rural Kerala (interior)
    (24.00,  73.00, 0.9, 0.28),   # Rural Rajasthan (west desert)
    (22.00,  80.50, 0.9, 0.34),   # Rural Madhya Pradesh
    (27.50,  80.00, 0.9, 0.32),   # Rural UP (east)
    (28.50,  79.50, 0.9, 0.35),   # Rural UP (west)
    (30.50,  75.50, 0.9, 0.46),   # Rural Punjab
    (29.50,  76.50, 0.9, 0.44),   # Rural Haryana
    (32.50,  76.50, 0.9, 0.40),   # Rural Himachal Pradesh
    (23.50,  92.50, 0.9, 0.28),   # Rural Mizoram / Assam hills
    (27.50,  94.50, 0.9, 0.26),   # Rural Arunachal Pradesh
    (26.50,  90.00, 0.9, 0.30),   # Rural Assam (west)
    (25.00,  92.00, 0.9, 0.29),   # Rural Assam/Meghalaya border
    (22.50,  70.00, 0.9, 0.38),   # Rural Saurashtra (Gujarat)
    (21.00,  73.50, 0.9, 0.36),   # Rural South Gujarat
    (17.00,  74.00, 0.9, 0.36),   # Rural Maharashtra (south)
    (16.00,  75.50, 0.9, 0.35),   # Rural Karnataka-Maharashtra border
    (19.50,  77.00, 0.9, 0.36),   # Rural Vidarbha (Maharashtra)
    (14.00,  76.00, 0.9, 0.38),   # Rural central Karnataka
    (12.00,  78.00, 0.9, 0.38),   # Rural Tamil Nadu (north)
    ( 9.00,  77.00, 0.9, 0.38),   # Rural Tamil Nadu (south)
    ( 8.50,  77.50, 0.9, 0.38),   # Rural Kerala-Tamil Nadu border
    (23.00,  86.50, 0.9, 0.36),   # Rural Jharkhand
    (21.00,  83.50, 0.9, 0.33),   # Rural Chhattisgarh/Odisha border
    (20.50,  80.00, 0.9, 0.28),   # Rural Bastar (Chhattisgarh)

    # ══════════════════════════════════════════════════════════════════════════
    # SOUTH ASIA (non-India)
    # ══════════════════════════════════════════════════════════════════════════
    (23.81,  90.41, 1.5, 0.38),   # Dhaka, Bangladesh
    (22.35,  91.83, 1.0, 0.36),   # Chittagong, Bangladesh
    (24.00,  90.00, 0.8, 0.28),   # Rural Bangladesh
    (24.86,  67.01, 1.5, 0.40),   # Karachi, Pakistan
    (31.55,  74.34, 1.5, 0.46),   # Lahore, Pakistan
    (33.69,  73.06, 1.5, 0.48),   # Islamabad, Pakistan
    (34.01,  71.58, 1.2, 0.38),   # Peshawar, Pakistan
    (30.19,  67.01, 1.0, 0.35),   # Quetta, Pakistan
    (27.70,  85.31, 1.5, 0.54),   # Kathmandu, Nepal
    (28.20,  83.98, 0.8, 0.30),   # Pokhara, Nepal
    (27.00,  84.00, 0.8, 0.24),   # Rural Terai, Nepal
    ( 6.93,  79.84, 1.2, 0.57),   # Colombo, Sri Lanka
    ( 7.29,  80.63, 0.8, 0.48),   # Kandy, Sri Lanka
    ( 4.17,  73.51, 0.8, 0.60),   # Malé, Maldives
    (27.47,  89.64, 0.8, 0.52),   # Thimphu, Bhutan
    (34.52,  69.17, 1.5, 0.40),   # Kabul, Afghanistan
    (31.61,  65.71, 1.0, 0.30),   # Kandahar, Afghanistan

    # ══════════════════════════════════════════════════════════════════════════
    # MIDDLE EAST & NORTH AFRICA
    # ══════════════════════════════════════════════════════════════════════════
    (25.20,  55.27, 1.8, 0.90),   # Dubai, UAE
    (24.45,  54.37, 1.5, 0.87),   # Abu Dhabi, UAE
    (25.30,  51.53, 1.5, 0.85),   # Doha, Qatar
    (26.22,  50.58, 1.5, 0.83),   # Manama, Bahrain
    (29.37,  47.97, 1.5, 0.79),   # Kuwait City
    (24.69,  46.72, 2.0, 0.72),   # Riyadh, Saudi Arabia
    (21.49,  39.19, 1.5, 0.70),   # Jeddah, Saudi Arabia
    (23.61,  58.59, 1.2, 0.68),   # Muscat, Oman
    (15.35,  44.21, 1.2, 0.34),   # Sana'a, Yemen
    (35.69,  51.39, 1.8, 0.59),   # Tehran, Iran
    (36.29,  59.61, 1.2, 0.50),   # Mashhad, Iran
    (32.66,  51.68, 1.2, 0.54),   # Isfahan, Iran
    (33.34,  44.40, 1.8, 0.55),   # Baghdad, Iraq
    (36.20,  37.16, 1.2, 0.45),   # Aleppo, Syria
    (33.51,  36.29, 1.5, 0.52),   # Damascus, Syria
    (33.89,  35.50, 1.5, 0.68),   # Beirut, Lebanon
    (31.95,  35.93, 1.5, 0.66),   # Amman, Jordan
    (31.77,  35.23, 1.5, 0.70),   # Jerusalem / Tel Aviv area
    (32.09,  34.78, 1.5, 0.85),   # Tel Aviv, Israel
    (30.04,  31.24, 2.0, 0.56),   # Cairo, Egypt
    (31.20,  29.92, 1.2, 0.54),   # Alexandria, Egypt
    (33.99,  -6.85, 1.5, 0.59),   # Rabat, Morocco
    (33.59,  -7.62, 1.5, 0.57),   # Casablanca, Morocco
    (31.63,  -8.00, 1.2, 0.55),   # Marrakech, Morocco
    (36.81,  10.18, 1.5, 0.59),   # Tunis, Tunisia
    (36.74,   3.06, 1.5, 0.55),   # Algiers, Algeria
    (32.90,  13.18, 1.2, 0.48),   # Tripoli, Libya

    # ══════════════════════════════════════════════════════════════════════════
    # EAST & SOUTHEAST ASIA
    # ══════════════════════════════════════════════════════════════════════════
    (35.68, 139.69, 2.0, 0.93),   # Tokyo, Japan
    (34.69, 135.50, 1.5, 0.91),   # Osaka, Japan
    (35.18, 136.90, 1.2, 0.90),   # Nagoya, Japan
    (37.57, 126.98, 2.0, 0.91),   # Seoul, South Korea
    (35.10, 128.99, 1.2, 0.86),   # Busan, South Korea
    (31.23, 121.47, 2.0, 0.84),   # Shanghai, China
    (39.91, 116.39, 2.0, 0.82),   # Beijing, China
    (22.54, 114.06, 1.5, 0.88),   # Shenzhen, China
    (23.11, 113.25, 1.5, 0.83),   # Guangzhou, China
    (30.57, 114.27, 1.5, 0.76),   # Wuhan, China
    (28.20, 112.97, 1.2, 0.72),   # Changsha, China
    (30.27, 120.15, 1.5, 0.80),   # Hangzhou, China
    (32.06, 118.79, 1.5, 0.79),   # Nanjing, China
    (36.06, 103.83, 1.2, 0.62),   # Lanzhou, China
    (22.28, 114.18, 1.2, 0.92),   # Hong Kong
    (25.04, 121.56, 1.5, 0.89),   # Taipei, Taiwan
     (1.35, 103.82, 1.2, 0.96),   # Singapore
     (3.14, 101.69, 1.5, 0.79),   # Kuala Lumpur, Malaysia
     (5.41, 100.33, 1.0, 0.72),   # Penang, Malaysia
    (14.58, 120.98, 1.5, 0.61),   # Manila, Philippines
    (10.32, 123.89, 1.0, 0.56),   # Cebu, Philippines
    (10.82, 106.63, 1.5, 0.63),   # Ho Chi Minh City, Vietnam
    (21.03, 105.85, 1.5, 0.59),   # Hanoi, Vietnam
    (16.05, 108.20, 1.0, 0.56),   # Da Nang, Vietnam
    (13.75, 100.52, 1.5, 0.73),   # Bangkok, Thailand
    (18.79, 98.99, 1.0, 0.62),    # Chiang Mai, Thailand
    (16.87, 96.20, 1.5, 0.55),    # Yangon, Myanmar
    (11.56, 104.93, 1.5, 0.52),   # Phnom Penh, Cambodia
    (17.96, 102.61, 1.2, 0.50),   # Vientiane, Laos
     (-6.21, 106.84, 1.8, 0.58), # Jakarta, Indonesia
    (-7.25, 112.75, 1.2, 0.54),   # Surabaya, Indonesia
    (-8.65, 115.22, 1.0, 0.58),   # Bali, Indonesia (tourism)
    (-0.89, 119.84, 0.8, 0.42),   # Palu, Indonesia
    (47.90, 106.90, 1.5, 0.56),   # Ulaanbaatar, Mongolia
    (27.47,  89.64, 0.8, 0.53),   # Thimphu, Bhutan

    # ══════════════════════════════════════════════════════════════════════════
    # EUROPE
    # ══════════════════════════════════════════════════════════════════════════
    (51.51,  -0.13, 2.0, 0.93),   # London, UK
    (53.48,  -2.24, 1.5, 0.87),   # Manchester, UK
    (55.86,  -4.25, 1.5, 0.87),   # Glasgow, UK
    (48.86,   2.35, 2.0, 0.92),   # Paris, France
    (45.75,   4.84, 1.5, 0.87),   # Lyon, France
    (43.30,   5.37, 1.5, 0.85),   # Marseille, France
    (52.52,  13.40, 1.8, 0.92),   # Berlin, Germany
    (48.13,  11.58, 1.5, 0.92),   # Munich, Germany
    (53.55,   9.99, 1.5, 0.91),   # Hamburg, Germany
    (51.23,   6.78, 1.5, 0.90),   # Düsseldorf, Germany
    (50.93,   6.96, 1.5, 0.90),   # Cologne, Germany
    (41.00,  28.97, 1.8, 0.72),   # Istanbul, Turkey
    (39.93,  32.87, 1.5, 0.67),   # Ankara, Turkey
    (38.42,  27.13, 1.2, 0.67),   # Izmir, Turkey
    (55.75,  37.62, 2.0, 0.72),   # Moscow, Russia
    (59.93,  30.32, 1.8, 0.68),   # St. Petersburg, Russia
    (56.84,  60.60, 1.5, 0.60),   # Yekaterinburg, Russia
    (43.05,  44.69, 1.2, 0.45),   # Vladikavkaz, Russia
    (40.41,  -3.70, 1.8, 0.85),   # Madrid, Spain
    (41.39,   2.15, 1.5, 0.84),   # Barcelona, Spain
    (37.38,  -5.97, 1.2, 0.80),   # Seville, Spain
    (41.90,  12.49, 1.8, 0.83),   # Rome, Italy
    (45.47,   9.19, 1.5, 0.86),   # Milan, Italy
    (40.64,  15.80, 1.2, 0.72),   # Naples, Italy
    (52.38,   4.90, 1.5, 0.91),   # Amsterdam, Netherlands
    (51.92,   4.48, 1.2, 0.90),   # Rotterdam, Netherlands
    (50.85,   4.35, 1.5, 0.89),   # Brussels, Belgium
    (47.38,   8.54, 1.5, 0.94),   # Zurich, Switzerland
    (46.52,   6.63, 1.2, 0.93),   # Lausanne, Switzerland
    (48.21,  16.37, 1.5, 0.89),   # Vienna, Austria
    (60.17,  24.93, 1.5, 0.93),   # Helsinki, Finland
    (59.33,  18.06, 1.5, 0.93),   # Stockholm, Sweden
    (57.71,  11.97, 1.2, 0.91),   # Gothenburg, Sweden
    (55.68,  12.57, 1.5, 0.92),   # Copenhagen, Denmark
    (59.91,  10.75, 1.5, 0.92),   # Oslo, Norway
    (60.39,   5.32, 1.2, 0.91),   # Bergen, Norway
    (64.14, -21.92, 1.0, 0.90),   # Reykjavik, Iceland
    (53.34,  -6.27, 1.5, 0.88),   # Dublin, Ireland
    (38.72,  -9.14, 1.5, 0.80),   # Lisbon, Portugal
    (41.15,  -8.61, 1.2, 0.78),   # Porto, Portugal
    (50.07,  14.44, 1.5, 0.86),   # Prague, Czech Republic
    (47.50,  19.04, 1.5, 0.82),   # Budapest, Hungary
    (52.23,  21.01, 1.5, 0.83),   # Warsaw, Poland
    (50.06,  19.94, 1.2, 0.81),   # Krakow, Poland
    (44.81,  20.46, 1.2, 0.73),   # Belgrade, Serbia
    (45.81,  15.98, 1.2, 0.76),   # Zagreb, Croatia
    (43.84,  18.36, 1.2, 0.68),   # Sarajevo, Bosnia
    (42.00,  21.43, 1.2, 0.66),   # Skopje, N. Macedonia
    (41.33,  19.83, 1.2, 0.62),   # Tirana, Albania
    (42.70,  23.32, 1.2, 0.72),   # Sofia, Bulgaria
    (44.44,  26.10, 1.5, 0.70),   # Bucharest, Romania
    (46.77,  23.58, 1.0, 0.67),   # Cluj-Napoca, Romania
    (50.45,  30.52, 1.8, 0.65),   # Kyiv, Ukraine
    (49.84,  24.03, 1.2, 0.62),   # Lviv, Ukraine
    (53.90,  27.57, 1.5, 0.62),   # Minsk, Belarus
    (37.98,  23.73, 1.5, 0.76),   # Athens, Greece
    (59.44,  24.75, 1.2, 0.88),   # Tallinn, Estonia
    (56.95,  24.10, 1.2, 0.87),   # Riga, Latvia
    (54.69,  25.28, 1.2, 0.86),   # Vilnius, Lithuania

    # ══════════════════════════════════════════════════════════════════════════
    # NORTH AMERICA
    # ══════════════════════════════════════════════════════════════════════════
    (40.71, -74.01, 2.0, 0.94),   # New York, USA
    (34.05,-118.24, 2.0, 0.92),   # Los Angeles, USA
    (41.85, -87.65, 2.0, 0.91),   # Chicago, USA
    (29.76, -95.37, 1.8, 0.88),   # Houston, USA
    (33.45,-112.07, 1.5, 0.87),   # Phoenix, USA
    (32.72,-117.15, 1.5, 0.89),   # San Diego, USA
    (37.78,-122.41, 1.8, 0.93),   # San Francisco, USA
    (47.61,-122.33, 1.5, 0.91),   # Seattle, USA
    (25.77, -80.19, 1.5, 0.88),   # Miami, USA
    (38.89, -77.03, 1.5, 0.91),   # Washington DC, USA
    (42.36, -71.06, 1.5, 0.92),   # Boston, USA
    (39.73,-104.99, 1.5, 0.89),   # Denver, USA
    (30.27, -97.74, 1.5, 0.89),   # Austin, USA
    (35.23, -80.84, 1.5, 0.87),   # Charlotte, USA
    (33.75, -84.39, 1.8, 0.87),   # Atlanta, USA
    (36.17, -86.78, 1.5, 0.86),   # Nashville, USA
    (43.65, -79.38, 1.8, 0.92),   # Toronto, Canada
    (45.50, -73.57, 1.5, 0.91),   # Montreal, Canada
    (49.25,-123.12, 1.5, 0.91),   # Vancouver, Canada
    (51.05,-114.07, 1.5, 0.90),   # Calgary, Canada
    (53.55,-113.49, 1.5, 0.89),   # Edmonton, Canada
    (45.42, -75.69, 1.5, 0.90),   # Ottawa, Canada
    (19.43, -99.13, 2.0, 0.64),   # Mexico City, Mexico
    (25.67,-100.31, 1.5, 0.62),   # Monterrey, Mexico
    (20.97, -89.62, 1.2, 0.55),   # Merida, Mexico
    (20.65,-105.22, 1.0, 0.54),   # Puerto Vallarta, Mexico
    (23.13, -82.38, 1.5, 0.58),   # Havana, Cuba
    (18.48, -69.93, 1.2, 0.52),   # Santo Domingo, DR
    (18.54, -72.34, 1.5, 0.30),   # Port-au-Prince, Haiti
    ( 9.93, -84.08, 1.2, 0.70),   # San José, Costa Rica
    (14.09, -87.21, 1.2, 0.46),   # Tegucigalpa, Honduras
    (13.69, -89.19, 1.2, 0.50),   # San Salvador, El Salvador
    (14.63, -90.51, 1.5, 0.54),   # Guatemala City
     (8.99, -79.52, 1.5, 0.68),   # Panama City

    # ══════════════════════════════════════════════════════════════════════════
    # SOUTH AMERICA
    # ══════════════════════════════════════════════════════════════════════════
    (-23.55, -46.63, 2.0, 0.68),  # São Paulo, Brazil
    (-22.90, -43.17, 2.0, 0.65),  # Rio de Janeiro, Brazil
    (-30.03, -51.23, 1.5, 0.66),  # Porto Alegre, Brazil
    (-19.92, -43.94, 1.5, 0.63),  # Belo Horizonte, Brazil
    (-15.78, -47.93, 1.5, 0.66),  # Brasília, Brazil
    (-12.97, -38.50, 1.2, 0.58),  # Salvador, Brazil
    ( -3.73, -38.52, 1.2, 0.55),  # Fortaleza, Brazil
    ( -8.05, -34.88, 1.2, 0.53),  # Recife, Brazil
    (-34.60, -58.38, 2.0, 0.68),  # Buenos Aires, Argentina
    (-31.41, -64.18, 1.5, 0.64),  # Córdoba, Argentina
    (-32.94, -60.65, 1.2, 0.63),  # Rosario, Argentina
    (-33.45, -70.67, 1.8, 0.73),  # Santiago, Chile
    (-23.00, -43.50, 1.0, 0.48),  # Rural Rio outskirts, Brazil
    (-12.05, -77.04, 1.5, 0.63),  # Lima, Peru
    (-17.38, -66.15, 1.2, 0.52),  # Cochabamba, Bolivia
    (-16.50, -68.15, 1.2, 0.50),  # La Paz, Bolivia
     (-0.23, -78.52, 1.2, 0.61), # Quito, Ecuador
    ( -2.19, -79.89, 1.2, 0.58),  # Guayaquil, Ecuador
     ( 4.71, -74.07, 1.5, 0.63), # Bogotá, Colombia
     ( 6.25, -75.56, 1.2, 0.61), # Medellín, Colombia
     ( 3.87,  11.52, 1.2, 0.38), # Yaoundé, Cameroon (repeat — see Africa)
    (10.49, -66.88, 1.5, 0.55),   # Caracas, Venezuela
     (-0.22, -78.51, 0.8, 0.46), # Quito periurban, Ecuador
    ( -4.84, -37.77, 0.8, 0.36),  # Rural Ceará, Brazil
    (-14.00, -52.00, 0.8, 0.30),  # Rural Mato Grosso, Brazil (Amazon fringe)

    # ══════════════════════════════════════════════════════════════════════════
    # SUB-SAHARAN AFRICA
    # ══════════════════════════════════════════════════════════════════════════
     ( 6.52,  3.38, 1.8, 0.36),  # Lagos, Nigeria
     ( 9.05,  7.49, 1.5, 0.42),  # Abuja, Nigeria
     ( 5.56, -0.20, 1.5, 0.48),  # Accra, Ghana
    (12.37, -1.53, 1.2, 0.37),   # Ouagadougou, Burkina Faso
    (12.65, -8.00, 1.0, 0.33),   # Bamako, Mali
    (13.52,  2.11, 1.0, 0.31),   # Niamey, Niger
    (15.55, 32.53, 1.5, 0.41),   # Khartoum, Sudan
    ( 9.03, 38.74, 1.5, 0.28),   # Addis Ababa, Ethiopia
     ( 2.05, 45.34, 1.2, 0.31), # Mogadishu, Somalia
     ( 0.33, 32.58, 1.5, 0.41), # Kampala, Uganda
    (-1.29, 36.82, 1.5, 0.42),   # Nairobi, Kenya
    (-4.04, 39.67, 1.0, 0.38),   # Mombasa, Kenya
    (-6.18, 35.74, 1.2, 0.34),   # Dodoma, Tanzania
    (-6.77, 39.27, 1.2, 0.40),   # Dar es Salaam, Tanzania
    (-13.97, 33.79, 1.0, 0.34),  # Lilongwe, Malawi
    (-15.42, 28.28, 1.2, 0.40),  # Lusaka, Zambia
    (-17.83, 31.05, 1.5, 0.46),  # Harare, Zimbabwe
    (-25.97, 32.59, 1.2, 0.45),  # Maputo, Mozambique
    (-4.32,  15.32, 1.5, 0.22),  # Kinshasa, DR Congo
    (-4.27,  15.29, 1.0, 0.24),  # Brazzaville, Congo
    (-25.75, 28.19, 1.8, 0.72),  # Pretoria, South Africa
    (-26.20, 28.04, 1.8, 0.73),  # Johannesburg, South Africa
    (-33.92, 18.42, 1.8, 0.74),  # Cape Town, South Africa
    (-29.86, 31.02, 1.5, 0.68),  # Durban, South Africa
    (-22.56, 17.08, 1.2, 0.56),  # Windhoek, Namibia
    (-24.66, 25.91, 1.0, 0.51),  # Gaborone, Botswana
    (-18.92, 47.54, 1.2, 0.36),  # Antananarivo, Madagascar
    (14.69, -17.44, 1.5, 0.46),  # Dakar, Senegal
     ( 4.36, 18.56, 1.2, 0.30), # Bangui, CAR
    (12.11,  15.04, 1.2, 0.30),  # N'Djamena, Chad
    (11.50,  43.13, 1.0, 0.35),  # Djibouti City
    (-18.15, 49.40, 0.8, 0.30),  # Toamasina, Madagascar
    # Rural Africa zones
    ( 5.00,  20.00, 1.0, 0.18),  # Rural DRC interior
    (12.00,  15.00, 1.0, 0.20),  # Rural Chad
    (15.00,  30.00, 1.0, 0.22),  # Rural Sudan
    ( 8.00,  40.00, 1.0, 0.22),  # Rural Ethiopia (remote)
    (-5.00,  28.00, 1.0, 0.20),  # Rural DRC east
    ( 3.00,  23.00, 1.0, 0.19),  # Rural CAR/Congo

    # ══════════════════════════════════════════════════════════════════════════
    # OCEANIA
    # ══════════════════════════════════════════════════════════════════════════
    (-33.87, 151.21, 2.0, 0.92),  # Sydney, Australia
    (-37.81, 144.96, 1.8, 0.91),  # Melbourne, Australia
    (-27.47, 153.02, 1.5, 0.90),  # Brisbane, Australia
    (-31.95, 115.86, 1.5, 0.90),  # Perth, Australia
    (-34.93, 138.60, 1.5, 0.89),  # Adelaide, Australia
    (-19.93, 143.99, 0.8, 0.55),  # Townsville, Australia
    (-12.46, 130.84, 0.8, 0.62),  # Darwin, Australia
    (-36.85, 174.76, 1.5, 0.89),  # Auckland, New Zealand
    (-41.29, 174.78, 1.2, 0.88),  # Wellington, New Zealand
    (-43.53, 172.63, 1.2, 0.87),  # Christchurch, New Zealand
    (-9.44,  147.18, 0.8, 0.38),  # Port Moresby, PNG
    (-9.43,  160.05, 0.8, 0.34),  # Honiara, Solomon Islands
    (-17.73, 168.32, 0.8, 0.42),  # Port Vila, Vanuatu
    (-18.14, 178.44, 0.8, 0.44),  # Suva, Fiji
    (-13.83,-171.77, 0.8, 0.45),  # Apia, Samoa

    # ══════════════════════════════════════════════════════════════════════════
    # RUSSIA & CENTRAL ASIA
    # ══════════════════════════════════════════════════════════════════════════
    (55.75,  37.62, 2.0, 0.72),   # Moscow
    (59.93,  30.32, 1.8, 0.68),   # St. Petersburg
    (56.84,  60.60, 1.2, 0.60),   # Yekaterinburg
    (55.00,  82.93, 1.2, 0.58),   # Novosibirsk
    (43.24,  76.89, 1.5, 0.56),   # Almaty, Kazakhstan
    (51.18,  71.45, 1.2, 0.54),   # Astana (Nur-Sultan), Kazakhstan
    (41.30,  69.24, 1.5, 0.51),   # Tashkent, Uzbekistan
    (39.67,  66.97, 1.0, 0.48),   # Samarkand, Uzbekistan
    (37.95,  58.38, 1.2, 0.44),   # Ashgabat, Turkmenistan
    (38.56,  68.77, 1.2, 0.45),   # Dushanbe, Tajikistan
    (42.87,  74.59, 1.2, 0.48),   # Bishkek, Kyrgyzstan
    (40.18,  44.51, 1.2, 0.58),   # Yerevan, Armenia
    (40.41,  49.87, 1.5, 0.60),   # Baku, Azerbaijan
    (41.69,  44.83, 1.5, 0.62),   # Tbilisi, Georgia
]


def _geo_development_prior(lat: float, lon: float) -> float:
    """
    Find the development score from the city database using
    distance-weighted lookup, with broad regional fallback.
    """
    best_score = None
    best_dist  = float("inf")

    for clat, clon, radius, cscore in CITY_DATABASE:
        dist = math.sqrt((lat - clat) ** 2 + (lon - clon) ** 2)
        if dist <= radius:
            # Smooth decay toward edges of radius
            weight = 1.0 - 0.12 * (dist / radius)
            adjusted = cscore * weight
            if best_score is None or dist < best_dist:
                best_score = adjusted
                best_dist  = dist

    if best_score is not None:
        return float(np.clip(best_score, 0.05, 0.98))

    # ── Broad regional fallbacks ──────────────────────────────────────────────
    if 30 < lat < 72 and -130 < lon < -60:   return 0.80  # N. America
    if 35 < lat < 72 and -10 < lon <  40:    return 0.82  # Europe
    if 30 < lat < 47 and 100 < lon < 148:    return 0.72  # E. Asia
    if 60 < lat:                              return 0.52  # Far north
    if -10 < lat < 30 and 65 < lon <  95:    return 0.36  # S. Asia rural
    if   8 < lat < 37 and 35 < lon <  65:    return 0.50  # MENA
    if -10 < lat < 20 and -20 < lon <  55:   return 0.28  # Sub-Saharan Africa
    if  20 < lat < 37 and -20 < lon <  40:   return 0.47  # North Africa
    if -55 < lat < 15 and -82 < lon < -35:   return 0.47  # S. America
    if -45 < lat < -10 and 110 < lon < 155:  return 0.76  # Australia rural
    if   5 < lat < 25 and  95 < lon < 140:   return 0.52  # SE Asia
    return 0.45   # global mean fallback


# ─────────────────────────────────────────────────────────────────────────────
# FEATURE EXTRACTION FROM IMAGE BYTES
# ─────────────────────────────────────────────────────────────────────────────

def extract_features_from_image(image_data: Union[bytes, np.ndarray]) -> np.ndarray:
    """
    Extract 12 socioeconomic proxy features from a satellite image.
    Handles any RGB image size up to 20 MB.
    """
    if isinstance(image_data, bytes):
        img = Image.open(io.BytesIO(image_data)).convert("RGB")
        arr = np.array(img, dtype=np.float32) / 255.0
    else:
        arr = image_data.astype(np.float32)
        if arr.max() > 1.0:
            arr /= 255.0

    r, g, b  = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    lum      = 0.299 * r + 0.587 * g + 0.114 * b   # perceptual luminance

    nightlight = float(np.mean(lum > 0.60))
    ndvi_raw   = _safe_div(g - r, g + r + 1e-6)
    ndvi       = float(np.clip(np.mean(ndvi_raw) * 0.5 + 0.5, 0, 1))
    grey       = 1.0 - (np.abs(r-g) + np.abs(g-b) + np.abs(r-b))
    built_up   = float(np.mean((grey > 0.70) & (lum > 0.30) & (lum < 0.90)))
    edges      = _edge_magnitude(lum)
    road       = float(np.mean(edges > 0.12))
    water      = float(np.mean((b > r + 0.06) & (b > g + 0.04) & (lum < 0.42)))
    uheat      = float(np.mean((r > 0.52) & (r > b + 0.08)))
    sp_var     = float(np.mean([np.std(r), np.std(g), np.std(b)]))
    tex_ent    = float(_texture_entropy(lum))
    edge_den   = float(np.mean(edges > 0.07))
    bright     = float(np.mean(lum > 0.68))
    infrared   = float(np.mean(r > 0.58))
    settle     = float(0.40 * nightlight + 0.30 * built_up + 0.30 * road)

    features = np.array([
        nightlight, ndvi,    built_up,
        road,       water,   uheat,
        sp_var,     tex_ent, edge_den,
        bright,     infrared, settle,
    ], dtype=np.float32)
    return np.clip(features, 0, 1)


# ─────────────────────────────────────────────────────────────────────────────
# FEATURE EXTRACTION FROM COORDINATES
# ─────────────────────────────────────────────────────────────────────────────

def extract_features_from_region(
    lat: float,
    lon: float,
    region_name: str = "Unknown",
) -> np.ndarray:
    """
    Simulate satellite feature extraction for any lat/lon on Earth.
    Uses city database priors with minimal noise for stable results.
    """
    seed = int(abs(lat * 1000 + lon * 100 + len(region_name) * 7)) % (2 ** 31)
    rng  = np.random.default_rng(seed)
    b    = _geo_development_prior(lat, lon)     # base development 0–1

    features = np.array([
        _jitter(b * 0.93,         0.025, rng),  # nightlight
        _jitter(1.0 - b * 0.74,   0.030, rng),  # ndvi (inverse of dev)
        _jitter(b * 0.89,         0.025, rng),  # built_up
        _jitter(b * 0.84,         0.030, rng),  # road_density
        _jitter(0.04 + rng.uniform(0, 0.10), 0.015, rng),  # water (independent)
        _jitter(b * 0.82,         0.030, rng),  # urban_heat
        _jitter(0.24 + b * 0.58,  0.025, rng),  # spectral_var
        _jitter(0.29 + b * 0.58,  0.025, rng),  # texture_entropy
        _jitter(b * 0.77,         0.030, rng),  # edge_density
        _jitter(b * 0.92,         0.025, rng),  # bright_pixel
        _jitter(0.15 + b * 0.35,  0.025, rng),  # infrared
        _jitter(b * 0.91,         0.025, rng),  # settlement
    ], dtype=np.float32)

    return np.clip(features, 0, 1)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _jitter(base: float, noise: float, rng) -> float:
    return float(np.clip(base + rng.normal(0, noise), 0, 1))

def _safe_div(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.where(np.abs(b) > 1e-8, a / b, 0.0)

def _edge_magnitude(gray: np.ndarray) -> np.ndarray:
    gy = np.abs(np.diff(gray, axis=0, prepend=gray[:1]))
    gx = np.abs(np.diff(gray, axis=1, prepend=gray[:, :1]))
    return np.clip(gx + gy, 0, 1)

def _texture_entropy(gray: np.ndarray) -> float:
    hist, _ = np.histogram(gray.flatten(), bins=32, range=(0, 1))
    hist     = hist.astype(float) + 1e-10
    prob     = hist / hist.sum()
    return float(-np.sum(prob * np.log2(prob)) / np.log2(32))
