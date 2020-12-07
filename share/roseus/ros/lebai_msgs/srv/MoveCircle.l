;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::MoveCircle)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'MoveCircle (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::MOVECIRCLE")
  (make-package "LEBAI_MSGS::MOVECIRCLE"))
(unless (find-package "LEBAI_MSGS::MOVECIRCLEREQUEST")
  (make-package "LEBAI_MSGS::MOVECIRCLEREQUEST"))
(unless (find-package "LEBAI_MSGS::MOVECIRCLERESPONSE")
  (make-package "LEBAI_MSGS::MOVECIRCLERESPONSE"))

(in-package "ROS")

(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))




(defclass lebai_msgs::MoveCircleRequest
  :super ros::object
  :slots (_way_point_is_joint_pose _way_point_joint_pose _way_point_cartesian_pose _end_point_is_joint_pose _end_point_joint_pose _end_point_cartesian_pose _circle_angle _common _execute_mode ))

(defmethod lebai_msgs::MoveCircleRequest
  (:init
   (&key
    ((:way_point_is_joint_pose __way_point_is_joint_pose) nil)
    ((:way_point_joint_pose __way_point_joint_pose) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:way_point_cartesian_pose __way_point_cartesian_pose) (instance geometry_msgs::Pose :init))
    ((:end_point_is_joint_pose __end_point_is_joint_pose) nil)
    ((:end_point_joint_pose __end_point_joint_pose) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:end_point_cartesian_pose __end_point_cartesian_pose) (instance geometry_msgs::Pose :init))
    ((:circle_angle __circle_angle) 0.0)
    ((:common __common) (instance lebai_msgs::MoveCommon :init))
    ((:execute_mode __execute_mode) (instance lebai_msgs::ExecuteMode :init))
    )
   (send-super :init)
   (setq _way_point_is_joint_pose __way_point_is_joint_pose)
   (setq _way_point_joint_pose __way_point_joint_pose)
   (setq _way_point_cartesian_pose __way_point_cartesian_pose)
   (setq _end_point_is_joint_pose __end_point_is_joint_pose)
   (setq _end_point_joint_pose __end_point_joint_pose)
   (setq _end_point_cartesian_pose __end_point_cartesian_pose)
   (setq _circle_angle (float __circle_angle))
   (setq _common __common)
   (setq _execute_mode __execute_mode)
   self)
  (:way_point_is_joint_pose
   (&optional __way_point_is_joint_pose)
   (if __way_point_is_joint_pose (setq _way_point_is_joint_pose __way_point_is_joint_pose)) _way_point_is_joint_pose)
  (:way_point_joint_pose
   (&optional __way_point_joint_pose)
   (if __way_point_joint_pose (setq _way_point_joint_pose __way_point_joint_pose)) _way_point_joint_pose)
  (:way_point_cartesian_pose
   (&rest __way_point_cartesian_pose)
   (if (keywordp (car __way_point_cartesian_pose))
       (send* _way_point_cartesian_pose __way_point_cartesian_pose)
     (progn
       (if __way_point_cartesian_pose (setq _way_point_cartesian_pose (car __way_point_cartesian_pose)))
       _way_point_cartesian_pose)))
  (:end_point_is_joint_pose
   (&optional __end_point_is_joint_pose)
   (if __end_point_is_joint_pose (setq _end_point_is_joint_pose __end_point_is_joint_pose)) _end_point_is_joint_pose)
  (:end_point_joint_pose
   (&optional __end_point_joint_pose)
   (if __end_point_joint_pose (setq _end_point_joint_pose __end_point_joint_pose)) _end_point_joint_pose)
  (:end_point_cartesian_pose
   (&rest __end_point_cartesian_pose)
   (if (keywordp (car __end_point_cartesian_pose))
       (send* _end_point_cartesian_pose __end_point_cartesian_pose)
     (progn
       (if __end_point_cartesian_pose (setq _end_point_cartesian_pose (car __end_point_cartesian_pose)))
       _end_point_cartesian_pose)))
  (:circle_angle
   (&optional __circle_angle)
   (if __circle_angle (setq _circle_angle __circle_angle)) _circle_angle)
  (:common
   (&rest __common)
   (if (keywordp (car __common))
       (send* _common __common)
     (progn
       (if __common (setq _common (car __common)))
       _common)))
  (:execute_mode
   (&rest __execute_mode)
   (if (keywordp (car __execute_mode))
       (send* _execute_mode __execute_mode)
     (progn
       (if __execute_mode (setq _execute_mode (car __execute_mode)))
       _execute_mode)))
  (:serialization-length
   ()
   (+
    ;; bool _way_point_is_joint_pose
    1
    ;; float64[] _way_point_joint_pose
    (* 8    (length _way_point_joint_pose)) 4
    ;; geometry_msgs/Pose _way_point_cartesian_pose
    (send _way_point_cartesian_pose :serialization-length)
    ;; bool _end_point_is_joint_pose
    1
    ;; float64[] _end_point_joint_pose
    (* 8    (length _end_point_joint_pose)) 4
    ;; geometry_msgs/Pose _end_point_cartesian_pose
    (send _end_point_cartesian_pose :serialization-length)
    ;; float64 _circle_angle
    8
    ;; lebai_msgs/MoveCommon _common
    (send _common :serialization-length)
    ;; lebai_msgs/ExecuteMode _execute_mode
    (send _execute_mode :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _way_point_is_joint_pose
       (if _way_point_is_joint_pose (write-byte -1 s) (write-byte 0 s))
     ;; float64[] _way_point_joint_pose
     (write-long (length _way_point_joint_pose) s)
     (dotimes (i (length _way_point_joint_pose))
       (sys::poke (elt _way_point_joint_pose i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; geometry_msgs/Pose _way_point_cartesian_pose
       (send _way_point_cartesian_pose :serialize s)
     ;; bool _end_point_is_joint_pose
       (if _end_point_is_joint_pose (write-byte -1 s) (write-byte 0 s))
     ;; float64[] _end_point_joint_pose
     (write-long (length _end_point_joint_pose) s)
     (dotimes (i (length _end_point_joint_pose))
       (sys::poke (elt _end_point_joint_pose i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; geometry_msgs/Pose _end_point_cartesian_pose
       (send _end_point_cartesian_pose :serialize s)
     ;; float64 _circle_angle
       (sys::poke _circle_angle (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; lebai_msgs/MoveCommon _common
       (send _common :serialize s)
     ;; lebai_msgs/ExecuteMode _execute_mode
       (send _execute_mode :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _way_point_is_joint_pose
     (setq _way_point_is_joint_pose (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float64[] _way_point_joint_pose
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _way_point_joint_pose (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _way_point_joint_pose i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; geometry_msgs/Pose _way_point_cartesian_pose
     (send _way_point_cartesian_pose :deserialize buf ptr-) (incf ptr- (send _way_point_cartesian_pose :serialization-length))
   ;; bool _end_point_is_joint_pose
     (setq _end_point_is_joint_pose (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float64[] _end_point_joint_pose
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _end_point_joint_pose (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _end_point_joint_pose i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; geometry_msgs/Pose _end_point_cartesian_pose
     (send _end_point_cartesian_pose :deserialize buf ptr-) (incf ptr- (send _end_point_cartesian_pose :serialization-length))
   ;; float64 _circle_angle
     (setq _circle_angle (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; lebai_msgs/MoveCommon _common
     (send _common :deserialize buf ptr-) (incf ptr- (send _common :serialization-length))
   ;; lebai_msgs/ExecuteMode _execute_mode
     (send _execute_mode :deserialize buf ptr-) (incf ptr- (send _execute_mode :serialization-length))
   ;;
   self)
  )

(defclass lebai_msgs::MoveCircleResponse
  :super ros::object
  :slots (_ret ))

(defmethod lebai_msgs::MoveCircleResponse
  (:init
   (&key
    ((:ret __ret) nil)
    )
   (send-super :init)
   (setq _ret __ret)
   self)
  (:ret
   (&optional __ret)
   (if __ret (setq _ret __ret)) _ret)
  (:serialization-length
   ()
   (+
    ;; bool _ret
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _ret
       (if _ret (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _ret
     (setq _ret (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass lebai_msgs::MoveCircle
  :super ros::object
  :slots ())

(setf (get lebai_msgs::MoveCircle :md5sum-) "76aefbda84057bd81221aca855230727")
(setf (get lebai_msgs::MoveCircle :datatype-) "lebai_msgs/MoveCircle")
(setf (get lebai_msgs::MoveCircle :request) lebai_msgs::MoveCircleRequest)
(setf (get lebai_msgs::MoveCircle :response) lebai_msgs::MoveCircleResponse)

(defmethod lebai_msgs::MoveCircleRequest
  (:response () (instance lebai_msgs::MoveCircleResponse :init)))

(setf (get lebai_msgs::MoveCircleRequest :md5sum-) "76aefbda84057bd81221aca855230727")
(setf (get lebai_msgs::MoveCircleRequest :datatype-) "lebai_msgs/MoveCircleRequest")
(setf (get lebai_msgs::MoveCircleRequest :definition-)
      "bool way_point_is_joint_pose
float64[] way_point_joint_pose
geometry_msgs/Pose way_point_cartesian_pose
bool end_point_is_joint_pose
float64[] end_point_joint_pose
geometry_msgs/Pose end_point_cartesian_pose
float64 circle_angle
lebai_msgs/MoveCommon common
lebai_msgs/ExecuteMode execute_mode

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

================================================================================
MSG: lebai_msgs/MoveCommon
float64 vel
float64 acc
float64 time
bool is_continous_mode
# 0: normal move, 1: smooth move
uint8 continuation_type
# until data
bool until
lebai_msgs/UntilInfo until_info
================================================================================
MSG: lebai_msgs/UntilInfo
uint8 io_express_logic
lebai_msgs/IOConditionalExpress[] io_express

uint8 LOGIC_AND=0
uint8 LOGIC_OR=1


================================================================================
MSG: lebai_msgs/IOConditionalExpress
uint32 group
uint32 pin
uint32 type
float64 float_value
uint8 uint_value
uint8 logic_operation

uint8 GROUP_ROBOT=0
uint8 GROUP_FLANGE=1

uint8 TYPE_ANALOG=0
uint8 TYPE_DIGITAL=1

# great >
uint8 LOGIC_OP_GT=0
# great and equal >=
uint8 LOGIC_OP_GE=1
# equal
uint8 LOGIC_OP_EQ=2
# not equal
uint8 LOGIC_OP_NE=3
# less than
uint8 LOGIC_OP_LT=4
# less than and equal
uint8 LOGIC_OP_LE=5




================================================================================
MSG: lebai_msgs/ExecuteMode
uint8 data
uint8 EXECUTE_MODE_BUFFER=0
---
bool ret
")

(setf (get lebai_msgs::MoveCircleResponse :md5sum-) "76aefbda84057bd81221aca855230727")
(setf (get lebai_msgs::MoveCircleResponse :datatype-) "lebai_msgs/MoveCircleResponse")
(setf (get lebai_msgs::MoveCircleResponse :definition-)
      "bool way_point_is_joint_pose
float64[] way_point_joint_pose
geometry_msgs/Pose way_point_cartesian_pose
bool end_point_is_joint_pose
float64[] end_point_joint_pose
geometry_msgs/Pose end_point_cartesian_pose
float64 circle_angle
lebai_msgs/MoveCommon common
lebai_msgs/ExecuteMode execute_mode

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of position and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

================================================================================
MSG: lebai_msgs/MoveCommon
float64 vel
float64 acc
float64 time
bool is_continous_mode
# 0: normal move, 1: smooth move
uint8 continuation_type
# until data
bool until
lebai_msgs/UntilInfo until_info
================================================================================
MSG: lebai_msgs/UntilInfo
uint8 io_express_logic
lebai_msgs/IOConditionalExpress[] io_express

uint8 LOGIC_AND=0
uint8 LOGIC_OR=1


================================================================================
MSG: lebai_msgs/IOConditionalExpress
uint32 group
uint32 pin
uint32 type
float64 float_value
uint8 uint_value
uint8 logic_operation

uint8 GROUP_ROBOT=0
uint8 GROUP_FLANGE=1

uint8 TYPE_ANALOG=0
uint8 TYPE_DIGITAL=1

# great >
uint8 LOGIC_OP_GT=0
# great and equal >=
uint8 LOGIC_OP_GE=1
# equal
uint8 LOGIC_OP_EQ=2
# not equal
uint8 LOGIC_OP_NE=3
# less than
uint8 LOGIC_OP_LT=4
# less than and equal
uint8 LOGIC_OP_LE=5




================================================================================
MSG: lebai_msgs/ExecuteMode
uint8 data
uint8 EXECUTE_MODE_BUFFER=0
---
bool ret
")



(provide :lebai_msgs/MoveCircle "76aefbda84057bd81221aca855230727")


