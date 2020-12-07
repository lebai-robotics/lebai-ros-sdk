; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-srv)


;//! \htmlinclude SetAO-request.msg.html

(cl:defclass <SetAO-request> (roslisp-msg-protocol:ros-message)
  ((pin
    :reader pin
    :initarg :pin
    :type cl:fixnum
    :initform 0)
   (value
    :reader value
    :initarg :value
    :type cl:float
    :initform 0.0)
   (execute_mode
    :reader execute_mode
    :initarg :execute_mode
    :type lebai_msgs-msg:ExecuteMode
    :initform (cl:make-instance 'lebai_msgs-msg:ExecuteMode)))
)

(cl:defclass SetAO-request (<SetAO-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetAO-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetAO-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetAO-request> is deprecated: use lebai_msgs-srv:SetAO-request instead.")))

(cl:ensure-generic-function 'pin-val :lambda-list '(m))
(cl:defmethod pin-val ((m <SetAO-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:pin-val is deprecated.  Use lebai_msgs-srv:pin instead.")
  (pin m))

(cl:ensure-generic-function 'value-val :lambda-list '(m))
(cl:defmethod value-val ((m <SetAO-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:value-val is deprecated.  Use lebai_msgs-srv:value instead.")
  (value m))

(cl:ensure-generic-function 'execute_mode-val :lambda-list '(m))
(cl:defmethod execute_mode-val ((m <SetAO-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:execute_mode-val is deprecated.  Use lebai_msgs-srv:execute_mode instead.")
  (execute_mode m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetAO-request>) ostream)
  "Serializes a message object of type '<SetAO-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pin)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'pin)) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'value))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'execute_mode) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetAO-request>) istream)
  "Deserializes a message object of type '<SetAO-request>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pin)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'pin)) (cl:read-byte istream))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'value) (roslisp-utils:decode-double-float-bits bits)))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'execute_mode) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetAO-request>)))
  "Returns string type for a service object of type '<SetAO-request>"
  "lebai_msgs/SetAORequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAO-request)))
  "Returns string type for a service object of type 'SetAO-request"
  "lebai_msgs/SetAORequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetAO-request>)))
  "Returns md5sum for a message object of type '<SetAO-request>"
  "62f232c76f8ee745408ad371412c03b5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetAO-request)))
  "Returns md5sum for a message object of type 'SetAO-request"
  "62f232c76f8ee745408ad371412c03b5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetAO-request>)))
  "Returns full string definition for message of type '<SetAO-request>"
  (cl:format cl:nil "uint16 pin~%float64 value~%lebai_msgs/ExecuteMode execute_mode~%~%================================================================================~%MSG: lebai_msgs/ExecuteMode~%uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetAO-request)))
  "Returns full string definition for message of type 'SetAO-request"
  (cl:format cl:nil "uint16 pin~%float64 value~%lebai_msgs/ExecuteMode execute_mode~%~%================================================================================~%MSG: lebai_msgs/ExecuteMode~%uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetAO-request>))
  (cl:+ 0
     2
     8
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'execute_mode))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetAO-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetAO-request
    (cl:cons ':pin (pin msg))
    (cl:cons ':value (value msg))
    (cl:cons ':execute_mode (execute_mode msg))
))
;//! \htmlinclude SetAO-response.msg.html

(cl:defclass <SetAO-response> (roslisp-msg-protocol:ros-message)
  ((code
    :reader code
    :initarg :code
    :type industrial_msgs-msg:ServiceReturnCode
    :initform (cl:make-instance 'industrial_msgs-msg:ServiceReturnCode)))
)

(cl:defclass SetAO-response (<SetAO-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetAO-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetAO-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetAO-response> is deprecated: use lebai_msgs-srv:SetAO-response instead.")))

(cl:ensure-generic-function 'code-val :lambda-list '(m))
(cl:defmethod code-val ((m <SetAO-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:code-val is deprecated.  Use lebai_msgs-srv:code instead.")
  (code m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetAO-response>) ostream)
  "Serializes a message object of type '<SetAO-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'code) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetAO-response>) istream)
  "Deserializes a message object of type '<SetAO-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'code) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetAO-response>)))
  "Returns string type for a service object of type '<SetAO-response>"
  "lebai_msgs/SetAOResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAO-response)))
  "Returns string type for a service object of type 'SetAO-response"
  "lebai_msgs/SetAOResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetAO-response>)))
  "Returns md5sum for a message object of type '<SetAO-response>"
  "62f232c76f8ee745408ad371412c03b5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetAO-response)))
  "Returns md5sum for a message object of type 'SetAO-response"
  "62f232c76f8ee745408ad371412c03b5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetAO-response>)))
  "Returns full string definition for message of type '<SetAO-response>"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetAO-response)))
  "Returns full string definition for message of type 'SetAO-response"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetAO-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'code))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetAO-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetAO-response
    (cl:cons ':code (code msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetAO)))
  'SetAO-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetAO)))
  'SetAO-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAO)))
  "Returns string type for a service object of type '<SetAO>"
  "lebai_msgs/SetAO")