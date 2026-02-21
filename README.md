📚 Unigine Exporter Pro - Documentation
Version 2.1.0 (Stable)
📑 Table of Contents
1.	Introduction
2.	Installation
3.	Quick Start
4.	Interface
5.	Export Modes
6.	Material Settings
7.	Animation Settings
8.	Batch Export
9.	Unigine Project Structure
10.	Frequently Asked Questions
11.	Troubleshooting
12.	Hotkeys
13.	Tips and Recommendations
________________________________________
📖 Introduction
Unigine Exporter Pro is a professional Blender addon designed for exporting 3D models to the Unigine game engine. It supports batch export, materials, textures, and skeletal animation.
🌟 Key Features
•	✅ Batch export of multiple models at once
•	✅ PBR material export with textures
•	✅ Skeletal animation support
•	✅ Automatic .node file creation
•	✅ Intelligent texture copying
•	✅ Support for all major Unigine versions (2.14 – 2.20)
•	✅ Compatible with Blender 4.0+
________________________________________
📥 Installation
System Requirements
•	Blender: version 4.0 or higher
•	Unigine: version 2.14 – 2.20
•	OS: Windows 10/11, Linux, macOS
Step-by-Step Installation
1.	Download the addon
o	Obtain the ZIP archive unigine_exporter_pro.zip
2.	Install in Blender
o	Open Blender
o	Go to Edit → Preferences → Add-ons
o	Click the Install... button
o	Select the downloaded ZIP file
o	Click Install Add-on
3.	Activate the addon
o	In the addon search field, type "Unigine"
o	Find "Unigine Exporter Pro"
o	Check the box to enable it
4.	Verify installation
o	Open the 3D Viewport
o	Press the N key
o	Find the "Unigine" tab in the sidebar
________________________________________
🚀 Quick Start
Export Your First Model in 1 Minute
1.	Prepare your scene
o	Create or import a model in Blender
o	Ensure the model has materials and textures (optional)
2.	Configure the addon
o	In the Unigine panel, specify the path to your Unigine project
o	Enter a file name in the "Asset Name" field
o	Select "Single Model" export mode
3.	Export
o	Select the objects to export
o	Click the "EXPORT" button
4.	Result
o	The FBX file will appear in the data/meshes/ folder
o	Textures will be copied to data/textures/
o	Materials will be saved in data/materials/
o	A .node file will be created for placement in Unigine
________________________________________
🎨 Interface
Main Panel
text
┌─────────────────────────────────┐
│ Unigine Exporter Pro v2.1.0     │
│ ✅ Project OK                    │
├─────────────────────────────────┤
│ Export Mode                      │
│ ○ Single ○ Batch ○ Collection   │
├─────────────────────────────────┤
│ Project Settings                 │
│ [Project Path] ▾                 │
│ [Mesh Folder]   [Texture Folder] │
├─────────────────────────────────┤
│ Materials                        │
│ ☑ Export Materials               │
│   ☑ Copy Textures                │
│   [Texture Handling: BOTH] ▾     │
├─────────────────────────────────┤
│ Animation                        │
│ ✅ Armature detected              │
│ ☑ Export Animation               │
│   ☑ Bake Animation               │
│   [FPS: 24.0]                    │
│   Frames: 1-100                  │
├─────────────────────────────────┤
│ Options                          │
│ ☑ Export Selected Only           │
│ ☑ Create .node File              │
│ ☐ Verbose Output                 │
├─────────────────────────────────┤
│         [EXPORT] [Test]          │
└─────────────────────────────────┘
UI Element Descriptions
Section	Element	Description
Main	Project Path	Path to the root folder of your Unigine project
	Mesh Folder	Folder for meshes inside data/
	Texture Folder	Folder for textures inside data/
Export Mode	Single	Export one model with the specified name
	Batch	Export each selected object as a separate model
	Collection	Export each collection as a separate model
Materials	Export Materials	Enable/disable material export
	Copy Textures	Copy textures to the project
	Texture Handling	Method of texture processing
Animation	Export Animation	Enable/disable animation export
	Bake Animation	Bake animation into FBX
	FPS	Animation frame rate
Options	Export Selected Only	Export only selected objects
	Create .node File	Create a .node file for the model
	Verbose Output	Detailed console output
