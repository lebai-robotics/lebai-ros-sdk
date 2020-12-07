;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::ExecuteMode)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'ExecuteMode (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::EXECUTEMODE")
  (make-package "LEBAI_MSGS::EXECUTEMODE"))

(in-package "ROS")
;;//! \htmlinclude ExecuteMode.msg.html


(intern "*EXECUTE_MODE_BUFFER*" (find-package "LEBAI_MSGS::EXECUTEMODE"))
(shadow '*EXECUTE_MODE_BUFFER* (find-package "LEBAI_MSGS::EXECUTEMODE"))
(defconstant lebai_msgs::ExecuteMode::*EXECUTE_MODE_BUFFER* 0)
(intern "*EXECUTE_MODE_IMMED*" (find-package "LEBAI_MSGS::EXECUTEMODE"))
(shadow '*EXECUTE_MODE_IMMED* (find-package "LEBAI_MSGS::EXECUTEMODE"))
(defconstant lebai_msgs::ExecuteMode::*EXECUTE_MODE_IMMED* 1)
(defclass lebai_msgs::ExecuteMode
  :super ros::object
  :slots (_data ))

(defmethod lebai_msgs::ExecuteMode
  (:init
   (&key
    ((:data __data) 0)
    )
   (send-super :init)
   (setq _data (round __data))
   self)
  (:data
   (&optional __data)
   (if __data (setq _data __data)) _data)
  (:serialization-length
   ()
   (+
    ;; uint8 _data
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _data
       (write-byte _data s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _data
     (setq _data (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get lebai_msgs::ExecuteMode :md5sum-) "ce2e0fd38d2abc7741472f6d6de5645a")
(setf (get lebai_msgs::ExecuteMode :datatype-) "lebai_msgs/ExecuteMode")
(setf (get lebai_msgs::ExecuteMode :definition-)
      "uint8 data
uint8 EXECUTE_MODE_BUFFER=0
uint8 EXECUTE_MODE_IMMED=1
")



(provide :lebai_msgs/ExecuteMode "ce2e0fd38d2abc7741472f6d6de5645a")


