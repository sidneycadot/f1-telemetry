
# See:
#
#     http://forums.codemasters.com/discussion/53139/f1-2017-d-box-and-udp-output-specification

import numpy as np

F1_2017_CarUDPData = np.dtype([
    ('m_worldPosition'           , np.float32, ( 3, )),
    ('m_lastLapTime'             , np.float32        ),
    ('m_currentLapTime'          , np.float32        ),
    ('m_bestLapTime'             , np.float32        ),
    ('m_sector1Time'             , np.float32        ),
    ('m_sector2Time'             , np.float32        ),
    ('m_lapDistance'             , np.float32        ),
    ('m_driverId'                , np.uint8          ),
    ('m_teamId'                  , np.uint8          ),
    ('m_carPosition'             , np.uint8          ),
    ('m_currentLapNum'           , np.uint8          ),
    ('m_tyreCompound'            , np.uint8          ),
    ('m_inPits'                  , np.uint8          ),
    ('m_sector'                  , np.uint8          ),
    ('m_currentLapInvalid'       , np.uint8          ),
    ('m_penalties'               , np.uint8          )
])

F1_2017_UDPPacket = np.dtype([
    ('m_time'                    , np.float32        ),
    ('m_lapTime'                 , np.float32        ),
    ('m_lapDistance'             , np.float32        ),
    ('m_totalDistance'           , np.float32        ),

    ('m_x'                       , np.float32        ),
    ('m_y'                       , np.float32        ),
    ('m_z'                       , np.float32        ),
    ('m_speed'                   , np.float32        ),
    ('m_xv'                      , np.float32        ),
    ('m_yv'                      , np.float32        ),
    ('m_zv'                      , np.float32        ),
    ('m_xr'                      , np.float32        ),
    ('m_yr'                      , np.float32        ),
    ('m_zr'                      , np.float32        ),
    ('m_xd'                      , np.float32        ),
    ('m_yd'                      , np.float32        ),
    ('m_zd'                      , np.float32        ),

    ('m_susp_pos'                , np.float32, ( 4, )),
    ('m_susp_vel'                , np.float32, ( 4, )),
    ('m_wheel_speed'             , np.float32, ( 4, )),

    ('m_throttle'                , np.float32        ),
    ('m_steer'                   , np.float32        ),
    ('m_brake'                   , np.float32        ),
    ('m_clutch'                  , np.float32        ),
    ('m_gear'                    , np.float32        ),
    ('m_gforce_lat'              , np.float32        ),
    ('m_gforce_lon'              , np.float32        ),
    ('m_lap'                     , np.float32        ),
    ('m_engineRate'              , np.float32        ),
    ('m_sli_pro_native_support'  , np.float32        ),
    ('m_car_position'            , np.float32        ),
    ('m_kers_level'              , np.float32        ),
    ('m_kers_max_level'          , np.float32        ),
    ('m_drs'                     , np.float32        ),
    ('m_traction_control'        , np.float32        ),
    ('m_anti_lock_brakes'        , np.float32        ),
    ('m_fuel_in_tank'            , np.float32        ),
    ('m_fuel_capacity'           , np.float32        ),
    ('m_in_pits'                 , np.float32        ),
    ('m_sector'                  , np.float32        ),
    ('m_sector1_time'            , np.float32        ),
    ('m_sector2_time'            , np.float32        ),

    ('m_brakes_temp'             , np.float32, ( 4, )),
    ('m_tyres_pressure'          , np.float32, ( 4, )),

    ('m_team_info'               , np.float32        ),
    ('m_total_laps'              , np.float32        ),
    ('m_track_size'              , np.float32        ),
    ('m_last_lap_time'           , np.float32        ),
    ('m_max_rpm'                 , np.float32        ),
    ('m_idle_rpm'                , np.float32        ),
    ('m_max_gears'               , np.float32        ),
    ('m_sessionType'             , np.float32        ),
    ('m_drsAllowed'              , np.float32        ),
    ('m_track_number'            , np.float32        ),
    ('m_vehicleFIAFlags'         , np.float32        ),
    ('m_era'                     , np.float32        ),
    ('m_engine_temperature'      , np.float32        ),
    ('m_gforce_vert'             , np.float32        ),
    ('m_ang_vel_x'               , np.float32        ),
    ('m_ang_vel_y'               , np.float32        ),
    ('m_ang_vel_z'               , np.float32        ),

    ('m_tyres_temperature'       , np.uint8,   ( 4, )),
    ('m_tyres_wear'              , np.uint8,   ( 4, )),

    ('m_tyre_compound'           , np.uint8          ),
    ('m_front_brake_bias'        , np.uint8          ),
    ('m_fuel_mix'                , np.uint8          ),
    ('m_currentLapInvalid'       , np.uint8          ),

    ('m_tyres_damage'            , np.uint8,   ( 4, )),

    ('m_front_left_wing_damage'  , np.uint8          ),
    ('m_front_right_wing_damage' , np.uint8          ),
    ('m_rear_wing_damage'        , np.uint8          ),
    ('m_engine_damage'           , np.uint8          ),
    ('m_gear_box_damage'         , np.uint8          ),
    ('m_exhaust_damage'          , np.uint8          ),
    ('m_pit_limiter_status'      , np.uint8          ),
    ('m_pit_speed_limit'         , np.uint8          ),

    ('m_session_time_left'       , np.float32        ),

    ('m_rev_lights_percent'      , np.uint8          ),
    ('m_is_spectating'           , np.uint8          ),
    ('m_spectator_car_index'     , np.uint8          ),

    ('m_num_cars'                , np.uint8          ),
    ('m_player_car_index'        , np.uint8          ),
    ('m_car_data'                , F1_2017_CarUDPData, (20, )),

    ('m_yaw'                     , np.float32        ),
    ('m_pitch'                   , np.float32        ),
    ('m_roll'                    , np.float32        ),
    ('m_x_local_velocity'        , np.float32        ),
    ('m_y_local_velocity'        , np.float32        ),
    ('m_z_local_velocity'        , np.float32        ),

    ('m_susp_acceleration'       , np.float32, ( 4, )),

    ('m_ang_acc_x'               , np.float32        ),
    ('m_ang_acc_y'               , np.float32        ),
    ('m_ang_acc_z'               , np.float32        )
])