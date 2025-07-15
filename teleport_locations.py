# Lies of P - Teleport Locations Data
# Generated from teleport_locations.txt - 192 Total Locations
# Last updated: 2025-01-22

# Boss name mapping based on chapter order
BOSS_NAMES = {
    1: "Parade Master",
    2: "Scrapped Watchman",
    3: "Kings Flame, Fuoco",
    4: "Fallen Archbishop Andreus", 
    5: "Eldest of the Black Rabbit Brotherhood",
    6: "King of Puppets",
    7: "Champion Victor",
    8: "Green Monster of the Swamp",
    9: "Corrupted Parade Master",
    11: "Black Rabbit Brotherhood",  # 10 is missing
    12: "Laxasia the Complete",
    13: "Simon Manus, Arm of God",
    14: "Nameless Puppet",
    15: "Markiona, Puppeteer of Death",
    16: "Anguished Guardian of the Ruins",
    17: "Arlecchino the Blood Artist",
    18: "Two-faced Overseer",
}

# Structured teleport locations data
TELEPORT_LOCATIONS = {
    "base_game": {
        "factory": [
            "LD_Factory_S",
            "LD_Factory_Channel", 
            "LD_Factory_ControlRoom",
            "LD_Factory_BossRoom",
            "LD_Factory_Portal"
        ],
        "boutique": [
            "LD_Boutique_S",
            "LD_Boutique_Apt",
            "LD_Boutique_Portal"
        ],
        "monastery": [
            "LD_Monastery_A_BlackBeach",
            "LD_Monastery_A_Enterance",
            "LD_Monastery_A_OuterWall",
            "LD_Monastery_A_SeedRoom",
            "LD_Monastery_A_BrokenTower",
            "LD_Monastery_A_BossRoomReady",
            "LD_Monastery_A_BossRoom",
            "LD_Monastery_B_InnerTower",
            "LD_Monastery_B_6F",
            "LD_Monastery_B_BossRoom",
            "LD_Monastery_B_HiddenBossRoom",
            "LD_Monastery_Enter",
            "LD_Monastery_A_S",
            "LD_Monastery_Portal",
            "LD_Monastery_Portal2"
        ],
        "arcade": [
            "LD_Arcade_S"
        ],
        "underdark": [
            "LD_Underdark_S",
            "LD_Underdark_Lab",
            "LD_Underdark_Ruin_S",
            "LD_Underdark_Ruin_Enterance",
            "LD_Underdark_Ruin_BossRoom",
            "LD_Underdark_Exit",
            "LD_Underdark_End"
        ],
        "cathedral": [
            "LD_Cathrdal_Village",
            "LD_Cathrdal_Road",
            "LD_Cathrdal_S",
            "LD_Cathrdal_Library",
            "LD_Cathrdal_BossRoom",
            "LD_Cathrdal_Portal",
            "LD_Cathrdal_Portal2"
        ],
        "hotel": [
            "LD_Hotel_Main",
            "LD_Hotel_I_Main",
            "LD_Hotel_S_Enter",
            "LD_Hotel_S_Exit",
            "LD_Hotel_N_Enter",
            "LD_Hotel_N_Exit",
            "LD_Hotel_E_Enter",
            "LD_Hotel_E_Exit",
            "LD_Hotel_NW_Enter",
            "LD_Hotel_NW_Exit",
            "LD_Hotel_I_S_Enter",
            "LD_Hotel_I_S_Exit",
            "LD_Hotel_I_N_Enter",
            "LD_Hotel_I_N_Exit",
            "LD_Hotel_I_E_Enter",
            "LD_Hotel_I_E_Exit",
            "LD_Hotel_I_NW_Enter",
            "LD_Hotel_I_NW_Exit",
            "LD_Hotel_Under_Enter",
            "LD_Hotel_Under_Exit"
        ],
        "station": [
            "LD_Station_Plaza",
            "LD_Station_Festival",
            "LD_Station_BossRoom",
            "LD_Station_Platform",
            "LD_Station_Lobby",
            "LD_Station_House",
            "LD_Station_Breakdown",
            "LD_Station_Street",
            "LD_Station_Street_Enter",
            "LD_Station_S",
            "LD_Station_S_Enter"
        ],
        "town_hall": [
            "LD_TownHall_Road",
            "LD_TownHall_BossRoom"
        ],
        "exhibition_hall": [
            "LD_ExhibitionHall_Plaza",
            "LD_ExhibitionHall_Center",
            "LD_ExhibitionHall_BossRoom",
            "LD_ExhibitionHall_Pieta",
            "LD_ExhibitionHall_Portal"
        ],
        "culture_street": [
            "LD_CultureStreet_S",
            "LD_CultureStreet_Subway",
            "LD_CultureStreet_Opera_S",
            "LD_CultureStreet_Opera_BossRoom",
            "LD_CultureStreet_Portal"
        ],
        "old_town": [
            "LD_OldTown_Pilgrimage",
            "LD_OldTown_S",
            "LD_OldTown_Bridge",
            "LD_OldTown_BossRoom",
            "LD_OldTown_Portal"
        ],
        "puppet_grave": [
            "LD_Puppet_Grave_S",
            "LD_Puppet_Grave_Swamp",
            "LD_Puppet_Grave_Valley",
            "LD_Puppet_Grave_Bridge",
            "LD_Puppet_Grave_BossRoom",
            "LD_Puppet_Grave_Mine"
        ]
    },
    "dlc_content": {
        "winter_sea": [
            "DLC_LD_Winter_Sea_Enterance",
            "DLC_LD_Winter_Sea_Beach",
            "DLC_LD_Winter_Sea_BeachCave",
            "DLC_LD_Winter_Sea_FrozenSea",
            "DLC_LD_Winter_Sea_WreckedShip",
            "DLC_LD_Winter_Sea_Whale",
            "DLC_LD_Winter_Sea_LightHouse",
            "DLC_LD_Winter_Sea_Forest",
            "DLC_LD_Winter_Sea_Mansion",
            "DLC_LD_Winter_Sea_Mansion_Basement",
            "DLC_LD_Winter_Sea_Mansion_Library",
            "DLC_LD_Winter_Sea_Mansion_2F",
            "DLC_LD_Winter_Sea_Boss",
            "DLC_LD_Winter_Sea_Portal",
            "DLC_LD_Winter_Sea_WreckedShip_Portal",
            "DLC_LD_Winter_Sea_Mansion_Portal"
        ],
        "zoo": [
            "DLC_LD_Krat_Zoo_FirstEntry",
            "DLC_LD_Krat_Zoo_Main",
            "DLC_LD_Krat_Zoo_RainForest",
            "DLC_LD_Krat_Zoo_Savana",
            "DLC_LD_Krat_Zoo_Swamp",
            "DLC_LD_Krat_Zoo_GreenHouse",
            "DLC_LD_Krat_Zoo_BossRoom",
            "DLC_LD_Krat_Zoo_Garden",
            "DLC_LD_Krat_Zoo_Tram",
            "DLC_LD_Krat_Zoo_Enter_1st",
            "DLC_LD_Krat_Zoo_Enter_2nd",
            "DLC_LD_Krat_Zoo_Exit_1st",
            "DLC_LD_Krat_Zoo_Exit_2nd"
        ],
        "underground_lab": [
            "DLC_LD_Underground_Lab_Enterance",
            "DLC_LD_Underground_Lab_Control",
            "DLC_LD_Underground_Lab_ControlRoom",
            "DLC_LD_Underground_Lab_Laboratory",
            "DLC_LD_Underground_Lab_Portal",
            "DLC_LD_Underground_Lab_CoolingDevice"
        ],
        "deserted_hotel": [
            "DLC_LD_Deserted_Hotel_Main",
            "DLC_LD_Deserted_Hotel_Portal_1st",
            "DLC_LD_Deserted_Hotel_Portal_2nd",
            "DLC_LD_Deserted_Hotel_Lab_Lift"
        ],
        "special_hotels": [
            "DLC_LD_AbyssHotel",
            "DLC_LD_TwilightHotel"
        ],
        "underground_ruin": [
            "DLC_LD_Underground_Ruin_Enterance",
            "DLC_LD_Underground_Ruin_Mine",
            "DLC_LD_Underground_Ruin_GreenHunter",
            "DLC_LD_Underground_Ruin_Dock",
            "DLC_LD_Underground_Ruin_Boss",
            "DLC_LD_Underground_Ruin_BossRoom",
            "DLC_LD_Underground_Ruin_Portal",
            "DLC_LD_Underground_Ruin_Boss_Portal"
        ]
    },
    "boss_challenges": [
        # Chapter 1
        "DLC_BC_CH01_Boss",
        "DLC_BC_CH01_Boss_Clear",
        "DLC_BC_CH01_Boss_Portal",
        # Chapter 2
        "DLC_BC_CH02_Boss",
        "DLC_BC_CH02_Boss_Clear", 
        "DLC_BC_CH02_Boss_Portal",
        # Chapter 3
        "DLC_BC_CH03_Boss",
        "DLC_BC_CH03_Boss_Clear",
        "DLC_BC_CH03_Boss_Portal",
        # Chapter 4
        "DLC_BC_CH04_Boss",
        "DLC_BC_CH04_Boss_Clear",
        "DLC_BC_CH04_Boss_Portal",
        # Chapter 5
        "DLC_BC_CH05_Boss",
        "DLC_BC_CH05_Boss_Clear",
        "DLC_BC_CH05_Boss_Portal",
        # Chapter 6
        "DLC_BC_CH06_Boss",
        "DLC_BC_CH06_Boss_Clear",
        "DLC_BC_CH06_Boss_Portal",
        # Chapter 7
        "DLC_BC_CH07_Boss",
        "DLC_BC_CH07_Boss_Clear",
        "DLC_BC_CH07_Boss_Portal",
        # Chapter 8
        "DLC_BC_CH08_Boss",
        "DLC_BC_CH08_Boss_Clear",
        "DLC_BC_CH08_Boss_Portal",
        # Chapter 9
        "DLC_BC_CH09_Boss",
        "DLC_BC_CH09_Boss_Clear",
        "DLC_BC_CH09_Boss_Portal",
        # Chapter 11 (10 missing)
        "DLC_BC_CH11_Boss",
        "DLC_BC_CH11_Boss_Clear",
        "DLC_BC_CH11_Boss_Portal",
        # Chapter 12
        "DLC_BC_CH12_Boss",
        "DLC_BC_CH12_Boss_Clear",
        "DLC_BC_CH12_Boss_Portal",
        # Chapter 13
        "DLC_BC_CH13_Boss",
        "DLC_BC_CH13_Boss_Clear",
        "DLC_BC_CH13_Boss_Portal",
        # Chapter 14
        "DLC_BC_CH14_Boss",
        "DLC_BC_CH14_Boss_Clear",
        "DLC_BC_CH14_Boss_Portal",
        # Chapter 15
        "DLC_BC_CH15_Boss",
        "DLC_BC_CH15_Boss_Clear",
        "DLC_BC_CH15_Boss_Portal",
        # Chapter 16
        "DLC_BC_CH16_Boss",
        "DLC_BC_CH16_Boss_Clear",
        "DLC_BC_CH16_Boss_Portal",
        # Chapter 17
        "DLC_BC_CH17_Boss",
        "DLC_BC_CH17_Boss_Clear",
        "DLC_BC_CH17_Boss_Portal",
        # Chapter 18
        "DLC_BC_CH18_Boss",
        "DLC_BC_CH18_Boss_Clear",
        "DLC_BC_CH18_Boss_Portal"
    ]
}