________________________________________
🔧 Export Modes
1. Single Mode
Exports all selected objects as a single model with the specified name.
Example:
•	Selected: character + weapon + armature
•	Asset Name: "Soldier"
•	Result: Soldier.fbx, Soldier.node
2. Batch Mode
Exports each selected mesh as a separate model.
Naming options:
•	Prefix + Object Name + Suffix + _Number
Example:
•	Selected: 3 meshes (Cube, Sphere, Cylinder)
•	Prefix: "char_"
•	Suffix: "_v2"
•	Auto Number: enabled (3 digits)
•	Result:
o	char_Cube_v2_001.fbx
o	char_Sphere_v2_002.fbx
o	char_Cylinder_v2_003.fbx
3. Collection Mode
Exports each collection as a separate model.
Example:
•	Collections: "Characters", "Props", "Environment"
•	Result:
o	Characters.fbx
o	Props.fbx
o	Environment.fbx
________________________________________
🎯 Material Settings
Texture Detection
The addon automatically detects texture types based on file names:
Type	Detected by
diffuse	diffuse, albedo, color, basecolor
normal	normal, nrm, nor
metallic	metallic, metal, _met
roughness	roughness, rough, gloss
specular	specular, spec
emission	emission, emissive, emit
ao	ao, ambient, occlusion
opacity	opacity, alpha, transparent
Texture Handling Modes
Mode	Description	When to use
BOTH	Copies textures to both .fbm and textures/	Recommended for most cases
FBM_ONLY	Only to .fbm (next to the FBX)	If you don't need separate .mat files
TEXTURES_ONLY	Only to textures/	If you import FBX manually
EMBED	Embeds textures inside the FBX	For portability as a single file
.mat File Structure
xml
<?xml version="1.0" encoding="utf-8"?>
<material version="2.0" guid="a1b2c3d4..." name="MyMaterial">
    <parameters>
        <texture name="diffuse">textures/diffuse.png</texture>
        <texture name="normal">textures/normal.png</texture>
        <texture name="metallic">textures/metallic.png</texture>
        <texture name="roughness">textures/roughness.png</texture>
    </parameters>
    <states>
        <state name="cull">back</state>
        <state name="blend">false</state>
        <state name="depth_test">true</state>
        <state name="depth_write">true</state>
    </states>
</material>
________________________________________
🎬 Animation Settings
Supported Formats
•	✅ Skeletal animation (via FBX)
•	✅ Baked animation
•	✅ Morph targets (shape keys)
Animation Export Settings
Parameter	Description	Recommendation
Bake Animation	Bakes animation into keyframes	Enable for complex rigs
FPS	Frame rate	24 for film, 30 for games
Frame Range	Automatically detected	Check before exporting
Structure for an Animated Model
text
data/
├── meshes/
│   ├── Character.fbx
│   ├── Character.fbm/
│   └── Character.node
├── materials/
│   └── Character.mat
└── textures/
    ├── diffuse.png
    ├── normal.png
    └── metallic.png
