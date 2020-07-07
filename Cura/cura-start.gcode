G28 ; home
G29 ; mesh bed leveling
G92 E0.0 ; reset extruder distance position
M211 S0 ; Disable software endtop to allow nozzel move to y=-1
G1 Y-1 F2500.0 ; go outside print area
M400 ; wait for complete
G1 Z30 F420 ; Raise Z
M400 ; wait for complete
M300 S440 P500 ; play sound
M0 S30 Clean nozzle then click to continue ; wait for user to clean nozzle
G1 Z0.3 F420.0 ; Lower Z
M400 ; wait for complete
G1 X60.0 E15.0 F1000.0 ; intro line
G1 X100.0 E21.5 F1000.0 ; intro line
M400 ; wait for complete
G1 Z2.0 F420 ; lift the extruder a bit
M400 ; wait for complete
G92 E0.0 ; reset extruder distance position
G1 Y0 ; move to Y0
M211 S1 ; re-enable software endstop