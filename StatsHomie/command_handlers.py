import copy
import datetime
import math
import pprint
from typing import Tuple, Optional, Any, Callable

import discord

import time

from . import hypixel_api, dict_compressor, predictions, bedwars_calcs

# following was extracted by printing keys of bedwars dictionary on 4/27/21
# level is added from achievements
stats_compression_format = ["level", "bedwars_christmas_boxes", "packages", "Experience", "first_join_7", "free_event_key_bedwars_christmas_boxes_2017", "Bedwars_openedChests", "Bedwars_openedCommons", "Bedwars_openedRares", "chest_history_new", "Bedwars_openedEpics", "coins", "Bedwars_openedLegendaries", "activeKillEffect", "activeNPCSkin", "games_played_bedwars_1", "winstreak", "eight_one_beds_lost_bedwars", "final_deaths_bedwars", "gold_resources_collected_bedwars", "void_deaths_bedwars", "eight_one_entity_attack_final_kills_bedwars", "eight_one_final_deaths_bedwars", "eight_one_void_deaths_bedwars", "eight_one_deaths_bedwars", "void_kills_bedwars", "eight_one_games_played_bedwars", "diamond_resources_collected_bedwars", "deaths_bedwars", "eight_one_final_kills_bedwars", "eight_one_beds_broken_bedwars", "emerald_resources_collected_bedwars", "resources_collected_bedwars", "eight_one_losses_bedwars", "games_played_bedwars", "eight_one_iron_resources_collected_bedwars", "permanent _items_purchased_bedwars", "entity_attack_final_kills_bedwars", "eight_one__items_purchased_bedwars", "eight_one_emerald_resources_collected_bedwars", "eight_one_items_purchased_bedwars", "beds_lost_bedwars", "kills_bedwars", "eight_one_diamond_resources_collected_bedwars", "entity_attack_kills_bedwars", "eight_one_permanent _items_purchased_bedwars", "eight_one_entity_attack_kills_bedwars", "eight_one_void_kills_bedwars", "eight_one_void_final_kills_bedwars", "eight_one_wrapped_present_resources_collected_bedwars", "void_final_deaths_bedwars", "eight_one_kills_bedwars", "eight_one_void_final_deaths_bedwars", "losses_bedwars", "items_purchased_bedwars", "final_kills_bedwars", "void_final_kills_bedwars", "eight_one_resources_collected_bedwars", "iron_resources_collected_bedwars", "beds_broken_bedwars", "eight_one_gold_resources_collected_bedwars", "_items_purchased_bedwars", "wrapped_present_resources_collected_bedwars", "eight_one_fall_final_kills_bedwars", "eight_one_entity_attack_deaths_bedwars", "eight_one_wins_bedwars", "entity_attack_deaths_bedwars", "fall_final_kills_bedwars", "wins_bedwars", "four_three_void_kills_bedwars", "four_three_entity_attack_kills_bedwars", "four_three_wins_bedwars", "four_three_iron_resources_collected_bedwars", "four_three_games_played_bedwars", "four_three__items_purchased_bedwars", "four_three_void_deaths_bedwars", "four_three_beds_lost_bedwars", "four_three_gold_resources_collected_bedwars", "four_three_permanent _items_purchased_bedwars", "four_three_deaths_bedwars", "four_three_beds_broken_bedwars", "four_three_entity_attack_final_kills_bedwars", "four_three_wrapped_present_resources_collected_bedwars", "four_three_diamond_resources_collected_bedwars", "four_three_final_kills_bedwars", "four_three_items_purchased_bedwars", "four_three_kills_bedwars", "four_three_resources_collected_bedwars", "four_three_entity_attack_deaths_bedwars", "four_three_entity_explosion_kills_bedwars", "entity_explosion_kills_bedwars", "four_three_void_final_kills_bedwars", "activeKillMessages", "activeSprays", "activeVictoryDance", "activeProjectileTrail", "activeGlyph", "free_event_key_bedwars_christmas_boxes_2018", "eight_one_entity_attack_final_deaths_bedwars", "entity_attack_final_deaths_bedwars", "eight_two_void_deaths_bedwars", "eight_two_beds_broken_bedwars", "eight_two_emerald_resources_collected_bedwars", "eight_two_permanent _items_purchased_bedwars", "eight_two_resources_collected_bedwars", "eight_two_diamond_resources_collected_bedwars", "eight_two_wins_bedwars", "eight_two_kills_bedwars", "eight_two_entity_attack_final_kills_bedwars", "eight_two_entity_attack_kills_bedwars", "eight_two_iron_resources_collected_bedwars", "eight_two_void_kills_bedwars", "eight_two_deaths_bedwars", "eight_two__items_purchased_bedwars", "eight_two_games_played_bedwars", "eight_two_items_purchased_bedwars", "eight_two_entity_attack_deaths_bedwars", "eight_two_gold_resources_collected_bedwars", "eight_two_final_kills_bedwars", "activeDeathCry", "eight_two_final_deaths_bedwars", "eight_two_entity_attack_final_deaths_bedwars", "eight_two_beds_lost_bedwars", "eight_two_losses_bedwars", "bedwars_boxes", "four_three_entity_attack_final_deaths_bedwars", "four_three_losses_bedwars", "four_three_final_deaths_bedwars", "eight_two_void_final_kills_bedwars", "fall_deaths_bedwars", "eight_two_fall_deaths_bedwars", "fall_kills_bedwars", "eight_two_fall_kills_bedwars", "eight_one_fall_kills_bedwars", "eight_two_void_final_deaths_bedwars", "entity_explosion_deaths_bedwars", "eight_two_entity_explosion_deaths_bedwars", "projectile_deaths_bedwars", "eight_two_projectile_deaths_bedwars", "four_three_fall_kills_bedwars", "eight_one_fall_deaths_bedwars", "four_three_emerald_resources_collected_bedwars", "four_three_void_final_deaths_bedwars", "entity_explosion_final_kills_bedwars", "eight_one_entity_explosion_final_kills_bedwars", "four_four__items_purchased_bedwars", "four_four_permanent _items_purchased_bedwars", "four_four_kills_bedwars", "four_four_final_deaths_bedwars", "four_four_deaths_bedwars", "four_four_gold_resources_collected_bedwars", "four_four_diamond_resources_collected_bedwars", "four_four_beds_lost_bedwars", "four_four_losses_bedwars", "four_four_iron_resources_collected_bedwars", "four_four_entity_attack_final_deaths_bedwars", "four_four_games_played_bedwars", "four_four_fall_kills_bedwars", "four_four_resources_collected_bedwars", "four_four_void_deaths_bedwars", "four_four_items_purchased_bedwars", "four_four_entity_attack_kills_bedwars", "four_four_beds_broken_bedwars", "four_four_void_kills_bedwars", "four_four_entity_attack_deaths_bedwars", "four_four_wins_bedwars", "four_four_void_final_kills_bedwars", "four_four_final_kills_bedwars", "four_four_emerald_resources_collected_bedwars", "seen_beta_menu", "favourites_2", "eight_two_fall_final_deaths_bedwars", "fall_final_deaths_bedwars", "free_event_key_bedwars_lunar_boxes_2018", "bedwars_lunar_boxes", "four_four_void_final_deaths_bedwars", "four_three_fall_final_deaths_bedwars", "four_three_fall_deaths_bedwars", "eight_one_projectile_kills_bedwars", "projectile_kills_bedwars", "four_four_entity_attack_final_kills_bedwars", "four_four_fall_final_kills_bedwars", "four_three_projectile_deaths_bedwars", "eight_two_fall_final_kills_bedwars", "projectile_final_deaths_bedwars", "eight_one_projectile_final_deaths_bedwars", "four_four_fall_deaths_bedwars", "four_four_entity_explosion_deaths_bedwars", "four_three_fall_final_kills_bedwars", "bedwars_easter_boxes", "free_event_key_bedwars_easter_boxes_2018", "selected_ultimate", "eight_two_ultimate_winstreak", "eight_two_ultimate_void_final_deaths_bedwars", "eight_two_ultimate_deaths_bedwars", "eight_two_ultimate__items_purchased_bedwars", "eight_two_ultimate_resources_collected_bedwars", "eight_two_ultimate_beds_lost_bedwars", "eight_two_ultimate_games_played_bedwars", "eight_two_ultimate_iron_resources_collected_bedwars", "eight_two_ultimate_final_deaths_bedwars", "eight_two_ultimate_losses_bedwars", "eight_two_ultimate_void_deaths_bedwars", "eight_two_ultimate_gold_resources_collected_bedwars", "eight_two_ultimate_items_purchased_bedwars", "eight_one_winstreak", "understands_resource_bank", "understands_streaks", "castle_permanent _items_purchased_bedwars", "castle_deaths_bedwars", "castle__items_purchased_bedwars", "castle_games_played_bedwars", "castle_wins_bedwars", "castle_entity_attack_kills_bedwars", "castle_items_purchased_bedwars", "castle_diamond_resources_collected_bedwars", "castle_gold_resources_collected_bedwars", "castle_resources_collected_bedwars", "castle_entity_attack_deaths_bedwars", "castle_emerald_resources_collected_bedwars", "castle_void_deaths_bedwars", "castle_iron_resources_collected_bedwars", "castle_kills_bedwars", "castle_winstreak", "castle_beds_lost_bedwars", "castle_entity_attack_final_kills_bedwars", "castle_final_kills_bedwars", "castle_fall_deaths_bedwars", "castle_void_kills_bedwars", "castle_entity_explosion_deaths_bedwars", "castle_void_final_kills_bedwars", "eight_two_winstreak", "castle_entity_attack_final_deaths_bedwars", "castle_final_deaths_bedwars", "castle_losses_bedwars", "activeBedDestroy", "eight_one_entity_explosion_deaths_bedwars", "four_three_winstreak", "four_four_winstreak", "eight_two_entity_explosion_kills_bedwars", "activeIslandTopper", "favorite_slots", "fire_tick_deaths_bedwars", "eight_two_fire_tick_deaths_bedwars", "eight_two_entity_explosion_final_kills_bedwars", "eight_two_rush_winstreak", "eight_two_rush_items_purchased_bedwars", "eight_two_rush_losses_bedwars", "eight_two_rush__items_purchased_bedwars", "eight_two_rush_resources_collected_bedwars", "eight_two_rush_entity_attack_deaths_bedwars", "eight_two_rush_emerald_resources_collected_bedwars", "eight_two_rush_kills_bedwars", "eight_two_rush_deaths_bedwars", "eight_two_rush_void_deaths_bedwars", "eight_two_rush_entity_attack_final_deaths_bedwars", "eight_two_rush_gold_resources_collected_bedwars", "eight_two_rush_games_played_bedwars", "eight_two_rush_entity_attack_kills_bedwars", "eight_two_rush_beds_lost_bedwars", "eight_two_rush_permanent _items_purchased_bedwars", "eight_two_rush_final_deaths_bedwars", "eight_two_rush_iron_resources_collected_bedwars", "eight_two_rush_void_final_deaths_bedwars", "eight_two_rush_beds_broken_bedwars", "eight_two_rush_entity_attack_final_kills_bedwars", "eight_two_rush_diamond_resources_collected_bedwars", "eight_two_rush_void_kills_bedwars", "eight_two_rush_final_kills_bedwars", "eight_two_entity_explosion_final_deaths_bedwars", "entity_explosion_final_deaths_bedwars", "eight_one_entity_explosion_kills_bedwars", "four_four_fall_final_deaths_bedwars", "four_four_projectile_deaths_bedwars", "four_four_fire_tick_deaths_bedwars", "four_three_entity_explosion_deaths_bedwars", "four_four_entity_explosion_kills_bedwars", "bedwars_halloween_boxes", "spooky_open_ach", "lastTourneyAd", "four_three_fire_tick_deaths_bedwars", "voted_sugar_cookie2", "four_four_rush_winstreak", "four_four_rush__items_purchased_bedwars", "four_four_rush_beds_lost_bedwars", "four_four_rush_deaths_bedwars", "four_four_rush_diamond_resources_collected_bedwars", "four_four_rush_emerald_resources_collected_bedwars", "four_four_rush_entity_attack_final_kills_bedwars", "four_four_rush_entity_attack_kills_bedwars", "four_four_rush_final_kills_bedwars", "four_four_rush_games_played_bedwars", "four_four_rush_gold_resources_collected_bedwars", "four_four_rush_iron_resources_collected_bedwars", "four_four_rush_items_purchased_bedwars", "four_four_rush_kills_bedwars", "four_four_rush_permanent _items_purchased_bedwars", "four_four_rush_resources_collected_bedwars", "four_four_rush_void_deaths_bedwars", "four_four_rush_void_final_kills_bedwars", "four_four_rush_wins_bedwars", "eight_two_fire_tick_final_deaths_bedwars", "fire_tick_final_deaths_bedwars", "eight_one_projectile_deaths_bedwars", "eight_two_projectile_final_kills_bedwars", "projectile_final_kills_bedwars", "eight_two_suffocation_final_deaths_bedwars", "suffocation_final_deaths_bedwars", "four_four_rush_entity_attack_final_deaths_bedwars", "four_four_rush_final_deaths_bedwars", "four_four_rush_losses_bedwars", "four_four_rush_void_kills_bedwars", "four_four_rush_fall_kills_bedwars", "four_four_rush_void_final_deaths_bedwars", "four_four_entity_explosion_final_kills_bedwars", "eight_two_armed_winstreak", "eight_two_armed__items_purchased_bedwars", "eight_two_armed_beds_lost_bedwars", "eight_two_armed_deaths_bedwars", "eight_two_armed_diamond_resources_collected_bedwars", "eight_two_armed_entity_attack_deaths_bedwars", "eight_two_armed_entity_attack_kills_bedwars", "eight_two_armed_final_deaths_bedwars", "eight_two_armed_games_played_bedwars", "eight_two_armed_gold_resources_collected_bedwars", "eight_two_armed_iron_resources_collected_bedwars", "eight_two_armed_items_purchased_bedwars", "eight_two_armed_kills_bedwars", "eight_two_armed_losses_bedwars", "eight_two_armed_projectile_deaths_bedwars", "eight_two_armed_projectile_final_deaths_bedwars", "eight_two_armed_projectile_kills_bedwars", "eight_two_armed_resources_collected_bedwars", "eight_two_armed_void_deaths_bedwars", "eight_two_armed_beds_broken_bedwars", "eight_two_armed_final_kills_bedwars", "eight_two_armed_void_final_kills_bedwars", "eight_two_armed_void_kills_bedwars", "eight_two_armed_entity_attack_final_deaths_bedwars", "eight_two_armed_entity_attack_final_kills_bedwars", "eight_two_armed_fire_tick_deaths_bedwars", "eight_two_armed_permanent _items_purchased_bedwars", "four_four_armed_winstreak", "four_four_armed__items_purchased_bedwars", "four_four_armed_deaths_bedwars", "four_four_armed_diamond_resources_collected_bedwars", "four_four_armed_emerald_resources_collected_bedwars", "four_four_armed_entity_attack_deaths_bedwars", "four_four_armed_entity_attack_final_kills_bedwars", "four_four_armed_entity_attack_kills_bedwars", "four_four_armed_final_kills_bedwars", "four_four_armed_games_played_bedwars", "four_four_armed_gold_resources_collected_bedwars", "four_four_armed_iron_resources_collected_bedwars", "four_four_armed_items_purchased_bedwars", "four_four_armed_kills_bedwars", "four_four_armed_permanent _items_purchased_bedwars", "four_four_armed_projectile_deaths_bedwars", "four_four_armed_projectile_kills_bedwars", "four_four_armed_resources_collected_bedwars", "four_four_armed_void_deaths_bedwars", "four_four_armed_void_final_kills_bedwars", "four_four_armed_void_kills_bedwars", "four_four_armed_wins_bedwars", "eight_two_armed_fall_deaths_bedwars", "eight_two_armed_projectile_final_kills_bedwars", "eight_two_armed_wins_bedwars", "free_event_key_bedwars_halloween_boxes_2019", "four_four_voidless_winstreak", "four_four_voidless__items_purchased_bedwars", "four_four_voidless_beds_lost_bedwars", "four_four_voidless_deaths_bedwars", "four_four_voidless_diamond_resources_collected_bedwars", "four_four_voidless_entity_attack_deaths_bedwars", "four_four_voidless_entity_attack_final_kills_bedwars", "four_four_voidless_entity_attack_kills_bedwars", "four_four_voidless_fall_final_kills_bedwars", "four_four_voidless_final_kills_bedwars", "four_four_voidless_games_played_bedwars", "four_four_voidless_gold_resources_collected_bedwars", "four_four_voidless_iron_resources_collected_bedwars", "four_four_voidless_items_purchased_bedwars", "four_four_voidless_kills_bedwars", "four_four_voidless_permanent _items_purchased_bedwars", "four_four_voidless_resources_collected_bedwars", "four_four_voidless_void_final_kills_bedwars", "four_four_voidless_wins_bedwars", "four_four_voidless_entity_attack_final_deaths_bedwars", "four_four_voidless_final_deaths_bedwars", "four_four_voidless_losses_bedwars", "four_four_voidless_beds_broken_bedwars", "four_four_voidless_fall_deaths_bedwars", "four_four_voidless_emerald_resources_collected_bedwars", "four_four_voidless_fall_kills_bedwars", "four_four_voidless_void_kills_bedwars", "four_four_voidless_void_deaths_bedwars", "four_four_rush_beds_broken_bedwars", "four_four_rush_entity_attack_deaths_bedwars", "tourney_bedwars_two_four_0_winstreak2", "tourney_bedwars_two_four_0__items_purchased_bedwars", "tourney_bedwars_two_four_0_beds_broken_bedwars", "tourney_bedwars_two_four_0_deaths_bedwars", "tourney_bedwars_two_four_0_entity_attack_deaths_bedwars", "tourney_bedwars_two_four_0_entity_attack_kills_bedwars", "tourney_bedwars_two_four_0_fall_deaths_bedwars", "tourney_bedwars_two_four_0_games_played_bedwars", "tourney_bedwars_two_four_0_gold_resources_collected_bedwars", "tourney_bedwars_two_four_0_iron_resources_collected_bedwars", "tourney_bedwars_two_four_0_items_purchased_bedwars", "tourney_bedwars_two_four_0_kills_bedwars", "tourney_bedwars_two_four_0_permanent _items_purchased_bedwars", "tourney_bedwars_two_four_0_resources_collected_bedwars", "tourney_bedwars_two_four_0_void_deaths_bedwars", "tourney_bedwars_two_four_0_void_kills_bedwars", "tourney_bedwars_two_four_0_wins_bedwars", "tourney_bedwars_two_four_0_entity_attack_final_kills_bedwars", "tourney_bedwars_two_four_0_final_kills_bedwars", "tourney_bedwars_two_four_0_beds_lost_bedwars", "tourney_bedwars_two_four_0_entity_attack_final_deaths_bedwars", "tourney_bedwars_two_four_0_fall_kills_bedwars", "tourney_bedwars_two_four_0_final_deaths_bedwars", "tourney_bedwars_two_four_0_losses_bedwars", "tourney_bedwars_two_four_0_emerald_resources_collected_bedwars", "tourney_bedwars_two_four_0_void_final_deaths_bedwars", "tourney_bedwars_two_four_0_void_final_kills_bedwars", "tourney_bedwars_two_four_0_projectile_final_kills_bedwars", "tourney_bedwars_two_four_0_fall_final_deaths_bedwars", "tourney_bedwars_two_four_0_diamond_resources_collected_bedwars", "tourney_bedwars_two_four_0_fall_final_kills_bedwars", "eight_one_fall_final_deaths_bedwars", "two_four_winstreak", "two_four__items_purchased_bedwars", "two_four_beds_broken_bedwars", "two_four_deaths_bedwars", "two_four_entity_attack_kills_bedwars", "two_four_games_played_bedwars", "two_four_gold_resources_collected_bedwars", "two_four_iron_resources_collected_bedwars", "two_four_items_purchased_bedwars", "two_four_kills_bedwars", "two_four_resources_collected_bedwars", "two_four_void_deaths_bedwars", "two_four_void_kills_bedwars", "two_four_wins_bedwars", "two_four_beds_lost_bedwars", "two_four_emerald_resources_collected_bedwars", "two_four_entity_attack_deaths_bedwars", "two_four_entity_attack_final_deaths_bedwars", "two_four_final_deaths_bedwars", "two_four_losses_bedwars", "two_four_permanent _items_purchased_bedwars", "two_four_entity_attack_final_kills_bedwars", "two_four_final_kills_bedwars", "two_four_void_final_kills_bedwars", "two_four_void_final_deaths_bedwars", "two_four_fall_kills_bedwars", "two_four_fall_deaths_bedwars", "two_four_fall_final_kills_bedwars", "two_four_diamond_resources_collected_bedwars", "two_four_projectile_deaths_bedwars", "two_four_fall_final_deaths_bedwars", "four_four_armed_beds_broken_bedwars", "four_four_armed_projectile_final_kills_bedwars", "four_three_entity_explosion_final_deaths_bedwars", "eight_one_fire_tick_deaths_bedwars", "eight_one_entity_explosion_final_deaths_bedwars", "eight_one_magic_final_deaths_bedwars", "magic_final_deaths_bedwars", "eight_one_magic_deaths_bedwars", "magic_deaths_bedwars", "eight_two_magic_deaths_bedwars", "four_three_entity_explosion_final_kills_bedwars", "eight_two_magic_kills_bedwars", "magic_kills_bedwars", "eight_two_magic_final_deaths_bedwars", "eight_one_magic_kills_bedwars", "eight_one_magic_final_kills_bedwars", "magic_final_kills_bedwars", "four_three_magic_final_deaths_bedwars", "eight_two_magic_final_kills_bedwars", "two_four_magic_final_kills_bedwars", "four_four_armed_entity_explosion_deaths_bedwars", "four_three_magic_deaths_bedwars", "two_four_magic_deaths_bedwars", "eight_one_fire_tick_final_deaths_bedwars", "eight_two_permanent_items_purchased_bedwars", "permanent_items_purchased_bedwars", "eight_two_lucky_winstreak", "eight_two_lucky__items_purchased_bedwars", "eight_two_lucky_beds_broken_bedwars", "eight_two_lucky_beds_lost_bedwars", "eight_two_lucky_deaths_bedwars", "eight_two_lucky_diamond_resources_collected_bedwars", "eight_two_lucky_entity_attack_deaths_bedwars", "eight_two_lucky_entity_attack_final_kills_bedwars", "eight_two_lucky_final_deaths_bedwars", "eight_two_lucky_final_kills_bedwars", "eight_two_lucky_games_played_bedwars", "eight_two_lucky_gold_resources_collected_bedwars", "eight_two_lucky_iron_resources_collected_bedwars", "eight_two_lucky_items_purchased_bedwars", "eight_two_lucky_kills_bedwars", "eight_two_lucky_losses_bedwars", "eight_two_lucky_permanent_items_purchased_bedwars", "eight_two_lucky_resources_collected_bedwars", "eight_two_lucky_void_deaths_bedwars", "eight_two_lucky_void_final_deaths_bedwars", "eight_two_lucky_void_kills_bedwars", "eight_two_lucky_emerald_resources_collected_bedwars", "eight_two_lucky_entity_attack_final_deaths_bedwars", "eight_two_lucky_entity_attack_kills_bedwars", "eight_two_lucky_magic_deaths_bedwars", "eight_two_lucky_void_final_kills_bedwars", "eight_two_lucky_wins_bedwars", "two_four_permanent_items_purchased_bedwars", "four_three_permanent_items_purchased_bedwars", "two_four_magic_kills_bedwars", "eight_one_permanent_items_purchased_bedwars", "two_four_magic_final_deaths_bedwars", "four_four_permanent_items_purchased_bedwars", "four_four_magic_final_deaths_bedwars", "four_four_magic_kills_bedwars", "four_four_ultimate_winstreak", "four_four_ultimate__items_purchased_bedwars", "four_four_ultimate_beds_lost_bedwars", "four_four_ultimate_deaths_bedwars", "four_four_ultimate_entity_attack_deaths_bedwars", "four_four_ultimate_entity_attack_kills_bedwars", "four_four_ultimate_final_deaths_bedwars", "four_four_ultimate_games_played_bedwars", "four_four_ultimate_gold_resources_collected_bedwars", "four_four_ultimate_iron_resources_collected_bedwars", "four_four_ultimate_items_purchased_bedwars", "four_four_ultimate_kills_bedwars", "four_four_ultimate_losses_bedwars", "four_four_ultimate_resources_collected_bedwars", "four_four_ultimate_void_deaths_bedwars", "four_four_ultimate_void_final_deaths_bedwars", "four_four_ultimate_beds_broken_bedwars", "four_four_ultimate_diamond_resources_collected_bedwars", "four_four_ultimate_final_kills_bedwars", "four_four_ultimate_permanent_items_purchased_bedwars", "four_four_ultimate_projectile_final_deaths_bedwars", "four_four_ultimate_void_final_kills_bedwars", "four_four_ultimate_void_kills_bedwars", "four_three_magic_final_kills_bedwars", "eight_two_ultimate_diamond_resources_collected_bedwars", "eight_two_ultimate_emerald_resources_collected_bedwars", "eight_two_ultimate_entity_attack_final_kills_bedwars", "eight_two_ultimate_entity_attack_kills_bedwars", "eight_two_ultimate_final_kills_bedwars", "eight_two_ultimate_kills_bedwars", "eight_two_ultimate_permanent_items_purchased_bedwars", "eight_two_ultimate_void_final_kills_bedwars", "eight_two_ultimate_wins_bedwars", "eight_two_ultimate_entity_attack_deaths_bedwars", "eight_two_ultimate_entity_attack_final_deaths_bedwars", "eight_two_ultimate_void_kills_bedwars", "eight_two_ultimate_beds_broken_bedwars", "eight_two_ultimate_magic_final_kills_bedwars", "eight_two_ultimate_fire_tick_deaths_bedwars", "two_four_entity_explosion_deaths_bedwars", "two_four_fire_tick_deaths_bedwars", "four_three_magic_kills_bedwars", "four_four_armed_permanent_items_purchased_bedwars", "four_four_armed_magic_final_kills_bedwars", "four_four_magic_deaths_bedwars", "four_four_magic_final_kills_bedwars", "four_four_armed_beds_lost_bedwars", "four_four_armed_final_deaths_bedwars", "four_four_armed_losses_bedwars", "four_four_armed_projectile_final_deaths_bedwars", "four_four_armed_entity_attack_final_deaths_bedwars", "four_four_armed_fall_kills_bedwars", "privategames", "four_four_armed_magic_deaths_bedwars", "four_four_armed_fall_deaths_bedwars", "four_four_entity_explosion_final_deaths_bedwars", "eight_two_lucky_magic_final_kills_bedwars", "eight_two_lucky_fall_deaths_bedwars", "eight_two_lucky_entity_explosion_final_kills_bedwars", "eight_two_lucky_fire_tick_deaths_bedwars", "eight_two_lucky_fall_final_kills_bedwars", "eight_two_lucky_projectile_deaths_bedwars", "eight_two_lucky_magic_kills_bedwars", "eight_two_lucky_fall_kills_bedwars", "eight_two_lucky_fall_final_deaths_bedwars", "eight_two_projectile_final_deaths_bedwars", "free_event_key_bedwars_christmas_boxes_2020", "four_four_lucky_winstreak", "four_four_lucky__items_purchased_bedwars", "four_four_lucky_beds_lost_bedwars", "four_four_lucky_deaths_bedwars", "four_four_lucky_diamond_resources_collected_bedwars", "four_four_lucky_entity_attack_deaths_bedwars", "four_four_lucky_entity_attack_final_kills_bedwars", "four_four_lucky_entity_attack_kills_bedwars", "four_four_lucky_final_kills_bedwars", "four_four_lucky_games_played_bedwars", "four_four_lucky_gold_resources_collected_bedwars", "four_four_lucky_iron_resources_collected_bedwars", "four_four_lucky_items_purchased_bedwars", "four_four_lucky_kills_bedwars", "four_four_lucky_permanent_items_purchased_bedwars", "four_four_lucky_resources_collected_bedwars", "four_four_lucky_void_final_kills_bedwars", "four_four_lucky_wins_bedwars", "four_four_lucky_void_kills_bedwars", "four_four_lucky_final_deaths_bedwars", "four_four_lucky_losses_bedwars", "four_four_lucky_void_deaths_bedwars", "four_four_lucky_void_final_deaths_bedwars", "four_four_lucky_emerald_resources_collected_bedwars", "four_four_lucky_fire_tick_deaths_bedwars", "four_four_lucky_beds_broken_bedwars", "four_four_lucky_entity_attack_final_deaths_bedwars", "shop_sort", "free_event_key_bedwars_christmas_boxes_2021", "eight_two_suffocation_deaths_bedwars", "suffocation_deaths_bedwars", "four_four_projectile_final_deaths_bedwars", "practice", "eight_one_fire_tick_final_kills_bedwars", "fire_tick_final_kills_bedwars", "four_four_fire_tick_final_kills_bedwars", "eight_two_fire_tick_kills_bedwars", "fire_tick_kills_bedwars", "four_four_fire_tick_kills_bedwars", "eight_two_fire_tick_final_kills_bedwars", "free_event_key_bedwars_easter_boxes_2021", "eight_two_voidless_winstreak", "eight_two_voidless__items_purchased_bedwars", "eight_two_voidless_beds_broken_bedwars", "eight_two_voidless_deaths_bedwars", "eight_two_voidless_emerald_resources_collected_bedwars", "eight_two_voidless_entity_attack_deaths_bedwars", "eight_two_voidless_entity_attack_final_kills_bedwars", "eight_two_voidless_entity_attack_kills_bedwars", "eight_two_voidless_fall_deaths_bedwars", "eight_two_voidless_final_kills_bedwars", "eight_two_voidless_games_played_bedwars", "eight_two_voidless_gold_resources_collected_bedwars", "eight_two_voidless_iron_resources_collected_bedwars", "eight_two_voidless_items_purchased_bedwars", "eight_two_voidless_kills_bedwars", "eight_two_voidless_permanent_items_purchased_bedwars", "eight_two_voidless_resources_collected_bedwars", "eight_two_voidless_wins_bedwars", "eight_two_voidless_beds_lost_bedwars", "eight_two_voidless_diamond_resources_collected_bedwars", "eight_two_voidless_final_deaths_bedwars", "eight_two_voidless_losses_bedwars", "eight_two_voidless_magic_final_deaths_bedwars", "eight_two_voidless_magic_final_kills_bedwars", "eight_two_voidless_fall_final_kills_bedwars", "four_four_fire_tick_final_deaths_bedwars", "eight_one_fire_tick_kills_bedwars", "eight_one_projectile_final_kills_bedwars"]

SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
DAYS_PER_MONTH = 30
MONTHS_PER_YEAR = 12

TIME_HUMANIZER_BASE = lambda _time: math.ceil (_time)
STAT_WHOLE_HUMANIZER_BASE = lambda stat_whole: math.floor (stat_whole)
DECIMAL_DISPLAY_DIGITS = 2
STAT_DECIMAL_HUMANIZER_BASE = lambda stat_dec: round (stat_dec, DECIMAL_DISPLAY_DIGITS)

future_spec_suffixes = {
    "d": {
        "type": "timestamp",
        "humanizer": lambda days: f"{TIME_HUMANIZER_BASE (days)} days",
        "ts_generator": lambda days: time.time () + (SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY * days)
    },
    "mo": {
        "type": "timestamp",
        "humanizer": lambda months: f"{TIME_HUMANIZER_BASE (months)} months",
        "ts_generator": lambda months: time.time () + (
                    SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY * DAYS_PER_MONTH * months)
    },
    "y": {
        "type": "timestamp",
        "humanizer": lambda years: f"{TIME_HUMANIZER_BASE (years)} years",
        "ts_generator": lambda years: time.time () + (
                    SECONDS_PER_MINUTE * MINUTES_PER_HOUR * HOURS_PER_DAY * DAYS_PER_MONTH * MONTHS_PER_YEAR * years)
    },
    "*": {
        "type": "stat",
        "humanizer": lambda stars: f"{STAT_DECIMAL_HUMANIZER_BASE (stars)} stars",
        "value_generator": lambda stats: bedwars_calcs.xp_to_level (xp = stats ["Experience"])
    },
    "fkdr": {
        "type": "stat",
        "humanizer": lambda fkdr: f"{STAT_DECIMAL_HUMANIZER_BASE (fkdr)} final kills per final death",
        "value_generator": lambda stats: stats ["final_kills_bedwars"] / stats ["final_deaths_bedwars"]
    },
    "wlr": {
        "type": "stat",
        "humanizer": lambda wlr: f"{STAT_DECIMAL_HUMANIZER_BASE (wlr)} wins per loss",
        "value_generator": lambda stats: stats ["wins_bedwars"] / stats ["losses_bedwars"]
    },
    "bblr": {
        "type": "stat",
        "humanizer": lambda bblr: f"{STAT_DECIMAL_HUMANIZER_BASE (bblr)} beds broken per bed lost",
        "value_generator": lambda stats: stats ["beds_broken_bedwars"] / stats ["beds_lost_bedwars"]
    },
    "fk": {
        "type": "stat",
        "humanizer": lambda fk: f"{STAT_WHOLE_HUMANIZER_BASE (fk)} final kills",
        "value_generator": lambda stats: stats ["final_kills_bedwars"]
    },
    "w": {
        "type": "stat",
        "humanizer": lambda w: f"{STAT_WHOLE_HUMANIZER_BASE (w)} wins",
        "value_generator": lambda stats: stats ["wins_bedwars"]
    },
    "b": {
        "type": "stat",
        "humanizer": lambda b: f"{STAT_WHOLE_HUMANIZER_BASE (b)} beds broken",
        "value_generator": lambda stats: stats ["beds_broken_bedwars"]
    }
}

