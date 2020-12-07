;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::SetAOutMode)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'SetAOutMode (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::SETAOUTMODE")
  (make-package "LEBAI_MSGS::SETAOUTMODE"))
(unless (find-package "LEBAI_MSGS::SETAOUTMODEREQUEST")
  (make-package "LEBAI_MSGS::SETAOUTMODEREQUEST"))
(unless (find-package "LEBAI_MSGS::SETAOUTMODERESPONSE")
  (make-package "LEBAI_MSGS::SETAOUTMODERESPONSE"))

(in-package "ROS")



(if (not (find-package "INDUSTRIAL_MSGS"))
  (ros::roseus-add-msgs "industrial_msgs"))


(defclass lebai_msgs::SetAOutModeRequest
  :super ros::object
  :slots (_group _index _mode ))

(defmethod lebai_msgs::SetAOutModeRequest
  (:init
   (&key
    ((:group __group) 0)
    ((:index __index) 0)
    ((:mode __mode) 0)
    )
   (send-super :init)
   (setq _group (round __group))
   (setq _index (round __index))
   (setq _mode (round __mode))
   self)
  (:group
   (&optional __group)
   (if __group (setq _group __group)) _group)
  (:index
   (&optional __index)
   (if __index (setq _index __index)) _index)
  (:mode
   (&optional __mode)
   (if __mode (setq _mode __mode)) _mode)
  (:serialization-length
   ()
   (+
    ;; uint8 _group
    1
    ;; uint16 _index
    2
    ;; uint8 _mode
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
     ;; uint8 _mode
       (write-byte _mode s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _group
     (setq _group (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint16 _index
     (setq _index (sys::peek buf ptr- :short)) (incf ptr- 2)
   ;; uint8 _mode
     (setq _mode (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(defclass lebai_msgs::SetAOutModeResponse
  :super ros::object
  :slots (_code ))

(defmethod lebai_msgs::SetAOutModeResponse
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

(defclass lebai_msgs::SetAOutMode
  :super ros::object
  :slots ())

(setf (get lebai_msgs::SetAOutMode :md5sum-) "faf7ab1e93a1650eb66028ad6d75331c")
(setf (get lebai_msgs::SetAOutMode :datatype-) "lebai_msgs/SetAOutMode")
(setf (get lebai_msgs::SetAOutMode :request) lebai_msgs::SetAOutModeRequest)
(setf (get lebai_msgs::SetAOutMode :response) lebai_msgs::SetAOutModeResponse)

(defmethod lebai_msgs::SetAOutModeRequest
  (:response () (instance lebai_msgs::SetAOutModeResponse :init)))

(setf (get lebai_msgs::SetAOutModeRequest :md5sum-) "faf7ab1e93a1650eb66028ad6d75331c")
(setf (get lebai_msgs::SetAOutModeRequest :datatype-) "lebai_msgs/SetAOutModeRequest")
(setf (get lebai_msgs::SetAOutModeRequest :definition-)
      "uint8 group
uint16 index
uint8 mode
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

(setf (get lebai_msgs::SetAOutModeResponse :md5sum-) "faf7ab1e93a1650eb66028ad6d75331c")
(setf (get lebai_msgs::SetAOutModeResponse :datatype-) "lebai_msgs/SetAOutModeResponse")
(setf (get lebai_msgs::SetAOutModeResponse :definition-)
      "uint8 group
uint16 index
uint8 mode
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



(provide :lebai_msgs/SetAOutMode "faf7ab1e93a1650eb66028ad6d75331c")


