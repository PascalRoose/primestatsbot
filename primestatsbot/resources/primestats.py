#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ** Stats Converter **
# This is a simple Telegram bot for converting exported stats from Ingress Prime to a nicely formatted message
#
# - Author: PascalRoose
# - Repo: https://github.com/PascalRoose/primestatsbot.git
#

PRIMESTATS = {
    "General": {
        "Time Span": "",
        "Agent Name": "",
        "Agent Faction": "",
        "Date (yyyy-mm-dd)": "",
        "Time (hh:mm:ss)": "",
        "Level": "",
        "Lifetime AP": "AP",
        "Current AP": "AP"
    },
    "Discovery": {
        "Unique Portals Visited": "",
        "Unique Portals Drone Visited": "",
        "Furthest Drone Distance": "km",
        "Portals Discovered": "",
        "Seer Points": "",
        "XM Collected": "XM",
        "OPR Agreements": "",
        "Portal Scans Uploaded": "",
        "Uniques Scout Controlled": ""
    },
    "Building": {
        "Resonators Deployed": "",
        "Links Created": "",
        "Control Fields Created": "",
        "Mind Units Captured": "MUs",
        "Longest Link Ever Created": "km",
        "Largest Control Field": "MUs",
        "XM Recharged": "",
        "Portals Captured": "",
        "Unique Portals Captured": "",
        "Mods Deployed": "",
        "Links Active": "",
        "Portals Owned": "",
        "Control Fields Active": "",
        "Mind Unit Control": "MUs"
    },
    "Resource Gathering": {
        "Hacks": "",
        "Drone Hacks": "",
        "Glyph Hack Points": ""
    },
    "Streaks": {
        "Longest Hacking Streak": "days",
        "Current Hacking Streak": "days",
        "Longest Sojourner Streak": "days",
        "Completed Hackstreaks": ""
    },
    "Combat": {
        "Resonators Destroyed": "",
        "Portals Neutralized": "",
        "Enemy Links Destroyed": "",
        "Enemy Fields Destroyed": "", 
        "Battle Beacon Combatant": "",
        "Drones Returned": ""
    },
    "Defense": {
        "Max Time Portal Held": "days",
        "Max Time Link Maintained": "days",
        "Max Link Length x Days": "km-days",
        "Max Time Field Held": "days",
        "Largest Field MUs x Days": "MU-days",
        "Forced Drone Recalls": ""
    },
    "Health": {
        "Distance Walked": "km", 
        "Kinetic Capsules Completed": ""
    },
    "Missions": {
        "Unique Missions Completed": ""
    },
    "Events": {
        "Mission Day(s) Attended": "",
        "NL-1331 Meetup(s) Attended": "",
        "First Saturday Events": "",
        "Second Sunday Events": "",
        "Clear Fields Events": "",
        "OPR Live Events": "",
        "Prime Challenges": "",
        "Intel Ops Missions": "",
        "Stealth Ops Missions": "",
        "Didact Fields Created": "",
        "EOS Points Earned": "",
        "Solstice XM Recharged": "XM",
        "Kythera": ""
    },
    "Mentoring": {
        "Agents Recruited": ""
    },
    "Recursion": {
        "Recursions": ""
    },
    "Subscription": {
        "Months Subscribed": ""
    }
}
