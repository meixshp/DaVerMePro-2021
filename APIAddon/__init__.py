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
import random
# import enum

bl_info = {
    "name": "API Visualizer",
    "author": "Champions",
    "description": "",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "location": "",
    "warning": "",
    "category": "Generic"
}

global scaleFac

class accountData(object):
    def __init__(self, puuid, gameName, tagLine):
        self.puuid = puuid
        self.gameName = gameName
        self.tagLine = tagLine


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
    bl_label = "LOL-API Visualizer"
    bl_description = "Generates meshes to visualise LOL-statistics"
    bl_info = {
        "name": "API Visualizer",
        "author": "Champions",
        "version": (1, 0),
        "blender": (2, 80, 0),
        "location": "Search menu",
        "description": "Generates meshes to visualise LOL-statistics",
        "warning": "",
        "wiki_url": "https://github.com/meixshp/DaVerMePro-2021",
        "category": "Add Mesh",
    }
    bl_options = {"REGISTER", "UNDO"}

    summoner_Name: bpy.props.StringProperty(
        name="Name of the Summoner",
        description="Put your name which you are called in LOL here.",
        default="HIDE ON SHROUD"
    )

    summoner_TagLine: bpy.props.StringProperty(
        name="Tagline of the Summoner",
        description="Put your tagline here, content following the hashtag (#).",
        default="EUW"
    )

    riot_Token: bpy.props.StringProperty(
        name="X-Riot-Token",
        description="You need to generate a X-Riot-Token and put it here to get acces to the data.",
        default="RGAPI-2879b46d-cf86-42a6-99bd-40c581c908eb"
    )

    type_of_chart: bpy.props.EnumProperty(
        items={
            ('BarChart', 'Bar-Chart', 'Displays masterypoints in a Bar chart'),
            ('PieChart', 'Pie-Chart', 'Displays winrate in a Pie chart'),
            ('RankDisplay', 'Display Rank', 'Displays Rank')},

        name="Type of chart",
        description="Which type of chart do your want? Bar chart, Cake chart, ...",
        default="BarChart"
    )

    type_of_Chart_Variant: bpy.props.EnumProperty(
        items={
            ('CubeBars', 'Cube-Bars', 'Bars out of tall cubes.'),
            ('NameBars', 'Name-Bars', 'Bars out of Names.'),
            ('CubeTowerBars', 'Cubetower-Bars', 'Bars out of many cubes which are rigged.')},

        name="Type of Bar chart",
        description="Which type of Bar chart do your want?",
        default=1,
    )

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

    scaleFac1: float = 0

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # r = requests.get('https://github.com/timeline.json%27)
        # resp = r.json()
        # print(type(resp))
        # print(r.json())

        summonerName = f"{self.summoner_Name}"
        summerTagline = f"{self.summoner_TagLine}"
        # requestString = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}"
        puuid = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summonerName}/{summerTagline}"

        header = {
            'X-Riot-Token': self.riot_Token,
        }
        # puuid: _cXJlH3kUv3IMeizi3eCDmeTGkABlml-BIf3298QmsV2wqO-PluzmY6Y3cermq-BSVHwWW8f5Alt_Q

        getPuuid = requests.get(puuid, headers=header)
        status = json.loads(getPuuid.text)
        #print(status)
        try:
            if (status["status"]["status_code"] == 403):
                print("You need to type in a valid Riot-Token.")
                self.report({'ERROR'}, 'You need to type in a valid Riot-Token.')
            else:
                print("An error occured. Please try again and reassure yourself that your inputs are correct.")
                self.report({'ERROR'}, 'An error occured. Please try again and reassure yourself that your inputs are correct.')
        except:
                idFromPuuid = accountData(**getPuuid.json())
                requestString = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{idFromPuuid.puuid}"
                resp = requests.get(requestString, headers=header)
                # print(resp.json())

                # print("help")
                # print(resp.json())
                # print("test")
                # resp.decode('utf-8')
                # summunor_dict = resp.json()
                # summunor_obj = Summoner(**summunor_dict)
                # try:
                s = account(**resp.json())

                # print(f"name: {s.name}")
                # print(f"id: {s.id}")

                requestChampionMasteryString = f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{s.id}"


                resp = requests.get(requestChampionMasteryString, headers=header)
                #print(resp.json())

                requestLeagueEntries= f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{s.id}"

                respEntries = requests.get(requestLeagueEntries, headers=header)
                # print(respEntries.text)

                requestChampionNames = f"http://ddragon.leagueoflegends.com/cdn/11.20.1/data/en_US/champion.json"
                respNames = requests.get(requestChampionNames)
                # print(respNames.json())

                championInfo = json.loads(respNames.text)
                # print(championInfo)

                champions = json.loads(resp.text)
                print(f"length of summoners: {len(champions)}")

                
                leagueEntries = json.loads(respEntries.text)
                # print(leagueEntries)

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
                if self.type_of_chart == "BarChart":
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

                    i = 0
                    masteryPointsMax = getCurrentChamp(self, championInfo, champions, 0).points
                    # for y in range(2):
                    try: 
                        for x in range(self.number_of_Champs):
                            # for champ in champs:

                            maxHeight = 40 # max Height of Bars
                            currentchamp = getCurrentChamp(
                                self, championInfo, champions, i)

                            if self.type_of_Chart_Variant == "CubeBars":
                                createCube(self, x, currentchamp,
                                        self.number_of_Champs, cubeMat, masteryPointsMax, maxHeight)
                            elif self.type_of_Chart_Variant == "NameBars":
                                createNameBars(self, i, currentchamp,
                                            self.number_of_Champs, cubeMat,masteryPointsMax, maxHeight)
                            elif self.type_of_Chart_Variant == "CubeTowerBars":
                                # creates the tower of small cubes
                                createCubeTower(self, currentchamp,
                                                self.number_of_Champs, i, cubeMat, masteryPointsMax, maxHeight)
                                self.report({'INFO'}, "Press play to see the tower crumble :)")

                            setNames(self, currentchamp, fontMat, i, self.number_of_Champs)
                            addScale(self, masteryPointsMax, maxHeight, self.number_of_Champs, fontMat)

                            # print("help")
                            print(currentchamp.name)

                            print(f"i: {i}")
                            print(f"ChPoints: {currentchamp.points}")
                            print(f"ChId: {currentchamp.id}")
                            print("")
                            i += 1
                    except: 
                        print(f"It seems there isn't enough data  for {self.number_of_Champs} champions to be displayed")
                        self.report({'ERROR'}, f"It seems there isn't enough data for {self.number_of_Champs} champions to be displayed")

                   

                    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
                    bpy.context.object.dimensions = (5 + self.number_of_Champs*5, 7, 1)
                    ob = bpy.context.active_object
                    # bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                    # bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

                    # Get material

                    if ob.data.materials:
                        # assign to 1st material slot
                        ob.data.materials[0] = planeMat
                    else:
                        # no slots
                        ob.data.materials.append(planeMat)
                    # bpy.ops.transform.resize(value=(7+ self.number_of_Champs*2, 7, 1))
                    bpy.ops.rigidbody.object_add()
                    bpy.context.object.rigid_body.type = 'PASSIVE'

                ########################## Pie Chart ####################################
                elif self.type_of_chart == "PieChart":
                    if respEntries.text != "[]":
                        print("Pie-Chart")
                        bpy.context.space_data.shading.type = 'MATERIAL'

                        print("var1")
                        bpy.ops.mesh.primitive_cylinder_add(
                            vertices=101, radius=4, depth=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                        ob = bpy.context.active_object
                        wins = leagueEntries[0]["wins"]
                        losses = leagueEntries[0]["losses"]
                        winrate =  wins/ (wins + losses) 
                        looserate = losses / (wins + losses)
                        print(f"wins: {wins} losses: {losses} winrate: {winrate} looserate: {looserate}")

                        # creates the material of the cylinder. 2nd parameter is the winrate, 3rd is the looserate
                        mat = createMaterialPieChart(self, winrate, looserate)

                        if ob.data.materials:
                            # assign to 1st material slot
                            ob.data.materials[0] = mat
                        else:
                            # no slots
                            ob.data.materials.append(mat)
                        
                    else:
                        self.report({'ERROR'}, 'It seems there are Data for your ranked games. You need to be placed in a rank for this to work.')   


                ########################## Rank Display ####################################
                elif self.type_of_chart == "RankDisplay":
                    if respEntries.text != "[]":
                        print("Rank Display")

                        ### Get Data ###

                        rank = leagueEntries[0]["rank"]
                        tier = leagueEntries[0]["tier"]

                        bpy.ops.mesh.primitive_plane_add(size=30, enter_editmode=False, align='WORLD', location=(0, 0, 30), rotation=(1.5708, 0, 0), scale=(1, 1, 1))

                        ob = bpy.context.active_object

                        mat = bpy.data.materials.new(name="Rank_Mat")
                        mat.use_nodes = True
                        bsdf = mat.node_tree.nodes["Principled BSDF"]
                        texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')

                        ############ Grade noch große Baustelle beim laden der Bilder ######################

                        #bpy.ops.image.open(filepath="C:\\Users\\Anwender\\OneDrive\\Documents\\Studium\\5. Semester\\Veranstalltung Datenverarbeitung in der Medienproduktion\\DaVerMePro-2021\\Pictures\\tft_regalia_gold.png", directory="C:\\Users\\Anwender\\OneDrive\\Documents\\Studium\\5. Semester\\Veranstalltung Datenverarbeitung in der Medienproduktion\\DaVerMePro-2021\\Pictures\\", files=[{"name":"tft_regalia_gold.png", "name":"tft_regalia_gold.png"}], show_multiview=False)
                        
                        #filepath=f"tft_regalia_{tier}.png"

                        #texImage.image = bpy.data.images.load(filepath, check_existing=False)
                        # Load a new image into the main database


                        #texImage.image = bpy.data.images.load(filepath=f"..\\Pictures\\tft_regalia_{tier}.png", relative_path = True)
                        texImage.image = bpy.data.images.load(filepath=f"C:\\Users\\Anwender\\OneDrive\\Documents\\Studium\\5. Semester\\Veranstalltung Datenverarbeitung in der Medienproduktion\\DaVerMePro-2021\\Pictures\\tft_regalia_{tier}.png")
                        #texImage.image = bpy.data.images.load("C:\\Users\\Anwender\\OneDrive\\Documents\\Studium\\5. Semester\\Veranstalltung Datenverarbeitung in der Medienproduktion\\DaVerMePro-2021\\Pictures\\tft_regalia_bronze.png")

                        ###################################################


                        mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

                        if ob.data.materials:
                            ob.data.materials[0] = mat
                        else:
                            ob.data.materials.append(mat)

                        fontMat = bpy.data.materials.get("FontMaterial")
                        if fontMat is None:
                            # create material
                            fontMat = bpy.data.materials.new(name="FontMaterial")

                        fontMat.diffuse_color = (
                            self.name_color.r, self.name_color.g, self.name_color.b, 1)
                        fontMat = bpy.data.materials['FontMaterial']


                        ### Display Name ###

                        bpy.data.curves.new(
                            type="FONT", name=f"Font Curve Name").body = self.summoner_Name
                        font_obj = bpy.data.objects.new(  name=f"Font Curve Name", object_data=bpy.data.curves[f"Font Curve Name"])
                        bpy.context.scene.collection.objects.link(font_obj)

                    
                        font_obj.rotation_euler[0] = 1.5708

                        font_obj.scale = (5,5,5)
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        font_obj.location = (-font_obj.dimensions.x/2, 0, 0)

                        bpy.data.curves[f"Font Curve Name"].materials.append(fontMat)
                        bpy.data.curves[f"Font Curve Name"].extrude = 0.1
                        font_obj.name = self.summoner_Name + "-Font"

                    

                        ### Display Tier ###


                        bpy.data.curves.new(
                            type="FONT", name=f"Font Curve Tier").body = tier
                        font_objTier = bpy.data.objects.new(  name=f"Font Curve Tier", object_data=bpy.data.curves[f"Font Curve Tier"])
                        bpy.context.scene.collection.objects.link(font_objTier)

                    
                        font_objTier.rotation_euler[0] = 1.5708

                        font_objTier.scale = (5,5,5)
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        font_objTier.location = (-font_objTier.dimensions.x/2, 0, 10)

                        bpy.data.curves[f"Font Curve Tier"].materials.append(fontMat)
                        bpy.data.curves[f"Font Curve Tier"].extrude = 0.1
                        font_objTier.name = tier + "-Font"

                        
                        
                        ### Display Rank ###

                        bpy.data.curves.new(
                            type="FONT", name=f"Font Curve Rank").body = rank
                        font_objRank = bpy.data.objects.new(  name=f"Font Curve Rank", object_data=bpy.data.curves[f"Font Curve Rank"])
                        bpy.context.scene.collection.objects.link(font_objRank)

                    
                        font_objRank.rotation_euler[0] = 1.5708

                        font_objRank.scale = (4,4,4)
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
                        font_objRank.location = (-font_objRank.dimensions.x, 0, 5)

                        bpy.data.curves[f"Font Curve Rank"].materials.append(fontMat)
                        bpy.data.curves[f"Font Curve Rank"].extrude = 0.1
                        font_objRank.name = rank + "-Font"

                    else:
                        self.report({'ERROR'}, 'It seems there are Data for your ranked games. You need to be placed in a rank for this to work.')   





        return {"FINISHED"}
    
    def draw(self, context):
        self.layout.use_property_split = True

        row1 = self.layout.row()
        row1.prop(self, "summoner_Name")

        row2 = self.layout.row()
        row2.prop(self, "summoner_TagLine")

        row3 = self.layout.row()
        row3.prop(self, "riot_Token")

        row4 = self.layout.row()
        row4.prop(self, "type_of_chart")

        


        if self.type_of_chart == "BarChart":
            row5 = self.layout.row()
            row5.prop(self, "type_of_Chart_Variant")

            row6 = self.layout.row()
            row6.prop(self, "number_of_Champs")
            
            row7 = self.layout.row()
            row7.prop(self, "cube_color")

            row8 = self.layout.row()
            row8.prop(self, "name_color")

            row9 = self.layout.row()
            row9.prop(self, "plane_color")  

            """ row5.enabled = True 
            row6.enabled = True
            row7.enabled = True
            row8.enabled = True
            row9.enabled = True """
        elif self.type_of_chart == "PieChart":
            """ row5.enabled = False
            row6.enabled = False
            row7.enabled = False
            row8.enabled = False
            row9.enabled = False """
        elif self.type_of_chart == "RankDisplay":
            row8 = self.layout.row()
            row8.prop(self, "name_color")


def createMaterialPieChart(self, winrate, looserate):
    material_PieChart = bpy.data.materials.new(name="Material_PieChart")
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
    colorRamp.color_ramp.elements.new(1 - winrate-looserate)

    # Setting the color for the stop that we recently created
    colorRamp.color_ramp.elements[0].color = (0, 1, 0, 1)
    colorRamp.color_ramp.elements[1].color = (1, 0, 0, 1)
    colorRamp.color_ramp.elements[2].color = (0.6, 0.6, 0.6, 1)

    link = material_PieChart.node_tree.links.new

    link(textCoor.outputs[3], gradTex.inputs[0])

    link(gradTex.outputs[0], colorRamp.inputs[0])

    link(colorRamp.outputs[0], DiffBSDF.inputs[0])

    link(colorRamp.outputs[0], DiffBSDF.inputs[0])

    link(DiffBSDF.outputs[0], material_out.inputs[0])

    return material_PieChart


def createCube(self, i, currentChamp, numberOfChamps, mat, masteryPointsMax, maxHeight):
    # maxHeight => 10 
    # currentChamp.points =>    
    
    scaleFac = maxHeight / masteryPointsMax * currentChamp.points

    #scaleFac = currentChamp.points / 10000 * 3
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=(-((numberOfChamps)/2 * 5) + (i + 0.5)*5, 0, scaleFac/2), scale=(1, 1, scaleFac))
    bpy.context.object.color = (
        self.cube_color.r, self.cube_color.g, self.cube_color.b, 1)
    ob = bpy.context.active_object

    ob.name = currentChamp.name + "-Bar"
    # bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    # bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    # Get material

    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)