________________________________________
📦 Batch Export
Scenario 1: Export Multiple Characters
1.	Select all characters in the scene
2.	Choose "Batch Export" mode
3.	Configure naming:
o	Prefix: "char_"
o	Auto Number: enabled
4.	Click EXPORT
Result:
•	char_Paladin_001.fbx
•	char_Mage_002.fbx
•	char_Rogue_003.fbx
Scenario 2: Export by Collections
1.	Organize models into collections
2.	Choose "By Collection" mode
3.	Add a prefix if needed
4.	Click EXPORT
Result:
•	props_Weapons.fbx (Weapons collection)
•	props_Furniture.fbx (Furniture collection)
•	env_Buildings.fbx (Buildings collection)
________________________________________
📁 Unigine Project Structure
Recommended Structure
text
YourUnigineProject/
├── data/
│   ├── meshes/
│   │   ├── Model1.fbx
│   │   ├── Model1.fbm/          (textures for Unigine)
│   │   ├── Model1.mesh           (after conversion)
│   │   ├── Model1.node            (ready-to-place object)
│   │   └── ... (other models)
│   ├── materials/
│   │   ├── Material1.mat
│   │   ├── Material2.mat
│   │   └── ...
│   └── textures/
│       ├── diffuse1.png
│       ├── normal1.png
│       └── ...
└── ... (other Unigine folders)
What the Addon Creates
File	Purpose	Location
*.fbx	Geometry + animation	data/meshes/
*.fbx.fbm/	Textures for Unigine	data/meshes/
*.mat	Unigine materials	data/materials/
*.node	Ready-to-place object	data/meshes/
(textures)	Copied textures	data/textures/
________________________________________
❓ Frequently Asked Questions
Q: Why aren't my textures showing up in Unigine?
A: Check:
1.	Is Texture Handling set correctly? (BOTH recommended)
2.	Does the .fbm folder exist next to the FBX?
3.	Are you using complex node based materials in Blender?
Q: How do I export animation?
A:
1.	Select mesh + armature
2.	Ensure the Animation panel shows "✅ Armature detected"
3.	Enable "Export Animation"
4.	Set the FPS (usually 24 or 30)
5.	Export
Q: Why does batch export create extra files?
A: In BATCH mode, every selected mesh is exported. If you have duplicate or hidden meshes, they will also be exported. Use "Export Selected Only" and select only the objects you need.
Q: How can I change the texture path in .mat files?
A: In the addon settings, specify the desired folder in the "Texture Folder" field. The default is textures.
Q: Does the addon support non-English file names?
A: Yes, but using Latin characters is recommended for better compatibility with Unigine.
________________________________________
🔍 Troubleshooting
Error: "Project path does not exist"
Solution: Make sure the project path exists and contains a data folder.
Error during FBX export
Solution: Check:
•	No objects in the scene contain errors
•	Write permissions for the target folder
•	The FBX file is not opened by another program
Textures are not copied
Solution:
1.	Verify that "Copy Textures" is enabled
2.	Check that the texture paths are correct
3.	Try "EMBED" mode to embed textures
Animation is not exported
Solution:
1.	Ensure the armature is selected
2.	Verify that an animation exists in the Action Editor
3.	Enable "Bake Animation"
Addon not visible in Blender
Solution:
1.	Check the console for errors (Window → Toggle System Console)
2.	Reinstall the addon
3.	Verify your Blender version (4.0+ required)
________________________________________
⌨️ Hotkeys
Key	Action
N	Open/close the sidebar
Ctrl + Shift + U	Quick export with current settings
F3 → "Unigine"	Search for addon commands
________________________________________
💡 Tips and Recommendations
For optimal workflow
1.	Organize your scene
o	Use collections to group models
o	Give objects meaningful names
o	Remove unused materials
2.	Texture settings
o	Use descriptive file names (diffuse.png, normal.png)
o	Follow standard naming conventions for PBR
o	Avoid spaces and special characters
3.	Batch export
o	Check the statistics before exporting
o	Use prefixes/suffixes for better organization
o	Perform a test export with a single model first
4.	Performance
o	Optimize geometry before exporting
o	Use LOD for complex models
o	Keep texture sizes reasonable
Recommended Workflow
text
1. Prepare in Blender
   ↓
2. Configure paths in the addon
   ↓
3. Choose export mode
   ↓
4. Check statistics
   ↓
5. Test export one model
   ↓
6. Verify in Unigine
   ↓
7. Batch export all models
________________________________________
📝 Changelog
Version 2.1.0 (current)
•	✅ Batch export (Batch, Collection)
•	✅ Intelligent texture detection
•	✅ Animation support
•	✅ Automatic .node file creation
•	✅ Improved error handling
•	✅ Verbose mode for detailed logging
Version 2.0.0
•	✅ Complete code refactor
•	✅ Modular architecture
•	✅ Enhanced performance
Version 1.5.0
•	✅ Basic material support
•	✅ Texture copying
•	✅ Animation export
________________________________________
📞 Support
Report an Issue
If you encounter a bug or have suggestions:
1.	Check the Troubleshooting section
2.	Enable "Verbose Output" and save the log
3.	Describe the problem and attach the log
Useful Links
•	Unigine Documentation
•	Unigine Developer Forum
•	Blender API
________________________________________
🎉 Conclusion
Unigine Exporter Pro is a powerful tool that significantly speeds up the process of exporting models from Blender to Unigine. With batch export, intelligent texture handling, and animation support, you can focus on creativity rather than repetitive tasks.
Thank you for using the addon! 🚀

