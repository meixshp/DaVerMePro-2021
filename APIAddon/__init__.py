# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
import requests
import json

bl_info = {
    "name" : "APIAddon",
    "author" : "Champions",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

class Summoner(object):
    def __init__(self, string):
        self.__dict__ = string


class APIAddon(bpy.types.Operator):

    bl_idname = "mesh.apivisual"
    bl_label = "Generate something"
    bl_description = "Generate something from api"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
            return True

    def execute(self, context):
        #r = requests.get('https://github.com/timeline.json%27)
        #resp = r.json()
        #print(type(resp))
        #print(r.json())

        summonerName = "glucides"
        requestString = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}"
        header = {
        'X-Riot-Token' : 'RGAPI-73f1412f-8795-43ed-9085-ab748ff7e8f3',
        }

        resp = requests.get(requestString, headers=header)
        #print(resp.json())

        print("test")
        print(resp.json())

        s = Summoner(resp.json())

        print(f"id: {s.id}")

        requestChampionMasteryString = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{s.id}"
        resp = requests.get(requestChampionMasteryString, headers=header)
        print(resp.json())
        
        return {"FINISHED"}


register, unregister = bpy.utils.register_classes_factory({APIAddon})
