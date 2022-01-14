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

from multiprocessing.dummy import Array
import bpy
import requests
import json
import random
#import enum

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

""" class charts(enum):
    BARCHART = 1
    CAKECHART = 2 """


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
    """ num: bpy.props.IntProperty(
        name="Cube Number",
        description="Defines the number of cubes",
        default=5)

    cube_size_min: bpy.props.FloatProperty(
        name="Min Cube Size",
        default=0.5)

    cube_size_max: bpy.props.FloatProperty(
        name="Max Cube Size",
        default=2.0)  """

    number_of_Champs: bpy.props.IntProperty(
        name="Number of Champions",
        description="How many Champions should be displayed? From top to bottom.",
        default=6)


    cube_color: bpy.props.FloatVectorProperty(
        name="Color of the bars",
        description="Choose which color the bars have.",
        default=(0.096, 0.614, 1),
        subtype="COLOR")

    name_color: bpy.props.FloatVectorProperty(
        name="Color of the names",
        description="Choose which color the names have.",
        default=(0.7, 0.5, 1.0),
        subtype="COLOR")

    plane_color: bpy.props.FloatVectorProperty(
        name="Color of the floor",
        description="Choose which color the floor has.",
        default=(0.1, 0.1, 0.1),
        subtype="COLOR")


    summoner_Name: bpy.props.StringProperty(
        name="Name of the Summoner",
        description="Put your name which you are called in LOL here.",
        default="veryfirstghost"
    )

    riot_Token: bpy.props.StringProperty(
        name="X-Riot-Token",
        description="You need to generate a X-Riot-Token and put it here to get acces to the data.",
        default="RGAPI-8213e50a-2ba8-4091-8b25-0937f0696671"
    )

    type_of_chart: bpy.props.EnumProperty(
        items={
        ('Bar chart', 'Bar chart', 'Displays masterypoints in a Bar chart'),
        ('Pie chart', 'Pie chart', 'Displays winrate in a Pie chart')},
                
        name="Type of chart",
        description="Which type of chart do your want? Bar chart, Cake chart, ...",  
        default="Bar chart"
    )

    type_of_BarChart: bpy.props.IntProperty(
        name="Type of Bar chart",
        description="Which type of Bar chart do your want? 1 = cubes 2 = names 3 = cubetower.",  
        default=1,
        min=1,
        max=3
    )
    

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # r = requests.get('https://github.com/timeline.json%27)
        #resp = r.json()
        # print(type(resp))
        # print(r.json())

        summonerName = f"{self.summoner_Name}"
        requestString = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}"
        header = {
            'X-Riot-Token': self.riot_Token,
        }
        # puuid: _cXJlH3kUv3IMeizi3eCDmeTGkABlml-BIf3298QmsV2wqO-PluzmY6Y3cermq-BSVHwWW8f5Alt_Q

        resp = requests.get(requestString, headers=header)
        # print(resp.json())

        # print("help")
        # print(resp.json())
        # print("test")
        # resp.decode('utf-8')
        #summunor_dict = resp.json()
        #summunor_obj = Summoner(**summunor_dict)
        #try:
        s = account(**resp.json())

        #print(f"name: {s.name}")
        #print(f"id: {s.id}")

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

        """ match i:
            case 1:
                print("First case")
            case 2:
                print("Second case")
            case _:
                print("Didn't match a case") """

        ############# Bar Chart ###############
        if self.type_of_chart == "Bar chart": 
            print("Bar-Chart")    


            fontMat = bpy.data.materials.get("FontMaterial")
            if fontMat is None:
                # create material
                fontMat = bpy.data.materials.new(name="FontMaterial")

            fontMat.diffuse_color = (
                self.name_color.r, self.name_color.g, self.name_color.b, 1)
            fontMat = bpy.data.materials['FontMaterial']

            cubeMat = bpy.data.materials.get("CubeMaterial")
            if cubeMat is None:
                # create material
                cubeMat = bpy.data.materials.new(name="CubeMaterial")
            cubeMat.diffuse_color = (
                self.cube_color.r, self.cube_color.g, self.cube_color.b, 1)
            
            planeMat = bpy.data.materials.get("PlaneMaterial")
            if planeMat is None:
                # create material
                planeMat = bpy.data.materials.new(name="PlaneMaterial")
            planeMat.diffuse_color = (
                self.plane_color.r, self.plane_color.g, self.plane_color.b, 1)

            i = 1

            # for y in range(2):
            for x in range(self.number_of_Champs):
                # for champ in champs:

                currentchamp = getCurrentChamp(self, championInfo, champions, i)

                if self.type_of_BarChart == 1:
                    createCube(self, x, currentchamp, self.number_of_Champs, cubeMat)
                elif self.type_of_BarChart == 2:
                    createNameBars(self, i, currentchamp, self.number_of_Champs, cubeMat)
                elif self.type_of_BarChart == 3:
                    createCubeTower(self, currentchamp, self.number_of_Champs, i, cubeMat) #creates the tower of small cubes
                
                
                setNames(self, currentchamp, fontMat, i, self.number_of_Champs)
                
                # print("help")
                print(currentchamp.name)

                print(f"i: {i}")
                print(f"ChPoints: {currentchamp.points}")
                print(f"ChId: {currentchamp.id}")
                print("")
                i += 1

            bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
            bpy.context.object.dimensions = (2.5 + self.number_of_Champs*5, 7, 1)
            ob = bpy.context.active_object
            #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            #bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

            # Get material

            if ob.data.materials:
                # assign to 1st material slot
                ob.data.materials[0] = planeMat
            else:
                # no slots
                ob.data.materials.append(planeMat)
            #bpy.ops.transform.resize(value=(7+ self.number_of_Champs*2, 7, 1))
            bpy.ops.rigidbody.object_add()
            bpy.context.object.rigid_body.type = 'PASSIVE'
        
        ##############################################################
        elif self.type_of_chart == "Pie chart":
            print("Pie-Chart")    

            bpy.ops.mesh.primitive_cylinder_add(vertices=101,radius=4, depth=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

            ob = bpy.context.active_object
            mat = createMaterialPieChart(self,0.7,0.2)

            if ob.data.materials:
                # assign to 1st material slot
                ob.data.materials[0] = mat
            else:
                # no slots
                ob.data.materials.append(mat)


        #except:
        #    print("Riot-Token is probably too old or the summonerName is Wrong")
        #    self.report({'ERROR'}, 'Riot-Token is probably to old or the summonerName is Wrong.')

        return {"FINISHED"}

def createMaterialPieChart(self,winrate,looserate):
    material_PieChart = bpy.data.materials.new(name= "Material_PieChart")
    material_PieChart.use_nodes = True


    principled_node = material_PieChart.node_tree.nodes.get('Principled BSDF')
    material_PieChart.node_tree.nodes.remove(principled_node)


    material_out = material_PieChart.node_tree.nodes.get('Material Output')

    textCoor = material_PieChart.node_tree.nodes.new('ShaderNodeTexCoord')

    gradTex = material_PieChart.node_tree.nodes.new('ShaderNodeTexGradient')

    colorRamp = material_PieChart.node_tree.nodes.new('ShaderNodeValToRGB')

    DiffBSDF = material_PieChart.node_tree.nodes.new('ShaderNodeBsdfDiffuse')

    gradTex.gradient_type = 'RADIAL'


    colorRamp.color_ramp.interpolation = 'CONSTANT'

    colorRamp.color_ramp.elements.remove(colorRamp.color_ramp.elements[0])

    # Adding new color stop at location 0.100
    colorRamp.color_ramp.elements.new(winrate)
    colorRamp.color_ramp.elements.new(winrate+looserate)
    colorRamp.color_ramp.elements.new(1- winrate-looserate)

    # Setting the color for the stop that we recently created
    colorRamp.color_ramp.elements[0].color = (0,1,0,1) 
    colorRamp.color_ramp.elements[1].color = (1,0,0,1)
    colorRamp.color_ramp.elements[2].color = (0.6,0.6,0.6,1)


    link = material_PieChart.node_tree.links.new

    link(textCoor.outputs[3],gradTex.inputs[0])

    link(gradTex.outputs[0],colorRamp.inputs[0])

    link(colorRamp.outputs[0],DiffBSDF.inputs[0])

    link(colorRamp.outputs[0],DiffBSDF.inputs[0])

    link(DiffBSDF.outputs[0],material_out.inputs[0])

    return material_PieChart


def createCube(self, i, currentChamp, numberOfChamps, mat):
    scaleFac = currentChamp.points / 10000 * 3
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=(-((numberOfChamps)/2 * 5) + (i + 0.5)*5, 0, scaleFac/2), scale=(1, 1, scaleFac))
    bpy.context.object.color = (
        self.cube_color.r, self.cube_color.g, self.cube_color.b, random.uniform(0.5, 1))
    ob = bpy.context.active_object
    #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    #bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    # Get material

    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)


