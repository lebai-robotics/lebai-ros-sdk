;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::MoveJoint)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'MoveJoint (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::MOVEJOINT")
  (make-package "LEBAI_MSGS::MOVEJOINT"))
(unless (find-package "LEBAI_MSGS::MOVEJOINTREQUEST")
  (make-package "LEBAI_MSGS::MOVEJOINTREQUEST"))
(unless (find-package "LEBAI_MSGS::MOVEJOINTRESPONSE")
  (make-package "LEBAI_MSGS::MOVEJOINTRESPONSE"))

(in-package "ROS")

(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))




(defclass lebai_msgs::MoveJointRequest
  :super ros::object
  :slots (_is_joint_pose _joint_pose _cartesian_pose _common _execute_mode ))

(defmethod lebai_msgs::MoveJointRequest
  (:init
   (&key
    ((:is_joint_pose __is_joint_pose) nil)
    ((:joint_pose __joint_pose) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:cartesian_pose __cartesian_pose) (instance geometry_msgs::Pose :init))
    ((:common __common) (instance lebai_msgs::MoveCommon :init))
    ((:execute_mode __execute_mode) (instance lebai_msgs::ExecuteMode :init))
    )
   (send-super :init)
   (setq _is_joint_pose __is_joint_pose)
   (setq _joint_pose __joint_pose)
   (setq _cartesian_pose __cartesian_pose)
   (setq _common __common)
   (setq _execute_mode __execute_mode)
   self)
  (:is_joint_pose
   (&optional __is_joint_pose)
   (if __is_joint_pose (setq _is_joint_pose __is_joint_pose)) _is_joint_pose)
  (:joint_pose
   (&optional __joint_pose)
   (if __joint_pose (setq _joint_pose __joint_pose)) _joint_pose)
  (:cartesian_pose
   (&rest __cartesian_pose)
   (if (keywordp (car __cartesian_pose))
       (send* _cartesian_pose __cartesian_pose)
     (progn
       (if __cartesian_pose (setq _cartesian_pose (car __cartesian_pose)))
       _cartesian_pose)))
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
    ;; bool _is_joint_pose
    1
    ;; float64[] _joint_pose
    (* 8    (length _joint_pose)) 4
    ;; geometry_msgs/Pose _cartesian_pose
    (send _cartesian_pose :serialization-length)
    ;; lebai_msgs/MoveCommon _common
    (send _common :serialization-length)
    ;; lebai_msgs/ExecuteMode _execute_mode
    (send _execute_mode :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _is_joint_pose
       (if _is_joint_pose (write-byte -1 s) (write-byte 0 s))
     ;; float64[] _joint_pose
     (write-long (length _joint_pose) s)
     (dotimes (i (length _joint_pose))
       (sys::poke (elt _joint_pose i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; geometry_msgs/Pose _cartesian_pose
       (send _cartesian_pose :serialize s)
     ;; lebai_msgs/MoveCommon _common
       (send _common :serialize s)
     ;; lebai_msgs/ExecuteMode _execute_mode
       (send _execute_mode :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _is_joint_pose
     (setq _is_joint_pose (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; float64[] _joint_pose
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_pose (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_pose i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; geometry_msgs/Pose _cartesian_pose
     (send _cartesian_pose :deserialize buf ptr-) (incf ptr- (send _cartesian_pose :serialization-length))
   ;; lebai_msgs/MoveCommon _common
     (send _common :deserialize buf ptr-) (incf ptr- (send _common :serialization-length))
   ;; lebai_msgs/ExecuteMode _execute_mode
     (send _execute_mode :deserialize buf ptr-) (incf ptr- (send _execute_mode :serialization-length))
   ;;
   self)
  )

(defclass lebai_msgs::MoveJointResponse
  :super ros::object
  :slots (_ret ))

(defmethod lebai_msgs::MoveJointResponse
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

(defclass lebai_msgs::MoveJoint
  :super ros::object
  :slots ())

(setf (get lebai_msgs::MoveJoint :md5sum-) "d7ba5f85f827d398c331d4fd7812bf30")
(setf (get lebai_msgs::MoveJoint :datatype-) "lebai_msgs/MoveJoint")
(setf (get lebai_msgs::MoveJoint :request) lebai_msgs::MoveJointRequest)
(setf (get lebai_msgs::MoveJoint :response) lebai_msgs::MoveJointResponse)

(defmethod lebai_msgs::MoveJointRequest
  (:response () (instance lebai_msgs::MoveJointResponse :init)))

(setf (get lebai_msgs::MoveJointRequest :md5sum-) "d7ba5f85f827d398c331d4fd7812bf30")
(setf (get lebai_msgs::MoveJointRequest :datatype-) "lebai_msgs/MoveJointRequest")
(setf (get lebai_msgs::MoveJointRequest :definition-)
      "bool is_joint_pose
float64[] joint_pose
geometry_msgs/Pose cartesian_pose
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

(setf (get lebai_msgs::MoveJointResponse :md5sum-) "d7ba5f85f827d398c331d4fd7812bf30")
(setf (get lebai_msgs::MoveJointResponse :datatype-) "lebai_msgs/MoveJointResponse")
(setf (get lebai_msgs::MoveJointResponse :definition-)
      "bool is_joint_pose
float64[] joint_pose
geometry_msgs/Pose cartesian_pose
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



(provide :lebai_msgs/MoveJoint "d7ba5f85f827d398c331d4fd7812bf30")


