; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-srv)


;//! \htmlinclude SetAOut-request.msg.html

(cl:defclass <SetAOut-request> (roslisp-msg-protocol:ros-message)
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
   (value
    :reader value
    :initarg :value
    :type cl:float
    :initform 0.0))
)

(cl:defclass SetAOut-request (<SetAOut-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetAOut-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetAOut-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetAOut-request> is deprecated: use lebai_msgs-srv:SetAOut-request instead.")))

(cl:ensure-generic-function 'group-val :lambda-list '(m))
(cl:defmethod group-val ((m <SetAOut-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:group-val is deprecated.  Use lebai_msgs-srv:group instead.")
  (group m))

(cl:ensure-generic-function 'index-val :lambda-list '(m))
(cl:defmethod index-val ((m <SetAOut-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:index-val is deprecated.  Use lebai_msgs-srv:index instead.")
  (index m))

(cl:ensure-generic-function 'value-val :lambda-list '(m))
(cl:defmethod value-val ((m <SetAOut-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:value-val is deprecated.  Use lebai_msgs-srv:value instead.")
  (value m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetAOut-request>) ostream)
  "Serializes a message object of type '<SetAOut-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'group)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'index)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'index)) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'value))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetAOut-request>) istream)
  "Deserializes a message object of type '<SetAOut-request>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'group)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'index)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'index)) (cl:read-byte istream))
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
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetAOut-request>)))
  "Returns string type for a service object of type '<SetAOut-request>"
  "lebai_msgs/SetAOutRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAOut-request)))
  "Returns string type for a service object of type 'SetAOut-request"
  "lebai_msgs/SetAOutRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetAOut-request>)))
  "Returns md5sum for a message object of type '<SetAOut-request>"
  "51928732046ffb5b5606f765ba7fcd8b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetAOut-request)))
  "Returns md5sum for a message object of type 'SetAOut-request"
  "51928732046ffb5b5606f765ba7fcd8b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetAOut-request>)))
  "Returns full string definition for message of type '<SetAOut-request>"
  (cl:format cl:nil "uint8 group~%uint16 index~%float64 value~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetAOut-request)))
  "Returns full string definition for message of type 'SetAOut-request"
  (cl:format cl:nil "uint8 group~%uint16 index~%float64 value~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetAOut-request>))
  (cl:+ 0
     1
     2
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetAOut-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetAOut-request
    (cl:cons ':group (group msg))
    (cl:cons ':index (index msg))
    (cl:cons ':value (value msg))
))
;//! \htmlinclude SetAOut-response.msg.html

(cl:defclass <SetAOut-response> (roslisp-msg-protocol:ros-message)
  ((code
    :reader code
    :initarg :code
    :type industrial_msgs-msg:ServiceReturnCode
    :initform (cl:make-instance 'industrial_msgs-msg:ServiceReturnCode)))
)

(cl:defclass SetAOut-response (<SetAOut-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetAOut-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetAOut-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetAOut-response> is deprecated: use lebai_msgs-srv:SetAOut-response instead.")))

(cl:ensure-generic-function 'code-val :lambda-list '(m))
(cl:defmethod code-val ((m <SetAOut-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:code-val is deprecated.  Use lebai_msgs-srv:code instead.")
  (code m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetAOut-response>) ostream)
  "Serializes a message object of type '<SetAOut-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'code) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetAOut-response>) istream)
  "Deserializes a message object of type '<SetAOut-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'code) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetAOut-response>)))
  "Returns string type for a service object of type '<SetAOut-response>"
  "lebai_msgs/SetAOutResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAOut-response)))
  "Returns string type for a service object of type 'SetAOut-response"
  "lebai_msgs/SetAOutResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetAOut-response>)))
  "Returns md5sum for a message object of type '<SetAOut-response>"
  "51928732046ffb5b5606f765ba7fcd8b")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetAOut-response)))
  "Returns md5sum for a message object of type 'SetAOut-response"
  "51928732046ffb5b5606f765ba7fcd8b")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetAOut-response>)))
  "Returns full string definition for message of type '<SetAOut-response>"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetAOut-response)))
  "Returns full string definition for message of type 'SetAOut-response"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetAOut-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'code))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetAOut-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetAOut-response
    (cl:cons ':code (code msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetAOut)))
  'SetAOut-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetAOut)))
  'SetAOut-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetAOut)))
  "Returns string type for a service object of type '<SetAOut>"
  "lebai_msgs/SetAOut")