def createNameBars(self, i, currentchamp, numberOfChamps, mat):
    scaleFac = currentchamp.points / 10000 *3

    bpy.data.curves.new(
        type="FONT", name=f"Font Bars{i}").body = currentchamp.name 
    font_obj = bpy.data.objects.new(
        name=f"Font BarsObj{i}", object_data=bpy.data.curves[f"Font Bars{i}"])
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.context.scene.collection.objects.link(font_obj)

    font_obj.location = (-((numberOfChamps)/2 * 5) + (i-0.5)*5 + font_obj.dimensions.x/4, 0, 0)
    #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    font_obj.dimensions = (scaleFac, scaleFac/3, 1)
    bpy.data.objects[f"Font BarsObj{i}"].rotation_euler[0] = 1.5708
    bpy.data.objects[f"Font BarsObj{i}"].rotation_euler[1] = -1.5708
    #font_obj.rotation_quaternion = (1,1,1,45) 
    #font_obj.rotation_euler.y = 90

    bpy.data.curves[f"Font Bars{i}"].materials.append(mat)
    bpy.data.curves[f"Font Bars{i}"].extrude = 0.3


def setNames(self, currentchamp, mat, i, numberOfChamps):
    bpy.data.curves.new(
        type="FONT", name=f"Font Curve{i}").body = currentchamp.name
    font_obj = bpy.data.objects.new(
        name=f"Font Object{i}", object_data=bpy.data.curves[f"Font Curve{i}"])
    bpy.context.scene.collection.objects.link(font_obj)

    font_obj.location = ((- ((numberOfChamps)/2 * 5) +
                         (i-0.5)*5) - font_obj.dimensions.x/2, -3, 0)
    font_obj.rotation_euler = (45, 0, 0)

    bpy.data.curves[f"Font Curve{i}"].materials.append(mat)
    bpy.data.curves[f"Font Curve{i}"].extrude = 0.1


