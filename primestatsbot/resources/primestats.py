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
        "Portals Discovered": "",
        "Seer Points": "",
        "XM Collected": "XM",
        "OPR Agreements": "",
        "Portal Scans Uploaded": ""
    },
    "Health": {
        "Distance Walked": "km"
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
    "Combat": {
        "Resonators Destroyed": "",
        "Portals Neutralized": "",
        "Enemy Links Destroyed": "",
        "Enemy Fields Destroyed": ""
    },
    "Defense": {
        "Max Time Portal Held": "days",
        "Max Time Link Maintained": "days",
        "Max Link Length x Days": "km-days",
        "Max Time Field Held": "days",
        "Largest Field MUs x Days": "MU-days"
    },
    "Missions": {
        "Unique Missions Completed": ""
    },
    "Resource Gathering": {
        "Hacks": "",
        "Drone Hacks": "",
        "Glyph Hack Points": "",
        "Longest Hacking Streak": "days",
        "Current Hacking Streak": "days"
    },
    "Mentoring": {
        "Agents Successfully Recruited": ""
    },
    "Events": {
        "Mission Day(s) Attended": "",
        "NL-1331 Meetup(s) Attended": "",
        "First Saturday Events": "",
        "Clear Fields Events": "",
        "OPR Live Events": "",
        "Prime Challenges": "",
        "Intel Ops Missions": "",
        "Stealth Ops Missions": "",
        "Didact Fields Created": ""
    },
    "Recursion": {
        "Recursions": ""
    }
}
