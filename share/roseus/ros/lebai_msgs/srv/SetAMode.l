;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::SetAMode)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'SetAMode (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::SETAMODE")
  (make-package "LEBAI_MSGS::SETAMODE"))
(unless (find-package "LEBAI_MSGS::SETAMODEREQUEST")
  (make-package "LEBAI_MSGS::SETAMODEREQUEST"))
(unless (find-package "LEBAI_MSGS::SETAMODERESPONSE")
  (make-package "LEBAI_MSGS::SETAMODERESPONSE"))

(in-package "ROS")



(if (not (find-package "INDUSTRIAL_MSGS"))
  (ros::roseus-add-msgs "industrial_msgs"))


(defclass lebai_msgs::SetAModeRequest
  :super ros::object
  :slots (_pin _mode _execute_mode ))

(defmethod lebai_msgs::SetAModeRequest
  (:init
   (&key
    ((:pin __pin) 0)
    ((:mode __mode) 0)
    ((:execute_mode __execute_mode) (instance lebai_msgs::ExecuteMode :init))
    )
   (send-super :init)
   (setq _pin (round __pin))
   (setq _mode (round __mode))
   (setq _execute_mode __execute_mode)
   self)
  (:pin
   (&optional __pin)
   (if __pin (setq _pin __pin)) _pin)
  (:mode
   (&optional __mode)
   (if __mode (setq _mode __mode)) _mode)
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
    ;; uint8 _mode
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
     ;; uint8 _mode
       (write-byte _mode s)
     ;; lebai_msgs/ExecuteMode _execute_mode
       (send _execute_mode :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint16 _pin
     (setq _pin (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint8 _mode
     (setq _mode (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; lebai_msgs/ExecuteMode _execute_mode
     (send _execute_mode :deserialize buf ptr-) (incf ptr- (send _execute_mode :serialization-length))
   ;;
   self)
  )

(defclass lebai_msgs::SetAModeResponse
  :super ros::object
  :slots (_code ))

(defmethod lebai_msgs::SetAModeResponse
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

(defclass lebai_msgs::SetAMode
  :super ros::object
  :slots ())

(setf (get lebai_msgs::SetAMode :md5sum-) "db41913f133aefb2bfdc45acc60725b5")
(setf (get lebai_msgs::SetAMode :datatype-) "lebai_msgs/SetAMode")
(setf (get lebai_msgs::SetAMode :request) lebai_msgs::SetAModeRequest)
(setf (get lebai_msgs::SetAMode :response) lebai_msgs::SetAModeResponse)

(defmethod lebai_msgs::SetAModeRequest
  (:response () (instance lebai_msgs::SetAModeResponse :init)))

(setf (get lebai_msgs::SetAModeRequest :md5sum-) "db41913f133aefb2bfdc45acc60725b5")
(setf (get lebai_msgs::SetAModeRequest :datatype-) "lebai_msgs/SetAModeRequest")
(setf (get lebai_msgs::SetAModeRequest :definition-)
      "uint16 pin
uint8 mode
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

(setf (get lebai_msgs::SetAModeResponse :md5sum-) "db41913f133aefb2bfdc45acc60725b5")
(setf (get lebai_msgs::SetAModeResponse :datatype-) "lebai_msgs/SetAModeResponse")
(setf (get lebai_msgs::SetAModeResponse :definition-)
      "uint16 pin
uint8 mode
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



(provide :lebai_msgs/SetAMode "db41913f133aefb2bfdc45acc60725b5")


