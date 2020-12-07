; Auto-generated. Do not edit!


(cl:in-package lebai_msgs-srv)


;//! \htmlinclude SetGripper-request.msg.html

(cl:defclass <SetGripper-request> (roslisp-msg-protocol:ros-message)
  ((val
    :reader val
    :initarg :val
    :type cl:float
    :initform 0.0)
   (execute_mode
    :reader execute_mode
    :initarg :execute_mode
    :type lebai_msgs-msg:ExecuteMode
    :initform (cl:make-instance 'lebai_msgs-msg:ExecuteMode)))
)

(cl:defclass SetGripper-request (<SetGripper-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetGripper-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetGripper-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetGripper-request> is deprecated: use lebai_msgs-srv:SetGripper-request instead.")))

(cl:ensure-generic-function 'val-val :lambda-list '(m))
(cl:defmethod val-val ((m <SetGripper-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:val-val is deprecated.  Use lebai_msgs-srv:val instead.")
  (val m))

(cl:ensure-generic-function 'execute_mode-val :lambda-list '(m))
(cl:defmethod execute_mode-val ((m <SetGripper-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:execute_mode-val is deprecated.  Use lebai_msgs-srv:execute_mode instead.")
  (execute_mode m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetGripper-request>) ostream)
  "Serializes a message object of type '<SetGripper-request>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'val))))
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
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetGripper-request>) istream)
  "Deserializes a message object of type '<SetGripper-request>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'val) (roslisp-utils:decode-double-float-bits bits)))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'execute_mode) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetGripper-request>)))
  "Returns string type for a service object of type '<SetGripper-request>"
  "lebai_msgs/SetGripperRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetGripper-request)))
  "Returns string type for a service object of type 'SetGripper-request"
  "lebai_msgs/SetGripperRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetGripper-request>)))
  "Returns md5sum for a message object of type '<SetGripper-request>"
  "38cc51b5a105d56ff2e64d1889e45a66")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetGripper-request)))
  "Returns md5sum for a message object of type 'SetGripper-request"
  "38cc51b5a105d56ff2e64d1889e45a66")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetGripper-request>)))
  "Returns full string definition for message of type '<SetGripper-request>"
  (cl:format cl:nil "float64 val~%lebai_msgs/ExecuteMode execute_mode~%~%================================================================================~%MSG: lebai_msgs/ExecuteMode~%uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetGripper-request)))
  "Returns full string definition for message of type 'SetGripper-request"
  (cl:format cl:nil "float64 val~%lebai_msgs/ExecuteMode execute_mode~%~%================================================================================~%MSG: lebai_msgs/ExecuteMode~%uint8 data~%uint8 EXECUTE_MODE_BUFFER=0~%uint8 EXECUTE_MODE_IMMED=1~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetGripper-request>))
  (cl:+ 0
     8
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'execute_mode))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetGripper-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SetGripper-request
    (cl:cons ':val (val msg))
    (cl:cons ':execute_mode (execute_mode msg))
))
;//! \htmlinclude SetGripper-response.msg.html

(cl:defclass <SetGripper-response> (roslisp-msg-protocol:ros-message)
  ((ret
    :reader ret
    :initarg :ret
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass SetGripper-response (<SetGripper-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SetGripper-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SetGripper-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name lebai_msgs-srv:<SetGripper-response> is deprecated: use lebai_msgs-srv:SetGripper-response instead.")))

(cl:ensure-generic-function 'ret-val :lambda-list '(m))
(cl:defmethod ret-val ((m <SetGripper-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader lebai_msgs-srv:ret-val is deprecated.  Use lebai_msgs-srv:ret instead.")
  (ret m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SetGripper-response>) ostream)
  "Serializes a message object of type '<SetGripper-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'ret) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SetGripper-response>) istream)
  "Deserializes a message object of type '<SetGripper-response>"
    (cl:setf (cl:slot-value msg 'ret) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SetGripper-response>)))
  "Returns string type for a service object of type '<SetGripper-response>"
  "lebai_msgs/SetGripperResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetGripper-response)))
  "Returns string type for a service object of type 'SetGripper-response"
  "lebai_msgs/SetGripperResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SetGripper-response>)))
  "Returns md5sum for a message object of type '<SetGripper-response>"
  "38cc51b5a105d56ff2e64d1889e45a66")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SetGripper-response)))
  "Returns md5sum for a message object of type 'SetGripper-response"
  "38cc51b5a105d56ff2e64d1889e45a66")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SetGripper-response>)))
  "Returns full string definition for message of type '<SetGripper-response>"
  (cl:format cl:nil "bool ret~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SetGripper-response)))
  "Returns full string definition for message of type 'SetGripper-response"
  (cl:format cl:nil "bool ret~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SetGripper-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SetGripper-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SetGripper-response
    (cl:cons ':ret (ret msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SetGripper)))
  'SetGripper-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SetGripper)))
  'SetGripper-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SetGripper)))
  "Returns string type for a service object of type '<SetGripper>"
  "lebai_msgs/SetGripper")