def addScale( self, masteryPointsMax, maxHeight, numberOfChamps, mat):
    scaleString = f"{masteryPointsMax}"
    for x in range(numberOfChamps):
        scaleString += "__________" 
    bpy.data.curves.new(
        type="FONT", name=f"Scale Font").body = scaleString
    font_obj = bpy.data.objects.new(
        name=f"Scale Font", object_data=bpy.data.curves[f"Scale Font"])
    bpy.context.scene.collection.objects.link(font_obj)

    font_obj.location = (- ((numberOfChamps)/2 * 5) - 3 ,0, maxHeight)
    font_obj.rotation_euler[0] = 1.5708

    bpy.data.curves[f"Scale Font"].materials.append(mat)
    bpy.data.curves[f"Scale Font"].extrude = 0.1
    font_obj.name = "Scale-Font"


def createNameBars(self, i, currentChamp, numberOfChamps, mat, masteryPointsMax, maxHeight):
    scaleFac = maxHeight / masteryPointsMax * currentChamp.points

    bpy.data.curves.new(
        type="FONT", name=f"Font Bars{i}").body = currentChamp.name
    font_obj = bpy.data.objects.new(
        name=f"Font BarsObj{i}", object_data=bpy.data.curves[f"Font Bars{i}"])
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.context.scene.collection.objects.link(font_obj)

    font_obj.location = (-((numberOfChamps)/2 * 5) + (i+0.5)
                         * 5 + font_obj.dimensions.x/4, 0, 0)
    # bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    font_obj.dimensions = (scaleFac, 2, 1)
    bpy.data.objects[f"Font BarsObj{i}"].rotation_euler[0] = 1.5708
    bpy.data.objects[f"Font BarsObj{i}"].rotation_euler[1] = -1.5708
    # font_obj.rotation_quaternion = (1,1,1,45)
    # font_obj.rotation_euler.y = 90

    bpy.data.curves[f"Font Bars{i}"].materials.append(mat)
    bpy.data.curves[f"Font Bars{i}"].extrude = 0.3
    font_obj.name = currentChamp.name + "-Bar"