def get_location_count():
    """Get total count of all locations"""
    base_count = sum(len(locations) for locations in TELEPORT_LOCATIONS["base_game"].values())
    dlc_count = sum(len(locations) for locations in TELEPORT_LOCATIONS["dlc_content"].values())
    boss_count = len(TELEPORT_LOCATIONS["boss_challenges"])
    return {
        "base_game": base_count,
        "dlc_content": dlc_count, 
        "boss_challenges": boss_count,
        "total": base_count + dlc_count + boss_count
    }

def create_display_name(location_name):
    """Create user-friendly display name from internal location name"""
    import re
    
    # Handle boss challenges specifically
    if 'DLC_BC_CH' in location_name and 'Boss' in location_name:
        ch_match = re.search(r'CH(\d+)', location_name)
        if ch_match:
            ch_num = int(ch_match.group(1))
            boss_name = BOSS_NAMES.get(ch_num, f"Chapter {ch_num} Boss")
            
            if 'Clear' in location_name:
                return f"{boss_name} (Victory)"
            elif 'Portal' in location_name:
                return f"{boss_name} (Portal)"
            else:
                return boss_name
    
    # Remove common prefixes
    display = location_name
    prefixes_to_remove = ['LD_', 'DLC_LD_', 'DLC_BC_CH', 'DLC_BC_']
    for prefix in prefixes_to_remove:
        if display.startswith(prefix):
            display = display[len(prefix):]
            break
    
    # Replace underscores with spaces and title case
    display = display.replace('_', ' ').title()
    
    # Special cases for better readability
    replacements = {
        'Cathrdal': 'Cathedral',
        'Townhall': 'Town Hall',
        'Culturestreet': 'Culture Street',
        'Exhibitionhall': 'Exhibition Hall',
        'Puppet Grave': 'Puppet Graveyard',
        'Underdark': 'Underground Areas',
        'Bossroom': 'Boss Arena',
        'Enterance': 'Entrance',
        'S Enter': 'South Entrance',
        'S Exit': 'South Exit',
        'N Enter': 'North Entrance',
        'N Exit': 'North Exit',
        'E Enter': 'East Entrance',
        'E Exit': 'East Exit',
        'NW Enter': 'Northwest Entrance',
        'NW Exit': 'Northwest Exit',
        'I Main': 'Inner Main',
        'I S': 'Inner South',
        'I N': 'Inner North',
        'I E': 'Inner East',
        'I NW': 'Inner Northwest'
    }
    
    for old, new in replacements.items():
        if old.lower() in display.lower():
            display = display.replace(old, new)
    
    return display