wanted_stats = {stat_name: stat_info for stat_name, stat_info in future_spec_suffixes.items () if stat_info ["type"] == "stat"}
def resolve_future_spec (*, future_spec: str):
    for suffix, suffix_info in future_spec_suffixes.items ():
        if future_spec.endswith (suffix):
            value = float (future_spec [:-(len (suffix))])
            out_dict = {
                "type": suffix_info ["type"],
                "humanized": suffix_info ["humanizer"] (value)
            }
            if suffix_info ["type"] == "timestamp":
                out_dict ["ts"] = suffix_info ["ts_generator"] (value)
            else: # suffix_info ["type"] == "stat"
                out_dict ["value"] = value
                out_dict ["value_generator"] = suffix_info ["value_generator"]
            return True, out_dict
    return False, None

def stats_at_time (*, source_data: dict, target_timestamp: float, requested_stats: dict):
    interpolated_stats = {}
    for name, stat_info in requested_stats.items ():
        source_data_for_stat = []
        for timestamp, data_point in source_data.items ():
            try: source_data_for_stat.append ((timestamp, stat_info ["value_generator"] (data_point)))
            except KeyError: pass
        interpolated_stats [name] = predictions.find_y_for_x (input_data = source_data_for_stat, x = target_timestamp)
    return interpolated_stats

