; ------------------- START GCODE -------------------
M201 X1000 Y1000 Z200 E6000 ; sets maximum accelerations, mm/sec^2
M203 X100 Y100 Z10 E120 ; sets maximum feedrates, mm/sec
M204 P1250 R1250 T1250 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
M205 X8.00 Y8.00 Z0.40 E1.50 ; sets the jerk limits, mm/sec
M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec
M107

M862.3 P "Weird Bear" ; printer model check
M862.1 P0.4 ; nozzle diameter check

G90 ; use absolute coordinates
M83 ; extruder relative mode
G21 ; set units to millimeters ; CURA

M117 Parking extruder


G28 X Y R5 ; raise Z by 5 then home XY



; then preheat (PRUSA SLICER ONLY)
M104 S{material_print_temperature_layer_0} ; set extruder temp
M140 S{material_bed_temperature_layer_0} ; set bed temp

; when the extruder tmp is high enough, home and move the extruder from the bed to avoid heating up the probe
M109 S{material_print_temperature_layer_0} ; wait for extruder temp
G28 ; Home
G0 X0 Y100 F2500 ; XY parking
M400 ;
G0 Z50 F420 ; Z parking
M400 ;

M190 S{material_bed_temperature_layer_0} ; wait for bed temp
M109 S{material_print_temperature_layer_0} ; wait for extruder temp

M400 ; wait for complete
M300 S440 P500 ; play sound
M0 S30 Wait for clean nozzle ; wait for user to clean nozzle
M400 ;

G28 ; home
G29 ; mesh bed leveling

G0 Z2 F420.0 ; Lower Z
G0 X250 Y-1 F2500.0 ; go outside print area
M400 ;
G0 Z0.3 F420.0 ;
G92 E0.0 ; reset extruder distance position
G1 X190.0 E9.0 F1000.0 ; intro line
G1 X130.0 E21.5 F1000.0 ; intro line

M400 ;
G0 Z2.0 F420 ; lift the extruder a bit
M400 ;
G0 Y0 ; move to Y0
M82 ; absolute extrusion mode ; CURA
G92 E0.0 ; reset extruder distance position
; --------------------------------------------------

; ------------------- STOP GCODE -------------------
M400 ; wait
G91 ; relative
G1 E-2 F300 ; retract
G0 Z5 F420
M221 S100
M104 S0 ; turn off temperature
M140 S0 ; turn off heatbed
M107 ; turn off fan
M400 ;
G90 ;
G0 X0 Y215 F3000 ; home X axis
M300 S440 P300 ; play sound
M300 S0 P100 ; mute
M300 S440 P300 ; play sound
M84 ; disable motors
; --------------------------------------------------