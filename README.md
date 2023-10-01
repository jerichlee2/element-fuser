# element-fuser

### What is it?
* ElementFuser is a program for engineers to be able to take dimensions of a fuse body
and generate codes for manufacturing these Elements to the specific dimensions of the body.

### Why?
* Engineers are often using the same body element dimensions over and over again (due to
constant height of fuse bodies), but changing the offsets to accommodate for the change
in body radius. Instead of rewriting the code for the elements over and over again,
this program grabs existing codes and allows the engineer to easily modify it for a new
body.

### Features:

* Ability to import sheet of codes and directly modify a row and each bend
* Ability to take any two codes and combine them to generate new code
* Exports codes to another sheet
* Ability to directly edit elements at specific locations, symmetry rules apply

### Flowchart:
* Given body, clearance, bridges, and legs, generate GCODE for an element
* Using the GCODE, generate a 3D model for the element
* Using the 3D model, perform mechanical analyses on it (thermal, structural)
* Extrapolate the data for expected voltage, amperage, stress distribution,
temperature distribution, watt loss to easy to read format for engineers and technicians

![image](https://github.com/jerich931/element-fuser/assets/139656538/747c7039-c3f2-4ad6-b739-aa3ec2f607bb)