def time_and_stats_at_stat (*, source_data: dict, target_stat_value_generator: Callable, target_stat_value: float, requested_stats: dict):
    source_data_for_stat = []
    for timestamp, data_point in source_data.items ():
        try: source_data_for_stat.append ((timestamp, target_stat_value_generator (data_point)))
        except KeyError: pass
    timestamp = predictions.find_x_for_y (input_data = source_data_for_stat, y = target_stat_value)
    return timestamp, stats_at_time (source_data = source_data, target_timestamp = timestamp, requested_stats = requested_stats)

async def get_latest_stats (*, bot, message, uuid: str):
    stats_success, stats_or_error = hypixel_api.get_bedwars_stats (uuid = uuid, api_key = bot.config ["hypixel_api_key"])
    if not stats_success:
        await message.reply (f"failed to retrieve stats, error is {stats_or_error}")
        return False, None

    compressed_stats = dict_compressor.DictCompressor.compress (decompressed = stats_or_error, _format = stats_compression_format)
    if uuid not in bot.storage ["minecraft_uuids"]: bot.storage ["minecraft_uuids"] [uuid] = {}
    storage_for_uuid = bot.storage ["minecraft_uuids"] [uuid]
    storage_for_uuid [str (time.time ())] = compressed_stats
    bot.storage.save ()

    return True, simplify_source_stats (source_stats = stats_or_error)

