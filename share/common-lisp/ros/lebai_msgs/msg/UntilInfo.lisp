; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-msg)


;//! \htmlinclude UntilInfo.msg.html

(cl:defclass <UntilInfo> (roslisp-msg-protocol:ros-message)
  ((io_express_logic
    :reader io_express_logic
    :initarg :io_express_logic
    :type cl:fixnum
    :initform 0)
   (io_express
    :reader io_express
    :initarg :io_express
    :type (cl:vector lebai_msgs-msg:IOConditionalExpress)
   :initform (cl:make-array 0 :element-type 'lebai_msgs-msg:IOConditionalExpress :initial-element (cl:make-instance 'lebai_msgs-msg:IOConditionalExpress))))
)

(cl:defclass UntilInfo (<UntilInfo>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <UntilInfo>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'UntilInfo)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-msg:<UntilInfo> is deprecated: use lebai_msgs-msg:UntilInfo instead.")))

(cl:ensure-generic-function 'io_express_logic-val :lambda-list '(m))
(cl:defmethod io_express_logic-val ((m <UntilInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:io_express_logic-val is deprecated.  Use lebai_msgs-msg:io_express_logic instead.")
  (io_express_logic m))

(cl:ensure-generic-function 'io_express-val :lambda-list '(m))
(cl:defmethod io_express-val ((m <UntilInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:io_express-val is deprecated.  Use lebai_msgs-msg:io_express instead.")
  (io_express m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<UntilInfo>)))
    "Constants for message type '<UntilInfo>"
  '((:LOGIC_AND . 0)
    (:LOGIC_OR . 1))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'UntilInfo)))
    "Constants for message type 'UntilInfo"
  '((:LOGIC_AND . 0)
    (:LOGIC_OR . 1))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <UntilInfo>) ostream)
  "Serializes a message object of type '<UntilInfo>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'io_express_logic)) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'io_express))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'io_express))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <UntilInfo>) istream)
  "Deserializes a message object of type '<UntilInfo>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'io_express_logic)) (cl:read-byte istream))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'io_express) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'io_express)))
    (cl:dotimes (i __ros_arr_len)
    (cl:setf (cl:aref vals i) (cl:make-instance 'lebai_msgs-msg:IOConditionalExpress))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<UntilInfo>)))
  "Returns string type for a message object of type '<UntilInfo>"
  "lebai_msgs/UntilInfo")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'UntilInfo)))
  "Returns string type for a message object of type 'UntilInfo"
  "lebai_msgs/UntilInfo")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<UntilInfo>)))
  "Returns md5sum for a message object of type '<UntilInfo>"
  "0907ad90f772aaa5fd1b8f10a92d018a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'UntilInfo)))
  "Returns md5sum for a message object of type 'UntilInfo"
  "0907ad90f772aaa5fd1b8f10a92d018a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<UntilInfo>)))
  "Returns full string definition for message of type '<UntilInfo>"
  (cl:format cl:nil "uint8 io_express_logic~%lebai_msgs/IOConditionalExpress[] io_express~%~%uint8 LOGIC_AND=0~%uint8 LOGIC_OR=1~%~%~%================================================================================~%MSG: lebai_msgs/IOConditionalExpress~%uint32 group~%uint32 pin~%uint32 type~%float64 float_value~%uint8 uint_value~%uint8 logic_operation~%~%uint8 GROUP_ROBOT=0~%uint8 GROUP_FLANGE=1~%~%uint8 TYPE_ANALOG=0~%uint8 TYPE_DIGITAL=1~%~%# great >~%uint8 LOGIC_OP_GT=0~%# great and equal >=~%uint8 LOGIC_OP_GE=1~%# equal~%uint8 LOGIC_OP_EQ=2~%# not equal~%uint8 LOGIC_OP_NE=3~%# less than~%uint8 LOGIC_OP_LT=4~%# less than and equal~%uint8 LOGIC_OP_LE=5~%~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'UntilInfo)))
  "Returns full string definition for message of type 'UntilInfo"
  (cl:format cl:nil "uint8 io_express_logic~%lebai_msgs/IOConditionalExpress[] io_express~%~%uint8 LOGIC_AND=0~%uint8 LOGIC_OR=1~%~%~%================================================================================~%MSG: lebai_msgs/IOConditionalExpress~%uint32 group~%uint32 pin~%uint32 type~%float64 float_value~%uint8 uint_value~%uint8 logic_operation~%~%uint8 GROUP_ROBOT=0~%uint8 GROUP_FLANGE=1~%~%uint8 TYPE_ANALOG=0~%uint8 TYPE_DIGITAL=1~%~%# great >~%uint8 LOGIC_OP_GT=0~%# great and equal >=~%uint8 LOGIC_OP_GE=1~%# equal~%uint8 LOGIC_OP_EQ=2~%# not equal~%uint8 LOGIC_OP_NE=3~%# less than~%uint8 LOGIC_OP_LT=4~%# less than and equal~%uint8 LOGIC_OP_LE=5~%~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <UntilInfo>))
  (cl:+ 0
     1
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'io_express) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <UntilInfo>))
  "Converts a ROS message object to a list"
  (cl:list 'UntilInfo
    (cl:cons ':io_express_logic (io_express_logic msg))
    (cl:cons ':io_express (io_express msg))
))
