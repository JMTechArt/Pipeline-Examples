# Getting Started

1. Before installation make sure you have Blender 3.2 or later.
    - This can be found on [Blender.org's Download Page](https://www.blender.org/download/)

2. Open Blender and navigate to Edit>Preferences>Add-ons.
    - Click the Install button and navigate to the shared dropbox folder and find the .zip file in the 3D/Blender/Addon directory.
    - Install it by selecting the zip file and then make sure it is enabled. You will see a new tab in the 3D viewport with the "Simu_LanceStage" label.

3. In the same preferences window, click on the File Paths tab and add the following directory to the Asset Libraries section:
    - Search for the 'Blender Asset Libraries' folder in the main Dropbox directory on your local machine.
    - You can name it anything you want, but the directory address should be exact.

# Asset Browswer Workflow

1. Configure Blender's viewports any way you see fit as long as one is set to be the Asset Browser
    - If the Asset Library was correctly configured in preferences you should be able to switch from 'current file' to the asset library link you set up, it should have the name you have given it.

2. The two categories should be Lance Rigs and Knight Rigs. All that has to be done is to click and drag an asset into the scene.
3. For addon functionality purposes, make sure you disable the 'Instance' checkbox in the 'Add Collection' redo panel in the lower left of the 3D viewport. This only shows up once after dragging in a new asset. This configuration is remembered after it is disabled the very first time.
4. Enter Pose Mode on the rigs to animate if needed, but you will have to be in Object mode to drag in new assets every time.

# Add-on Workflow

1. Each lance rig has a circle with the name '0LanceStage_Controller' above everything else in the rig. To use the addon this needs to be selected and active(bright orange).
2. Simply change the settings for each lance as you see fit and press the update button. 
3. All needed textures are in the 3D/Blender/Textures directories. It is recommended that you create a bookmark for this location in the Blender file browser for faster changes. 
4. Skins are shared by all lances and weapons. Nose art textures are specific to each lance and are in their own specific folders.