def setNames(self, currentChamp, mat, i, numberOfChamps):
    bpy.data.curves.new(
        type="FONT", name=f"Font Curve{i}").body = currentChamp.name
    font_obj = bpy.data.objects.new(
        name=f"Font Object{i}", object_data=bpy.data.curves[f"Font Curve{i}"])
    bpy.context.scene.collection.objects.link(font_obj)

    font_obj.location = ((- ((numberOfChamps)/2 * 5) +
                         (i+0.5)*5) - font_obj.dimensions.x/2, -3, 0)
    font_obj.rotation_euler = (45, 0, 0)

    bpy.data.curves[f"Font Curve{i}"].materials.append(mat)
    bpy.data.curves[f"Font Curve{i}"].extrude = 0.1
    font_obj.name = currentChamp.name + "-Font"


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
def createCubeTower(self, currentChamp, numberOfChamps, x, mat, masteryPointsMax, maxHeight):

    height = maxHeight / masteryPointsMax * currentChamp.points
    total_height = 0
    rand_offset = 0.4

    for z in range(int(height*(5/3))):
        # c_cube_size = random.uniform( self.cube_size_min, self.cube_size_max)
        c_cube_size = 1*(3/5)
        bpy.ops.mesh.primitive_cube_add(
            location=(-((numberOfChamps)/2 * 5) + (x+0.5)*5, 0, total_height + c_cube_size/2), size=(c_cube_size))
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
        # bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        # bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

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
