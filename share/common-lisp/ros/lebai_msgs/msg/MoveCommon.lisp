; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-msg)


;//! \htmlinclude MoveCommon.msg.html

(cl:defclass <MoveCommon> (roslisp-msg-protocol:ros-message)
  ((vel
    :reader vel
    :initarg :vel
    :type cl:float
    :initform 0.0)
   (acc
    :reader acc
    :initarg :acc
    :type cl:float
    :initform 0.0)
   (time
    :reader time
    :initarg :time
    :type cl:float
    :initform 0.0)
   (is_continous_mode
    :reader is_continous_mode
    :initarg :is_continous_mode
    :type cl:boolean
    :initform cl:nil)
   (continuation_type
    :reader continuation_type
    :initarg :continuation_type
    :type cl:fixnum
    :initform 0)
   (until
    :reader until
    :initarg :until
    :type cl:boolean
    :initform cl:nil)
   (until_info
    :reader until_info
    :initarg :until_info
    :type lebai_msgs-msg:UntilInfo
    :initform (cl:make-instance 'lebai_msgs-msg:UntilInfo)))
)

(cl:defclass MoveCommon (<MoveCommon>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MoveCommon>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MoveCommon)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-msg:<MoveCommon> is deprecated: use lebai_msgs-msg:MoveCommon instead.")))

(cl:ensure-generic-function 'vel-val :lambda-list '(m))
(cl:defmethod vel-val ((m <MoveCommon>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:vel-val is deprecated.  Use lebai_msgs-msg:vel instead.")
  (vel m))

(cl:ensure-generic-function 'acc-val :lambda-list '(m))
(cl:defmethod acc-val ((m <MoveCommon>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:acc-val is deprecated.  Use lebai_msgs-msg:acc instead.")
  (acc m))

(cl:ensure-generic-function 'time-val :lambda-list '(m))
(cl:defmethod time-val ((m <MoveCommon>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:time-val is deprecated.  Use lebai_msgs-msg:time instead.")
  (time m))

(cl:ensure-generic-function 'is_continous_mode-val :lambda-list '(m))
(cl:defmethod is_continous_mode-val ((m <MoveCommon>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:is_continous_mode-val is deprecated.  Use lebai_msgs-msg:is_continous_mode instead.")
  (is_continous_mode m))

(cl:ensure-generic-function 'continuation_type-val :lambda-list '(m))
(cl:defmethod continuation_type-val ((m <MoveCommon>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:continuation_type-val is deprecated.  Use lebai_msgs-msg:continuation_type instead.")
  (continuation_type m))

(cl:ensure-generic-function 'until-val :lambda-list '(m))
(cl:defmethod until-val ((m <MoveCommon>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:until-val is deprecated.  Use lebai_msgs-msg:until instead.")
  (until m))

(cl:ensure-generic-function 'until_info-val :lambda-list '(m))
(cl:defmethod until_info-val ((m <MoveCommon>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:until_info-val is deprecated.  Use lebai_msgs-msg:until_info instead.")
  (until_info m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MoveCommon>) ostream)
  "Serializes a message object of type '<MoveCommon>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'vel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'acc))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'is_continous_mode) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'continuation_type)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'until) 1 0)) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'until_info) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MoveCommon>) istream)
  "Deserializes a message object of type '<MoveCommon>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'vel) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'acc) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'time) (roslisp-utils:decode-double-float-bits bits)))
    (cl:setf (cl:slot-value msg 'is_continous_mode) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'continuation_type)) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'until) (cl:not (cl:zerop (cl:read-byte istream))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'until_info) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MoveCommon>)))
  "Returns string type for a message object of type '<MoveCommon>"
  "lebai_msgs/MoveCommon")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MoveCommon)))
  "Returns string type for a message object of type 'MoveCommon"
  "lebai_msgs/MoveCommon")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MoveCommon>)))
  "Returns md5sum for a message object of type '<MoveCommon>"
  "4ddffee09af26b88275ddf204fecc8d2")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MoveCommon)))
  "Returns md5sum for a message object of type 'MoveCommon"
  "4ddffee09af26b88275ddf204fecc8d2")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MoveCommon>)))
  "Returns full string definition for message of type '<MoveCommon>"
  (cl:format cl:nil "float64 vel~%float64 acc~%float64 time~%bool is_continous_mode~%# 0: normal move, 1: smooth move~%uint8 continuation_type~%# until data~%bool until~%lebai_msgs/UntilInfo until_info~%================================================================================~%MSG: lebai_msgs/UntilInfo~%uint8 io_express_logic~%lebai_msgs/IOConditionalExpress[] io_express~%~%uint8 LOGIC_AND=0~%uint8 LOGIC_OR=1~%~%~%================================================================================~%MSG: lebai_msgs/IOConditionalExpress~%uint32 group~%uint32 pin~%uint32 type~%float64 float_value~%uint8 uint_value~%uint8 logic_operation~%~%uint8 GROUP_ROBOT=0~%uint8 GROUP_FLANGE=1~%~%uint8 TYPE_ANALOG=0~%uint8 TYPE_DIGITAL=1~%~%# great >~%uint8 LOGIC_OP_GT=0~%# great and equal >=~%uint8 LOGIC_OP_GE=1~%# equal~%uint8 LOGIC_OP_EQ=2~%# not equal~%uint8 LOGIC_OP_NE=3~%# less than~%uint8 LOGIC_OP_LT=4~%# less than and equal~%uint8 LOGIC_OP_LE=5~%~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MoveCommon)))
  "Returns full string definition for message of type 'MoveCommon"
  (cl:format cl:nil "float64 vel~%float64 acc~%float64 time~%bool is_continous_mode~%# 0: normal move, 1: smooth move~%uint8 continuation_type~%# until data~%bool until~%lebai_msgs/UntilInfo until_info~%================================================================================~%MSG: lebai_msgs/UntilInfo~%uint8 io_express_logic~%lebai_msgs/IOConditionalExpress[] io_express~%~%uint8 LOGIC_AND=0~%uint8 LOGIC_OR=1~%~%~%================================================================================~%MSG: lebai_msgs/IOConditionalExpress~%uint32 group~%uint32 pin~%uint32 type~%float64 float_value~%uint8 uint_value~%uint8 logic_operation~%~%uint8 GROUP_ROBOT=0~%uint8 GROUP_FLANGE=1~%~%uint8 TYPE_ANALOG=0~%uint8 TYPE_DIGITAL=1~%~%# great >~%uint8 LOGIC_OP_GT=0~%# great and equal >=~%uint8 LOGIC_OP_GE=1~%# equal~%uint8 LOGIC_OP_EQ=2~%# not equal~%uint8 LOGIC_OP_NE=3~%# less than~%uint8 LOGIC_OP_LT=4~%# less than and equal~%uint8 LOGIC_OP_LE=5~%~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MoveCommon>))
  (cl:+ 0
     8
     8
     8
     1
     1
     1
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'until_info))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MoveCommon>))
  "Converts a ROS message object to a list"
  (cl:list 'MoveCommon
    (cl:cons ':vel (vel msg))
    (cl:cons ':acc (acc msg))
    (cl:cons ':time (time msg))
    (cl:cons ':is_continous_mode (is_continous_mode msg))
    (cl:cons ':continuation_type (continuation_type msg))
    (cl:cons ':until (until msg))
    (cl:cons ':until_info (until_info msg))
))
