;; Auto-generated. Do not edit!


(when (boundp 'lebai_msgs::GripperStatus)
  (if (not (find-package "LEBAI_MSGS"))
    (make-package "LEBAI_MSGS"))
  (shadow 'GripperStatus (find-package "LEBAI_MSGS")))
(unless (find-package "LEBAI_MSGS::GRIPPERSTATUS")
  (make-package "LEBAI_MSGS::GRIPPERSTATUS"))

(in-package "ROS")
;;//! \htmlinclude GripperStatus.msg.html


(defclass lebai_msgs::GripperStatus
  :super ros::object
  :slots (_position _force ))

(defmethod lebai_msgs::GripperStatus
  (:init
   (&key
    ((:position __position) 0.0)
    ((:force __force) 0.0)
    )
   (send-super :init)
   (setq _position (float __position))
   (setq _force (float __force))
   self)
  (:position
   (&optional __position)
   (if __position (setq _position __position)) _position)
  (:force
   (&optional __force)
   (if __force (setq _force __force)) _force)
  (:serialization-length
   ()
   (+
    ;; float64 _position
    8
    ;; float64 _force
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _position
       (sys::poke _position (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _force
       (sys::poke _force (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _position
     (setq _position (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _force
     (setq _force (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get lebai_msgs::GripperStatus :md5sum-) "fead2ec07015c5b0fb77c4988270a39b")
(setf (get lebai_msgs::GripperStatus :datatype-) "lebai_msgs/GripperStatus")
(setf (get lebai_msgs::GripperStatus :definition-)
      "float64 position
float64 force

")



(provide :lebai_msgs/GripperStatus "fead2ec07015c5b0fb77c4988270a39b")


