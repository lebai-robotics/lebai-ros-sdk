;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::SetAOut)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'SetAOut (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::SETAOUT")
  (make-package "LEBAI_MSGS::SETAOUT"))
(unless (find-package "LEBAI_MSGS::SETAOUTREQUEST")
  (make-package "LEBAI_MSGS::SETAOUTREQUEST"))
(unless (find-package "LEBAI_MSGS::SETAOUTRESPONSE")
  (make-package "LEBAI_MSGS::SETAOUTRESPONSE"))

(in-package "ROS")



(if (not (find-package "INDUSTRIAL_MSGS"))
  (ros::roseus-add-msgs "industrial_msgs"))


(defclass lebai_msgs::SetAOutRequest
  :super ros::object
  :slots (_group _index _value ))

(defmethod lebai_msgs::SetAOutRequest
  (:init
   (&key
    ((:group __group) 0)
    ((:index __index) 0)
    ((:value __value) 0.0)
    )
   (send-super :init)
   (setq _group (round __group))
   (setq _index (round __index))
   (setq _value (float __value))
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
    ;; float64 _value
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _group
       (write-byte _group s)
     ;; uint16 _index
       (write-word _index s)
     ;; float64 _value
       (sys::poke _value (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _group
     (setq _group (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint16 _index
     (setq _index (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; float64 _value
     (setq _value (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass lebai_msgs::SetAOutResponse
  :super ros::object
  :slots (_code ))

(defmethod lebai_msgs::SetAOutResponse
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

(defclass lebai_msgs::SetAOut
  :super ros::object
  :slots ())

(setf (get lebai_msgs::SetAOut :md5sum-) "51928732046ffb5b5606f765ba7fcd8b")
(setf (get lebai_msgs::SetAOut :datatype-) "lebai_msgs/SetAOut")
(setf (get lebai_msgs::SetAOut :request) lebai_msgs::SetAOutRequest)
(setf (get lebai_msgs::SetAOut :response) lebai_msgs::SetAOutResponse)

(defmethod lebai_msgs::SetAOutRequest
  (:response () (instance lebai_msgs::SetAOutResponse :init)))

(setf (get lebai_msgs::SetAOutRequest :md5sum-) "51928732046ffb5b5606f765ba7fcd8b")
(setf (get lebai_msgs::SetAOutRequest :datatype-) "lebai_msgs/SetAOutRequest")
(setf (get lebai_msgs::SetAOutRequest :definition-)
      "uint8 group
uint16 index
float64 value
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

(setf (get lebai_msgs::SetAOutResponse :md5sum-) "51928732046ffb5b5606f765ba7fcd8b")
(setf (get lebai_msgs::SetAOutResponse :datatype-) "lebai_msgs/SetAOutResponse")
(setf (get lebai_msgs::SetAOutResponse :definition-)
      "uint8 group
uint16 index
float64 value
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



(provide :lebai_msgs/SetAOut "51928732046ffb5b5606f765ba7fcd8b")


