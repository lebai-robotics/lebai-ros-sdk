;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::SetAO)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'SetAO (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::SETAO")
  (make-package "LEBAI_MSGS::SETAO"))
(unless (find-package "LEBAI_MSGS::SETAOREQUEST")
  (make-package "LEBAI_MSGS::SETAOREQUEST"))
(unless (find-package "LEBAI_MSGS::SETAORESPONSE")
  (make-package "LEBAI_MSGS::SETAORESPONSE"))

(in-package "ROS")



(if (not (find-package "INDUSTRIAL_MSGS"))
  (ros::roseus-add-msgs "industrial_msgs"))


(defclass lebai_msgs::SetAORequest
  :super ros::object
  :slots (_pin _value _execute_mode ))

(defmethod lebai_msgs::SetAORequest
  (:init
   (&key
    ((:pin __pin) 0)
    ((:value __value) 0.0)
    ((:execute_mode __execute_mode) (instance lebai_msgs::ExecuteMode :init))
    )
   (send-super :init)
   (setq _pin (round __pin))
   (setq _value (float __value))
   (setq _execute_mode __execute_mode)
   self)
  (:pin
   (&optional __pin)
   (if __pin (setq _pin __pin)) _pin)
  (:value
   (&optional __value)
   (if __value (setq _value __value)) _value)
  (:execute_mode
   (&rest __execute_mode)
   (if (keywordp (car __execute_mode))
       (send* _execute_mode __execute_mode)
     (progn
       (if __execute_mode (setq _execute_mode (car __execute_mode)))
       _execute_mode)))
  (:serialization-length
   ()
   (+
    ;; uint16 _pin
    2
    ;; float64 _value
    8
    ;; lebai_msgs/ExecuteMode _execute_mode
    (send _execute_mode :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint16 _pin
       (write-word _pin s)
     ;; float64 _value
       (sys::poke _value (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; lebai_msgs/ExecuteMode _execute_mode
       (send _execute_mode :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint16 _pin
     (setq _pin (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; float64 _value
     (setq _value (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; lebai_msgs/ExecuteMode _execute_mode
     (send _execute_mode :deserialize buf ptr-) (incf ptr- (send _execute_mode :serialization-length))
   ;;
   self)
  )

(defclass lebai_msgs::SetAOResponse
  :super ros::object
  :slots (_code ))

(defmethod lebai_msgs::SetAOResponse
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

(defclass lebai_msgs::SetAO
  :super ros::object
  :slots ())

(setf (get lebai_msgs::SetAO :md5sum-) "62f232c76f8ee745408ad371412c03b5")
(setf (get lebai_msgs::SetAO :datatype-) "lebai_msgs/SetAO")
(setf (get lebai_msgs::SetAO :request) lebai_msgs::SetAORequest)
(setf (get lebai_msgs::SetAO :response) lebai_msgs::SetAOResponse)

(defmethod lebai_msgs::SetAORequest
  (:response () (instance lebai_msgs::SetAOResponse :init)))

(setf (get lebai_msgs::SetAORequest :md5sum-) "62f232c76f8ee745408ad371412c03b5")
(setf (get lebai_msgs::SetAORequest :datatype-) "lebai_msgs/SetAORequest")
(setf (get lebai_msgs::SetAORequest :definition-)
      "uint16 pin
float64 value
lebai_msgs/ExecuteMode execute_mode

================================================================================
MSG: lebai_msgs/ExecuteMode
uint8 data
uint8 EXECUTE_MODE_BUFFER=0
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

(setf (get lebai_msgs::SetAOResponse :md5sum-) "62f232c76f8ee745408ad371412c03b5")
(setf (get lebai_msgs::SetAOResponse :datatype-) "lebai_msgs/SetAOResponse")
(setf (get lebai_msgs::SetAOResponse :definition-)
      "uint16 pin
float64 value
lebai_msgs/ExecuteMode execute_mode

================================================================================
MSG: lebai_msgs/ExecuteMode
uint8 data
uint8 EXECUTE_MODE_BUFFER=0
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



(provide :lebai_msgs/SetAO "62f232c76f8ee745408ad371412c03b5")