def simplify_source_stats (*, source_stats: dict):
    return {requested_stat_name: requested_stat_info ["value_generator"] (source_stats) for requested_stat_name, requested_stat_info in wanted_stats.items ()}

def humanize_timestamp (*, timestamp: float) -> str:
    try:
        return datetime.datetime.utcfromtimestamp (timestamp).strftime ("%m/%d/%Y")
    except ValueError as value_error:
        return f"(date formatting error: {str (value_error)})"

NEWLINE = "\n"
async def send_stats_printout (*, message: discord.Message, first_line: str, stats: dict):
    # await message.reply (f"lmao ur bad, only {stats ['final_kills_bedwars']} finals and {stats ['level']}*?")
    printout = f"{first_line}{NEWLINE}"
    for requested_stat_name, requested_stat_info in wanted_stats.items ():
        printout += f"{requested_stat_info ['humanizer'] (stats [requested_stat_name])}{NEWLINE}"
    await message.reply (printout)
    return True

async def resolve_self_command (*, bot, message: discord.Message, args: Optional [Tuple [Any]]):
    author_id = str (message.author.id)
    if args is not None:
        if len (args) not in [0, 1]:
            await message.reply ("need either no arguments (you've set your account) or one argument")
            return False, None
        if len (args) == 1:
            uuid = hypixel_api.get_player_uuid (username = args [0])
            if uuid is None:
                await message.reply ("setting your account: invalid username!")
                return False, None
            bot.storage ["discord_user_ids_to_minecraft_uuids"] [author_id] = uuid
            bot.storage.save ()
        if author_id not in bot.storage ["discord_user_ids_to_minecraft_uuids"]:
            await message.reply ("you need to set your account to use this! (add your username to the command)")
            return False, None
    else:
        if author_id not in bot.storage ["discord_user_ids_to_minecraft_uuids"]:
            await message.reply ("you need to set your account to use this! (run the me command with your username)")
            return False, None
    return True, bot.storage ["discord_user_ids_to_minecraft_uuids"] [author_id]

