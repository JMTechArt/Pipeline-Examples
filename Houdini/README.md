# Real-Time Houdini Simulation Examples
Below are some examples of Houdini simulations. These were created for real-time playback in Unity. However, I have since moved onto Unreal for such work.  
## FLIP Fluid Simulation
This is quite easily the most taxing simulations for real-time applications. While technically acheivable in Unity via Alembic exports out of Houdini, this type of simulation is rather large and playback performance is limiting. Unreal, on the otherhand, has a dedicated GPU-based solution for FLIP simulations that are currently available as a beta feature in Niagara system modules.

![Tab Image](./IMG/FLIP_Fluid_Sim.gif) 

## Rigid Body Interaction
The simplest form of real-time simulation. Everything is simulated in Houdini and then exported as a simple FBX animation and then transferred into Unity. In Unreal, this type of simulation can be made in Niagara since it has the ability to use physics in a controlled manner while Unity's VFX Graph does not.

![Tab Image](./IMG/RBD_Sim.gif) 

## Vellum Simulation and Footprint Displacement
Due to the lack of integration in Unity a custom file format was created to read in point position per frame via Python in Houdini. Unreal allows for efficient postion based dynamics in Niagara using a nearest neighbor algorhythm. The footprints are simulated in Houdini and then imported as an Alembic in this case.

![Tab Image](./IMG/Vellum_Sim.gif) 

## Plant Rigging for Interaction
A lot of foliage was rigged and then given special contraints in order to mimic the natural motion of plant branches. Rigging was automated using Houdini's KineFX system. Unreal potentially allows this kind of work to be done internally with the newer Control Rig toolset.

![Tab Image](./IMG/Plant_Rigging.gif) 

### Click to watch better quality video of the above examples:
[![Houdini Real-time Examples](https://vumbnail.com/940423123.jpg)](https://vimeo.com/940423123 "Omniverse Replicator Output Example - Click to Watch!")
