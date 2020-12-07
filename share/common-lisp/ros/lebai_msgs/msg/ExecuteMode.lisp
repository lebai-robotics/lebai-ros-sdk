; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-msg)


;//! \htmlinclude ExecuteMode.msg.html

(cl:defclass <ExecuteMode> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type cl:fixnum
    :initform 0))
)

(cl:defclass ExecuteMode (<ExecuteMode>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ExecuteMode>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ExecuteMode)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-msg:<ExecuteMode> is deprecated: use lebai_msgs-msg:ExecuteMode instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <ExecuteMode>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-msg:data-val is deprecated.  Use lebai_msgs-msg:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<ExecuteMode>)))
    "Constants for message type '<ExecuteMode>"
  '((:EXECUTE_MODE_BUFFER . 0)
    (:EXECUTE_MODE_IMMED . 1))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'ExecuteMode)))
    "Constants for message type 'ExecuteMode"
  '((:EXECUTE_MODE_BUFFER . 0)
    (:EXECUTE_MODE_IMMED . 1))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ExecuteMode>) ostream)
  "Serializes a message object of type '<ExecuteMode>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'data)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ExecuteMode>) istream)
  "Deserializes a message object of type '<ExecuteMode>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'data)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ExecuteMode>)))
  "Returns string type for a message object of type '<ExecuteMode>"
  "lebai_msgs/ExecuteMode")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ExecuteMode)))
  "Returns string type for a message object of type 'ExecuteMode"
  "lebai_msgs/ExecuteMode")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ExecuteMode>)))
  "Returns md5sum for a message object of type '<ExecuteMode>"
  "ce2e0fd38d2abc7741472f6d6de5645a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ExecuteMode)))
  "Returns md5sum for a message object of type 'ExecuteMode"
  "ce2e0fd38d2abc7741472f6d6de5645a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ExecuteMode>)))
  "Returns full string definition for message of type '<ExecuteMode>"
  (cl:format cl:nil "uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ExecuteMode)))
  "Returns full string definition for message of type 'ExecuteMode"
  (cl:format cl:nil "uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ExecuteMode>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ExecuteMode>))
  "Converts a ROS message object to a list"
  (cl:list 'ExecuteMode
    (cl:cons ':data (data msg))
))
