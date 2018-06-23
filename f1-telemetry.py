 #! /usr/bin/env python3

import socket
import time
import struct

# UDPPacket: 76 floats, followed by 24 bytes, followed by 1 float, followed by 5 bytes, followed by 20 CarUDPData structs, followed by 13 floats.
#
# struct UDPPacket
# {
#       float m_time;                     // [   0 +   4]
#       float m_lapTime;                  // [   4 +   4]
#       float m_lapDistance;              // [   8 +   4]
#       float m_totalDistance;            // [  12 +   4]
#       float m_x;                        // [  16 +   4] World space position
#       float m_y;                        // [  20 +   4] World space position
#       float m_z;                        // [  24 +   4] World space position
#       float m_speed;                    // [  28 +   4] Speed of car in MPH
#       float m_xv;                       // [  32 +   4] Velocity in world space
#       float m_yv;                       // [  36 +   4] Velocity in world space
#       float m_zv;                       // [  40 +   4] Velocity in world space
#       float m_xr;                       // [  44 +   4] World space right direction
#       float m_yr;                       // [  48 +   4] World space right direction
#       float m_zr;                       // [  52 +   4] World space right direction
#       float m_xd;                       // [  56 +   4] World space forward direction
#       float m_yd;                       // [  60 +   4] World space forward direction
#       float m_zd;                       // [  64 +   4] World space forward direction
#       float m_susp_pos[4];              // [  68 +  16] Note: All wheel arrays have the order:
#       float m_susp_vel[4];              // [  84 +  16] RL, RR, FL, FR
#       float m_wheel_speed[4];           // [ 100 +  16]
#       float m_throttle;                 // [ 116 +   4]
#       float m_steer;                    // [ 120 +   4]
#       float m_brake;                    // [ 124 +   4]
#       float m_clutch;                   // [ 128 +   4]
#       float m_gear;                     // [ 132 +   4]
#       float m_gforce_lat;               // [ 136 +   4]
#       float m_gforce_lon;               // [ 140 +   4]
#       float m_lap;                      // [ 144 +   4]
#       float m_engineRate;               // [ 148 +   4]
#       float m_sli_pro_native_support;   // [ 152 +   4] SLI Pro support
#       float m_car_position;             // [ 156 +   4] car race position
#       float m_kers_level;               // [ 160 +   4] kers energy left
#       float m_kers_max_level;           // [ 164 +   4] kers maximum energy
#       float m_drs;                      // [ 168 +   4] 0 = off, 1 = on
#       float m_traction_control;         // [ 172 +   4] 0 (off) - 2 (high)
#       float m_anti_lock_brakes;         // [ 176 +   4] 0 (off) - 1 (on)
#       float m_fuel_in_tank;             // [ 180 +   4] current fuel mass
#       float m_fuel_capacity;            // [ 184 +   4] fuel capacity
#       float m_in_pits;                  // [ 188 +   4] 0 = none, 1 = pitting, 2 = in pit area
#       float m_sector;                   // [ 192 +   4] 0 = sector1, 1 = sector2, 2 = sector3
#       float m_sector1_time;             // [ 196 +   4] time of sector1 (or 0)
#       float m_sector2_time;             // [ 200 +   4] time of sector2 (or 0)
#       float m_brakes_temp[4];           // [ 204 +  16] brakes temperature (centigrade)
#       float m_tyres_pressure[4];        // [ 220 +  16] tyres pressure PSI
#       float m_team_info;                // [ 236 +   4] team ID 
#       float m_total_laps;               // [ 240 +   4] total number of laps in this race
#       float m_track_size;               // [ 244 +   4] track size meters
#       float m_last_lap_time;            // [ 248 +   4] last lap time
#       float m_max_rpm;                  // [ 252 +   4] cars max RPM, at which point the rev limiter will kick in
#       float m_idle_rpm;                 // [ 256 +   4] cars idle RPM
#       float m_max_gears;                // [ 260 +   4] maximum number of gears
#       float m_sessionType;              // [ 264 +   4] 0 = unknown, 1 = practice, 2 = qualifying, 3 = race
#       float m_drsAllowed;               // [ 268 +   4] 0 = not allowed, 1 = allowed, -1 = invalid / unknown
#       float m_track_number;             // [ 272 +   4] -1 for unknown, 0-21 for tracks
#       float m_vehicleFIAFlags;          // [ 276 +   4] -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
#       float m_era;                      // [ 280 +   4] era, 2017 (modern) or 1980 (classic)
#       float m_engine_temperature;       // [ 284 +   4] engine temperature (centigrade)
#       float m_gforce_vert;              // [ 288 +   4] vertical g-force component
#       float m_ang_vel_x;                // [ 292 +   4] angular velocity x-component
#       float m_ang_vel_y;                // [ 296 +   4] angular velocity y-component
#       float m_ang_vel_z;                // [ 300 +   4] angular velocity z-component
#       byte  m_tyres_temperature[4];     // [ 304 +   4] tyres temperature (centigrade)
#       byte  m_tyres_wear[4];            // [ 308 +   4] tyre wear percentage
#       byte  m_tyre_compound;            // [ 312 +   1] compound of tyre – 0 = ultra soft, 1 = super soft, 2 = soft, 3 = medium, 4 = hard, 5 = inter, 6 = wet
#       byte  m_front_brake_bias;         // [ 313 +   1] front brake bias (percentage)
#       byte  m_fuel_mix;                 // [ 314 +   1] fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
#       byte  m_currentLapInvalid;        // [ 315 +   1] current lap invalid - 0 = valid, 1 = invalid
#       byte  m_tyres_damage[4];          // [ 316 +   4] tyre damage (percentage)
#       byte  m_front_left_wing_damage;   // [ 320 +   1] front left wing damage (percentage)
#       byte  m_front_right_wing_damage;  // [ 321 +   1] front right wing damage (percentage)
#       byte  m_rear_wing_damage;         // [ 322 +   1] rear wing damage (percentage)
#       byte  m_engine_damage;            // [ 323 +   1] engine damage (percentage)
#       byte  m_gear_box_damage;          // [ 324 +   1] gear box damage (percentage)
#       byte  m_exhaust_damage;           // [ 325 +   1] exhaust damage (percentage)
#       byte  m_pit_limiter_status;       // [ 326 +   1] pit limiter status – 0 = off, 1 = on
#       byte  m_pit_speed_limit;          // [ 327 +   1] pit speed limit in mph
#       float m_session_time_left;        // [ 328 +   4] NEW: time left in session in seconds 
#       byte  m_rev_lights_percent;       // [ 332 +   1] NEW: rev lights indicator (percentage)
#       byte  m_is_spectating;            // [ 333 +   1] NEW: whether the player is spectating
#       byte  m_spectator_car_index;      // [ 334 +   1] NEW: index of the car being spectated

