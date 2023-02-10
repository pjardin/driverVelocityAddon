

#!/usr/bin/python
# -*- coding: utf-8 -*-
bl_info = {
    "name": "Velocity Driver",
    "description": "adds velocity functions to the drivers",
    "author": "Pascal Jardin",
    "version": (0, 0, 0),
    "blender": (3, 4, 1),
    "location": "drivers",
    "warning": "use at your own risk", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

import bpy
from bpy.app.handlers import persistent

velocityObjects = {}

#https://blender.stackexchange.com/questions/281308/how-to-calculate-speed-detect-movement-per-frame
def createVelocity(name, frame, var):
    velocityObject = []
  
    if name in velocityObjects:
        velocityObject = velocityObjects[name]
    else:
        # Not found - create a new record for it and store it
        velocityObject = [{'frame':frame, 'value':var}]
        velocityObjects[name] = velocityObject


    found = False 
    for vo in velocityObjects[name]:
        if vo["frame"] == frame: 
            found = True
            break
        
    if found == False:
        velocityObjects[name].append( {'frame':frame, 'value':var} )
        
    velocity = 0
        
    if len(velocityObjects[name]) > 2: 
        del velocityObjects[name][0]
        
    if len(velocityObjects[name]) >= 2:
        

        frameDif = velocityObjects[name][1]["frame"] - velocityObjects[name][0]["frame"]
        posDif = velocityObjects[name][1]["value"] - velocityObjects[name][0]["value"]
        
        
        if posDif != 0 and frameDif !=0:
            velocity = posDif / frameDif

    return velocity
  

def getVelocity(name):
    velocity = 0
        
    if name in velocityObjects and len(velocityObjects[name]) >= 2:
        
        frameDif = velocityObjects[name][1]["frame"] - velocityObjects[name][0]["frame"]
        posDif = velocityObjects[name][1]["value"] - velocityObjects[name][0]["value"]
        
        if posDif != 0 and frameDif !=0:
            velocity = posDif / frameDif

    return velocity

#https://blender.stackexchange.com/questions/71305/how-to-make-an-addon-with-custom-driver-function

@persistent
def load_handler(dummy):
    if 'createVelocity' in bpy.app.driver_namespace:
        del bpy.app.driver_namespace['createVelocity']
    bpy.app.driver_namespace['createVelocity'] = createVelocity

    if 'getVelocity' in bpy.app.driver_namespace:
        del bpy.app.driver_namespace['getVelocity']
    bpy.app.driver_namespace['getVelocity'] = getVelocity

def register():
    load_handler(None)
    bpy.app.handlers.load_post.append(load_handler)

def unregister():
    bpy.app.handlers.load_post.remove(load_handler)
    if 'createVelocity' in bpy.app.driver_namespace:
        del bpy.app.driver_namespace['createVelocity']

    if 'getVelocity' in bpy.app.driver_namespace:
        del bpy.app.driver_namespace['getVelocity']

if __name__ == "__main__":
    register()
