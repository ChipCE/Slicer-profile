; ------------------- START GCODE -------------------
M201 X1000 Y1000 Z200 E6000 ; sets maximum accelerations, mm/sec^2
M203 X100 Y100 Z10 E120 ; sets maximum feedrates, mm/sec
M204 P1250 R1250 T1250 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
M205 X8.00 Y8.00 Z0.40 E1.50 ; sets the jerk limits, mm/sec
M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec
M107

M862.3 P "MK3" ; printer model check
M862.1 P0.4 ; nozzle diameter check
G90 ; use absolute coordinates
M83 ; extruder relative mode
G21 ; set units to millimeters ; CURA

M117 Parking extruder
G28 W ; home all without mesh bed level
M400 ;
G0 Z50 F1000 ; Z parking
M400 ;
G0 X0 Y100 F2500 ; XY parking
M400 ;


; then preheat (PRUSA SLICER ONLY)
M104 S{material_print_temperature_layer_0} ; set extruder temp
M140 S{material_bed_temperature_layer_0} ; set bed temp
M190 S{material_bed_temperature_layer_0} ; wait for bed temp
M109 S{material_print_temperature_layer_0} ; wait for extruder temp

M400 ;
M300 S440 P500 ; play sound
M0 S30 Wait for clean nozzle ; wait for user to clean nozzle
M400 ;

G28 W ; home all without mesh bed level
G80 ; mesh bed leveling

G0 Y-3.0 F1000.0 ; go outside print area
G92 E0.0
G1 X60.0 E9.0 F1000.0 ; intro line
G1 X100.0 E12.5 F1000.0 ; intro line
M82 ; absolute extrusion mode ; CURA
G92 E0.0
M221 S95
; --------------------------------------------------

; ------------------- STOP GCODE -------------------
G4 ; wait
M221 S100
M104 S0 ; turn off temperature
M140 S0 ; turn off heatbed
M107 ; turn off fan
;{if layer_z < max_print_height}G1 Z{z_offset+min(layer_z+30, max_print_height)}{endif} ; Move print head up
G0 X0 Y200 F2500 ; home X axis
M300 S440 P300 ; play sound
M300 S0 P100 ; mute
M300 S440 P300 ; play sound
M84 ; disable motors
; --------------------------------------------------