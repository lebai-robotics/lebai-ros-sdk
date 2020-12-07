; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-srv)


;//! \htmlinclude MoveCircle-request.msg.html

(cl:defclass <MoveCircle-request> (roslisp-msg-protocol:ros-message)
  ((way_point_is_joint_pose
    :reader way_point_is_joint_pose
    :initarg :way_point_is_joint_pose
    :type cl:boolean
    :initform cl:nil)
   (way_point_joint_pose
    :reader way_point_joint_pose
    :initarg :way_point_joint_pose
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (way_point_cartesian_pose
    :reader way_point_cartesian_pose
    :initarg :way_point_cartesian_pose
    :type geometry_msgs-msg:Pose
    :initform (cl:make-instance 'geometry_msgs-msg:Pose))
   (end_point_is_joint_pose
    :reader end_point_is_joint_pose
    :initarg :end_point_is_joint_pose
    :type cl:boolean
    :initform cl:nil)
   (end_point_joint_pose
    :reader end_point_joint_pose
    :initarg :end_point_joint_pose
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (end_point_cartesian_pose
    :reader end_point_cartesian_pose
    :initarg :end_point_cartesian_pose
    :type geometry_msgs-msg:Pose
    :initform (cl:make-instance 'geometry_msgs-msg:Pose))
   (circle_angle
    :reader circle_angle
    :initarg :circle_angle
    :type cl:float
    :initform 0.0)
   (common
    :reader common
    :initarg :common
    :type lebai_msgs-msg:MoveCommon
    :initform (cl:make-instance 'lebai_msgs-msg:MoveCommon))
   (execute_mode
    :reader execute_mode
    :initarg :execute_mode
    :type lebai_msgs-msg:ExecuteMode
    :initform (cl:make-instance 'lebai_msgs-msg:ExecuteMode)))
)

(cl:defclass MoveCircle-request (<MoveCircle-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MoveCircle-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MoveCircle-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<MoveCircle-request> is deprecated: use lebai_msgs-srv:MoveCircle-request instead.")))

(cl:ensure-generic-function 'way_point_is_joint_pose-val :lambda-list '(m))
(cl:defmethod way_point_is_joint_pose-val ((m <MoveCircle-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:way_point_is_joint_pose-val is deprecated.  Use lebai_msgs-srv:way_point_is_joint_pose instead.")
  (way_point_is_joint_pose m))

(cl:ensure-generic-function 'way_point_joint_pose-val :lambda-list '(m))
(cl:defmethod way_point_joint_pose-val ((m <MoveCircle-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:way_point_joint_pose-val is deprecated.  Use lebai_msgs-srv:way_point_joint_pose instead.")
  (way_point_joint_pose m))

(cl:ensure-generic-function 'way_point_cartesian_pose-val :lambda-list '(m))
(cl:defmethod way_point_cartesian_pose-val ((m <MoveCircle-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:way_point_cartesian_pose-val is deprecated.  Use lebai_msgs-srv:way_point_cartesian_pose instead.")
  (way_point_cartesian_pose m))

(cl:ensure-generic-function 'end_point_is_joint_pose-val :lambda-list '(m))
(cl:defmethod end_point_is_joint_pose-val ((m <MoveCircle-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:end_point_is_joint_pose-val is deprecated.  Use lebai_msgs-srv:end_point_is_joint_pose instead.")
  (end_point_is_joint_pose m))

(cl:ensure-generic-function 'end_point_joint_pose-val :lambda-list '(m))
(cl:defmethod end_point_joint_pose-val ((m <MoveCircle-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:end_point_joint_pose-val is deprecated.  Use lebai_msgs-srv:end_point_joint_pose instead.")
  (end_point_joint_pose m))

(cl:ensure-generic-function 'end_point_cartesian_pose-val :lambda-list '(m))
(cl:defmethod end_point_cartesian_pose-val ((m <MoveCircle-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:end_point_cartesian_pose-val is deprecated.  Use lebai_msgs-srv:end_point_cartesian_pose instead.")
  (end_point_cartesian_pose m))

(cl:ensure-generic-function 'circle_angle-val :lambda-list '(m))
(cl:defmethod circle_angle-val ((m <MoveCircle-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:circle_angle-val is deprecated.  Use lebai_msgs-srv:circle_angle instead.")
  (circle_angle m))

(cl:ensure-generic-function 'common-val :lambda-list '(m))
(cl:defmethod common-val ((m <MoveCircle-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:common-val is deprecated.  Use lebai_msgs-srv:common instead.")
  (common m))

(cl:ensure-generic-function 'execute_mode-val :lambda-list '(m))
(cl:defmethod execute_mode-val ((m <MoveCircle-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:execute_mode-val is deprecated.  Use lebai_msgs-srv:execute_mode instead.")
  (execute_mode m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MoveCircle-request>) ostream)
  "Serializes a message object of type '<MoveCircle-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'way_point_is_joint_pose) 1 0)) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'way_point_joint_pose))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'way_point_joint_pose))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'way_point_cartesian_pose) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'end_point_is_joint_pose) 1 0)) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'end_point_joint_pose))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'end_point_joint_pose))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'end_point_cartesian_pose) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'circle_angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'common) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'execute_mode) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MoveCircle-request>) istream)
  "Deserializes a message object of type '<MoveCircle-request>"
    (cl:setf (cl:slot-value msg 'way_point_is_joint_pose) (cl:not (cl:zerop (cl:read-byte istream))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'way_point_joint_pose) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'way_point_joint_pose)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'way_point_cartesian_pose) istream)
    (cl:setf (cl:slot-value msg 'end_point_is_joint_pose) (cl:not (cl:zerop (cl:read-byte istream))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'end_point_joint_pose) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'end_point_joint_pose)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'end_point_cartesian_pose) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'circle_angle) (roslisp-utils:decode-double-float-bits bits)))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'common) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'execute_mode) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MoveCircle-request>)))
  "Returns string type for a service object of type '<MoveCircle-request>"
  "lebai_msgs/MoveCircleRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MoveCircle-request)))
  "Returns string type for a service object of type 'MoveCircle-request"
  "lebai_msgs/MoveCircleRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MoveCircle-request>)))
  "Returns md5sum for a message object of type '<MoveCircle-request>"
  "76aefbda84057bd81221aca855230727")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MoveCircle-request)))
  "Returns md5sum for a message object of type 'MoveCircle-request"
  "76aefbda84057bd81221aca855230727")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MoveCircle-request>)))
  "Returns full string definition for message of type '<MoveCircle-request>"
  (cl:format cl:nil "bool way_point_is_joint_pose~%float64[] way_point_joint_pose~%geometry_msgs/Pose way_point_cartesian_pose~%bool end_point_is_joint_pose~%float64[] end_point_joint_pose~%geometry_msgs/Pose end_point_cartesian_pose~%float64 circle_angle~%lebai_msgs/MoveCommon common~%lebai_msgs/ExecuteMode execute_mode~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%================================================================================~%MSG: lebai_msgs/MoveCommon~%float64 vel~%float64 acc~%float64 time~%bool is_continous_mode~%# 0: normal move, 1: smooth move~%uint8 continuation_type~%# until data~%bool until~%lebai_msgs/UntilInfo until_info~%================================================================================~%MSG: lebai_msgs/UntilInfo~%uint8 io_express_logic~%lebai_msgs/IOConditionalExpress[] io_express~%~%uint8 LOGIC_AND=0~%uint8 LOGIC_OR=1~%~%~%================================================================================~%MSG: lebai_msgs/IOConditionalExpress~%uint32 group~%uint32 pin~%uint32 type~%float64 float_value~%uint8 uint_value~%uint8 logic_operation~%~%uint8 GROUP_ROBOT=0~%uint8 GROUP_FLANGE=1~%~%uint8 TYPE_ANALOG=0~%uint8 TYPE_DIGITAL=1~%~%# great >~%uint8 LOGIC_OP_GT=0~%# great and equal >=~%uint8 LOGIC_OP_GE=1~%# equal~%uint8 LOGIC_OP_EQ=2~%# not equal~%uint8 LOGIC_OP_NE=3~%# less than~%uint8 LOGIC_OP_LT=4~%# less than and equal~%uint8 LOGIC_OP_LE=5~%~%~%~%~%================================================================================~%MSG: lebai_msgs/ExecuteMode~%uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MoveCircle-request)))
  "Returns full string definition for message of type 'MoveCircle-request"
  (cl:format cl:nil "bool way_point_is_joint_pose~%float64[] way_point_joint_pose~%geometry_msgs/Pose way_point_cartesian_pose~%bool end_point_is_joint_pose~%float64[] end_point_joint_pose~%geometry_msgs/Pose end_point_cartesian_pose~%float64 circle_angle~%lebai_msgs/MoveCommon common~%lebai_msgs/ExecuteMode execute_mode~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%================================================================================~%MSG: lebai_msgs/MoveCommon~%float64 vel~%float64 acc~%float64 time~%bool is_continous_mode~%# 0: normal move, 1: smooth move~%uint8 continuation_type~%# until data~%bool until~%lebai_msgs/UntilInfo until_info~%================================================================================~%MSG: lebai_msgs/UntilInfo~%uint8 io_express_logic~%lebai_msgs/IOConditionalExpress[] io_express~%~%uint8 LOGIC_AND=0~%uint8 LOGIC_OR=1~%~%~%================================================================================~%MSG: lebai_msgs/IOConditionalExpress~%uint32 group~%uint32 pin~%uint32 type~%float64 float_value~%uint8 uint_value~%uint8 logic_operation~%~%uint8 GROUP_ROBOT=0~%uint8 GROUP_FLANGE=1~%~%uint8 TYPE_ANALOG=0~%uint8 TYPE_DIGITAL=1~%~%# great >~%uint8 LOGIC_OP_GT=0~%# great and equal >=~%uint8 LOGIC_OP_GE=1~%# equal~%uint8 LOGIC_OP_EQ=2~%# not equal~%uint8 LOGIC_OP_NE=3~%# less than~%uint8 LOGIC_OP_LT=4~%# less than and equal~%uint8 LOGIC_OP_LE=5~%~%~%~%~%================================================================================~%MSG: lebai_msgs/ExecuteMode~%uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MoveCircle-request>))
  (cl:+ 0
     1
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'way_point_joint_pose) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'way_point_cartesian_pose))
     1
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'end_point_joint_pose) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'end_point_cartesian_pose))
     8
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'common))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'execute_mode))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MoveCircle-request>))
  "Converts a ROS message object to a list"
  (cl:list 'MoveCircle-request
    (cl:cons ':way_point_is_joint_pose (way_point_is_joint_pose msg))
    (cl:cons ':way_point_joint_pose (way_point_joint_pose msg))
    (cl:cons ':way_point_cartesian_pose (way_point_cartesian_pose msg))
    (cl:cons ':end_point_is_joint_pose (end_point_is_joint_pose msg))
    (cl:cons ':end_point_joint_pose (end_point_joint_pose msg))
    (cl:cons ':end_point_cartesian_pose (end_point_cartesian_pose msg))
    (cl:cons ':circle_angle (circle_angle msg))
    (cl:cons ':common (common msg))
    (cl:cons ':execute_mode (execute_mode msg))
))
;//! \htmlinclude MoveCircle-response.msg.html

(cl:defclass <MoveCircle-response> (roslisp-msg-protocol:ros-message)
  ((ret
    :reader ret
    :initarg :ret
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass MoveCircle-response (<MoveCircle-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MoveCircle-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MoveCircle-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<MoveCircle-response> is deprecated: use lebai_msgs-srv:MoveCircle-response instead.")))

(cl:ensure-generic-function 'ret-val :lambda-list '(m))
(cl:defmethod ret-val ((m <MoveCircle-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:ret-val is deprecated.  Use lebai_msgs-srv:ret instead.")
  (ret m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MoveCircle-response>) ostream)
  "Serializes a message object of type '<MoveCircle-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'ret) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MoveCircle-response>) istream)
  "Deserializes a message object of type '<MoveCircle-response>"
    (cl:setf (cl:slot-value msg 'ret) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MoveCircle-response>)))
  "Returns string type for a service object of type '<MoveCircle-response>"
  "lebai_msgs/MoveCircleResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MoveCircle-response)))
  "Returns string type for a service object of type 'MoveCircle-response"
  "lebai_msgs/MoveCircleResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MoveCircle-response>)))
  "Returns md5sum for a message object of type '<MoveCircle-response>"
  "76aefbda84057bd81221aca855230727")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MoveCircle-response)))
  "Returns md5sum for a message object of type 'MoveCircle-response"
  "76aefbda84057bd81221aca855230727")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MoveCircle-response>)))
  "Returns full string definition for message of type '<MoveCircle-response>"
  (cl:format cl:nil "bool ret~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MoveCircle-response)))
  "Returns full string definition for message of type 'MoveCircle-response"
  (cl:format cl:nil "bool ret~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MoveCircle-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MoveCircle-response>))
  "Converts a ROS message object to a list"
  (cl:list 'MoveCircle-response
    (cl:cons ':ret (ret msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'MoveCircle)))
  'MoveCircle-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'MoveCircle)))
  'MoveCircle-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MoveCircle)))
  "Returns string type for a service object of type '<MoveCircle>"
  "lebai_msgs/MoveCircle")