def get_all_locations_flat():
    """Get all locations as a flat list with categories and display names"""
    locations = []
    
    # Add base game locations
    for subcategory, location_list in TELEPORT_LOCATIONS["base_game"].items():
        for location_name in location_list:
            locations.append({
                "id": location_name,
                "name": location_name,
                "displayName": create_display_name(location_name),
                "description": subcategory.replace('_', ' ').title(),
                "chapter": subcategory.replace('_', ' ').title(),
                "category": "Base Game",
                "subcategory": subcategory.replace('_', ' ').title()
            })
    
    # Add DLC locations  
    for subcategory, location_list in TELEPORT_LOCATIONS["dlc_content"].items():
        for location_name in location_list:
            locations.append({
                "id": location_name,
                "name": location_name,
                "displayName": create_display_name(location_name),
                "description": subcategory.replace('_', ' ').title(),
                "chapter": subcategory.replace('_', ' ').title(),
                "category": "DLC Content",
                "subcategory": subcategory.replace('_', ' ').title()
            })
    
    # Add boss challenges
    for location_name in TELEPORT_LOCATIONS["boss_challenges"]:
        import re
        ch_match = re.search(r'CH(\d+)', location_name)
        chapter_num = int(ch_match.group(1)) if ch_match else 0
        
        locations.append({
            "id": location_name,
            "name": location_name,
            "displayName": create_display_name(location_name),
            "description": f"Chapter {chapter_num} Boss Challenge",
            "chapter": f"Chapter {chapter_num}",
            "category": "Boss Challenges",
            "subcategory": f"Chapter {chapter_num}",
            "chapterNum": chapter_num
        })
    
    return locations

if __name__ == "__main__":
    # Debug info
    counts = get_location_count()
    print(f"📊 Location counts:")
    print(f"   Base Game: {counts['base_game']}")
    print(f"   DLC Content: {counts['dlc_content']}")  
    print(f"   Boss Challenges: {counts['boss_challenges']}")
    print(f"   Total: {counts['total']}")
    
    # Test a few display names
    print(f"\n🎯 Sample display names:")
    print(f"   LD_Hotel_Main -> {create_display_name('LD_Hotel_Main')}")
    print(f"   DLC_BC_CH12_Boss -> {create_display_name('DLC_BC_CH12_Boss')}")
    print(f"   DLC_LD_Winter_Sea_Mansion -> {create_display_name('DLC_LD_Winter_Sea_Mansion')}")
