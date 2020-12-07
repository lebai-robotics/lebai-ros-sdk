; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-srv)


;//! \htmlinclude SetAMode-request.msg.html

(cl:defclass <SetAMode-request> (roslisp-msg-protocol:ros-message)
  ((pin
    :reader pin
    :initarg :pin
    :type cl:fixnum
    :initform 0)
   (mode
    :reader mode
    :initarg :mode
    :type cl:fixnum
    :initform 0)
   (execute_mode
    :reader execute_mode
    :initarg :execute_mode
    :type lebai_msgs-msg:ExecuteMode
    :initform (cl:make-instance 'lebai_msgs-msg:ExecuteMode)))
)

(cl:defclass SetAMode-request (<SetAMode-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetAMode-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetAMode-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetAMode-request> is deprecated: use lebai_msgs-srv:SetAMode-request instead.")))

(cl:ensure-generic-function 'pin-val :lambda-list '(m))
(cl:defmethod pin-val ((m <SetAMode-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:pin-val is deprecated.  Use lebai_msgs-srv:pin instead.")
  (pin m))

(cl:ensure-generic-function 'mode-val :lambda-list '(m))
(cl:defmethod mode-val ((m <SetAMode-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:mode-val is deprecated.  Use lebai_msgs-srv:mode instead.")
  (mode m))

(cl:ensure-generic-function 'execute_mode-val :lambda-list '(m))
(cl:defmethod execute_mode-val ((m <SetAMode-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:execute_mode-val is deprecated.  Use lebai_msgs-srv:execute_mode instead.")
  (execute_mode m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetAMode-request>) ostream)
  "Serializes a message object of type '<SetAMode-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pin)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'pin)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mode)) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'execute_mode) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetAMode-request>) istream)
  "Deserializes a message object of type '<SetAMode-request>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pin)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'pin)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mode)) (cl:read-byte istream))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'execute_mode) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetAMode-request>)))
  "Returns string type for a service object of type '<SetAMode-request>"
  "lebai_msgs/SetAModeRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAMode-request)))
  "Returns string type for a service object of type 'SetAMode-request"
  "lebai_msgs/SetAModeRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetAMode-request>)))
  "Returns md5sum for a message object of type '<SetAMode-request>"
  "db41913f133aefb2bfdc45acc60725b5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetAMode-request)))
  "Returns md5sum for a message object of type 'SetAMode-request"
  "db41913f133aefb2bfdc45acc60725b5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetAMode-request>)))
  "Returns full string definition for message of type '<SetAMode-request>"
  (cl:format cl:nil "uint16 pin~%uint8 mode~%lebai_msgs/ExecuteMode execute_mode~%~%================================================================================~%MSG: lebai_msgs/ExecuteMode~%uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetAMode-request)))
  "Returns full string definition for message of type 'SetAMode-request"
  (cl:format cl:nil "uint16 pin~%uint8 mode~%lebai_msgs/ExecuteMode execute_mode~%~%================================================================================~%MSG: lebai_msgs/ExecuteMode~%uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetAMode-request>))
  (cl:+ 0
     2
     1
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'execute_mode))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetAMode-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetAMode-request
    (cl:cons ':pin (pin msg))
    (cl:cons ':mode (mode msg))
    (cl:cons ':execute_mode (execute_mode msg))
))
;//! \htmlinclude SetAMode-response.msg.html

(cl:defclass <SetAMode-response> (roslisp-msg-protocol:ros-message)
  ((code
    :reader code
    :initarg :code
    :type industrial_msgs-msg:ServiceReturnCode
    :initform (cl:make-instance 'industrial_msgs-msg:ServiceReturnCode)))
)

(cl:defclass SetAMode-response (<SetAMode-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetAMode-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetAMode-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetAMode-response> is deprecated: use lebai_msgs-srv:SetAMode-response instead.")))

(cl:ensure-generic-function 'code-val :lambda-list '(m))
(cl:defmethod code-val ((m <SetAMode-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:code-val is deprecated.  Use lebai_msgs-srv:code instead.")
  (code m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetAMode-response>) ostream)
  "Serializes a message object of type '<SetAMode-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'code) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetAMode-response>) istream)
  "Deserializes a message object of type '<SetAMode-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'code) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetAMode-response>)))
  "Returns string type for a service object of type '<SetAMode-response>"
  "lebai_msgs/SetAModeResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAMode-response)))
  "Returns string type for a service object of type 'SetAMode-response"
  "lebai_msgs/SetAModeResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetAMode-response>)))
  "Returns md5sum for a message object of type '<SetAMode-response>"
  "db41913f133aefb2bfdc45acc60725b5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetAMode-response)))
  "Returns md5sum for a message object of type 'SetAMode-response"
  "db41913f133aefb2bfdc45acc60725b5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetAMode-response>)))
  "Returns full string definition for message of type '<SetAMode-response>"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetAMode-response)))
  "Returns full string definition for message of type 'SetAMode-response"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetAMode-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'code))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetAMode-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetAMode-response
    (cl:cons ':code (code msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetAMode)))
  'SetAMode-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetAMode)))
  'SetAMode-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAMode)))
  "Returns string type for a service object of type '<SetAMode>"
  "lebai_msgs/SetAMode")