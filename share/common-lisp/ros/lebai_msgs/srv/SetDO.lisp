; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-srv)


;//! \htmlinclude SetDO-request.msg.html

(cl:defclass <SetDO-request> (roslisp-msg-protocol:ros-message)
  ((pin
    :reader pin
    :initarg :pin
    :type cl:fixnum
    :initform 0)
   (value
    :reader value
    :initarg :value
    :type cl:boolean
    :initform cl:nil)
   (execute_mode
    :reader execute_mode
    :initarg :execute_mode
    :type lebai_msgs-msg:ExecuteMode
    :initform (cl:make-instance 'lebai_msgs-msg:ExecuteMode)))
)

(cl:defclass SetDO-request (<SetDO-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetDO-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetDO-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetDO-request> is deprecated: use lebai_msgs-srv:SetDO-request instead.")))

(cl:ensure-generic-function 'pin-val :lambda-list '(m))
(cl:defmethod pin-val ((m <SetDO-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:pin-val is deprecated.  Use lebai_msgs-srv:pin instead.")
  (pin m))

(cl:ensure-generic-function 'value-val :lambda-list '(m))
(cl:defmethod value-val ((m <SetDO-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:value-val is deprecated.  Use lebai_msgs-srv:value instead.")
  (value m))

(cl:ensure-generic-function 'execute_mode-val :lambda-list '(m))
(cl:defmethod execute_mode-val ((m <SetDO-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:execute_mode-val is deprecated.  Use lebai_msgs-srv:execute_mode instead.")
  (execute_mode m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetDO-request>) ostream)
  "Serializes a message object of type '<SetDO-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pin)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'pin)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'value) 1 0)) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'execute_mode) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetDO-request>) istream)
  "Deserializes a message object of type '<SetDO-request>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'pin)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'pin)) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'value) (cl:not (cl:zerop (cl:read-byte istream))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'execute_mode) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetDO-request>)))
  "Returns string type for a service object of type '<SetDO-request>"
  "lebai_msgs/SetDORequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetDO-request)))
  "Returns string type for a service object of type 'SetDO-request"
  "lebai_msgs/SetDORequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetDO-request>)))
  "Returns md5sum for a message object of type '<SetDO-request>"
  "5a536dfb6aaff1ccac47c5a754efe2e6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetDO-request)))
  "Returns md5sum for a message object of type 'SetDO-request"
  "5a536dfb6aaff1ccac47c5a754efe2e6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetDO-request>)))
  "Returns full string definition for message of type '<SetDO-request>"
  (cl:format cl:nil "uint16 pin~%bool value~%lebai_msgs/ExecuteMode execute_mode~%~%================================================================================~%MSG: lebai_msgs/ExecuteMode~%uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetDO-request)))
  "Returns full string definition for message of type 'SetDO-request"
  (cl:format cl:nil "uint16 pin~%bool value~%lebai_msgs/ExecuteMode execute_mode~%~%================================================================================~%MSG: lebai_msgs/ExecuteMode~%uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetDO-request>))
  (cl:+ 0
     2
     1
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'execute_mode))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetDO-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetDO-request
    (cl:cons ':pin (pin msg))
    (cl:cons ':value (value msg))
    (cl:cons ':execute_mode (execute_mode msg))
))
;//! \htmlinclude SetDO-response.msg.html

(cl:defclass <SetDO-response> (roslisp-msg-protocol:ros-message)
  ((code
    :reader code
    :initarg :code
    :type industrial_msgs-msg:ServiceReturnCode
    :initform (cl:make-instance 'industrial_msgs-msg:ServiceReturnCode)))
)

(cl:defclass SetDO-response (<SetDO-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetDO-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetDO-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetDO-response> is deprecated: use lebai_msgs-srv:SetDO-response instead.")))

(cl:ensure-generic-function 'code-val :lambda-list '(m))
(cl:defmethod code-val ((m <SetDO-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:code-val is deprecated.  Use lebai_msgs-srv:code instead.")
  (code m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetDO-response>) ostream)
  "Serializes a message object of type '<SetDO-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'code) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetDO-response>) istream)
  "Deserializes a message object of type '<SetDO-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'code) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetDO-response>)))
  "Returns string type for a service object of type '<SetDO-response>"
  "lebai_msgs/SetDOResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetDO-response)))
  "Returns string type for a service object of type 'SetDO-response"
  "lebai_msgs/SetDOResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetDO-response>)))
  "Returns md5sum for a message object of type '<SetDO-response>"
  "5a536dfb6aaff1ccac47c5a754efe2e6")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetDO-response)))
  "Returns md5sum for a message object of type 'SetDO-response"
  "5a536dfb6aaff1ccac47c5a754efe2e6")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetDO-response>)))
  "Returns full string definition for message of type '<SetDO-response>"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetDO-response)))
  "Returns full string definition for message of type 'SetDO-response"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetDO-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'code))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetDO-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetDO-response
    (cl:cons ':code (code msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetDO)))
  'SetDO-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetDO)))
  'SetDO-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetDO)))
  "Returns string type for a service object of type '<SetDO>"
  "lebai_msgs/SetDO")