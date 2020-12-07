; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-msg)


;//! \htmlinclude IOConditionalExpress.msg.html

(cl:defclass <IOConditionalExpress> (roslisp-msg-protocol:ros-message)
  ((group
    :reader group
    :initarg :group
    :type cl:integer
    :initform 0)
   (pin
    :reader pin
    :initarg :pin
    :type cl:integer
    :initform 0)
   (type
    :reader type
    :initarg :type
    :type cl:integer
    :initform 0)
   (float_value
    :reader float_value
    :initarg :float_value
    :type cl:float
    :initform 0.0)
   (uint_value
    :reader uint_value
    :initarg :uint_value
    :type cl:fixnum
    :initform 0)
   (logic_operation
    :reader logic_operation
    :initarg :logic_operation
    :type cl:fixnum
    :initform 0))
)

(cl:defclass IOConditionalExpress (<IOConditionalExpress>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <IOConditionalExpress>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'IOConditionalExpress)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-msg:<IOConditionalExpress> is deprecated: use lebai_msgs-msg:IOConditionalExpress instead.")))

(cl:ensure-generic-function 'group-val :lambda-list '(m))
(cl:defmethod group-val ((m <IOConditionalExpress>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:group-val is deprecated.  Use lebai_msgs-msg:group instead.")
  (group m))

(cl:ensure-generic-function 'pin-val :lambda-list '(m))
(cl:defmethod pin-val ((m <IOConditionalExpress>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:pin-val is deprecated.  Use lebai_msgs-msg:pin instead.")
  (pin m))

(cl:ensure-generic-function 'type-val :lambda-list '(m))
(cl:defmethod type-val ((m <IOConditionalExpress>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:type-val is deprecated.  Use lebai_msgs-msg:type instead.")
  (type m))

(cl:ensure-generic-function 'float_value-val :lambda-list '(m))
(cl:defmethod float_value-val ((m <IOConditionalExpress>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:float_value-val is deprecated.  Use lebai_msgs-msg:float_value instead.")
  (float_value m))

(cl:ensure-generic-function 'uint_value-val :lambda-list '(m))
(cl:defmethod uint_value-val ((m <IOConditionalExpress>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:uint_value-val is deprecated.  Use lebai_msgs-msg:uint_value instead.")
  (uint_value m))

(cl:ensure-generic-function 'logic_operation-val :lambda-list '(m))
(cl:defmethod logic_operation-val ((m <IOConditionalExpress>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:logic_operation-val is deprecated.  Use lebai_msgs-msg:logic_operation instead.")
  (logic_operation m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<IOConditionalExpress>)))
    "Constants for message type '<IOConditionalExpress>"
  '((:GROUP_ROBOT . 0)
    (:GROUP_FLANGE . 1)
    (:TYPE_ANALOG . 0)
    (:TYPE_DIGITAL . 1)
    (:LOGIC_OP_GT . 0)
    (:LOGIC_OP_GE . 1)
    (:LOGIC_OP_EQ . 2)
    (:LOGIC_OP_NE . 3)
    (:LOGIC_OP_LT . 4)
    (:LOGIC_OP_LE . 5))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'IOConditionalExpress)))
    "Constants for message type 'IOConditionalExpress"
  '((:GROUP_ROBOT . 0)
    (:GROUP_FLANGE . 1)
    (:TYPE_ANALOG . 0)
    (:TYPE_DIGITAL . 1)
    (:LOGIC_OP_GT . 0)
    (:LOGIC_OP_GE . 1)
    (:LOGIC_OP_EQ . 2)
    (:LOGIC_OP_NE . 3)
    (:LOGIC_OP_LT . 4)
    (:LOGIC_OP_LE . 5))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <IOConditionalExpress>) ostream)
  "Serializes a message object of type '<IOConditionalExpress>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'group)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'group)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'group)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'group)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pin)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'pin)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'pin)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'pin)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'type)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'type)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'type)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'type)) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'float_value))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'uint_value)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'logic_operation)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <IOConditionalExpress>) istream)
  "Deserializes a message object of type '<IOConditionalExpress>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'group)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'group)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'group)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'group)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pin)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'pin)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'pin)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'pin)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'type)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'type)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'type)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'type)) (cl:read-byte istream))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'float_value) (roslisp-utils:decode-double-float-bits bits)))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'uint_value)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'logic_operation)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<IOConditionalExpress>)))
  "Returns string type for a message object of type '<IOConditionalExpress>"
  "lebai_msgs/IOConditionalExpress")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'IOConditionalExpress)))
  "Returns string type for a message object of type 'IOConditionalExpress"
  "lebai_msgs/IOConditionalExpress")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<IOConditionalExpress>)))
  "Returns md5sum for a message object of type '<IOConditionalExpress>"
  "35d2fc6b432f8da8c61c0faaba79afff")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'IOConditionalExpress)))
  "Returns md5sum for a message object of type 'IOConditionalExpress"
  "35d2fc6b432f8da8c61c0faaba79afff")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<IOConditionalExpress>)))
  "Returns full string definition for message of type '<IOConditionalExpress>"
  (cl:format cl:nil "uint32 group~%uint32 pin~%uint32 type~%float64 float_value~%uint8 uint_value~%uint8 logic_operation~%~%uint8 GROUP_ROBOT=0~%uint8 GROUP_FLANGE=1~%~%uint8 TYPE_ANALOG=0~%uint8 TYPE_DIGITAL=1~%~%# great >~%uint8 LOGIC_OP_GT=0~%# great and equal >=~%uint8 LOGIC_OP_GE=1~%# equal~%uint8 LOGIC_OP_EQ=2~%# not equal~%uint8 LOGIC_OP_NE=3~%# less than~%uint8 LOGIC_OP_LT=4~%# less than and equal~%uint8 LOGIC_OP_LE=5~%~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'IOConditionalExpress)))
  "Returns full string definition for message of type 'IOConditionalExpress"
  (cl:format cl:nil "uint32 group~%uint32 pin~%uint32 type~%float64 float_value~%uint8 uint_value~%uint8 logic_operation~%~%uint8 GROUP_ROBOT=0~%uint8 GROUP_FLANGE=1~%~%uint8 TYPE_ANALOG=0~%uint8 TYPE_DIGITAL=1~%~%# great >~%uint8 LOGIC_OP_GT=0~%# great and equal >=~%uint8 LOGIC_OP_GE=1~%# equal~%uint8 LOGIC_OP_EQ=2~%# not equal~%uint8 LOGIC_OP_NE=3~%# less than~%uint8 LOGIC_OP_LT=4~%# less than and equal~%uint8 LOGIC_OP_LE=5~%~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <IOConditionalExpress>))
  (cl:+ 0
     4
     4
     4
     8
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <IOConditionalExpress>))
  "Converts a ROS message object to a list"
  (cl:list 'IOConditionalExpress
    (cl:cons ':group (group msg))
    (cl:cons ':pin (pin msg))
    (cl:cons ':type (type msg))
    (cl:cons ':float_value (float_value msg))
    (cl:cons ':uint_value (uint_value msg))
    (cl:cons ':logic_operation (logic_operation msg))
))