def normalize_data (data):
    timestamps = list (data.keys ())
    timestamps.sort ()
    out_data = {}
    first_timestamp = timestamps [0]
    first_data = data [first_timestamp]
    for timestamp in timestamps [1:]:
        print (f"### NORMALIZING {timestamp} ###")
        fixed_data = {}
        for key, value in data [timestamp].items ():
            if type (value) in (int, float):
                normalized = value - first_data [key]
                print (f"key {key}, first data {first_data [key]}, this data {value}: normalized {value} to {normalized}")
                if normalized > 0: fixed_data [key] = normalized
            else:
                print (f"{value} (key {key}) is not int or float")
        out_data [timestamp] = fixed_data
    print (f"number of output points: {len (out_data.keys ())}")
    for timestamp, data in out_data.items ():
        if 'final_kills_bedwars' in data and 'final_deaths_bedwars' in data: print (f"at {timestamp}: {data ['final_kills_bedwars']} / {data ['final_deaths_bedwars']}")
    return out_data

class CommandHandlers:
    @staticmethod
    async def me (bot, message: discord.Message, *args):
        success, uuid = await resolve_self_command (bot = bot, message = message, args = args)
        if not success: return False
        success, stats = await get_latest_stats (bot = bot, message = message, uuid = uuid)
        if not success: return success
        return await send_stats_printout (message = message, first_line = f"**Current stats for you:**", stats = stats)
    @staticmethod
    async def username (bot, message: discord.Message, *args):
        if len (args) != 1:
            await message.reply ("need one argument (username to look up stats for)")
            return False
        uuid = hypixel_api.get_player_uuid (username = args [0])
        if uuid is None:
            await message.reply ("invalid username!")
            return False
        success, stats = await get_latest_stats (bot = bot, message = message, uuid = uuid)
        if not success: return success
        return await send_stats_printout (message = message, first_line = f"**Current stats for {args [0]}:**", stats = stats)
    @staticmethod
    async def past (bot, message: discord.Message, *args):
        await message.reply (f"This command is currently disabled due to Discord message size limitations.")
        return False
        # success, uuid = await resolve_self_command (bot = bot, message = message, args = args)
        # if not success: return False
        # storage_for_uuid = bot.storage ["minecraft_uuids"] [uuid]
        # for _time, compressed_entry in storage_for_uuid.items ():
        #     entry = dict_compressor.DictCompressor.decompress (compressed = compressed_entry, _format = stats_compression_format)
        #     print (f"at {_time}:")
        #     for key, value in entry.items ():
        #         print (f"{key}: {value}")
        # await message.reply (f"Printed your history to Eric's console. (haha trolled)")
    @staticmethod
    async def future (bot, message: discord.Message, *args):
        if len (args) not in [1, 2]:
            await message.reply ("need one or two arguments (future spec, or player and future spec)")
            return False
        if len (args) == 1:
            success, uuid = await resolve_self_command (bot = bot, message = message, args = None)
            if not success: return False
            future_spec = args [0]
        else: # len (args) == 2
            uuid = hypixel_api.get_player_uuid (username = args [0])
            if uuid is None:
                await message.reply ("invalid username!")
                return False
            future_spec = args [1]

        # await message.reply (f"uuid {uuid}, future_spec {future_spec}")

        success, _ = await get_latest_stats (bot = bot, message = message, uuid = uuid)
        if not success: return False

        source_data = {float (_time): dict_compressor.DictCompressor.decompress (compressed = compressed_entry, _format = stats_compression_format) for _time, compressed_entry in bot.storage ["minecraft_uuids"] [uuid].items ()}
        success, future_spec_info = resolve_future_spec (future_spec = future_spec)
        if not success:
            await message.reply (f"unable to resolve your specification of the future time or statistic")
            return False
        if not (len (source_data) > 1):
            await message.reply (f"you need at least two data points! check back after playing for a bit")
            return False
        source_data = normalize_data (source_data)
        if not (len (source_data) > 1):
            await message.reply (f"you need at least two normalized data points! check back after playing for a bit")
            return False
        if future_spec_info ["type"] == "timestamp":
            first_line = f"**Stats in {future_spec_info ['humanized']}:**"
            out_stats = stats_at_time (source_data = source_data, target_timestamp = future_spec_info ["ts"], requested_stats = wanted_stats)
        else: # future_spec_info ["type"] == "stat"
            try:
                timestamp, out_stats = time_and_stats_at_stat (source_data = source_data, target_stat_value_generator = future_spec_info ["value_generator"], target_stat_value = future_spec_info ["value"], requested_stats = wanted_stats)
            except predictions.ZeroSlopeError:
                await message.reply (f"zero slope encountered when predicting your statistics, play a little and try again")
                return False
            first_line = f"**Stats at {future_spec_info ['humanized']} (on {humanize_timestamp (timestamp = timestamp)}):**"
        return await send_stats_printout (message = message, first_line = first_line, stats = out_stats)
    @staticmethod
    async def help (bot, message: discord.Message, *args):
        help_printout = [
            f"**StatsHomie**, written by <@199195868400713729>, hosted by <@{bot.config ['host_discord_user_id']}>",
            f"*Source code available at https://github.com/An0nDev/StatsHomie*",
            f"*Invite this instance of the bot to your server with the following link: https://discord.com/oauth2/authorize?client_id={bot.client.user.id}&scope=bot*",
            f"**Prefix:** `{bot.config ['prefix']}` (e.g. `{bot.config ['prefix']}.command_name arguments here`)",
            f"**Default command:** `{bot.command_database ['default']}` (e.g. `{bot.config ['prefix']}` is the same as  `{bot.config ['prefix']}.{bot.command_database ['default']}`",
            f"**Commands:**",
            *[f"- `{bot.config ['prefix']}.{command_name}` (aliases {', '.join (f'`{alias}`' for alias in command_info ['aliases'])}): {command_info ['description']}" for command_name, command_info in bot.command_database ["commands"].items ()]
        ]
        await message.reply (NEWLINE.join (help_printout))
        return True