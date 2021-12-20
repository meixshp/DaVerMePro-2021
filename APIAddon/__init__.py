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
from bpy import context
import requests
import json
import random

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
    def __init__(self, id, accountId, puuid, name, profileIconId, revisionDate, summonerLevel):
        self.id = id
        self.accountId = accountId
        self.puuid = puuid
        self.name = name
        self.profileIconId = profileIconId
        self.revisionDate = revisionDate
        self.summonerLevel = summonerLevel


class summoner(object):
    def __init__(self, championId, championLevel, championPoints, lastPlayTime, championPointsSinceLastLevel, championPointsUntilNextLevel, chestGranted, tokensEarned, summonerId):
        self.championId = championId
        self.championLevel = championLevel
        self.championPoints = championPoints
        self.lastPlayTime = lastPlayTime
        self.championPointsSinceLastLevel = championPointsSinceLastLevel
        self.championPointsUntilNextLevel = championPointsUntilNextLevel
        self.chestGranted = chestGranted
        self.tokensEarned = tokensEarned
        self.summonerId = summonerId

class champ(object):
    def __init__(self, id,  name, points, ):
        self.id = id
        self.name = name
        self.points = points


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
    num: bpy.props.IntProperty(
        name="Cube Number",
        description="Defines the number of cubes",
        default=5)

    cube_size_min: bpy.props.FloatProperty(
        name="Min Cube Size",
        default=0.5)

    cube_size_max: bpy.props.FloatProperty(
        name="Max Cube Size",
        default=2.0)

    cube_color: bpy.props.FloatVectorProperty(
        name="My Vector",
        default=(0, 0, 1),
        subtype="COLOR")

    summoner_Name: bpy.props.StringProperty(
        name="Name of the Summoner",
        default="veryfirstghost")

    riot_Token: bpy.props.StringProperty(
        name="X-Riot-Token",
        default="RGAPI-694c54e5-0e3e-4173-80d4-a8a2afa5fe40")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # r = requests.get('https://github.com/timeline.json%27)
        #resp = r.json()
        # print(type(resp))
        # print(r.json())

        #if (self.riot_Token == ""):
        #    self.riot_Token = "RGAPI-694c54e5-0e3e-4173-80d4-a8a2afa5fe40"
        

        summonerName = f"{self.summoner_Name}"
        requestString = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}"
        header = {
            'X-Riot-Token': self.riot_Token,
        }

        resp = requests.get(requestString, headers=header)
        # print(resp.json())

        # print("help")
        # print(resp.json())
        # print("test")
        # resp.decode('utf-8')
        #summunor_dict = resp.json()
        #summunor_obj = Summoner(**summunor_dict)
        s = account(**resp.json())

        print(f"name: {s.name}")
        print(f"id: {s.id}")

        requestChampionMasteryString = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{s.id}"
        resp = requests.get(requestChampionMasteryString, headers=header)
        # print(resp.json())

        requestChampionNames = f"http://ddragon.leagueoflegends.com/cdn/11.20.1/data/en_US/champion.json"
        respNames = requests.get(requestChampionNames)
        # print(respNames.json())

        championInfo = json.loads(respNames.text)
        # print(championInfo)

        champions = json.loads(resp.text)
        print(f"length of summoners: {len(champions)}")

        bpy.ops.object.select_all(action='SELECT')  # selektiert alle Objekte
        # löscht selektierte objekte
        bpy.ops.object.delete(use_global=False, confirm=False)
        bpy.ops.outliner.orphans_purge()  # löscht überbleibende Meshdaten etc.

        mat = bpy.data.materials.new(name="Font Color")
        mat.diffuse_color = (0.7, 0.5, 1.0, 1.0)
        mat = bpy.data.materials['Font Color']

        i = 0
        # for y in range(2):
        for x in range(6):
            # for summoner in summoners:
            currentchamp = getCurrentChamp(self, championInfo, champions, i)

            createCube(self, context, x, currentchamp, mat)
            setNames(self, currentchamp, mat, x, i)

            # createCubeTower(self, context, currentchamp, champions, mat, i, x) #creates the tower of small cubes
            # print("help")
            print(currentchamp.name)

            print(f"i: {i}")
            print(f"ChPoints: {currentchamp.points}")
            print(f"ChId: {currentchamp.id}")
            print("")
            i += 1

        bpy.ops.mesh.primitive_plane_add(size=30)
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.type = 'PASSIVE'

        return {"FINISHED"}

def createCube(self, context, x, currentChamp, mat):
    scaleFac = currentChamp.points / 10000
    print(scaleFac)
    bpy.ops.mesh.primitive_cube_add(size=1,location=(x*7-17, 0, scaleFac/2), scale=(1,1,scaleFac))
    


def getCurrentChamp(self, championInfo, champions, i): 
    currentchamp = champ(0,"lol",21)
    for key in championInfo["data"]:
        # print(championInfo['data'][key]['id'])
        if str(championInfo['data'][key]['key']) == str(champions[i]["championId"]):
            currentchamp = champ(champions[i]['championId'],str(championInfo['data'][key]['name']), champions[i]['championPoints'])
            #print(currentchamp)
            break
    return currentchamp

def setNames(self, currentchamp, mat, x, i):
    bpy.data.curves.new(
        type="FONT", name=f"Font Curve{i}").body = currentchamp.name
    font_obj = bpy.data.objects.new(
        name=f"Font Object{i}", object_data=bpy.data.curves[f"Font Curve{i}"])
    bpy.context.scene.collection.objects.link(font_obj)
    font_obj.location = (x*7-17-1, -3, 0)
    font_obj.rotation_euler = (45, 0, 0)
    bpy.data.curves[f"Font Curve{i}"].materials.append(mat)
    
def createCubeTower(self,context, currentchamp, champions, mat, i, x): #creates the tower of small cubes with names in front
        total_height = 0
        rand_offset = 0.4


        for z in range(int(champions[i]['championPoints']/1000)):
            c_cube_size = random.uniform(
                self.cube_size_min, self.cube_size_max)

            bpy.ops.mesh.primitive_cube_add(
                location=(x*7-17, 0, total_height + c_cube_size/2), size=(c_cube_size))
            total_height += c_cube_size

            bpy.context.object.rotation_euler.z = random.uniform(0, 360)

            bpy.context.object.location.x += random.uniform(
                -c_cube_size*rand_offset, +c_cube_size*rand_offset)
            bpy.context.object.location.y += random.uniform(
                -c_cube_size*rand_offset, +c_cube_size*rand_offset)
            bpy.ops.rigidbody.object_add()
            bpy.context.object.color = (
                self.cube_color.r, self.cube_color.g, self.cube_color.b, random.uniform(0.5, 1))


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