#        // Car data

#       byte  m_num_cars;                 // [ 335 +   1] number of cars in data
#       byte  m_player_car_index;         // [ 336 +   1] index of player's car in the array
#       CarUDPData m_car_data[20];        // [ 337 + 900] data for all cars on track

#       float m_yaw;                      // [1237 +   4] NEW (v1.8)
#       float m_pitch;                    // [1241 +   4] NEW (v1.8)
#       float m_roll;                     // [1245 +   4] NEW (v1.8)
#       float m_x_local_velocity;         // [1249 +   4] NEW (v1.8) Velocity in local space
#       float m_y_local_velocity;         // [1253 +   4] NEW (v1.8) Velocity in local space
#       float m_z_local_velocity;         // [1257 +   4] NEW (v1.8) Velocity in local space
#       float m_susp_acceleration[4];     // [1261 +  16] NEW (v1.8) RL, RR, FL, FR
#       float m_ang_acc_x;                // [1277 +   4] NEW (v1.8) angular acceleration x-component
#       float m_ang_acc_y;                // [1281 +   4] NEW (v1.8) angular acceleration y-component
#       float m_ang_acc_z;                // [1285 +   4] NEW (v1.8) angular acceleration z-component
# };                                      // [1289      ]
#
#
# struct CarUDPData
# {
#       float m_worldPosition[3];         // [   0 +  12] world co-ordinates of vehicle
#       float m_lastLapTime;              // [  12 +   4]
#       float m_currentLapTime;           // [  16 +   4]
#       float m_bestLapTime;              // [  20 +   4]
#       float m_sector1Time;              // [  24 +   4]
#       float m_sector2Time;              // [  28 +   4]
#       float m_lapDistance;              // [  32 +   4]
#       byte  m_driverId;                 // [  36 +   1]
#       byte  m_teamId;                   // [  37 +   1]
#       byte  m_carPosition;              // [  38 +   1] UPDATED: track positions of vehicle
#       byte  m_currentLapNum;            // [  39 +   1]
#       byte  m_tyreCompound;             // [  40 +   1] compound of tyre – 0 = ultra soft, 1 = super soft, 2 = soft, 3 = medium, 4 = hard, 5 = inter, 6 = wet
#       byte  m_inPits;                   // [  41 +   1] 0 = none, 1 = pitting, 2 = in pit area
#       byte  m_sector;                   // [  42 +   1] 0 = sector1, 1 = sector2, 2 = sector3
#       byte  m_currentLapInvalid;        // [  43 +   1] current lap invalid - 0 = valid, 1 = invalid
#       byte  m_penalties;                // [  44 +   1] NEW: accumulated time penalties in seconds to be added
# };                                      // [  45      ]

packet_format_2017 = "<76f24B1f5B" + 20 * "9f9B" + "13f"

sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
try:
    # Allow multiple receiving endpoints...
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('', 20777)
    sock.bind(address)
    while True:
        (packet, address) = sock.recvfrom(2048)
        if len(packet) != 1289:
            print("Bad packet (length: {} bytes)".format(len(packet)))
            continue
            
        print("Received {!r} from {!r}".format(len(packet), address))

        packet = struct.unpack(packet_format_2017, packet)
        print(packet)
       
finally:
    sock.close()
