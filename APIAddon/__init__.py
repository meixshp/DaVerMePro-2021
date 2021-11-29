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
    "name": "APIAddon",
    "author": "Champions",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}


class account(object):
    def __init__(self,id,accountId,puuid,name,profileIconId,revisionDate,summonerLevel):
        self.id = id
        self.accountId = accountId
        self.puuid = puuid
        self.name = name
        self.profileIconId = profileIconId
        self.revisionDate = revisionDate
        self.summonerLevel = summonerLevel
    
class summoner(object):
    def __init__(self, championId, championLevel, championPoints, lastPlayTime, championPointsSinceLastLevel, championPointsUntilNextLevel, chestGranted, tokensEarned, summonerId ):
        self.championId = championId
        self.championLevel = championLevel
        self.championPoints = championPoints
        self.lastPlayTime = lastPlayTime
        self.championPointsSinceLastLevel = championPointsSinceLastLevel
        self.championPointsUntilNextLevel = championPointsUntilNextLevel
        self.chestGranted = chestGranted
        self.tokensEarned = tokensEarned
        self.summonerId = summonerId

class APIAddon(bpy.types.Operator):

    bl_idname = "mesh.apivisual"
    bl_label = "Visualise LOL-API"
    bl_description = "Generates meshes to visualise LOL-statistics"
    bl_info = {
        "name": "API Visualizer",
        "author": "Champions",
        "version": (1, 0),
        "blender": (2, 80, 0),
        "location": "Search menu",
        "description": "Generates meshes to visualise LOL-statistics",
        "warning": "",
        "wiki_url": "",
        "category": "Add Mesh",
    }
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # r = requests.get('https://github.com/timeline.json%27)
        #resp = r.json()
        # print(type(resp))
        # print(r.json())

        summonerName = "glucides"
        requestString = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}"
        header = {
            'X-Riot-Token': 'RGAPI-8224790b-11c8-4cf9-85fa-c6da6f120581',
        }

        resp = requests.get(requestString, headers=header)
        #print(resp.json())

        #print("help")
        #print(resp.json())
        #print("test")
        #resp.decode('utf-8')
        #summunor_dict = resp.json()
        #summunor_obj = Summoner(**summunor_dict)
        s = account(**resp.json())

        print(f"name: {s.name}")
        print(f"id: {s.id}")
        

        requestChampionMasteryString = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{s.id}"
        resp = requests.get(requestChampionMasteryString, headers=header)
        #print(resp.json())

        summoners = json.loads(resp.text)
        print(f"length of summoners: {len(summoners)}")


        for summoner in summoners:
            print(summoner['championId'])


        return {"FINISHED"}

def menu_func(self, context):
    self.layout.operator(APIAddon.bl_idname, icon="SELECT_EXTEND")

def register():
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    bpy.utils.register_class(APIAddon)
    
def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(APIAddon)
        
if __name__ == "__main__":
    register()