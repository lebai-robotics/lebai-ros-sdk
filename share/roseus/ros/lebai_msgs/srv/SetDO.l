;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::SetDO)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'SetDO (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::SETDO")
  (make-package "LEBAI_MSGS::SETDO"))
(unless (find-package "LEBAI_MSGS::SETDOREQUEST")
  (make-package "LEBAI_MSGS::SETDOREQUEST"))
(unless (find-package "LEBAI_MSGS::SETDORESPONSE")
  (make-package "LEBAI_MSGS::SETDORESPONSE"))

(in-package "ROS")



(if (not (find-package "INDUSTRIAL_MSGS"))
  (ros::roseus-add-msgs "industrial_msgs"))


(defclass lebai_msgs::SetDORequest
  :super ros::object
  :slots (_pin _value _execute_mode ))

(defmethod lebai_msgs::SetDORequest
  (:init
   (&key
    ((:pin __pin) 0)
    ((:value __value) nil)
    ((:execute_mode __execute_mode) (instance lebai_msgs::ExecuteMode :init))
    )
   (send-super :init)
   (setq _pin (round __pin))
   (setq _value __value)
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
    ;; bool _value
    1
    ;; lebai_msgs/ExecuteMode _execute_mode
    (send _execute_mode :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint16 _pin
       (write-word _pin s)
     ;; bool _value
       (if _value (write-byte -1 s) (write-byte 0 s))
     ;; lebai_msgs/ExecuteMode _execute_mode
       (send _execute_mode :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint16 _pin
     (setq _pin (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; bool _value
     (setq _value (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; lebai_msgs/ExecuteMode _execute_mode
     (send _execute_mode :deserialize buf ptr-) (incf ptr- (send _execute_mode :serialization-length))
   ;;
   self)
  )

(defclass lebai_msgs::SetDOResponse
  :super ros::object
  :slots (_code ))

(defmethod lebai_msgs::SetDOResponse
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

(defclass lebai_msgs::SetDO
  :super ros::object
  :slots ())

(setf (get lebai_msgs::SetDO :md5sum-) "5a536dfb6aaff1ccac47c5a754efe2e6")
(setf (get lebai_msgs::SetDO :datatype-) "lebai_msgs/SetDO")
(setf (get lebai_msgs::SetDO :request) lebai_msgs::SetDORequest)
(setf (get lebai_msgs::SetDO :response) lebai_msgs::SetDOResponse)

(defmethod lebai_msgs::SetDORequest
  (:response () (instance lebai_msgs::SetDOResponse :init)))

(setf (get lebai_msgs::SetDORequest :md5sum-) "5a536dfb6aaff1ccac47c5a754efe2e6")
(setf (get lebai_msgs::SetDORequest :datatype-) "lebai_msgs/SetDORequest")
(setf (get lebai_msgs::SetDORequest :definition-)
      "uint16 pin
bool value
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

(setf (get lebai_msgs::SetDOResponse :md5sum-) "5a536dfb6aaff1ccac47c5a754efe2e6")
(setf (get lebai_msgs::SetDOResponse :datatype-) "lebai_msgs/SetDOResponse")
(setf (get lebai_msgs::SetDOResponse :definition-)
      "uint16 pin
bool value
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



(provide :lebai_msgs/SetDO "5a536dfb6aaff1ccac47c5a754efe2e6")


