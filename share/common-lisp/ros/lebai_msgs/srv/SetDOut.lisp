; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-srv)


;//! \htmlinclude SetDOut-request.msg.html

(cl:defclass <SetDOut-request> (roslisp-msg-protocol:ros-message)
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
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass SetDOut-request (<SetDOut-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetDOut-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetDOut-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetDOut-request> is deprecated: use lebai_msgs-srv:SetDOut-request instead.")))

(cl:ensure-generic-function 'group-val :lambda-list '(m))
(cl:defmethod group-val ((m <SetDOut-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:group-val is deprecated.  Use lebai_msgs-srv:group instead.")
  (group m))

(cl:ensure-generic-function 'index-val :lambda-list '(m))
(cl:defmethod index-val ((m <SetDOut-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:index-val is deprecated.  Use lebai_msgs-srv:index instead.")
  (index m))

(cl:ensure-generic-function 'value-val :lambda-list '(m))
(cl:defmethod value-val ((m <SetDOut-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:value-val is deprecated.  Use lebai_msgs-srv:value instead.")
  (value m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetDOut-request>) ostream)
  "Serializes a message object of type '<SetDOut-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'group)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'index)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'index)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'value) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetDOut-request>) istream)
  "Deserializes a message object of type '<SetDOut-request>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'group)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'index)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'index)) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'value) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetDOut-request>)))
  "Returns string type for a service object of type '<SetDOut-request>"
  "lebai_msgs/SetDOutRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetDOut-request)))
  "Returns string type for a service object of type 'SetDOut-request"
  "lebai_msgs/SetDOutRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetDOut-request>)))
  "Returns md5sum for a message object of type '<SetDOut-request>"
  "e6191b92a4b149f13f17282b8739af44")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetDOut-request)))
  "Returns md5sum for a message object of type 'SetDOut-request"
  "e6191b92a4b149f13f17282b8739af44")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetDOut-request>)))
  "Returns full string definition for message of type '<SetDOut-request>"
  (cl:format cl:nil "uint8 group~%uint16 index~%bool value~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetDOut-request)))
  "Returns full string definition for message of type 'SetDOut-request"
  (cl:format cl:nil "uint8 group~%uint16 index~%bool value~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetDOut-request>))
  (cl:+ 0
     1
     2
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetDOut-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetDOut-request
    (cl:cons ':group (group msg))
    (cl:cons ':index (index msg))
    (cl:cons ':value (value msg))
))
;//! \htmlinclude SetDOut-response.msg.html

(cl:defclass <SetDOut-response> (roslisp-msg-protocol:ros-message)
  ((code
    :reader code
    :initarg :code
    :type industrial_msgs-msg:ServiceReturnCode
    :initform (cl:make-instance 'industrial_msgs-msg:ServiceReturnCode)))
)

(cl:defclass SetDOut-response (<SetDOut-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetDOut-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetDOut-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetDOut-response> is deprecated: use lebai_msgs-srv:SetDOut-response instead.")))

(cl:ensure-generic-function 'code-val :lambda-list '(m))
(cl:defmethod code-val ((m <SetDOut-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:code-val is deprecated.  Use lebai_msgs-srv:code instead.")
  (code m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetDOut-response>) ostream)
  "Serializes a message object of type '<SetDOut-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'code) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetDOut-response>) istream)
  "Deserializes a message object of type '<SetDOut-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'code) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetDOut-response>)))
  "Returns string type for a service object of type '<SetDOut-response>"
  "lebai_msgs/SetDOutResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetDOut-response)))
  "Returns string type for a service object of type 'SetDOut-response"
  "lebai_msgs/SetDOutResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetDOut-response>)))
  "Returns md5sum for a message object of type '<SetDOut-response>"
  "e6191b92a4b149f13f17282b8739af44")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetDOut-response)))
  "Returns md5sum for a message object of type 'SetDOut-response"
  "e6191b92a4b149f13f17282b8739af44")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetDOut-response>)))
  "Returns full string definition for message of type '<SetDOut-response>"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetDOut-response)))
  "Returns full string definition for message of type 'SetDOut-response"
  (cl:format cl:nil "industrial_msgs/ServiceReturnCode code~%~%================================================================================~%MSG: industrial_msgs/ServiceReturnCode~%# Service return codes for simple requests.  All ROS-Industrial service~%# replies are required to have a return code indicating success or failure~%# Specific return codes for different failure should be negative.~%int8 val~%~%int8 SUCCESS = 1~%int8 FAILURE = -1~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetDOut-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'code))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetDOut-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetDOut-response
    (cl:cons ':code (code msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetDOut)))
  'SetDOut-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetDOut)))
  'SetDOut-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetDOut)))
  "Returns string type for a service object of type '<SetDOut>"
  "lebai_msgs/SetDOut")