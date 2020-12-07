;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::SetGripper)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'SetGripper (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::SETGRIPPER")
  (make-package "LEBAI_MSGS::SETGRIPPER"))
(unless (find-package "LEBAI_MSGS::SETGRIPPERREQUEST")
  (make-package "LEBAI_MSGS::SETGRIPPERREQUEST"))
(unless (find-package "LEBAI_MSGS::SETGRIPPERRESPONSE")
  (make-package "LEBAI_MSGS::SETGRIPPERRESPONSE"))

(in-package "ROS")





(defclass lebai_msgs::SetGripperRequest
  :super ros::object
  :slots (_val _execute_mode ))

(defmethod lebai_msgs::SetGripperRequest
  (:init
   (&key
    ((:val __val) 0.0)
    ((:execute_mode __execute_mode) (instance lebai_msgs::ExecuteMode :init))
    )
   (send-super :init)
   (setq _val (float __val))
   (setq _execute_mode __execute_mode)
   self)
  (:val
   (&optional __val)
   (if __val (setq _val __val)) _val)
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
    ;; float64 _val
    8
    ;; lebai_msgs/ExecuteMode _execute_mode
    (send _execute_mode :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _val
       (sys::poke _val (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; lebai_msgs/ExecuteMode _execute_mode
       (send _execute_mode :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _val
     (setq _val (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; lebai_msgs/ExecuteMode _execute_mode
     (send _execute_mode :deserialize buf ptr-) (incf ptr- (send _execute_mode :serialization-length))
   ;;
   self)
  )

(defclass lebai_msgs::SetGripperResponse
  :super ros::object
  :slots (_ret ))

(defmethod lebai_msgs::SetGripperResponse
  (:init
   (&key
    ((:ret __ret) nil)
    )
   (send-super :init)
   (setq _ret __ret)
   self)
  (:ret
   (&optional __ret)
   (if __ret (setq _ret __ret)) _ret)
  (:serialization-length
   ()
   (+
    ;; bool _ret
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _ret
       (if _ret (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _ret
     (setq _ret (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass lebai_msgs::SetGripper
  :super ros::object
  :slots ())

(setf (get lebai_msgs::SetGripper :md5sum-) "38cc51b5a105d56ff2e64d1889e45a66")
(setf (get lebai_msgs::SetGripper :datatype-) "lebai_msgs/SetGripper")
(setf (get lebai_msgs::SetGripper :request) lebai_msgs::SetGripperRequest)
(setf (get lebai_msgs::SetGripper :response) lebai_msgs::SetGripperResponse)

(defmethod lebai_msgs::SetGripperRequest
  (:response () (instance lebai_msgs::SetGripperResponse :init)))

(setf (get lebai_msgs::SetGripperRequest :md5sum-) "38cc51b5a105d56ff2e64d1889e45a66")
(setf (get lebai_msgs::SetGripperRequest :datatype-) "lebai_msgs/SetGripperRequest")
(setf (get lebai_msgs::SetGripperRequest :definition-)
      "float64 val
lebai_msgs/ExecuteMode execute_mode

================================================================================
MSG: lebai_msgs/ExecuteMode
uint8 data
uint8 EXECUTE_MODE_BUFFER=0
---
bool ret
")

(setf (get lebai_msgs::SetGripperResponse :md5sum-) "38cc51b5a105d56ff2e64d1889e45a66")
(setf (get lebai_msgs::SetGripperResponse :datatype-) "lebai_msgs/SetGripperResponse")
(setf (get lebai_msgs::SetGripperResponse :definition-)
      "float64 val
lebai_msgs/ExecuteMode execute_mode

================================================================================
MSG: lebai_msgs/ExecuteMode
uint8 data
uint8 EXECUTE_MODE_BUFFER=0
---
bool ret
")



(provide :lebai_msgs/SetGripper "38cc51b5a105d56ff2e64d1889e45a66")


