// Generated by gencpp from file lebai_msgs/SetAORequest.msg
// DO NOT EDIT!


#ifndef LEBAI_MSGS_MESSAGE_SETAOREQUEST_H
#define LEBAI_MSGS_MESSAGE_SETAOREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <lebai_msgs/ExecuteMode.h>

namespace lebai_msgs
{
template <class ContainerAllocator>
struct SetAORequest_
{
  typedef SetAORequest_<ContainerAllocator> Type;

  SetAORequest_()
    : pin(0)
    , value(0.0)
    , execute_mode()  {
    }
  SetAORequest_(const ContainerAllocator& _alloc)
    : pin(0)
    , value(0.0)
    , execute_mode(_alloc)  {
  (void)_alloc;
    }



   typedef uint16_t _pin_type;
  _pin_type pin;

   typedef double _value_type;
  _value_type value;

   typedef  ::lebai_msgs::ExecuteMode_<ContainerAllocator>  _execute_mode_type;
  _execute_mode_type execute_mode;





  typedef boost::shared_ptr< ::lebai_msgs::SetAORequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::lebai_msgs::SetAORequest_<ContainerAllocator> const> ConstPtr;

}; // struct SetAORequest_

typedef ::lebai_msgs::SetAORequest_<std::allocator<void> > SetAORequest;

typedef boost::shared_ptr< ::lebai_msgs::SetAORequest > SetAORequestPtr;
typedef boost::shared_ptr< ::lebai_msgs::SetAORequest const> SetAORequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::lebai_msgs::SetAORequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::lebai_msgs::SetAORequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::lebai_msgs::SetAORequest_<ContainerAllocator1> & lhs, const ::lebai_msgs::SetAORequest_<ContainerAllocator2> & rhs)
{
  return lhs.pin == rhs.pin &&
    lhs.value == rhs.value &&
    lhs.execute_mode == rhs.execute_mode;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::lebai_msgs::SetAORequest_<ContainerAllocator1> & lhs, const ::lebai_msgs::SetAORequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace lebai_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::lebai_msgs::SetAORequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::lebai_msgs::SetAORequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lebai_msgs::SetAORequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lebai_msgs::SetAORequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lebai_msgs::SetAORequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lebai_msgs::SetAORequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::lebai_msgs::SetAORequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "0351e1f16076529abe80b1cda6c8fe59";
  }

  static const char* value(const ::lebai_msgs::SetAORequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x0351e1f16076529aULL;
  static const uint64_t static_value2 = 0xbe80b1cda6c8fe59ULL;
};

template<class ContainerAllocator>
struct DataType< ::lebai_msgs::SetAORequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "lebai_msgs/SetAORequest";
  }

  static const char* value(const ::lebai_msgs::SetAORequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::lebai_msgs::SetAORequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint16 pin\n"
"float64 value\n"
"lebai_msgs/ExecuteMode execute_mode\n"
"\n"
"================================================================================\n"
"MSG: lebai_msgs/ExecuteMode\n"
"uint8 data\n"
"uint8 EXECUTE_MODE_BUFFER=0\n"
"uint8 EXECUTE_MODE_IMMED=1\n"
;
  }

  static const char* value(const ::lebai_msgs::SetAORequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::lebai_msgs::SetAORequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.pin);
      stream.next(m.value);
      stream.next(m.execute_mode);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SetAORequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::lebai_msgs::SetAORequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::lebai_msgs::SetAORequest_<ContainerAllocator>& v)
  {
    s << indent << "pin: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.pin);
    s << indent << "value: ";
    Printer<double>::stream(s, indent + "  ", v.value);
    s << indent << "execute_mode: ";
    s << std::endl;
    Printer< ::lebai_msgs::ExecuteMode_<ContainerAllocator> >::stream(s, indent + "  ", v.execute_mode);
  }
};

} // namespace message_operations
} // namespace ros

#endif // LEBAI_MSGS_MESSAGE_SETAOREQUEST_H