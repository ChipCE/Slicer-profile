; ------------------- START GCODE -------------------
M862.3 P "[printer_model]" ; printer model check
G90 ; use absolute coordinates
M83 ; extruder relative mode

M117 Parking extruder
G28 ; Home
G1 X0 Y100 F2500 ; XY parking
M400 ;
G1 Z50 F420 ; Z parking
M400 ;

; then preheat (PRUSA SLICER ONLY)
M104 S[first_layer_temperature] ; set extruder temp
M140 S[first_layer_bed_temperature] ; set bed temp
M190 S[first_layer_bed_temperature] ; wait for bed temp
M109 S[first_layer_temperature] ; wait for extruder temp

M400 ; wait for complete
M300 S440 P500 ; play sound
M0 S30 Wait for clean nozzle ; wait for user to clean nozzle
M400 ;

G28 ; home
G29 ; mesh bed leveling

M211 S0 ; Disable software endtop to allow nozzel move to y=-1
G1 Y-1 F2500.0 ; go outside print area
M400 ;
G1 Z0.3 F420.0 ; Lower Z
M400 ;
G92 E0.0 ; reset extruder distance position
G1 X190.0 E9.0 F1000.0 ; intro line
G1 X150.0 E21.5 F1000.0 ; intro line

M400 ;
G1 Z2.0 F420 ; lift the extruder a bit
M400 ;
G1 Y0 ; move to Y0
M211 S1 ; re-enable software endstop
G92 E0.0 ; reset extruder distance position



; ------------------- STOP GCODE -------------------
G4 ; wait
M221 S100
M104 S0 ; turn off temperature
M140 S0 ; turn off heatbed
M107 ; turn off fan
M400 ;
{if layer_z < max_print_height}G1 Z{z_offset+min(layer_z+30, max_print_height)}{endif} F420; Move print head up
M400 ;
G1 X0 Y215 F3000 ; home X axis
M300 S440 P300 ; play sound
M300 S0 P100 ; mute
M300 S440 P300 ; play sound
M84 ; disable motors