def getCurrentChamp(self, championInfo, champions, i):
    currentchamp = champ(0, "lol", 21)
    for key in championInfo["data"]:
        # print(championInfo['data'][key]['id'])
        if str(championInfo['data'][key]['key']) == str(champions[i]["championId"]):
            currentchamp = champ(champions[i]['championId'], str(
                championInfo['data'][key]['name']), champions[i]['championPoints'])
            # print(currentchamp)
            break
    return currentchamp


# creates the tower of small cubes with names in front
def createCubeTower(self, currentchamp, numberOfChamps, x, mat ):
    total_height = 0
    rand_offset = 0.4

    for z in range(int(currentchamp.points/1000)):
        #c_cube_size = random.uniform( self.cube_size_min, self.cube_size_max)
        c_cube_size = 1.5
        bpy.ops.mesh.primitive_cube_add(
            location=(-((numberOfChamps)/2 * 5) + (x-0.5)*5, 0, total_height + c_cube_size/2), size=(c_cube_size))
        total_height += c_cube_size

        bpy.context.object.rotation_euler.z = random.uniform(0, 360)

        bpy.context.object.location.x += random.uniform(
            -c_cube_size*rand_offset, +c_cube_size*rand_offset)
        bpy.context.object.location.y += random.uniform(
            -c_cube_size*rand_offset, +c_cube_size*rand_offset)
        bpy.ops.rigidbody.object_add()
        bpy.context.object.color = (
            self.cube_color.r, self.cube_color.g, self.cube_color.b, random.uniform(0.5, 1))
        ob = bpy.context.active_object
        #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        #bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        # Get material

        if ob.data.materials:
            # assign to 1st material slot
            ob.data.materials[0] = mat
        else:
            # no slots
            ob.data.materials.append(mat)


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
