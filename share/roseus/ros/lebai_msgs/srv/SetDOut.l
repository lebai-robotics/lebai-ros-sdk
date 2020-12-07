;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::SetDOut)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'SetDOut (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::SETDOUT")
  (make-package "LEBAI_MSGS::SETDOUT"))
(unless (find-package "LEBAI_MSGS::SETDOUTREQUEST")
  (make-package "LEBAI_MSGS::SETDOUTREQUEST"))
(unless (find-package "LEBAI_MSGS::SETDOUTRESPONSE")
  (make-package "LEBAI_MSGS::SETDOUTRESPONSE"))

(in-package "ROS")



(if (not (find-package "INDUSTRIAL_MSGS"))
  (ros::roseus-add-msgs "industrial_msgs"))


(defclass lebai_msgs::SetDOutRequest
  :super ros::object
  :slots (_group _index _value ))

(defmethod lebai_msgs::SetDOutRequest
  (:init
   (&key
    ((:group __group) 0)
    ((:index __index) 0)
    ((:value __value) nil)
    )
   (send-super :init)
   (setq _group (round __group))
   (setq _index (round __index))
   (setq _value __value)
   self)
  (:group
   (&optional __group)
   (if __group (setq _group __group)) _group)
  (:index
   (&optional __index)
   (if __index (setq _index __index)) _index)
  (:value
   (&optional __value)
   (if __value (setq _value __value)) _value)
  (:serialization-length
   ()
   (+
    ;; uint8 _group
    1
    ;; uint16 _index
    2
    ;; bool _value
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _group
       (write-byte _group s)
     ;; uint16 _index
       (write-word _index s)
     ;; bool _value
       (if _value (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _group
     (setq _group (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint16 _index
     (setq _index (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; bool _value
     (setq _value (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass lebai_msgs::SetDOutResponse
  :super ros::object
  :slots (_code ))

(defmethod lebai_msgs::SetDOutResponse
  (:init
   (&key
    ((:code __code) (instance industrial_msgs::ServiceReturnCode :init))
    )
   (send-super :init)
   (setq _code __code)
   self)
  (:code
   (&rest __code)
   (if (keywordp (car __code))
       (send* _code __code)
     (progn
       (if __code (setq _code (car __code)))
       _code)))
  (:serialization-length
   ()
   (+
    ;; industrial_msgs/ServiceReturnCode _code
    (send _code :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; industrial_msgs/ServiceReturnCode _code
       (send _code :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; industrial_msgs/ServiceReturnCode _code
     (send _code :deserialize buf ptr-) (incf ptr- (send _code :serialization-length))
   ;;
   self)
  )

(defclass lebai_msgs::SetDOut
  :super ros::object
  :slots ())

(setf (get lebai_msgs::SetDOut :md5sum-) "e6191b92a4b149f13f17282b8739af44")
(setf (get lebai_msgs::SetDOut :datatype-) "lebai_msgs/SetDOut")
(setf (get lebai_msgs::SetDOut :request) lebai_msgs::SetDOutRequest)
(setf (get lebai_msgs::SetDOut :response) lebai_msgs::SetDOutResponse)

(defmethod lebai_msgs::SetDOutRequest
  (:response () (instance lebai_msgs::SetDOutResponse :init)))

(setf (get lebai_msgs::SetDOutRequest :md5sum-) "e6191b92a4b149f13f17282b8739af44")
(setf (get lebai_msgs::SetDOutRequest :datatype-) "lebai_msgs/SetDOutRequest")
(setf (get lebai_msgs::SetDOutRequest :definition-)
      "uint8 group
uint16 index
bool value
---
industrial_msgs/ServiceReturnCode code

================================================================================
MSG: industrial_msgs/ServiceReturnCode
# Service return codes for simple requests.  All ROS-Industrial service
# replies are required to have a return code indicating success or failure
# Specific return codes for different failure should be negative.
int8 val

int8 SUCCESS = 1
int8 FAILURE = -1

")

(setf (get lebai_msgs::SetDOutResponse :md5sum-) "e6191b92a4b149f13f17282b8739af44")
(setf (get lebai_msgs::SetDOutResponse :datatype-) "lebai_msgs/SetDOutResponse")
(setf (get lebai_msgs::SetDOutResponse :definition-)
      "uint8 group
uint16 index
bool value
---
industrial_msgs/ServiceReturnCode code

================================================================================
MSG: industrial_msgs/ServiceReturnCode
# Service return codes for simple requests.  All ROS-Industrial service
# replies are required to have a return code indicating success or failure
# Specific return codes for different failure should be negative.
int8 val

int8 SUCCESS = 1
int8 FAILURE = -1

")



(provide :lebai_msgs/SetDOut "e6191b92a4b149f13f17282b8739af44")


