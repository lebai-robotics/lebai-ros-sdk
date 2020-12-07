; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-srv)


;//! \htmlinclude SetAOutMode-request.msg.html

(cl:defclass <SetAOutMode-request> (roslisp-msg-protocol:ros-message)
  ((group
    :reader group
    :initarg :group
    :type cl:fixnum
    :initform 0)
   (index
    :reader index
    :initarg :index
    :type cl:fixnum
    :initform 0)
   (mode
    :reader mode
    :initarg :mode
    :type cl:fixnum
    :initform 0))
)

(cl:defclass SetAOutMode-request (<SetAOutMode-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetAOutMode-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetAOutMode-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetAOutMode-request> is deprecated: use lebai_msgs-srv:SetAOutMode-request instead.")))

(cl:ensure-generic-function 'group-val :lambda-list '(m))
(cl:defmethod group-val ((m <SetAOutMode-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:group-val is deprecated.  Use lebai_msgs-srv:group instead.")
  (group m))

(cl:ensure-generic-function 'index-val :lambda-list '(m))
(cl:defmethod index-val ((m <SetAOutMode-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:index-val is deprecated.  Use lebai_msgs-srv:index instead.")
  (index m))

(cl:ensure-generic-function 'mode-val :lambda-list '(m))
(cl:defmethod mode-val ((m <SetAOutMode-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:mode-val is deprecated.  Use lebai_msgs-srv:mode instead.")
  (mode m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetAOutMode-request>) ostream)
  "Serializes a message object of type '<SetAOutMode-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'group)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'index)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'index)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mode)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetAOutMode-request>) istream)
  "Deserializes a message object of type '<SetAOutMode-request>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'group)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'index)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'index)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'mode)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetAOutMode-request>)))
  "Returns string type for a service object of type '<SetAOutMode-request>"
  "lebai_msgs/SetAOutModeRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAOutMode-request)))
  "Returns string type for a service object of type 'SetAOutMode-request"
  "lebai_msgs/SetAOutModeRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetAOutMode-request>)))
  "Returns md5sum for a message object of type '<SetAOutMode-request>"
  "faf7ab1e93a1650eb66028ad6d75331c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetAOutMode-request)))
  "Returns md5sum for a message object of type 'SetAOutMode-request"
  "faf7ab1e93a1650eb66028ad6d75331c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetAOutMode-request>)))
  "Returns full string definition for message of type '<SetAOutMode-request>"
  (cl:format cl:nil "uint8 group~%uint16 index~%uint8 mode~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetAOutMode-request)))
  "Returns full string definition for message of type 'SetAOutMode-request"
  (cl:format cl:nil "uint8 group~%uint16 index~%uint8 mode~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetAOutMode-request>))
  (cl:+ 0
     1
     2
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetAOutMode-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetAOutMode-request
    (cl:cons ':group (group msg))
    (cl:cons ':index (index msg))
    (cl:cons ':mode (mode msg))
))
;//! \htmlinclude SetAOutMode-response.msg.html

(cl:defclass <SetAOutMode-response> (roslisp-msg-protocol:ros-message)
  ((code
    :reader code
    :initarg :code
    :type industrial_msgs-msg:ServiceReturnCode
    :initform (cl:make-instance 'industrial_msgs-msg:ServiceReturnCode)))
)

(cl:defclass SetAOutMode-response (<SetAOutMode-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetAOutMode-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetAOutMode-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetAOutMode-response> is deprecated: use lebai_msgs-srv:SetAOutMode-response instead.")))

(cl:ensure-generic-function 'code-val :lambda-list '(m))
(cl:defmethod code-val ((m <SetAOutMode-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:code-val is deprecated.  Use lebai_msgs-srv:code instead.")
  (code m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetAOutMode-response>) ostream)
  "Serializes a message object of type '<SetAOutMode-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'code) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetAOutMode-response>) istream)
  "Deserializes a message object of type '<SetAOutMode-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'code) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetAOutMode-response>)))
  "Returns string type for a service object of type '<SetAOutMode-response>"
  "lebai_msgs/SetAOutModeResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAOutMode-response)))
  "Returns string type for a service object of type 'SetAOutMode-response"
  "lebai_msgs/SetAOutModeResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetAOutMode-response>)))
  "Returns md5sum for a message object of type '<SetAOutMode-response>"
  "faf7ab1e93a1650eb66028ad6d75331c")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetAOutMode-response)))
  "Returns md5sum for a message object of type 'SetAOutMode-response"
  "faf7ab1e93a1650eb66028ad6d75331c")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetAOutMode-response>)))
  "Returns full string definition for message of type '<SetAOutMode-response>"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetAOutMode-response)))
  "Returns full string definition for message of type 'SetAOutMode-response"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetAOutMode-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'code))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetAOutMode-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetAOutMode-response
    (cl:cons ':code (code msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetAOutMode)))
  'SetAOutMode-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetAOutMode)))
  'SetAOutMode-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAOutMode)))
  "Returns string type for a service object of type '<SetAOutMode>"
  "lebai_msgs/SetAOutMode")